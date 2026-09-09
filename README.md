# PosvdM 分流配置

供 Clash Party、FlClash 和 Stash 使用的分流配置。通过一份 `source.yaml` 管理规则引用、策略组、DNS 和 TUN，自定义规则存放在 `list/`。

包含广告拦截、AI、流媒体、游戏平台、Telegram 等分流策略，以及地区节点选择和低倍率 fallback 策略组。配置不提供代理节点，需要搭配自己的订阅使用。

## 导入使用

先导入代理订阅，再添加对应的覆写并绑定到当前配置。覆写保留订阅中的节点和 `proxy-providers`，替换规则、策略组及公共设置。

| 客户端 | 配置入口 |
| --- | --- |
| Windows / macOS：Clash Party | [JS 覆写](https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.js) |
| Android：FlClash | [JS 覆写](https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.js)，需要支持覆写脚本的版本 |
| iOS / iPadOS：Stash | [Stash 覆写](https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.stoverride) |
| Subconverter | [远程配置 main.ini](https://raw.githubusercontent.com/PosvdM/Clash-rules/main/rules/main.ini) |

复制链接时，请复制表格中的链接地址。启用后更新规则集，并在策略组中选择节点。

同一订阅只启用一份主规则覆写；客户端额外设置的 DNS 或 TUN 覆盖若与本配置冲突，需要关闭。

Subconverter 后端需要保留基础模板中的 `rule-providers`，最终规则通过 `RULE-SET` 引用规则集。若后端不支持，请使用客户端覆写。

## 添加规则

直接编辑对应的 `.list` 文件，每行一条规则，以 `#` 开头的行是注释。

| 文件 | 用途 |
| --- | --- |
| [ai.list](list/ai.list) | AI 服务 |
| [proxy.list](list/proxy.list) | 代理访问 |
| [direct.list](list/direct.list) | 直连 |
| [SteamDownload.list](list/SteamDownload.list) | Steam 下载直连 |
| [bulk.list](list/bulk.list) | 大宗流量 |
| [reject.list](list/reject.list) | 拦截 |
| [sexy.list](list/sexy.list) | 成人内容分组 |
| [final.list](list/final.list) | 使用“漏网之鱼”策略组的指定站点 |

例如，在 `list/proxy.list` 中添加：

```text
# 示例站点
DOMAIN-SUFFIX,example.com
DOMAIN,api.example.net
```

向现有列表添加域名或 IP 时，无需修改 `source.yaml`。生成器会判断列表内容：单一类型直接引用原文件，混合域名/进程与目标 IP 时自动拆分，空列表暂时跳过。生成的 IP 规则集引用放在非 IP 规则之后，并使用 `no-resolve`。

新增列表、调整规则引用顺序或策略组、修改 DNS/TUN 时，编辑 [source.yaml](source.yaml)。`output/`、`rules/main.ini` 和 `yml/GeneralClashConfig.yml` 由程序生成，无需手动维护。

## 自动更新

[GitHub Actions](https://github.com/PosvdM/Clash-rules/actions/workflows/generate.yml) 在相关源文件推送到 `main` 后运行，生成配置、执行测试，并提交有变化的产物。工作流每天北京时间 10:19 同步需要拆分的远程列表；GitHub 调度可能延迟。也可以在工作流页面通过 **Run workflow** 手动运行。

客户端直接更新 Sukka、anti-AD 等上游规则和单一类型的本地列表。SteamDownload 等本地混合列表，以及 YouTube、GoogleFCM 的拆分快照，由 Actions 生成。

普通规则内容更新后，在客户端刷新规则集即可。如果列表因添加或移除 IP 改变了拆分方式，或修改了策略组、DNS/TUN，还需要更新覆写或重新生成订阅。直连和 Steam 列表中的域名也用于生成 DNS 策略，修改后应一并更新覆写或订阅。

## 客户端兼容

各入口由同一份配置生成，但字段是否生效取决于客户端内核。Stash 的 VPN 由系统接管，Mihomo 的 TUN 栈和部分 DNS/fake-ip/fallback 设置不一定适用。手机需要授予 VPN 权限，桌面 TUN 需要客户端服务权限。

[common.yaml](output/common.yaml) 是不含代理节点的公共配置，供查看或合并使用，不能作为独立订阅连接。

## 本地生成

需要 Python 3.12 和 Node.js 22。

```sh
python -m pip install -r scripts/requirements.txt
python scripts/generate.py
python -m unittest discover -s tests -v
```

离线生成使用已提交的远程快照，自定义列表仍从本地读取：

```sh
python scripts/generate.py --offline
python scripts/generate.py --offline --check
```

`--check` 检查生成文件是否与源配置一致，不写入文件。测试覆盖配置一致性、节点保留、规则拆分与顺序、节点筛选和 DNS 引用；实际联网效果需在客户端确认。

## 规则来源

规则引用见 [source.yaml](source.yaml)，生成快照中的 `Source` 注释记录上游地址。第三方规则遵循各自的许可证。
