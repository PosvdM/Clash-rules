# 历史配置与参考文件

此目录保存旧配置、测试模板、PAC 脚本和参考文件，不参与当前配置生成。现用配置的导入方式见[仓库首页](../README.md)，构建和维护见[维护文档](../docs/maintenance.md)。

## 目录用途

| 目录 | 内容 |
| --- | --- |
| `subconverter/` | 旧 INI 备份及测试配置 |
| `clash/` | 旧 Clash 测试模板 |
| `source/` | 配置源历史快照 |
| `pac/` | PAC 脚本；`%mixed-port%` 需要使用方替换 |
| `references/subconverter/` | ShellClash 参考配置 |
| `references/clash/` | Clash 参考模板及来源地址 |

## 路径映射

历史文件已迁入下表位置，旧的 raw 地址不再可用。若仍直接使用这些文件，请将 URL 中的路径替换为新路径；当前 README 中的使用入口不受影响。

| 原路径 | 新路径（相对于本目录） |
| --- | --- |
| `files/.pac` | [pac/proxy.pac](pac/proxy.pac) |
| `rules/Backup.ini` | [subconverter/Backup.ini](subconverter/Backup.ini) |
| `rules/Backup0.ini` | [subconverter/Backup0.ini](subconverter/Backup0.ini) |
| `rules/test.ini` | [subconverter/test.ini](subconverter/test.ini) |
| `yml/GCCtest.yml` | [clash/GCCtest.yml](clash/GCCtest.yml) |
| `others-rules/ShellClash_Full.ini` | [references/subconverter/ShellClash_Full.ini](references/subconverter/ShellClash_Full.ini) |
| `others-yml/GeneralClashConfig.yml` | [references/clash/GeneralClashConfig.yml](references/clash/GeneralClashConfig.yml) |
| `others-yml/yml.txt` | [references/clash/sources.txt](references/clash/sources.txt) |

`subconverter/test.ini` 已改为引用 `archive/clash/GCCtest.yml`。`subconverter/Backup0.ini` 已同步改为引用现用的 `output/GeneralClashConfig.yml`。其余归档文件内容保持不变。

归档文件仅供查阅或自行调整，不保证兼容当前客户端；其中的上游地址与分流策略不会由 Actions 更新。

## 配置源快照

- [2026-09-10：哔哩哔哩改直连前](source/2026-09-10-before-bilibili-direct.yaml)：保存提交 `5483b65` 的完整 `source.yaml`，包含原哔哩哔哩策略组及规则映射。现用配置删除该组，原规则改为 `🟢 直连`。
