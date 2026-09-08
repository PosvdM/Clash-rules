import copy
import importlib.util
import json
import re
import subprocess
import unittest
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
        for key in ('dns', 'tun', 'hosts', 'rule-providers'):
            self.assertEqual(self.common[key], base[key])

    def test_js_retains_nodes_and_replaces_old_settings(self):
        program = """
const fs=require('fs'),vm=require('vm');
const ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync('output/override.js','utf8'),ctx);
const original={proxies:[{name:'香港 01',type:'ss',server:'example.org',password:'test-only'}],
 'proxy-providers':{airport:{type:'http',url:'https://example.org/sub'}},dns:{nameserver:['bad']},rules:['MATCH,REJECT']};
const result=ctx.main(original);
process.stdout.write(JSON.stringify(result));
"""
        result = json.loads(subprocess.check_output(['node','-e',program],cwd=ROOT))
        self.assertEqual(result.pop('proxies')[0]['password'], 'test-only')
        self.assertIn('airport', result.pop('proxy-providers'))
        self.assertEqual(result, self.common)

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
            actual=[]
            for stage in ('non_ip','ip'):
                text=self.files.get(f"output/rules/{entry['id']}_{stage}.txt",'')
                items=gen.lines(text);actual+=items
                for r in items:
                    self.assertEqual(r.split(',')[0] in gen.IP_TYPES,stage=='ip')
            self.assertCountEqual(gen.lines((ROOT/entry['file']).read_text()),actual)

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
        self.assertFalse(any(k.startswith('rule-set:') for k in policy))
        self.assertEqual(policy['+.steamserver.net'],'https://dns.alidns.com/dns-query')
        self.assertEqual(policy['+.spotifycdn.com'],'https://dns.alidns.com/dns-query')

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
