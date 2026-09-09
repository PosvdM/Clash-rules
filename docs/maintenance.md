# 维护文档

## 文件结构

| 路径 | 用途 |
| --- | --- |
| `source.yaml` | 规则引用、策略组、节点筛选和 DNS 设置 |
| `list/*.list` | 自定义规则内容 |
| `scripts/generate.py` | 配置生成器 |
| `tests/test_config.py` | 配置与生成行为测试 |
| `.github/workflows/generate.yml` | 自动校验、生成和提交 |
| `output/common.yaml` | 不含节点的公共配置，供查看或合并 |
| `output/override.js` | Clash Party、FlClash 共用覆写 |
| `output/override.stoverride` | Stash 覆写 |
| `output/rules/` | 需要拆分的规则快照 |
| `rules/main.ini`、`yml/GeneralClashConfig.yml` | Subconverter 入口及基础模板 |

`output/` 和 Subconverter 入口由程序生成。修改源文件后重新生成，不要手动维护产物。

## 添加规则

在对应列表中每行写一条规则，以 `#` 开头的行是注释。

| 文件 | 策略用途 |
| --- | --- |
| [ai.list](../list/ai.list) | AI 服务 |
| [proxy.list](../list/proxy.list) | 代理访问 |
| [direct.list](../list/direct.list) | 直连 |
| [SteamDownload.list](../list/SteamDownload.list) | Steam 下载直连 |
| [bulk.list](../list/bulk.list) | 大宗流量 |
| [reject.list](../list/reject.list) | 拦截 |
| [sexy.list](../list/sexy.list) | 成人内容分组 |
| [final.list](../list/final.list) | 使用“漏网之鱼”策略组的指定站点 |

例如，在 `list/proxy.list` 中添加：

```text
# 示例站点
DOMAIN-SUFFIX,example.com
DOMAIN,api.example.net
```

向现有列表添加域名或 IP，无需修改 `source.yaml`。单一类型的本地列表直接引用原文件；混合域名/进程与目标 IP 时自动拆分；空列表暂时跳过。添加或移除 IP 导致拆分方式变化后，需要更新客户端覆写或重新生成订阅。

新增列表时，在 `source.yaml` 的 `rulesets` 中添加唯一 `id`、已有策略组 `group`、`behavior: classical`、`format: text` 和 `file: list/文件名.list`。本地列表由生成器判断类型。外部规则使用 `url` 和 `stage`；需拆分的远程 classical 列表设置 `split: true`，并在线生成一次快照。

## 规则与 DNS

规则顺序为：非 IP 规则 → GEOSITE CN → IP 规则 → GEOIP CN → MATCH。各阶段保持源配置顺序，IP 规则集引用使用 `no-resolve`。

Sukka、anti-AD、GamePlatform 和单一类型的本地列表由客户端直接更新。远程 YouTube、GoogleFCM 列表及本地混合列表由生成器拆分。第三方规则遵循各自许可证，快照中的 `Source` 注释保留上游地址。

DNS 保持规则集引用，不展开域名：

```yaml
nameserver-policy:
  rule-set:direct (Domain): https://dns.alidns.com/dns-query
  rule-set:SteamDownload (Domain): https://dns.alidns.com/dns-query
  geosite:cn,private,apple: https://dns.alidns.com/dns-query
  geosite:!cn,gfw: https://posvdm.cloudflare-gateway.com/dns-query
```

`dns_name` 为直连和 Steam 列表生成同名 classical provider，直接引用原始列表。修改列表内容后刷新规则集即可；修改 DNS 设置后更新覆写或订阅。TUN 开关、协议栈和路由由客户端管理。

## 自动构建

每次提交到 `main` 都会触发校验和在线生成，有变化的产物由机器人提交。PR 更新执行校验，不提交产物。也可以在 [Actions 页面](https://github.com/PosvdM/Clash-rules/actions/workflows/generate.yml) 选择 **Run workflow** 手动运行。

定时任务使用 `19 2 * * *`，即每天北京时间 10:19。选择非整点是为了避开任务高峰；GitHub 不保证准时启动。[GitHub 调度说明](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows#schedule)

校验任务使用只读权限，更新任务声明 `contents: write`。在线抓取或编译失败时不会写入产物。构建成功不代表客户端已经刷新，需要在客户端更新规则集或覆写。

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

`--check` 不写入文件，发现生成内容不一致或存在过期快照时失败。测试覆盖跨入口一致性、JS 保留节点及 TUN、规则保全与拆分、筛选、DNS 引用和可重复生成。

## 客户端兼容

各入口共享配置数据，字段是否生效取决于内核。Mihomo 支持 DNS 的 `rule-set:` 写法；Stash 文档未明确说明支持，需在设备上确认。Stash 对部分 Mihomo DNS/fake-ip/fallback 字段的支持也不能假定相同。

Stash 覆写以 `#!replace` 替换映射和数组；JS 覆写替换公共配置字段，保留订阅节点、`proxy-providers` 及客户端传入的 TUN 设置。

Subconverter 使用字面 `RULE-SET` 引用，后端必须保留基础模板中的 `rule-providers`。公共配置不含代理节点，不能作为独立订阅连接。自动测试不能替代客户端的 VPN、DNS 和联网验证。
