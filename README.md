# PosvdM 分流配置

适用于 Clash Party、FlClash 和 Stash 的自用分流配置，包含广告拦截、AI、流媒体、游戏及 Telegram 分流，提供地区节点选择和低倍率策略组。

各客户端共用一份规则和 DNS 配置，TUN 由客户端管理。本项目不提供代理节点，需要搭配自己的订阅使用。

## 使用方法

1. 在客户端导入自己的代理订阅。
2. 复制下方对应链接，添加覆写并绑定到当前订阅。
3. 启用覆写，更新规则集，在策略组中选择节点。

每个链接单独放在代码块中，可点击右上角的复制按钮。

### Clash Party · Windows / macOS

添加 JavaScript 覆写：

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.js
```

### FlClash · Android

使用支持覆写脚本的版本，添加 JavaScript 覆写：

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.js
```

### Stash · iOS / iPadOS

添加 Stash 覆写：

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/override.stoverride
```

Stash 对部分 DNS 字段的支持与 Mihomo 不同，使用前请查看[兼容说明](docs/maintenance.md#客户端兼容)。

### Subconverter

在订阅转换工具中填写远程配置地址：

```text
https://raw.githubusercontent.com/PosvdM/Clash-rules/main/rules/main.ini
```

后端需要保留 `rule-providers`；不支持时，请改用客户端覆写。

同一订阅只启用一份主规则覆写。若客户端额外设置了 DNS 覆盖，需要检查是否与本配置冲突。修改策略或 DNS 后，更新覆写或重新生成订阅。

添加规则、自动构建和本地验证见[维护文档](docs/maintenance.md)。
