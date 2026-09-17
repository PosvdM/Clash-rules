# 历史配置与参考文件

本目录保存历史配置、测试模板、PAC 和参考文件，不参与构建或自动更新。现用配置见[仓库首页](../README.md)，构建方法见[维护文档](../docs/maintenance.md)。

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

旧 raw 地址已失效。继续使用归档文件时，请按下表更新 URL 路径；README 中的现用入口不受影响。

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

`subconverter/test.ini` 引用 `archive/clash/GCCtest.yml`；`subconverter/Backup0.ini` 引用现用模板 `output/GeneralClashConfig.yml`。

归档仅供查阅或自行调整，不保证兼容当前客户端。参考模板中的 DNS 等说明反映原版本，不作为现用配置的依据。

## 配置源快照

- [2026-09-10：哔哩哔哩改直连前](source/2026-09-10-before-bilibili-direct.yaml)：保存提交 `5483b65` 的 `source.yaml`，含哔哩哔哩策略组及规则映射。现用配置已移除该组，规则改为 `🟢 直连`。
