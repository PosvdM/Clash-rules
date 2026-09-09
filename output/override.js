// Generated from source.yaml; shared by Clash Party and FlClash.
const policy = {
  "dns": {
    "enable": true,
    "ipv6": true,
    "use-hosts": true,
    "prefer-h3": true,
    "listen": "0.0.0.0:53",
    "enhanced-mode": "fake-ip",
    "fake-ip-range": "198.18.0.1/16",
    "fake-ip-filter": [
      "geosite:private",
      "geosite:connectivity-check",
      "time.*.com",
      "ntp.*.com"
    ],
    "default-nameserver": [
      "https://223.5.5.5/dns-query"
    ],
    "nameserver": [
      "https://dns.alidns.com/dns-query"
    ],
    "proxy-server-nameserver": [
      "https://dns.alidns.com/dns-query"
    ],
    "fallback": [
      "https://dns.cloudflare.com/dns-query"
    ],
    "fallback-filter": {
      "geoip": true,
      "geoip-code": "CN",
      "geosite": [
        "gfw"
      ],
      "ipcidr": [
        "240.0.0.0/4"
      ]
    },
    "nameserver-policy": {
      "rule-set:direct (Domain)": "https://dns.alidns.com/dns-query",
      "rule-set:SteamDownload (Domain)": "https://dns.alidns.com/dns-query",
      "geosite:cn,private,apple": "https://dns.alidns.com/dns-query",
      "geosite:!cn,gfw": "https://posvdm.cloudflare-gateway.com/dns-query"
    }
  },
  "hosts": {
    "iosapps.itunes.apple.com": "hls.itunes.apple.com.mwcname.com"
  },
  "proxy-groups": [
    {
      "name": "🐟 漏网之鱼",
      "type": "select",
      "proxies": [
        "DIRECT",
        "🚀 节点选择",
        "🏷️ 低倍率",
        "📌 指定节点",
        "1️⃣ 港台新",
        "2️⃣ 日韩",
        "🇭🇰 香港",
        "🇨🇳 台湾",
        "🇸🇬 新加坡",
        "🇯🇵 日本",
        "🇰🇷 韩国",
        "🇺🇲 美国"
      ]
    },
    {
      "name": "🚀 节点选择",
      "type": "select",
      "proxies": [
        "1️⃣ 港台新",
        "2️⃣ 日韩",
        "🇭🇰 香港",
        "🇨🇳 台湾",
        "🇸🇬 新加坡",
        "🇯🇵 日本",
        "🇰🇷 韩国",
        "🇺🇲 美国",
        "♻️ 自动选择",
        "📌 指定节点"
      ]
    },
    {
      "name": "✨ 人工智能",
      "type": "select",
      "proxies": [
        "🗄️ Oracle",
        "🇸🇬 新加坡",
        "🇨🇳 台湾",
        "🇯🇵 日本",
        "🇺🇲 美国",
        "🇭🇰 香港",
        "🚀 节点选择",
        "📌 指定节点"
      ]
    },
    {
      "name": "🥵 不可以涩涩",
      "type": "select",
      "proxies": [
        "🏷️ 低倍率",
        "🚀 节点选择",
        "🇸🇬 新加坡",
        "🇨🇳 台湾",
        "🇭🇰 香港",
        "🇯🇵 日本",
        "🇰🇷 韩国",
        "🇺🇲 美国",
        "📌 指定节点",
        "DIRECT"
      ]
    },
    {
      "name": "💬 Telegram",
      "type": "select",
      "proxies": [
        "🏷️ 低倍率",
        "🚀 节点选择",
        "♻️ 自动选择",
        "📌 指定节点",
        "🇭🇰 香港",
        "🇨🇳 台湾",
        "🇸🇬 新加坡",
        "🇯🇵 日本",
        "🇰🇷 韩国",
        "🇺🇲 美国"
      ]
    },
    {
      "name": "📺 YouTube",
      "type": "select",
      "proxies": [
        "🏷️ 低倍率",
        "🚀 节点选择",
        "🇭🇰 香港",
        "🇨🇳 台湾",
        "🇸🇬 新加坡",
        "🇯🇵 日本",
        "🇰🇷 韩国",
        "🇺🇲 美国"
      ]
    },
    {
      "name": "📦 大宗流量",
      "type": "select",
      "proxies": [
        "🏷️ 低倍率",
        "🚀 节点选择",
        "📌 指定节点"
      ]
    },
    {
      "name": "🎮 游戏平台",
      "type": "select",
      "proxies": [
        "🇭🇰 香港",
        "🇨🇳 台湾",
        "🇸🇬 新加坡",
        "🇯🇵 日本",
        "🇰🇷 韩国",
        "🇺🇲 美国",
        "🚀 节点选择",
        "📌 指定节点",
        "DIRECT"
      ]
    },
    {
      "name": "🅱️ 哔哩哔哩",
      "type": "select",
      "proxies": [
        "DIRECT",
        "🏷️ 低倍率",
        "🇭🇰 香港",
        "🇨🇳 台湾",
        "📌 指定节点"
      ]
    },
    {
      "name": "📌 指定节点",
      "type": "select",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(香港|台湾|新加坡|美国|日本|韩国|Hong Kong|Taiwan|Singapore|USA|Japan|Korea))))[\\s\\S]*$",
      "include-all": true,
      "proxies": [
        "🌍 其他地区"
      ]
    },
    {
      "name": "🌍 其他地区",
      "type": "select",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:^(?!(.*(?:香港|台湾|新加坡|美国|日本|韩国|Hong Kong|Taiwan|Singapore|USA|Japan|Korea)))))[\\s\\S]*$",
      "include-all": true
    },
    {
      "name": "🏷️ 低倍率",
      "type": "fallback",
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50,
      "proxies": [
        "🧪 低倍检测",
        "🚀 节点选择"
      ]
    },
    {
      "name": "1️⃣ 港台新",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(香港|台湾|新加坡|Hong Kong|Taiwan|Singapore))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "2️⃣ 日韩",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(日本|韩国|Japan|Korea))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "♻️ 自动选择",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(香港|台湾|新加坡|美国|日本|韩国|Hong Kong|Taiwan|Singapore|USA|Japan|Korea))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🧪 低倍检测",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(实验)).*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🇭🇰 香港",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(香港|Hong Kong))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🇨🇳 台湾",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(台湾|Taiwan))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🇸🇬 新加坡",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(新加坡|Singapore))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🇯🇵 日本",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(日本|Japan))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🇰🇷 韩国",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(韩国|Korea))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🇺🇲 美国",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:(?=.*(美国|USA))^((?!小带宽|倍率|计费|0\\.|(?:[2-9][0-9]*|1[0-9]+)[x×]).)*$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🗄️ Oracle",
      "type": "url-test",
      "filter": "(?i)^(?!.*(?:(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)))(?=[\\s\\S]*(?:^🗄️\\|🇺🇸 美国 Oracle (?:Vless|Hy2)$))[\\s\\S]*$",
      "include-all": true,
      "url": "https://www.gstatic.com/generate_204",
      "interval": 300,
      "tolerance": 50
    },
    {
      "name": "🟢 直连",
      "type": "url-test",
      "url": "http://connect.rom.miui.com/generate_204",
      "interval": 300,
      "tolerance": 50,
      "proxies": [
        "DIRECT"
      ]
    },
    {
      "name": "🛑 广告隐私",
      "type": "select",
      "proxies": [
        "REJECT",
        "DIRECT"
      ]
    }
  ],
  "rule-providers": {
    "anti_ad_net": {
      "type": "http",
      "behavior": "domain",
      "format": "yaml",
      "url": "https://anti-ad.net/clash.yaml",
      "path": "./ruleset/posvdm/anti_ad_net.txt",
      "interval": 86400
    },
    "local_reject": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/reject.list",
      "path": "./ruleset/posvdm/local_reject.txt",
      "interval": 86400
    },
    "direct (Domain)": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/direct.list",
      "path": "./ruleset/posvdm/local_direct_dns.txt",
      "interval": 86400
    },
    "local_direct": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/direct.list",
      "path": "./ruleset/posvdm/local_direct.txt",
      "interval": 86400
    },
    "SteamDownload (Domain)": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/SteamDownload.list",
      "path": "./ruleset/posvdm/local_SteamDownload_dns.txt",
      "interval": 86400
    },
    "local_SteamDownload_non_ip": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/rules/local_SteamDownload_non_ip.txt",
      "path": "./ruleset/posvdm/local_SteamDownload_non_ip.txt",
      "interval": 86400
    },
    "local_SteamDownload_ip": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/rules/local_SteamDownload_ip.txt",
      "path": "./ruleset/posvdm/local_SteamDownload_ip.txt",
      "interval": 86400
    },
    "sukka_non_ip_ai": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/ai.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_ai.txt",
      "interval": 86400
    },
    "local_ai": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/ai.list",
      "path": "./ruleset/posvdm/local_ai.txt",
      "interval": 86400
    },
    "local_proxy": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/proxy.list",
      "path": "./ruleset/posvdm/local_proxy.txt",
      "interval": 86400
    },
    "local_bulk": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/bulk.list",
      "path": "./ruleset/posvdm/local_bulk.txt",
      "interval": 86400
    },
    "local_sexy": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/sexy.list",
      "path": "./ruleset/posvdm/local_sexy.txt",
      "interval": 86400
    },
    "local_final": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/list/final.list",
      "path": "./ruleset/posvdm/local_final.txt",
      "interval": 86400
    },
    "sukka_non_ip_stream_biliintl": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/stream_biliintl.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_stream_biliintl.txt",
      "interval": 86400
    },
    "sukka_non_ip_lan": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/lan.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_lan.txt",
      "interval": 86400
    },
    "sukka_non_ip_domestic": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/domestic.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_domestic.txt",
      "interval": 86400
    },
    "sukka_non_ip_direct": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/direct.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_direct.txt",
      "interval": 86400
    },
    "external_Global_Services_YouTube_non_ip": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/rules/external_Global_Services_YouTube_non_ip.txt",
      "path": "./ruleset/posvdm/external_Global_Services_YouTube_non_ip.txt",
      "interval": 86400
    },
    "external_Global_Services_YouTube_ip": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/rules/external_Global_Services_YouTube_ip.txt",
      "path": "./ruleset/posvdm/external_Global_Services_YouTube_ip.txt",
      "interval": 86400
    },
    "sukka_non_ip_stream": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/stream.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_stream.txt",
      "interval": 86400
    },
    "sukka_ip_stream": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/ip/stream.txt",
      "path": "./ruleset/posvdm/sukka_ip_stream.txt",
      "interval": 86400
    },
    "external_Ruleset_GoogleFCM_non_ip": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/rules/external_Ruleset_GoogleFCM_non_ip.txt",
      "path": "./ruleset/posvdm/external_Ruleset_GoogleFCM_non_ip.txt",
      "interval": 86400
    },
    "external_Ruleset_GoogleFCM_ip": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/PosvdM/Clash-rules/main/output/rules/external_Ruleset_GoogleFCM_ip.txt",
      "path": "./ruleset/posvdm/external_Ruleset_GoogleFCM_ip.txt",
      "interval": 86400
    },
    "sukka_domainset_apple_cdn": {
      "type": "http",
      "behavior": "domain",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/domainset/apple_cdn.txt",
      "path": "./ruleset/posvdm/sukka_domainset_apple_cdn.txt",
      "interval": 86400
    },
    "sukka_non_ip_apple_cn": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/apple_cn.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_apple_cn.txt",
      "interval": 86400
    },
    "sukka_non_ip_apple_services": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/apple_services.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_apple_services.txt",
      "interval": 86400
    },
    "sukka_non_ip_microsoft": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/microsoft.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_microsoft.txt",
      "interval": 86400
    },
    "sukka_non_ip_microsoft_cdn": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/microsoft_cdn.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_microsoft_cdn.txt",
      "interval": 86400
    },
    "sukka_non_ip_telegram": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/telegram.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_telegram.txt",
      "interval": 86400
    },
    "sukka_ip_telegram": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/ip/telegram.txt",
      "path": "./ruleset/posvdm/sukka_ip_telegram.txt",
      "interval": 86400
    },
    "sukka_ip_telegram_asn": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/ip/telegram_asn.txt",
      "path": "./ruleset/posvdm/sukka_ip_telegram_asn.txt",
      "interval": 86400
    },
    "external_Clash_GamePlatform": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://raw.githubusercontent.com/LoveMyself666/ACL4SSR/master/Clash/GamePlatform.list",
      "path": "./ruleset/posvdm/external_Clash_GamePlatform.txt",
      "interval": 86400
    },
    "sukka_non_ip_global": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/non_ip/global.txt",
      "path": "./ruleset/posvdm/sukka_non_ip_global.txt",
      "interval": 86400
    },
    "sukka_ip_china_ip": {
      "type": "http",
      "behavior": "ipcidr",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/ip/china_ip.txt",
      "path": "./ruleset/posvdm/sukka_ip_china_ip.txt",
      "interval": 86400
    },
    "sukka_ip_china_ip_ipv6": {
      "type": "http",
      "behavior": "ipcidr",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/ip/china_ip_ipv6.txt",
      "path": "./ruleset/posvdm/sukka_ip_china_ip_ipv6.txt",
      "interval": 86400
    },
    "sukka_ip_lan": {
      "type": "http",
      "behavior": "classical",
      "format": "text",
      "url": "https://ruleset.skk.moe/Clash/ip/lan.txt",
      "path": "./ruleset/posvdm/sukka_ip_lan.txt",
      "interval": 86400
    }
  },
  "rules": [
    "RULE-SET,anti_ad_net,🛑 广告隐私",
    "RULE-SET,local_reject,🛑 广告隐私",
    "RULE-SET,local_direct,🟢 直连",
    "RULE-SET,local_SteamDownload_non_ip,🟢 直连",
    "RULE-SET,sukka_non_ip_ai,✨ 人工智能",
    "RULE-SET,local_ai,✨ 人工智能",
    "RULE-SET,local_proxy,🚀 节点选择",
    "RULE-SET,local_bulk,📦 大宗流量",
    "RULE-SET,local_sexy,🥵 不可以涩涩",
    "RULE-SET,local_final,🐟 漏网之鱼",
    "RULE-SET,sukka_non_ip_stream_biliintl,🅱️ 哔哩哔哩",
    "RULE-SET,sukka_non_ip_lan,🟢 直连",
    "RULE-SET,sukka_non_ip_domestic,🟢 直连",
    "RULE-SET,sukka_non_ip_direct,🟢 直连",
    "RULE-SET,external_Global_Services_YouTube_non_ip,📺 YouTube",
    "RULE-SET,sukka_non_ip_stream,🚀 节点选择",
    "RULE-SET,external_Ruleset_GoogleFCM_non_ip,🟢 直连",
    "RULE-SET,sukka_domainset_apple_cdn,🟢 直连",
    "RULE-SET,sukka_non_ip_apple_cn,🟢 直连",
    "RULE-SET,sukka_non_ip_apple_services,🟢 直连",
    "RULE-SET,sukka_non_ip_microsoft,🟢 直连",
    "RULE-SET,sukka_non_ip_microsoft_cdn,🟢 直连",
    "RULE-SET,sukka_non_ip_telegram,💬 Telegram",
    "RULE-SET,external_Clash_GamePlatform,🎮 游戏平台",
    "RULE-SET,sukka_non_ip_global,🚀 节点选择",
    "GEOSITE,cn,🟢 直连",
    "RULE-SET,local_SteamDownload_ip,🟢 直连,no-resolve",
    "RULE-SET,external_Global_Services_YouTube_ip,📺 YouTube,no-resolve",
    "RULE-SET,sukka_ip_stream,🚀 节点选择,no-resolve",
    "RULE-SET,external_Ruleset_GoogleFCM_ip,🟢 直连,no-resolve",
    "RULE-SET,sukka_ip_telegram,💬 Telegram,no-resolve",
    "RULE-SET,sukka_ip_telegram_asn,💬 Telegram,no-resolve",
    "RULE-SET,sukka_ip_china_ip,🟢 直连,no-resolve",
    "RULE-SET,sukka_ip_china_ip_ipv6,🟢 直连,no-resolve",
    "RULE-SET,sukka_ip_lan,🟢 直连,no-resolve",
    "GEOIP,CN,🟢 直连,no-resolve",
    "MATCH,🐟 漏网之鱼"
  ]
};
const excludedNodePattern = "(?:\\d+(\\.\\d*)?\\s*GB|traffic|expire|premium|github|isp|流量|官网|网址|官址|机场|套餐|应急|时间|重置|剩余|[到过]期|订阅|失联|下载|可用|建议)";
const nodeFlagAliases = {"HK": ["香港", "Hong Kong", "HongKong", "HK"], "TW": ["台湾", "台灣", "Taiwan", "TW"], "SG": ["新加坡", "狮城", "獅城", "Singapore", "SG"], "JP": ["日本", "东京", "東京", "大阪", "Japan", "Tokyo", "Osaka", "JP"], "KR": ["韩国", "韓國", "南韩", "首尔", "首爾", "South Korea", "Korea", "Seoul", "KR"], "US": ["美国", "美國", "洛杉矶", "洛杉磯", "西雅图", "西雅圖", "United States", "USA", "Los Angeles", "Seattle", "US"], "GB": ["英国", "英國", "伦敦", "倫敦", "United Kingdom", "Britain", "London", "UK", "GB"], "DE": ["德国", "德國", "法兰克福", "法蘭克福", "Germany", "Frankfurt", "DE"], "FR": ["法国", "法國", "巴黎", "France", "Paris", "FR"], "CA": ["加拿大", "Canada", "CA"], "AU": ["澳大利亚", "澳大利亞", "澳洲", "悉尼", "Australia", "Sydney", "AU"], "MO": ["澳门", "澳門", "Macau", "Macao", "MO"], "CN": ["中国", "中國", "大陆", "大陸", "China", "CN"], "IN": ["印度", "India", "IN"], "ID": ["印度尼西亚", "印度尼西亞", "印尼", "Indonesia", "ID"], "PK": ["巴基斯坦", "Pakistan", "PK"], "IL": ["以色列", "Israel", "IL"], "AE": ["阿联酋", "阿聯酋", "迪拜", "杜拜", "United Arab Emirates", "Dubai", "UAE", "AE"], "PH": ["菲律宾", "菲律賓", "Philippines", "PH"], "MY": ["马来西亚", "馬來西亞", "Malaysia", "MY"], "EG": ["埃及", "Egypt", "EG"], "NG": ["尼日利亚", "尼日利亞", "Nigeria", "NG"], "TH": ["泰国", "泰國", "Thailand", "TH"], "VN": ["越南", "Vietnam", "VN"], "NL": ["荷兰", "荷蘭", "Netherlands", "NL"], "RU": ["俄罗斯", "俄羅斯", "Russia", "RU"], "TR": ["土耳其", "Turkey", "Türkiye", "TR"], "BR": ["巴西", "Brazil", "BR"], "AR": ["阿根廷", "Argentina", "AR"], "MX": ["墨西哥", "Mexico", "MX"], "ZA": ["南非", "South Africa", "ZA"], "NZ": ["新西兰", "新西蘭", "纽西兰", "紐西蘭", "New Zealand", "NZ"], "CH": ["瑞士", "Switzerland", "CH"], "SE": ["瑞典", "Sweden", "SE"], "NO": ["挪威", "Norway", "NO"], "FI": ["芬兰", "芬蘭", "Finland", "FI"], "DK": ["丹麦", "丹麥", "Denmark", "DK"], "IT": ["意大利", "義大利", "Italy", "IT"], "ES": ["西班牙", "Spain", "ES"], "PT": ["葡萄牙", "Portugal", "PT"], "IE": ["爱尔兰", "愛爾蘭", "Ireland", "IE"], "PL": ["波兰", "波蘭", "Poland", "PL"], "UA": ["乌克兰", "烏克蘭", "Ukraine", "UA"], "IS": ["冰岛", "冰島", "Iceland", "IS"], "BE": ["比利时", "比利時", "Belgium", "BE"], "AT": ["奥地利", "奧地利", "Austria", "AT"], "CZ": ["捷克", "Czechia", "Czech Republic", "CZ"], "HU": ["匈牙利", "Hungary", "HU"], "RO": ["罗马尼亚", "羅馬尼亞", "Romania", "RO"], "SA": ["沙特", "Saudi Arabia", "SA"], "CL": ["智利", "Chile", "CL"], "CO": ["哥伦比亚", "哥倫比亞", "Colombia", "CO"], "PE": ["秘鲁", "秘魯", "Peru", "PE"], "BD": ["孟加拉", "Bangladesh", "BD"], "NP": ["尼泊尔", "尼泊爾", "Nepal", "NP"], "KH": ["柬埔寨", "Cambodia", "KH"], "KZ": ["哈萨克斯坦", "哈薩克斯坦", "Kazakhstan", "KZ"]};
// Cosmetic changes only: never infer location from the server address.
function addNodeFlags(config) {
  const flagPresent = /[\u{1F1E6}-\u{1F1FF}]{2}/u;
  const leadingFlag = /^(?<flag>[\u{1F1E6}-\u{1F1FF}]{2})\s*/u;
  const separatorPrefix = /^[^|｜]*[|｜]\s*/u;
  const placeFlag = (name, flag) => {
    const prefix = name.match(separatorPrefix)?.[0] || '';
    return prefix + flag + ' ' + name.slice(prefix.length);
  };
  const matchers = Object.entries(nodeFlagAliases).map(([code, aliases]) => ({
    flag: Array.from(code, c => String.fromCodePoint(0x1F1E6 + c.charCodeAt(0) - 65)).join(''),
    // Bound Latin aliases so IN/US do not match words such as BUSINESS.
    patterns: aliases.map(alias => {
      const escaped = alias.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      return new RegExp(/[A-Za-z]/.test(alias) ? '(^|[^A-Za-z])(?<region>' + escaped + ')(?![A-Za-z])' : '(?<region>' + escaped + ')', /^[A-Z]{2,3}$/.test(alias) ? 'g' : 'gi');
    })
  }));
  const providers = Object.values(config['proxy-providers'] || {});
  const allNodes = [...(config.proxies || []), ...providers.flatMap(p => p.payload || [])];
  // Provider filters/name overrides run later in the core. Do not rename their input.
  const eligible = new Set(config.proxies || []);
  for (const p of providers) {
    const o = p.override || {};
    if (p.type === 'inline' && !p.filter && !p['exclude-filter'] &&
        !o['proxy-name'] && !o['additional-prefix'] && !o['additional-suffix'] && !o['override-expr']) {
      for (const node of p.payload || []) eligible.add(node);
    }
  }
  const reserved = new Set(['DIRECT', 'REJECT', ...config['proxy-groups'].map(g => g.name),
    ...Object.keys(config['proxy-providers'] || {})]);
  const occupied = new Set([...reserved, ...allNodes.map(n => n.name)]);
  const proposals = new Map();
  for (const node of allNodes) {
    const name = node.name;
    if (!eligible.has(node) || typeof name !== 'string' || reserved.has(name)) continue;
    if (flagPresent.test(name)) {
      // Move a leading flag behind the first separator when present.
      const leading = name.match(leadingFlag);
      const rest = leading ? name.slice(leading[0].length) : '';
      if (leading && separatorPrefix.test(rest) && !flagPresent.test(rest)) {
        const target = placeFlag(rest, leading.groups.flag);
        if (!occupied.has(target)) proposals.set(name, target);
      }
      continue;
    }
    const hits = matchers.flatMap(m => m.patterns.flatMap(pattern => {
      return Array.from(name.matchAll(pattern), match => {
        const end = match.index + match[0].length;
        return {flag: m.flag, start: end - match.groups.region.length, end};
      });
    }));
    // 印度尼西亚 contains 印度: prefer the full region name at the same position.
    const matches = new Set(hits.filter(h => !hits.some(other =>
      other.start <= h.start && other.end >= h.end &&
      other.end - other.start > h.end - h.start)).map(h => h.flag));
    if (matches.size !== 1) continue;
    const target = placeFlag(name, [...matches][0]);
    if (!occupied.has(target)) proposals.set(name, target);
  }
  // A name shared by a node we cannot safely rename must stay unchanged everywhere.
  for (const node of allNodes) if (!eligible.has(node)) proposals.delete(node.name);
  // Raw and previously decorated versions may converge on the same new name.
  const targetCounts = new Map();
  for (const target of proposals.values()) targetCounts.set(target, (targetCounts.get(target) || 0) + 1);
  for (const [name, target] of proposals) if (targetCounts.get(target) > 1) proposals.delete(name);
  const rename = name => proposals.get(name) || name;
  for (const node of allNodes) {
    node.name = rename(node.name);
    if (typeof node['dialer-proxy'] === 'string') node['dialer-proxy'] = rename(node['dialer-proxy']);
  }
  for (const p of providers) {
    if (typeof p.proxy === 'string') p.proxy = rename(p.proxy);
    if (typeof p.override?.['dialer-proxy'] === 'string') {
      p.override['dialer-proxy'] = rename(p.override['dialer-proxy']);
    }
  }
}

function main(config) {
  if (!config || typeof config !== 'object' || Array.isArray(config)) throw new Error('需要先导入机场订阅');
  if (!(Array.isArray(config.proxies) && config.proxies.length) &&
      !Object.keys(config['proxy-providers'] || {}).length) throw new Error('订阅中没有代理节点');
  // Build from our policy; never inherit unknown subscription settings (including tun).
  // Providers are node sources. Keep their credentials and transport options intact.
  const result = JSON.parse(JSON.stringify(policy));
  for (const key of ['proxies', 'proxy-providers']) {
    if (Object.prototype.hasOwnProperty.call(config, key)) {
      result[key] = JSON.parse(JSON.stringify(config[key]));
    }
  }
  const excludedNode = new RegExp(excludedNodePattern, 'i');
  const keepNode = (node) => !excludedNode.test(node.name || '');
  if (Array.isArray(result.proxies)) result.proxies = result.proxies.filter(keepNode);
  // Remote/file providers load later in Mihomo; filter them at the source too.
  for (const provider of Object.values(result['proxy-providers'] || {})) {
    if (Array.isArray(provider.payload)) provider.payload = provider.payload.filter(keepNode);
  }
  addNodeFlags(result);
  const providerExclusion = '(?i:' + excludedNodePattern + ')';
  for (const provider of Object.values(result['proxy-providers'] || {})) {
    const previous = provider['exclude-filter'];
    if (!previous) provider['exclude-filter'] = providerExclusion;
    else if (previous !== providerExclusion && !previous.endsWith('|' + providerExclusion)) {
      provider['exclude-filter'] = '(?:' + previous + ')|' + providerExclusion;
    }
  }
  return result;
}
