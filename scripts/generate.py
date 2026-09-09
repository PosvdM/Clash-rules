#!/usr/bin/env python3
"""One source, one policy. Client wrappers never introduce platform-specific rules."""
import argparse
import copy
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
IP_TYPES = {'IP-CIDR', 'IP-CIDR6', 'IP-ASN', 'GEOIP'}
HEADER = '# Generated from source.yaml by scripts/generate.py; do not edit.\n'


def dump(value):
    return yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=180)


def lines(text):
    return [s.strip() for s in text.splitlines() if s.strip() and not s.lstrip().startswith(('#', ';', '//'))]


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'PosvdM-Clash-rules/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read().decode('utf-8-sig')
    if not lines(content) or '<html' in content.lower():
        raise ValueError(f'Empty or invalid upstream: {url}')
    return content


def compile_config(src, offline=False):
    raw = f"https://raw.githubusercontent.com/{src['repository']}/{src['branch']}"
    files = {}
    settings = copy.deepcopy(src['settings'])
    # Use explicit domain policies on every platform; no subconverter-generated provider names.
    direct_dns = settings['dns']['nameserver'][0]
    explicit = {}
    for filename in src.get('dns_direct_lists', []):
        for rule in lines((ROOT / filename).read_text()):
            kind, value, *_ = rule.split(',')
            if kind in ('DOMAIN', 'DOMAIN-SUFFIX'):
                explicit[('+' + '.' if kind == 'DOMAIN-SUFFIX' else '') + value] = direct_dns
    settings['dns']['nameserver-policy'] = {**explicit, **settings['dns'].get('nameserver-policy', {})}

    groups = copy.deepcopy(src['proxy_groups'])
    exclusion = src['exclude_remarks'].removeprefix('(?i)')
    names = [g['name'] for g in groups]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate group name')
    for g in groups:
        for name in g.get('proxies', []):
            if name not in names + ['DIRECT', 'REJECT']:
                raise ValueError(f'Unknown group: {name}')
        if g.get('include-all'):
            original = g.get('filter', '.*').removeprefix('(?i)')
            # Both assertions start at the beginning: do not break (?i), alternation or lookaheads.
            g['filter'] = f'(?i)^(?!.*(?:{exclusion}))(?=[\\s\\S]*(?:{original}))[\\s\\S]*$'

    providers, non_ip, ip = {}, [], []
    split_rules = [r for r in src['rulesets'] if 'file' in r or r.get('split')]

    def get_split(rule):
        if 'file' in rule:
            return (ROOT / rule['file']).read_text()
        if offline:
            parts = [ROOT / f"output/rules/{rule['id']}_{stage}.txt" for stage in ('non_ip', 'ip')]
            if not any(p.exists() for p in parts):
                raise ValueError(f"Missing offline snapshots: {rule['id']}")
            return '\n'.join(p.read_text() for p in parts if p.exists())
        return fetch(rule['url'])

    with ThreadPoolExecutor(max_workers=6) as pool:
        contents = dict(zip((r['id'] for r in split_rules), pool.map(get_split, split_rules)))

    def add(rule, key, url, stage, behavior=None):
        if key in providers:
            raise ValueError(f'Duplicate provider: {key}')
        providers[key] = {'type': 'http', 'behavior': behavior or rule['behavior'],
                          'format': rule['format'], 'url': url,
                          'path': f'./ruleset/posvdm/{key}.txt', 'interval': 86400}
        target = ip if stage == 'ip' else non_ip
        target.append(f"RULE-SET,{key},{rule['group']}" + (',no-resolve' if stage == 'ip' else ''))

    for rule in src['rulesets']:
        if rule['group'] not in names:
            raise ValueError(f"Unknown policy: {rule['group']}")
        if 'file' in rule or rule.get('split'):
            text = contents[rule['id']]
            buckets = {'non_ip': [], 'ip': []}
            for item in lines(text):
                kind = item.split(',', 1)[0]
                if ',' not in item or kind in {'MATCH', 'FINAL', 'RULE-SET', 'AND', 'OR', 'NOT'}:
                    raise ValueError(f"Unsupported rule for safe split: {rule['id']}: {item}")
                buckets['ip' if kind in IP_TYPES else 'non_ip'].append(item)
            origin = rule.get('url', raw + '/' + rule.get('file', ''))
            # Local lists only need snapshots when they mix IP and non-IP rules.
            # Adding/removing IP rules requires no source.yaml changes.
            if 'file' in rule and not all(buckets.values()):
                stage = 'ip' if buckets['ip'] else 'non_ip'
                if any(buckets.values()):
                    add(rule, rule['id'], origin, stage)
                continue
            # Keep attribution/comments from the original list, without recursively duplicating generated headers.
            comments = '\n'.join(x for x in text.splitlines() if x.startswith('#') and not x.startswith(('# Generated', '# Source:')))
            comments = '\n'.join(dict.fromkeys(comments.splitlines()))
            for stage, items in buckets.items():
                if not items:
                    continue
                key = rule['id'] + '_' + stage
                path = f'output/rules/{key}.txt'
                files[path] = HEADER + f'# Source: {origin}\n' + comments + '\n' + '\n'.join(items) + '\n'
                add(rule, key, raw + '/' + path, stage)
        else:
            if rule['behavior'] == 'domain' and rule['stage'] == 'ip':
                raise ValueError('Domain rule cannot be in IP stage')
            add(rule, rule['id'], rule['url'], rule['stage'])

    tail = src['tail_rules']
    # Country domain fallback remains before every IP rule. IP order is stable.
    domain_tail = [r for r in tail if r.startswith('GEOSITE,')]
    final_tail = [r for r in tail if not r.startswith('GEOSITE,')]
    rules = non_ip + domain_tail + ip + final_tail
    if not rules[-1].startswith('MATCH,') or sum(x.startswith('MATCH,') for x in rules) != 1:
        raise ValueError('Exactly one final MATCH required')
    common = {**settings, 'proxy-groups': groups, 'rule-providers': providers, 'rules': rules}
    files['output/common.yaml'] = HEADER + dump(common)
    # Both JS consumers execute precisely the same policy, without changing subscription credentials.
    js = '// Generated from source.yaml; shared by Clash Party and FlClash.\n'
    js += 'const policy = ' + json.dumps(common, ensure_ascii=False, indent=2) + ';\n'
    js += '''function main(config) {
  if (!config || typeof config !== 'object') throw new Error('需要先导入机场订阅');
  if (!(Array.isArray(config.proxies) && config.proxies.length) &&
      !Object.keys(config['proxy-providers'] || {}).length) throw new Error('订阅中没有代理节点');
  // Replace whole sections, preventing the subscription's DNS/rules from being merged back in.
  for (const key of Object.keys(policy)) config[key] = JSON.parse(JSON.stringify(policy[key]));
  return config;
}
'''
    files['output/override.js'] = js
    stash = 'name: PosvdM 全平台统一配置\ndesc: 由 source.yaml 生成；规则、DNS 与桌面及 Android 同源；TUN 由客户端管理。\n'
    for key, value in common.items():
        section = dump({key: value})
        if isinstance(value, (list, dict)):
            section = section.replace(key + ':', key + ': #!replace', 1)
        stash += section
    files['output/override.stoverride'] = HEADER + stash

    # Legacy INI entry point: the converter only creates node groups. Providers are native in base YAML.
    # Literal RULE-SET references pass through unchanged, including ASN and text domain/ipcidr providers.
    ini = [HEADER.rstrip(), '[custom]', 'exclude_remarks=' + src['exclude_remarks']]
    for rule in rules:
        fields = rule.split(',')
        if fields[0] == 'MATCH':
            ini.append(f'ruleset={fields[1]},[]FINAL')
        else:
            ini.append(f'ruleset={fields[2]},[]{fields[0]},{fields[1]}' + (',' + ','.join(fields[3:]) if len(fields) > 3 else ''))
    for g in src['proxy_groups']:
        parts = [g['name'], g['type']] + ['[]' + p for p in g.get('proxies', [])]
        if 'filter' in g:
            parts.append(g['filter'])
        if g['type'] != 'select':
            parts += [g['url'], f"{g.get('interval',300)},,{g.get('tolerance',50)}"]
        ini.append('custom_proxy_group=' + '`'.join(parts))
    ini += ['enable_rule_generator=true', 'overwrite_original_rules=true',
            f'clash_rule_base={raw}/yml/GeneralClashConfig.yml', '']
    files['rules/main.ini'] = '\n'.join(ini)
    files['yml/GeneralClashConfig.yml'] = HEADER + dump({**settings, 'rule-providers': providers})
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--offline', action='store_true', help='Reuse committed upstream split snapshots')
    parser.add_argument('--check', action='store_true', help='Verify reproducible generated files without writing')
    args = parser.parse_args()
    src = yaml.safe_load((ROOT / 'source.yaml').read_text())
    files = compile_config(src, args.offline)
    stale = set(str(p.relative_to(ROOT)) for p in (ROOT / 'output/rules').glob('*.txt')) - files.keys()
    if args.check:
        mismatch = [name for name, text in files.items() if not (ROOT/name).exists() or (ROOT/name).read_text() != text]
        if mismatch or stale:
            raise SystemExit('Out of date outputs: ' + ', '.join(mismatch + sorted(stale)))
    else:
        # All fetches and validation completed before mutating any output.
        for name, text in files.items():
            path = ROOT / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        for name in stale:
            (ROOT / name).unlink()
    print(f'Validated {len(files)} generated files')


if __name__ == '__main__':
    main()
