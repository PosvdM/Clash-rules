# 维护文档

## 文件结构

| 路径 | 用途 |
| --- | --- |
| `source.yaml` | 规则引用、策略组、节点筛选和 DNS 设置 |
| `list/*.list` | 自定义规则 |
| `scripts/generate.py` | 配置生成器 |
| `scripts/node-flags.js` | JS 节点国旗补全 |
| `tests/test_config.py` | 配置与生成行为测试 |
| `.github/workflows/generate.yml` | 自动校验、生成和提交 |
| `output/common.yaml` | 公共配置，供查看或合并，不含节点 |
| `output/PosvdM_rules.js` | Clash Party、FlClash 完整版覆写 |
| `output/override.js` | 完整版 JS 的旧链接兼容副本 |
| `output/PosvdM_rules_simple.js` | 四分类 JS 覆写 |
| `output/PosvdM_rules_simple.yaml` | 四分类 YAML 配置，需补入节点或 provider |
| `output/override.stoverride` | Stash 覆写 |
| `output/rules/` | 拆分规则快照 |
| `output/main.ini`、`output/GeneralClashConfig.yml` | Subconverter 入口及基础模板 |
| `archive/` | 历史配置、测试模板、PAC 和参考文件，不参与构建 |

日常修改 `source.yaml` 和 `list/`，然后重新生成 `output/`，不要直接修改产物。构建逻辑、测试和说明分别放在 `scripts/`、`tests/`、`docs/`。

旧入口迁移：

- Clash Party 用导入 URL 的文件名作为覆写标题。旧 `override.js` 仍同步更新；要改为 `PosvdM_rules.js`，可编辑客户端条目名称，或用新链接重新导入。
- `rules/main.ini`、`yml/GeneralClashConfig.yml` 已移至 `output/`，旧目录不再保留。使用旧地址的订阅需更新链接。
- 历史文件的新旧路径见[归档索引](../archive/README.md)。归档不自动更新，可能依赖旧版客户端或已变化的上游。

## 添加规则

在对应列表中每行写一条规则，`#` 开头的行是注释。

| 文件 | 用途 |
| --- | --- |
| [ai.list](../list/ai.list) | AI 服务 |
| [proxy.list](../list/proxy.list) | 代理访问 |
| [direct.list](../list/direct.list) | 直连 |
| [SteamDownload.list](../list/SteamDownload.list) | Steam 下载直连 |
| [bulk.list](../list/bulk.list) | 大宗流量 |
| [reject.list](../list/reject.list) | 拦截 |
| [sexy.list](../list/sexy.list) | 成人内容 |
| [final.list](../list/final.list) | 指定站点交给“漏网之鱼”组 |

`list/game.list` 供单独使用，未被 `source.yaml` 引用；当前游戏平台分流使用上游 GamePlatform 规则。

例如，在 `list/proxy.list` 添加：

```text
# 示例站点
DOMAIN-SUFFIX,example.com
DOMAIN,api.example.net
```

现有列表增删域名或 IP 无需修改 `source.yaml`。生成器直接引用单一类型列表，拆分混合 IP/非 IP 列表，跳过空列表。增删 IP 导致拆分方式变化后，需更新覆写或重新生成订阅。

新增列表时，在 `source.yaml` 的 `rulesets` 中按所需优先级登记：

```yaml
- id: local_custom
  group: 🚀 节点选择
  behavior: classical
  format: text
  file: list/custom.list
```

`id` 必须唯一，`group` 必须已存在。仅上传 `.list` 不会加入分流；登记后无需手建快照或修改测试。外部规则使用 `url` 和 `stage`；需拆分的远程 classical 列表加上 `split: true`，再在线生成快照。

拆分列表不支持 `MATCH`、`FINAL`、`RULE-SET`、`AND`、`OR`、`NOT`，遇到这些规则会报错。重复 ID、缺失文件、本地列表格式错误或 DNS 引用不存在的 provider 也会使生成失败，并提示具体条目。

策略组类型、选项及顺序以 `source.yaml` 为准；测试不固定选项名单或 DNS 策略数量。

## 规则与 DNS

规则按以下阶段排列，各阶段保留源配置顺序：

**非 IP → GEOSITE CN → IP → GEOIP CN → MATCH**

IP 规则集引用使用 `no-resolve`，末尾只保留一个 MATCH。

Sukka、anti-AD、GamePlatform 和单一类型的本地列表由客户端直接更新。远程 YouTube、GoogleFCM 列表及本地混合列表由生成器拆分。第三方规则遵循各自许可证，快照的 `Source` 注释保留上游地址。

DNS 使用规则集引用，不展开域名：

```yaml
nameserver-policy:
  rule-set:local_direct: https://dns.alidns.com/dns-query
  rule-set:local_SteamDownload: https://dns.alidns.com/dns-query
  geosite:cn,private,apple: https://dns.alidns.com/dns-query
  geosite:!cn,gfw: https://posvdm.cloudflare-gateway.com/dns-query
```

`dns_name` 为本地列表指定 classical provider 名称，直接引用原列表：

- 单一类型列表：DNS 与分流共用 `local_*` provider。
- 混合 IP/非 IP 列表：DNS 引用原列表，分流引用拆分后的 provider，保持规则顺序。

新增 DNS 规则集引用时，须确保 provider 存在。列表内容变化后刷新规则集；DNS 设置变化后更新覆写或订阅。TUN 开关、协议栈和路由由客户端管理。

## 四分类精简版

`simple_groups` 将 `direct`、`proxy`、`reject`、`match` 关联到四个不同的已有策略组。名称、emoji、`icon` 和组顺序沿用 `proxy_groups`；更名时需同步修改引用。

生成器先编译完整规则，再将业务组映射到四类：

| 类别 | 规则目标与节点选择 |
| --- | --- |
| 直连 | 保留原目标，默认 DIRECT |
| 代理 | 接收其余业务组规则，通过 `url-test` 自动选择节点 |
| 拒绝 | 保留原目标，默认 REJECT |
| MATCH | 保留漏网之鱼规则（含 `local_final`），承接末尾 MATCH，默认 DIRECT |

规则内容、顺序、`no-resolve`、provider 和 DNS 与完整版一致。新增业务规则自动归入代理，无需另建规则清单。

代理组通过 `include-all` 纳入节点和 provider，用 `exclude_remarks` 排除提示节点；测速 URL、间隔和容差由 `simple_url_test` 设置。其余三组保留源组类型、图标等字段，选项映射到四类后去重，不保留地区、自动选择或低倍率子组。

两份精简产物均参与生成、`--check` 和 Actions 更新。JS 共用完整版的订阅清理、凭据保留及国旗逻辑；YAML 需补入节点，不执行 JS，也不使用 Stash 的 `#!replace`。

## 节点名称与国旗

JS 根据 `node_flags` 别名表为节点名称补国旗，支持中文、英文和大写地区缩写（如 `HK01`）。只匹配名称，不查询服务器 IP 或判断真实出口位置。

| 情况 | 处理方式 |
| --- | --- |
| 有 `\|` 或 `｜` | 国旗放在第一个分隔符后，如 `🌸\|印度标准 IEPL 专线 1` → `🌸\|🇮🇳 印度标准 IEPL 专线 1` |
| 无分隔符 | 国旗放在名称开头 |
| 国旗在分隔符前 | 将开头的国旗移到分隔符后，如 `🇮🇳 🌸\|印度…` → `🌸\|🇮🇳 印度…` |
| 其他已有国旗、无法识别、命中多个地区或名称冲突 | 保留原名 |

匹配重叠时优先完整地区名，避免把“印度尼西亚”认成“印度”。原图标、编号、线路说明、连接参数和凭据保留；`dialer-proxy`、provider 的 `proxy` 及 `override.dialer-proxy` 引用随改名更新。

处理范围包括 `proxies` 和未设置筛选或名称覆写的 inline provider。带 `filter`、`exclude-filter` 或名称覆写的 inline provider 保留原名，避免影响内核后续处理。远程、文件 provider 由内核加载，JS 不下载或改名。参见 [Mihomo 代理集合文档](https://wiki.metacubex.one/config/proxy-providers/)。

更新 JS 覆写并重新应用后生效，改名的节点可能需重新选择。此功能不改变分流策略，Stash 静态覆写和 Subconverter 不提供国旗补全。

## 自动构建

| 触发方式 | 操作 |
| --- | --- |
| 推送到 `main` | 校验、在线生成，机器人提交产物变化 |
| PR 更新 | 校验，不提交产物 |
| 每天北京时间 10:19（`19 2 * * *`） | 定时同步 |
| [Actions](https://github.com/PosvdM/Clash-rules/actions/workflows/generate.yml) → **Run workflow** | 手动同步 |

定时任务避开整点高峰，但 GitHub 不保证准时启动，见[调度说明](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows#schedule)。

校验任务只读，更新任务使用 `contents: write`。抓取或编译失败时不写入产物。构建完成后仍需在客户端更新规则集或覆写。

## 本地验证

使用 Python 3.12 和 Node.js 22：

```sh
python -m pip install -r scripts/requirements.txt
python scripts/generate.py
python -m unittest discover -s tests -v
```

离线生成读取已提交的远程快照，本地列表仍实时读取：

```sh
python scripts/generate.py --offline
python scripts/generate.py --offline --check
```

`--check` 不写文件；产物不一致或存在过期快照时失败。

测试覆盖跨入口一致性、规则拆分与保全、节点与凭据保留、订阅字段清理（含 TUN）、筛选、DNS 引用、国旗和图标更新、输入不变、重复执行隔离及可重复生成。自动测试不能替代客户端的 VPN、DNS 和联网验证。

## 客户端兼容

各入口共享配置数据，字段是否生效取决于内核。Mihomo 支持 DNS 的 `rule-set:`；Stash 文档未明确说明支持，需在设备上确认。其他 DNS、fake-ip、fallback 字段也需分别确认。

### JavaScript 覆写

覆写从公共配置创建新对象，仅复制订阅的 `proxies` 和 `proxy-providers`。其余订阅顶层字段全部丢弃，包括 `sniffer`、`geox-url`、`tun`、端口、认证、监听器及未知字段。公共设置写入 `source.yaml` 的 `settings`；节点连接字段、凭据及 provider 的 URL 和连接选项保留。

`exclude_remarks` 同时用于 JS、策略组筛选和 Subconverter。JS 删除 `proxies` 及内联 `payload` 中的提示节点（如 Traffic、Expire、流量、到期），并给 provider 补入 `exclude-filter`，供内核过滤后续加载的节点。已有排除条件按“或”合并，保留大小写语义。不按服务器地址删除节点；若全部被过滤，返回空列表，需补充有效订阅。参见 [Mihomo 排除筛选说明](https://wiki.metacubex.one/config/proxy-providers/#exclude-filter)。

Clash Party 执行覆写后还会合并客户端设置。要保留脚本中的 DNS 和嗅探配置，需关闭客户端对应覆写，并避免叠加其他配置覆写。端口、TUN、控制接口和 Geo 数据地址等由客户端管理，仍可能出现在运行配置中，不能据此判断订阅字段残留。参见 [Clash Party 配置生成逻辑](https://github.com/mihomo-party-org/clash-party/blob/smart_core/src/main/core/factory.ts)。

### Stash

以 `#!replace` 替换列出的映射和数组，未列出的订阅字段仍会保留。

### Subconverter

使用字面 `RULE-SET` 引用，后端须保留基础模板中的 `rule-providers`。公共配置不含节点，不能直接作为独立订阅连接。
