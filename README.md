# PosvdM 全平台分流配置

只维护 `source.yaml`（规则引用、策略组、DNS、TUN）和 `list/*.list`（自己的规则内容）。
借鉴 [sounfury-Clash_rules](https://github.com/sounfury/sounfury-Clash_rules) 的单源生成架构，生成器独立实现。
所有产物的规则、DNS、TUN 内容一致，不维护客户端专用策略。

## 使用

先导入自己的机场订阅，再启用以下覆写。覆写只替换规则、策略组和公共设置，保留原订阅的节点和 proxy-providers。

| 客户端 | 入口 |
| --- | --- |
| Win / Mac：Clash Party | 导入 JS 覆写 `https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.js` |
| Android：FlClash | 导入同一个 JS 覆写，绑定当前配置；需要支持覆写脚本的版本 |
| iPhone / iPad：Stash | 导入 `https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.stoverride` |
| 继续使用 Subconverter | 保留原远程配置 `https://raw.githubusercontent.com/PosvdM/Clash-rules/main/rules/main.ini` |

`output/common.yaml` 是不包含机场节点的公共配置，供审阅或合并，不是独立可连接的订阅。
不要同时叠加多份主规则覆写。客户端若设置了额外 DNS / TUN 覆盖，需关闭冲突的覆盖，才能采用本仓库的设置。

旧 INI 将 `RULE-SET` 原样写入最终规则，原生 providers 来自 `yml/GeneralClashConfig.yml`。
无需再依赖旧转换器展开 domain text、ipcidr text 或 IP-ASN。此路径要求后端保留基础模板的 rule-providers；
若后端会清理这些字段，请使用客户端原生覆写。客户端启动后自行下载规则，所有产物合入 main 后链接才生效。

## 一份配置的边界

所有产物共享完全相同的 DNS/TUN 数据；生成器没有平台 DNS/TUN 分支。
原 DNS 上游、fake-ip 设置、hosts 均保留。旧 `rule-set:direct (Domain)` 等生成名称被替换为从自己的直连/Steam 列表生成的显式域名 policy，避免跨客户端悬空引用。
旧基础模板没有 TUN 段，因此统一增加启用 TUN、mixed 栈、自动路由和 DNS 劫持的设置。

同一配置不等于不同内核实现完全一致：iOS Stash 的隧道由 Network Extension/VPN 接管，不能用 Mihomo 的 `tun.stack`、`auto-route` 等字段替换其内部实现。Stash 对 Mihomo 独有的 DNS/fake-ip/fallback 字段支持也不可假定相同。
保留这些字段用于统一维护；不宣称未知字段已在 Stash 生效。Stash 的 default-nameserver/proxy-server-nameserver 需支持这些字段的新版本（文档标注 iOS 3.6+）。
手机需在系统中允许 VPN，桌面 TUN 需要客户端服务权限。这些是安装设置，无需另写规则。

## 已修复

- 删除废弃的 `Clash/non_ip/apple_cdn.txt`，保留 domainset Apple CDN，以 `domain + text` 读取。
- China IPv4/IPv6 使用 `ipcidr + text`；Telegram ASN 直接用原生 classical provider，绕过旧转换器。
- 保留原策略组名称、默认选项、节点过滤正则与低倍率 fallback。
- 保留全部自己的规则。混合 classical 列表按域名/进程与目标 IP 拆分，统一将目标 IP 类规则置后，并使用 no-resolve。
- 所有 DNS、hosts、TUN 及策略内容从同一 source 生成；Stash 对整个映射/数组使用 `#!replace`，不混入机场的旧 DNS 或规则。
- 生成失败时不写输出；构建监听 source、list、scripts、tests，并每天同步需拆分的远程列表。

规则顺序：原顺序的非 IP 规则 → GEOSITE CN → 原顺序的 IP 规则 → GEOIP CN → MATCH。
Sukka 原生规则和 anti-AD 仍由客户端直接更新。自己的单一类型列表和 GamePlatform 直接引用原文件；只有混合域名/进程与 IP 的本地列表，以及 YouTube、GoogleFCM 这两份远程混合列表生成到 `output/rules/`；每天北京时间 10:19 尝试更新，GitHub 调度可能延迟。
每个规则快照保留上游来源及注释，规则内容遵循各上游原有许可证，不在此重新授权。

## 日常加规则

仍然编辑原来的 `list/*.list`，例如 AI 域名加到 `list/ai.list`，代理域名加到 `list/proxy.list`，直连规则加到 `list/direct.list`。注释和写法照旧，不用编辑生成文件。

本地列表只有域名/进程或只有 IP 时，直接引用原文件；混合两类时，生成器自动拆分。以后向现有列表加入 IP 或删除最后一条 IP，也不需要修改 `source.yaml`。空列表会暂时跳过。

提交到 main 后 Actions 自动处理；普通规则内容由客户端更新规则集取得。如果增加 IP 导致列表拆分方式变化，或修改了直连/Steam 的 DNS 域名，还需要更新一次客户端覆写/订阅，让生成的配置生效。

只有新增一个列表、调整列表对应的策略组、规则顺序或 DNS/TUN 时，才需要修改 `source.yaml`。

## 维护与验证

```sh
python -m pip install -r scripts/requirements.txt
python scripts/generate.py
python -m unittest discover -s tests -v
```

修改 source 或自己的 list 后推送，Actions 自动生成并提交产物。
离线重建可使用 `python scripts/generate.py --offline`；它读取已提交的远程拆分快照，自己的列表仍实时读取。
用 `--offline --check` 检查生成物是否一致。不要手改 output、rules/main.ini、yml/GeneralClashConfig.yml。

自动检查覆盖全平台内容一致、JS 保留节点、域名/IP 顺序、规则保全、筛选与 fallback、原生格式、DNS 引用、生成可重复性。
尚需在实际设备确认 VPN、DNS、节点列表及联网；Python/JS 检查不能替代 Stash 或 FlClash 的运行测试。

参考：[Mihomo rule-providers](https://wiki.metacubex.one/config/rule-providers/)、[Stash 规则集合](https://stash.wiki/rules/rule-set)、[Stash 覆写](https://stash.wiki/configuration/override)、[Stash DNS](https://stash.wiki/features/dns-server)。
