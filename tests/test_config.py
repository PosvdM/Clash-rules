import copy
import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('generate', ROOT/'scripts/generate.py')
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

class ConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = yaml.safe_load((ROOT/'source.yaml').read_text())
        cls.files = gen.compile_config(cls.src, offline=True)
        cls.common = yaml.safe_load(cls.files['output/common.yaml'])
        cls.provider_exclusion = '(?i:' + cls.src['exclude_remarks'].removeprefix('(?i)') + ')'

    def test_all_wrappers_share_entire_policy(self):
        stash = yaml.safe_load(self.files['output/override.stoverride'])
        stash.pop('name'); stash.pop('desc')
        self.assertEqual(self.common, stash)
        for key, value in self.common.items():
            if isinstance(value, (list, dict)):
                self.assertIn(key + ': #!replace', self.files['output/override.stoverride'])
        base = yaml.safe_load(self.files['output/GeneralClashConfig.yml'])
        for config in (self.common, stash, base):
            self.assertNotIn('tun', config)
        for key in ('dns', 'hosts', 'rule-providers'):
            self.assertEqual(self.common[key], base[key])

    def test_js_retains_nodes_and_replaces_old_settings(self):
        program = """
const fs=require('fs'),vm=require('vm');
const ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('output/PosvdM_rules.js','utf8'),ctx);
const original={proxies:[{name:'香港 01',type:'ss',server:'example.org',password:'test-only'}],
 'proxy-providers':{airport:{type:'http',url:'https://example.org/sub',header:{Authorization:['test-only']}}},
 dns:{nameserver:['bad']},rules:['MATCH,REJECT'],tun:{enable:true,stack:'system'},
 sniffer:{enable:true},'geox-url':{geosite:'https://example.org/geosite.dat'},
 'mixed-port':12345,authentication:['old:password'],listeners:[{name:'old'}],
 'sub-rules':{old:['MATCH,REJECT']},'unknown-subscription-setting':{enabled:true}};
const before=JSON.stringify(original);
const result=ctx.main(original);
if(JSON.stringify(original)!==before) throw new Error('Input mutated');
if(result.proxies===original.proxies || result['proxy-providers']===original['proxy-providers']) throw new Error('Shared node objects');
process.stdout.write(JSON.stringify(result));
"""
        result = json.loads(subprocess.check_output(['node','-e',program],cwd=ROOT))
        self.assertEqual(result.pop('proxies')[0]['password'], 'test-only')
        self.assertEqual(result.pop('proxy-providers')['airport'], {
            'type': 'http', 'url': 'https://example.org/sub',
            'exclude-filter': self.provider_exclusion,
            'header': {'Authorization': ['test-only']}})
        self.assertEqual(result, self.common)

    def test_js_node_sources_errors_and_repeat_calls(self):
        program = """
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('output/PosvdM_rules.js','utf8'),ctx);
for(const input of [null,undefined,[],42,'bad']) assert.throws(()=>ctx.main(input),/需要先导入机场订阅/);
for(const input of [{},{proxies:[]},{'proxy-providers':{}}]) assert.throws(()=>ctx.main(input),/订阅中没有代理节点/);
const nodes={proxies:[{name:'test',type:'ss',server:'example.org',password:'test-only'}]};
const providers={'proxy-providers':{airport:{type:'http',url:'https://example.org/sub'}}};
const first=ctx.main(nodes);
first.dns.nameserver.push('https://example.org/unwanted');
first.proxies[0].password='changed';
process.stdout.write(JSON.stringify([ctx.main(nodes),ctx.main(providers)]));
"""
        nodes, providers = json.loads(subprocess.check_output(['node', '-e', program], cwd=ROOT))
        self.assertEqual(nodes.pop('proxies')[0]['password'], 'test-only')
        self.assertEqual(providers.pop('proxy-providers'), {
            'airport': {'type': 'http', 'url': 'https://example.org/sub',
                        'exclude-filter': self.provider_exclusion}})
        self.assertEqual(nodes, self.common)
        self.assertEqual(providers, self.common)

    def test_js_removes_notice_nodes_and_filters_provider_sources(self):
        program = """
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('output/PosvdM_rules.js','utf8'),ctx);
const notices=['Traffic: 41.44 GB | 150 GB','Expire: 2026-12-31','TRAFFIC: 1 GB', '剩余流量：10 GB','到期时间：2026-12-31'];
const valid=['香港 01','日本 实验 0.1x','美国 2x'];
const makeNode=name=>({name,type:'trojan',server:'example.org',port:443,password:'test-only'});
const nodes=[...notices,...valid].map(makeNode);
const input={proxies:nodes,'proxy-providers':{
 http:{type:'http',url:'https://example.org/sub','exclude-filter':'^Blocked'},
 file:{type:'file',path:'./nodes.yaml','exclude-filter':'(?i)custom'},
 inline:{type:'inline',payload:nodes}}};
const before=JSON.stringify(input);
const result=ctx.main(input);
assert.strictEqual(JSON.stringify(input),before);
assert.strictEqual(JSON.stringify(ctx.main(result)),JSON.stringify(result));
assert.deepStrictEqual(Array.from(result.proxies,n=>n.name),['🇭🇰 香港 01','🇯🇵 日本 实验 0.1x','🇺🇸 美国 2x']);
assert.deepStrictEqual(Array.from(result['proxy-providers'].inline.payload,n=>n.name),['🇭🇰 香港 01','🇯🇵 日本 实验 0.1x','🇺🇸 美国 2x']);
assert.strictEqual(ctx.main({proxies:notices.map(makeNode)}).proxies.length,0);
process.stdout.write(JSON.stringify(result));
"""
        result = json.loads(subprocess.check_output(['node', '-e', program], cwd=ROOT))
        self.assertTrue(all(n['password'] == 'test-only' for n in result['proxies']))
        providers = result['proxy-providers']
        self.assertEqual(providers['http']['exclude-filter'], '(?:^Blocked)|' + self.provider_exclusion)
        self.assertEqual(providers['file']['exclude-filter'], '(?:(?i)custom)|' + self.provider_exclusion)
        for provider in (providers['http'], providers['inline']):
            pattern = re.compile(provider['exclude-filter'])
            for name in ['Traffic: 41.44 GB | 150 GB', 'Expire: 2026-12-31', '剩余流量']:
                self.assertIsNotNone(pattern.search(name))
            self.assertIsNone(pattern.search('香港 01'))
        self.assertIsNotNone(re.search(providers['http']['exclude-filter'], 'Blocked'))
        self.assertIsNone(re.search(providers['http']['exclude-filter'], 'blocked'))

    def test_js_flags_preserve_names_credentials_and_references(self):
        program = """
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('output/PosvdM_rules.js','utf8'),ctx);
const examples=[
 ['🌸|印度标准 IEPL 专线 1','🌸|🇮🇳 印度标准 IEPL 专线 1'],
 ['🌸|巴基斯坦标准 IEPL 专线 1','🌸|🇵🇰 巴基斯坦标准 IEPL 专线 1'],
 ['以色列 1','🇮🇱 以色列 1'],['阿联酋 1','🇦🇪 阿联酋 1'],
 ['菲律宾 1','🇵🇭 菲律宾 1'],['马来西亚 1','🇲🇾 马来西亚 1'],
 ['埃及 1','🇪🇬 埃及 1'],['尼日利亚 1','🇳🇬 尼日利亚 1'],
 ['印度尼西亚 1','🇮🇩 印度尼西亚 1'],['印度尼西亞 2','🇮🇩 印度尼西亞 2'],
 ['🇮🇳 🌸|印度标准 IEPL 专线 2','🌸|🇮🇳 印度标准 IEPL 专线 2'],
 ['🌸｜ 马来西亚 2','🌸｜ 🇲🇾 马来西亚 2'],
 ['🌸|🇮🇳 印度 3','🌸|🇮🇳 印度 3'],
 ['服务A|日本专线 4','服务A|🇯🇵 日本专线 4'],
 ['线路1｜香港专线 5','线路1｜🇭🇰 香港专线 5'],
 ['服务B|新加坡|IEPL 6','服务B|🇸🇬 新加坡|IEPL 6'],
 ['🇯🇵 服务C|日本专线 7','服务C|🇯🇵 日本专线 7'],
 ['香港实验性 IEPL 专线 8','🇭🇰 香港实验性 IEPL 专线 8'],
 ['JP01','🇯🇵 JP01'],['singapore 2','🇸🇬 singapore 2'],['🇭🇰 香港01','🇭🇰 香港01'],
 ['👾|🇸🇬【亚洲】新加坡01','👾|🇸🇬【亚洲】新加坡01'],
 ['英国 IEPL 1','🇬🇧 英国 IEPL 1'],['BUSINESS LINE','BUSINESS LINE'],
 ['test in progress','test in progress'],['香港→日本','香港→日本'],
 ['印度尼西亚→印度','印度尼西亚→印度'],['自动 01','自动 01']];
const makeNode=name=>({name,type:'ss',server:'unchanged.example',port:443,password:'keep-me'});
const input={proxies:examples.map(([name])=>makeNode(name))};
input.proxies[1]['dialer-proxy']=examples[0][0];
input['proxy-providers']={remote:{type:'http',url:'https://example.org/sub',
 proxy:examples[0][0],override:{'dialer-proxy':examples[0][0],'additional-prefix':'Airport '}}};
const before=JSON.stringify(input),result=ctx.main(input);
assert.strictEqual(JSON.stringify(input),before);
assert.deepStrictEqual(Array.from(result.proxies,n=>n.name),examples.map(e=>e[1]));
for(let i=0;i<input.proxies.length;i++) {
 const expected=JSON.parse(JSON.stringify(input.proxies[i]));expected.name=examples[i][1];
 if(expected['dialer-proxy']) expected['dialer-proxy']=examples[0][1];
 assert.strictEqual(JSON.stringify(result.proxies[i]),JSON.stringify(expected));
}
assert.strictEqual(result['proxy-providers'].remote.proxy,examples[0][1]);
assert.strictEqual(result['proxy-providers'].remote.override['dialer-proxy'],examples[0][1]);
assert.strictEqual(result['proxy-providers'].remote.override['additional-prefix'],'Airport ');
assert.strictEqual(JSON.stringify(ctx.main(result)),JSON.stringify(result));
"""
        subprocess.check_call(['node', '-e', program], cwd=ROOT)

    def test_js_flags_avoid_collisions_and_respect_provider_name_processing(self):
        program = """
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('output/PosvdM_rules.js','utf8'),ctx);
const node=name=>({name,type:'ss',server:'example.org',password:'test'});
const input={proxies:['香港 1','🇭🇰 香港 1','日本 1','🌸|印度 9','🇮🇳 🌸|印度 9'].map(node),'proxy-providers':{
 inline:{type:'inline',payload:[node('新加坡 1')]},
 filtered:{type:'inline',filter:'^日本',payload:[node('日本 1')]},
 renamed:{type:'inline',override:{'additional-prefix':'🇺🇸 '},payload:[node('美国 1')]},
 remote:{type:'http',url:'https://example.org/sub',override:{'proxy-name':[{pattern:'^JP',target:'Japan'}]}}}};
const result=ctx.main(input);
assert.deepStrictEqual(Array.from(result.proxies,n=>n.name),['香港 1','🇭🇰 香港 1','日本 1','🌸|印度 9','🇮🇳 🌸|印度 9']);
assert.strictEqual(result['proxy-providers'].inline.payload[0].name,'🇸🇬 新加坡 1');
assert.strictEqual(result['proxy-providers'].filtered.payload[0].name,'日本 1');
assert.strictEqual(result['proxy-providers'].renamed.payload[0].name,'美国 1');
assert.strictEqual(JSON.stringify(ctx.main(result)),JSON.stringify(result));
"""
        subprocess.check_call(['node', '-e', program], cwd=ROOT)

    def test_order_and_native_formats(self):
        providers = self.common['rule-providers']
        rules = self.common['rules']
        self.assertEqual(rules[-1], self.src['tail_rules'][-1])
        first_ip = next(i for i,r in enumerate(rules) if r.endswith(',no-resolve'))
        for r in rules[first_ip:-1]:
            self.assertTrue(r.endswith(',no-resolve'),r)
        self.assertLess(rules.index('GEOSITE,cn,🟢 直连'), first_ip)
        by_url = {p['url']:p for p in providers.values()}
        self.assertFalse(any('/non_ip/apple_cdn.txt' in u for u in by_url))
        apple = by_url['https://ruleset.skk.moe/Clash/domainset/apple_cdn.txt']
        self.assertEqual((apple['behavior'],apple['format']),('domain','text'))
        for filename in ('china_ip','china_ip_ipv6'):
            self.assertEqual(by_url[f'https://ruleset.skk.moe/Clash/ip/{filename}.txt']['behavior'],'ipcidr')
        self.assertIn('https://ruleset.skk.moe/Clash/ip/telegram_asn.txt', by_url)

    def test_local_rules_not_lost_and_correctly_split(self):
        for entry in self.src['rulesets']:
            if 'file' not in entry: continue
            original = gen.lines((ROOT/entry['file']).read_text())
            if entry['id'] in self.common['rule-providers']:
                provider = self.common['rule-providers'][entry['id']]
                self.assertEqual(provider['url'], f"https://raw.githubusercontent.com/{self.src['repository']}/{self.src['branch']}/{entry['file']}")
                self.assertFalse(any(name.startswith(f"output/rules/{entry['id']}_") for name in self.files))
                self.assertEqual(len({r.split(',')[0] in gen.IP_TYPES for r in original}), 1)
                continue
            actual=[]
            for stage in ('non_ip','ip'):
                text=self.files.get(f"output/rules/{entry['id']}_{stage}.txt",'')
                items=gen.lines(text);actual+=items
                for r in items:
                    self.assertEqual(r.split(',')[0] in gen.IP_TYPES,stage=='ip')
            self.assertCountEqual(gen.lines((ROOT/entry['file']).read_text()),actual)

    def test_local_list_automatically_switches_between_direct_and_split(self):
        entry = next(r for r in self.src['rulesets'] if r['id'] == 'local_ai')
        original_read = Path.read_text
        cases = [
            ('DOMAIN,example.test\nIP-CIDR,192.0.2.0/24,no-resolve\n', True, 'ip'),
            ('DOMAIN,example.test\n', False, 'non_ip'),
            ('IP-CIDR,192.0.2.0/24,no-resolve\n', False, 'ip'),
            ('# temporarily empty\n', False, None),
        ]
        for content, mixed, stage in cases:
            with self.subTest(content=content):
                def read(path, *args, **kwargs):
                    return content if path == ROOT / entry['file'] else original_read(path, *args, **kwargs)
                with patch.object(Path, 'read_text', read):
                    files = gen.compile_config(self.src, offline=True)
                common = yaml.safe_load(files['output/common.yaml'])
                providers = common['rule-providers']
                if mixed:
                    self.assertNotIn('local_ai', providers)
                    for part in ('non_ip', 'ip'):
                        self.assertIn(f'local_ai_{part}', providers)
                        self.assertIn(f'output/rules/local_ai_{part}.txt', files)
                else:
                    self.assertFalse(any(k.startswith('output/rules/local_ai_') for k in files))
                    self.assertEqual('local_ai' in providers, stage is not None)
                if stage is not None:
                    key = 'local_ai_ip' if mixed else 'local_ai'
                    expected = f"RULE-SET,{key},{entry['group']}" + (',no-resolve' if stage == 'ip' else '')
                    self.assertIn(expected, common['rules'])

    def test_new_local_lists_and_dns_extensions(self):
        src = copy.deepcopy(self.src)
        src['rulesets'] = [
            {'id': 'new_list', 'group': src['proxy_groups'][0]['name'],
             'behavior': 'classical', 'format': 'text',
             'file': 'list/new.list', 'dns_name': 'New DNS'},
        ]
        src['settings']['dns']['nameserver-policy'] = {
            'rule-set:New DNS': 'https://example.test/dns-query',
            'geosite:cn': 'https://example.test/other-dns',
        }
        cases = [
            ('DOMAIN,example.test\n', {'new_list': 'non_ip'}),
            ('DOMAIN,example.test\nIP-CIDR,192.0.2.0/24,no-resolve\n',
             {'new_list_non_ip': 'non_ip', 'new_list_ip': 'ip'}),
            ('IP-CIDR6,2001:db8::/32,no-resolve\n', {'new_list': 'ip'}),
            ('# empty list\n', {}),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'list').mkdir()
            (root/'scripts').mkdir()
            (root/'scripts/node-flags.js').write_text((ROOT/'scripts/node-flags.js').read_text())
            for content, expected in cases:
                with self.subTest(content=content):
                    (root/'list/new.list').write_text(content)
                    with patch.object(gen, 'ROOT', root):
                        files = gen.compile_config(src, offline=True)
                    common = yaml.safe_load(files['output/common.yaml'])
                    self.assertEqual(set(common['rule-providers']), set(expected) | {'New DNS'})
                    self.assertEqual(common['dns'], src['settings']['dns'])
                    actual = []
                    for key, stage in expected.items():
                        rule = f"RULE-SET,{key},{src['rulesets'][0]['group']}"
                        if stage == 'ip':
                            rule += ',no-resolve'
                        self.assertIn(rule, common['rules'])
                        provider = common['rule-providers'][key]
                        if key == 'new_list':
                            self.assertTrue(provider['url'].endswith('/list/new.list'))
                            actual += gen.lines(content)
                        else:
                            actual += gen.lines(files[f'output/rules/{key}.txt'])
                    self.assertCountEqual(actual, gen.lines(content))
                    self.assertEqual(len([p for p in files if p.startswith('output/rules/')]),
                                     2 if len(expected) == 2 else 0)

    def test_invalid_ruleset_extensions_fail_clearly(self):
        for case, message in [('duplicate', 'Duplicate ruleset id'),
                              ('missing', 'Missing local ruleset'),
                              ('dns', 'Unknown DNS rule provider'),
                              ('format', 'Local ruleset requires classical/text')]:
            with self.subTest(case=case):
                src = copy.deepcopy(self.src)
                local = next(r for r in src['rulesets'] if 'file' in r)
                if case == 'duplicate':
                    src['rulesets'].append(copy.deepcopy(local))
                elif case == 'missing':
                    local['file'] = 'list/does-not-exist.list'
                elif case == 'format':
                    local['format'] = 'yaml'
                else:
                    src['settings']['dns']['nameserver-policy']['rule-set:missing'] = '1.1.1.1'
                with self.assertRaisesRegex(ValueError, message):
                    gen.compile_config(src, offline=True)

    def test_game_platform_uses_upstream_directly(self):
        key = 'external_Clash_GamePlatform'
        entry = next(r for r in self.src['rulesets'] if r['id'] == key)
        self.assertEqual(self.common['rule-providers'][key]['url'], entry['url'])
        self.assertFalse(any(name.startswith(f'output/rules/{key}_') for name in self.files))

    def test_preserved_filters_and_fallback(self):
        groups={g['name']:g for g in self.common['proxy-groups']}
        self.assertEqual(list(groups), [g['name'] for g in self.src['proxy_groups']])
        for original in self.src['proxy_groups']:
            actual = dict(groups[original['name']])
            expected = dict(original)
            if original.get('include-all'):
                actual.pop('filter')
                expected.pop('filter', None)
            self.assertEqual(actual, expected)

    def test_group_extensions_and_filter_composition(self):
        src = copy.deepcopy(self.src)
        src['exclude_remarks'] = '(?i)traffic|剩余'
        src['proxy_groups'] = [
            {'name': 'fallback fixture', 'type': 'fallback',
             'proxies': ['new fixture', 'DIRECT', 'REJECT'],
             'url': 'https://example.test/check', 'interval': 123},
            {'name': 'new fixture', 'type': 'url-test', 'include-all': True,
             'filter': '(?i)香港|Japan', 'url': 'https://example.test/check'},
        ] + src['proxy_groups']
        files = gen.compile_config(src, offline=True)
        groups = yaml.safe_load(files['output/common.yaml'])['proxy-groups']
        self.assertEqual(groups[0], src['proxy_groups'][0])
        pattern = re.compile(groups[1]['filter'])
        for name in ['香港 01', 'JAPAN 02']:
            self.assertIsNotNone(pattern.search(name))
        for name in ['香港 TRAFFIC', 'Japan 剩余', '美国 01']:
            self.assertIsNone(pattern.search(name))
        self.assertIn('custom_proxy_group=fallback fixture`fallback`[]new fixture`[]DIRECT`[]REJECT`',
                      files['output/main.ini'])

    def test_dns_has_no_dangling_provider_references(self):
        policy=self.common['dns']['nameserver-policy']
        self.assertEqual(policy, self.src['settings']['dns']['nameserver-policy'])
        providers = self.common['rule-providers']
        for key in policy:
            if key.startswith('rule-set:'):
                for name in key.removeprefix('rule-set:').split(','):
                    self.assertIn(name.strip(), providers)
        for entry in self.src['rulesets']:
            if not entry.get('dns_name'):
                continue
            provider = providers[entry['dns_name']]
            self.assertEqual(provider['behavior'], 'classical')
            self.assertEqual(provider['url'],
                             f"https://raw.githubusercontent.com/{self.src['repository']}/{self.src['branch']}/{entry['file']}")

    def test_legacy_entry_uses_native_provider_references(self):
        ini=self.files['output/main.ini']
        base_url = next(line.split('=', 1)[1] for line in ini.splitlines() if line.startswith('clash_rule_base='))
        raw = f"https://raw.githubusercontent.com/{self.src['repository']}/{self.src['branch']}/"
        self.assertTrue(base_url.startswith(raw))
        self.assertIn(base_url.removeprefix(raw), self.files)
        self.assertNotIn('ruleset=🟢 直连,https://',ini)
        self.assertIn('[]RULE-SET,sukka_ip_telegram_asn,no-resolve',ini)
        for group in self.src['proxy_groups']:
            self.assertIn('custom_proxy_group=' + group['name'] + '`' + group['type'] + '`', ini)
        for rule in self.common['rules']:
            if rule.startswith('RULE-SET,'):
                self.assertIn('[]RULE-SET,'+rule.split(',')[1],ini)

    def test_generation_is_reproducible(self):
        for filename,content in self.files.items():
            self.assertEqual((ROOT/filename).read_text(),content,filename)

if __name__ == '__main__': unittest.main()
