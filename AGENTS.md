# 项目说明

本仓库生成 Clash Party、FlClash、Stash 和 Subconverter 使用的分流配置。使用简体中文沟通，文档保持直接、简洁。

## 先阅读

- `README.md`：用户导入方法。
- `docs/maintenance.md`：文件结构、规则维护、构建和兼容边界。
- `source.yaml`、`scripts/generate.py`：配置源及实际生成逻辑。
- `tests/test_config.py`、`.github/workflows/generate.yml`：验证方式与自动更新流程。

## 配置约束

- 以 `source.yaml` 和 `list/*.list` 为维护入口。现有列表加规则应只需修改原列表，不要求用户同步编辑生成文件。
- 单一类型的本地列表直接引用原文件，只有混合 IP/非 IP 时自动拆分。不要为纯域名列表创建多余副本。
- 保留规则内容、策略组名称、默认选项、筛选正则和低倍率 fallback，除非任务明确要求调整。
- TUN 由客户端管理，不向公共配置或覆写加入 `tun`。JS 不保留订阅传入的 TUN 设置，由客户端在覆写后补入。
- DNS 保留 `rule-set:direct (Domain)` 和 `rule-set:SteamDownload (Domain)` 引用，不展开为逐域名策略。通过 `dns_name` 保证对应 provider 存在，直接引用原列表。
- 各客户端共用规则和 DNS 配置。不要擅自引入平台策略分支，也不要把相同配置数据说成相同运行效果。
- JS 仅保留节点、凭据和 `proxy-providers`，从公共配置重新构建对象，丢弃订阅其他所有顶层字段；Stash 映射和数组使用 `#!replace`，不承诺清除未列出的字段。
- Sukka 使用原生 provider 格式；保留 Telegram ASN，避免恢复废弃的 `Clash/non_ip/apple_cdn.txt`。
- 规则顺序为非 IP → GEOSITE CN → IP → GEOIP CN → MATCH。IP 引用使用 `no-resolve`，只保留一个末尾 MATCH。

## 修改与验证

修改前检查当前分支、工作区和远端最新提交，保留用户及 Actions 机器人的修改。`archive/` 保存历史配置、测试模板、PAC 和参考文件，不属于当前生成流程；除非任务明确要求，不要修改或清理。目录索引与旧路径映射见 `archive/README.md`。

生成产物统一放在 `output/`，包括 Subconverter 入口 `output/main.ini` 和基础模板 `output/GeneralClashConfig.yml`。修改生成器或配置源后重新生成；不要单独修改产物。需要删除的过期拆分快照由生成器清理。

```sh
python -m pip install -r scripts/requirements.txt
python scripts/generate.py --offline
python scripts/generate.py --offline --check
python -m unittest discover -s tests -v
git diff --check
```

修改远程拆分源后，运行不带 `--offline` 的在线生成，检查快照及来源注释。测试应验证实际行为，例如添加或移除 IP 后的拆分转换、DNS 引用存在、节点保留和订阅额外配置清除。

仅修改文档时检查内容、相对链接和 Markdown 格式即可，不必为文档新增测试。不得把 Python/Node 测试通过描述成 Stash、FlClash 或 Clash Party 实机验证通过。

## 自动化与文档

Actions 在每次 `main` 推送时校验、在线生成并提交变化；PR 只校验。每天北京时间 10:19 定时同步，另有手动触发入口。不要恢复文件路径过滤，生成和验证失败时不得提交产物。

README 只放总体说明和使用方法，配置链接每个单独放在代码块中，使用 GitHub 自带复制按钮。维护和实现细节写入 `docs/maintenance.md`，不要在 README 堆放迁移记录或本次修改说明。
