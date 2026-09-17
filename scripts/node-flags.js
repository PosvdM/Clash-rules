// Add flags from node names, without IP lookups.
function addNodeFlags(config) {
  const flagPresent = /[\u{1F1E6}-\u{1F1FF}]{2}/u;
  const leadingFlag = /^(?<flag>[\u{1F1E6}-\u{1F1FF}]{2})\s*/u;
  const separatorPrefix = /^[^|｜]*[|｜]\s*/u;
  const placeFlag = (name, flag) => {
    const prefix = name.match(separatorPrefix)?.[0] || '';
    return prefix + flag + ' ' + name.slice(prefix.length);
  };
  const matchers = Object.entries(nodeFlagAliases).map(([code, aliases]) => ({
    flag: Array.from(code, c => String.fromCodePoint(0x1F1E6 + c.charCodeAt(0) - 65)).join(''),
    // Use letter boundaries so IN/US cannot match BUSINESS.
    patterns: aliases.map(alias => {
      const escaped = alias.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      return new RegExp(/[A-Za-z]/.test(alias) ? '(^|[^A-Za-z])(?<region>' + escaped + ')(?![A-Za-z])' : '(?<region>' + escaped + ')', /^[A-Z]{2,3}$/.test(alias) ? 'g' : 'gi');
    })
  }));
  const providers = Object.values(config['proxy-providers'] || {});
  const allNodes = [...(config.proxies || []), ...providers.flatMap(p => p.payload || [])];
  // Preserve names used by provider filters or name overrides in the core.
  const eligible = new Set(config.proxies || []);
  for (const p of providers) {
    const o = p.override || {};
    if (p.type === 'inline' && !p.filter && !p['exclude-filter'] &&
        !o['proxy-name'] && !o['additional-prefix'] && !o['additional-suffix'] && !o['override-expr']) {
      for (const node of p.payload || []) eligible.add(node);
    }
  }
  const reserved = new Set(['DIRECT', 'REJECT', ...config['proxy-groups'].map(g => g.name),
    ...Object.keys(config['proxy-providers'] || {})]);
  const occupied = new Set([...reserved, ...allNodes.map(n => n.name)]);
  const proposals = new Map();
  for (const node of allNodes) {
    const name = node.name;
    if (!eligible.has(node) || typeof name !== 'string' || reserved.has(name)) continue;
    if (flagPresent.test(name)) {
      // Move a leading flag after the first separator.
      const leading = name.match(leadingFlag);
      const rest = leading ? name.slice(leading[0].length) : '';
      if (leading && separatorPrefix.test(rest) && !flagPresent.test(rest)) {
        const target = placeFlag(rest, leading.groups.flag);
        if (!occupied.has(target)) proposals.set(name, target);
      }
      continue;
    }
    const hits = matchers.flatMap(m => m.patterns.flatMap(pattern => {
      return Array.from(name.matchAll(pattern), match => {
        const end = match.index + match[0].length;
        return {flag: m.flag, start: end - match.groups.region.length, end};
      });
    }));
    // Prefer full region names: 印度尼西亚 over 印度.
    const matches = new Set(hits.filter(h => !hits.some(other =>
      other.start <= h.start && other.end >= h.end &&
      other.end - other.start > h.end - h.start)).map(h => h.flag));
    if (matches.size !== 1) continue;
    const target = placeFlag(name, [...matches][0]);
    if (!occupied.has(target)) proposals.set(name, target);
  }
  // Preserve names shared with nodes that cannot be renamed.
  for (const node of allNodes) if (!eligible.has(node)) proposals.delete(node.name);
  // Reject renames that would share a target name.
  const targetCounts = new Map();
  for (const target of proposals.values()) targetCounts.set(target, (targetCounts.get(target) || 0) + 1);
  for (const [name, target] of proposals) if (targetCounts.get(target) > 1) proposals.delete(name);
  const rename = name => proposals.get(name) || name;
  for (const node of allNodes) {
    node.name = rename(node.name);
    if (typeof node['dialer-proxy'] === 'string') node['dialer-proxy'] = rename(node['dialer-proxy']);
  }
  for (const p of providers) {
    if (typeof p.proxy === 'string') p.proxy = rename(p.proxy);
    if (typeof p.override?.['dialer-proxy'] === 'string') {
      p.override['dialer-proxy'] = rename(p.override['dialer-proxy']);
    }
  }
}
