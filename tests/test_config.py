import copy
import importlib.util
import json
import re
import subprocess
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

    def test_all_wrappers_share_entire_policy(self):
        stash = yaml.safe_load(self.files['output/override.stoverride'])
        stash.pop('name'); stash.pop('desc')
        self.assertEqual(self.common, stash)
        for key, value in self.common.items():
            if isinstance(value, (list, dict)):
                self.assertIn(key + ': #!replace', self.files['output/override.stoverride'])
        base = yaml.safe_load(self.files['yml/GeneralClashConfig.yml'])
        for config in (self.common, stash, base):
            self.assertNotIn('tun', config)
        for key in ('dns', 'hosts', 'rule-providers'):
            self.assertEqual(self.common[key], base[key])

    def test_js_retains_nodes_and_replaces_old_settings(self):
        program = """
const fs=require('fs'),vm=require('vm');
const ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('output/override.js','utf8'),ctx);
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
            'header': {'Authorization': ['test-only']}})
        self.assertEqual(result, self.common)

    def test_js_node_sources_errors_and_repeat_calls(self):
        program = """
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('output/override.js','utf8'),ctx);
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
            'airport': {'type': 'http', 'url': 'https://example.org/sub'}})
        self.assertEqual(nodes, self.common)
        self.assertEqual(providers, self.common)

    def test_order_and_native_formats(self):
        providers = self.common['rule-providers']
        rules = self.common['rules']
        self.assertEqual(rules[-1], 'MATCH,🐟 漏网之鱼')
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

    def test_game_platform_uses_upstream_directly(self):
        key = 'external_Clash_GamePlatform'
        entry = next(r for r in self.src['rulesets'] if r['id'] == key)
        self.assertEqual(self.common['rule-providers'][key]['url'], entry['url'])
        self.assertFalse(any(name.startswith(f'output/rules/{key}_') for name in self.files))

    def test_preserved_filters_and_fallback(self):
        groups={g['name']:g for g in self.common['proxy-groups']}
        low=groups['🏷️ 低倍率']
        self.assertEqual(low['type'],'fallback')
        self.assertEqual(low['proxies'],['🧪 低倍检测','🚀 节点选择'])
        auto=re.compile(groups['🇭🇰 香港']['filter'])
        self.assertTrue(auto.search('香港 01'))
        for name in ['香港 2x','香港 0.1x','香港 小带宽','香港 剩余 100GB','日本 01']:
            self.assertFalse(auto.search(name),name)
        for original in self.src['proxy_groups']:
            self.assertEqual(groups[original['name']]['type'],original['type'])
            self.assertEqual(groups[original['name']].get('proxies'),original.get('proxies'))

    def test_dns_has_no_dangling_provider_references(self):
        policy=self.common['dns']['nameserver-policy']
        self.assertEqual(policy, self.src['settings']['dns']['nameserver-policy'])
        for name, filename in [('direct (Domain)', 'direct'), ('SteamDownload (Domain)', 'SteamDownload')]:
            self.assertEqual(policy['rule-set:' + name], 'https://dns.alidns.com/dns-query')
            provider = self.common['rule-providers'][name]
            self.assertEqual(provider['behavior'], 'classical')
            self.assertEqual(provider['url'], f'https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/{filename}.list')
        self.assertEqual(len(policy), 4)

    def test_legacy_entry_uses_native_provider_references(self):
        ini=self.files['rules/main.ini']
        self.assertNotIn('ruleset=🟢 直连,https://',ini)
        self.assertIn('[]RULE-SET,sukka_ip_telegram_asn,no-resolve',ini)
        self.assertIn('custom_proxy_group=🏷️ 低倍率`fallback`',ini)
        for rule in self.common['rules']:
            if rule.startswith('RULE-SET,'):
                self.assertIn('[]RULE-SET,'+rule.split(',')[1],ini)

    def test_generation_is_reproducible(self):
        for filename,content in self.files.items():
            self.assertEqual((ROOT/filename).read_text(),content,filename)

if __name__ == '__main__': unittest.main()
