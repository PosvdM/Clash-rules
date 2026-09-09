# PosvdM 分流配置

适用于 Clash Party、FlClash 和 Stash 的自用分流配置，包含广告拦截、AI、流媒体、游戏及 Telegram 分流，提供地区节点选择和低倍率策略组。

## 使用方法

1. 在客户端导入自己的代理订阅。
2. 复制下方对应链接，添加覆写并绑定到当前订阅。
3. 启用覆写，更新规则集，在策略组中选择节点。

### Clash Party / FlClash 等

添加 JavaScript 覆写：

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.js
```

此脚本仅保留订阅的节点及节点来源（`proxies`、`proxy-providers`），其余订阅配置全部丢弃，使用本仓库配置。

### Stash

添加 Stash 覆写：

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.stoverride
```

Stash 对部分 DNS 字段的支持与 Mihomo 不同，使用前请查看[兼容说明](docs/maintenance.md#客户端兼容)。

Stash 的 YAML 覆写只替换列出的字段，不保证清除订阅中其他配置。

### Subconverter

在订阅转换工具中填写远程配置地址：

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/rules/main.ini
```

后端需要保留 `rule-providers`；不支持时，请改用客户端覆写。

添加规则、自动构建和本地验证见[维护文档](docs/maintenance.md)。
