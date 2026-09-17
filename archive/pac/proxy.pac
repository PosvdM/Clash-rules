function FindProxyForURL(url, host) {

  // 直连列表：分别按域名后缀和完整主机名匹配
  var direct_domains_with_subdomains = ["xboxlive.cn"];
  var direct_domains_without_subdomains = ["192.168.0.1","ufi.ztedevice.com","e-hentai.org","exhentai.org"];

  for (var i = 0; i < direct_domains_with_subdomains.length; i++) {
    if (dnsDomainIs(host, direct_domains_with_subdomains[i])) {
      return "DIRECT";
    }
  }
  for (var i = 0; i < direct_domains_without_subdomains.length; i++) {
    if (host == direct_domains_without_subdomains[i]) {
      return "DIRECT";
    }
  }

  return "PROXY 127.0.0.1:%mixed-port%; SOCKS5 127.0.0.1:%mixed-port%; DIRECT;";
}
