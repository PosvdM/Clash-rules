# PosvdM Clash-rules

[![Generate](https://github.com/PosvdM/Clash-rules/actions/workflows/generate.yml/badge.svg)](https://github.com/PosvdM/Clash-rules/actions/workflows/generate.yml)
[![Last Commit](https://img.shields.io/github/last-commit/PosvdM/Clash-rules)](https://github.com/PosvdM/Clash-rules/commits/main)

适用于 **Clash Party、FlClash、Stash** 的自用分流配置，支持广告拦截及 AI、流媒体、游戏、Telegram 分流，提供地区和低倍率节点分组。

在 [`source.yaml`](source.yaml) 维护配置，由 GitHub Actions 自动生成各客户端入口。

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

自动补全节点名称中的国旗，见[节点名称说明](docs/maintenance.md#节点名称与国旗)。

### 四分类精简版

保留 **直连、代理、拒绝、MATCH** 四类策略，沿用 `source.yaml` 的名称、图标及顺序。代理组通过 **URL-Test** 自动选择节点。

**JavaScript 覆写**

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/PosvdM_rules_simple.js
```

**YAML 配置**

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/PosvdM_rules_simple.yaml
```

> YAML 不含节点，需补入 `proxies` 或 `proxy-providers`。仅 JS 覆写补全国旗。

## Stash

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.stoverride
```

部分 DNS 字段需在设备上确认支持情况，见[客户端兼容说明](docs/maintenance.md#客户端兼容)。

## Subconverter

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/main.ini
```

后端须支持并保留 `rule-providers`；不支持时请使用客户端覆写。

## 维护

添加规则、生成配置、本地验证及兼容说明见[维护文档](docs/maintenance.md)。
