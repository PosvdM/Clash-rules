# PosvdM Clash-rules

[![Generate](https://github.com/PosvdM/Clash-rules/actions/workflows/generate.yml/badge.svg)](https://github.com/PosvdM/Clash-rules/actions/workflows/generate.yml)
[![Last Commit](https://img.shields.io/github/last-commit/PosvdM/Clash-rules)](https://github.com/PosvdM/Clash-rules/commits/main)

适用于 **Clash Party、FlClash、Stash** 等客户端的自用分流配置，支持广告拦截、AI、流媒体、游戏、Telegram、地区节点及低倍率节点分流。

配置由 [`source.yaml`](source.yaml) 统一维护，并通过 GitHub Actions 自动生成各客户端所需文件。

## 使用

1. 导入自己的代理订阅。
2. 添加对应覆写并绑定订阅。
3. 启用覆写，更新规则后选择节点。

## Clash Party / FlClash

### 完整版

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/PosvdM_rules.js
```

JavaScript 覆写仅保留订阅中的 `proxies` 和 `proxy-providers`，其余配置由本仓库接管。

支持自动补全节点名称中缺失的国旗，详见[节点名称说明](docs/maintenance.md#节点名称与国旗)。

### 四分类精简版

仅保留 **直连、代理、拒绝、MATCH** 四类策略，并保持 `source.yaml` 中的名称、图标及顺序。

代理节点通过 **URL-Test** 自动测速选择。

**JavaScript 覆写**

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/PosvdM_rules_simple.js
```

**YAML 配置**

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/PosvdM_rules_simple.yaml
```

> YAML 不包含订阅节点，需要自行提供 `proxies` 或 `proxy-providers`。节点国旗补全仅由 JavaScript 覆写执行。

## Stash

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.stoverride
```

部分 DNS 配置与 Mihomo 存在兼容性差异，详见[客户端兼容说明](docs/maintenance.md#客户端兼容)。

## Subconverter

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/main.ini
```

需要后端支持并保留 `rule-providers`，否则建议使用客户端覆写。

## 维护

规则添加、配置生成、客户端兼容及本地验证见：

**[维护文档 →](docs/maintenance.md)**
