from redis import Redis
import requests

r = Redis(host='10.30.1.20', port=6379)
_proxy_pool_map = {'low': 'GZYF_Test:Proxy_Pool',
                   'middle': 'GZYF_Test:Proxy_Pool:M',
                   'high': 'GZYF_Test:Proxy_Pool:H'
                   }


def _response_get(url, proxy_level, payload):
    proxies = {}
    if proxy_level:
        _proxy = r.srandmember(_proxy_pool_map[proxy_level])
        if _proxy:
            proxy = _proxy.decode('utf-8')
            proxies = {"http": "http:{}".format(proxy), "https": "http://{}".format(proxy)}

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}

    resp = requests.get(url,
                        params=payload,
                        headers=headers,
                        proxies=proxies,
                        timeout=10
                        )
    print(resp.text)


if __name__ == '__main__':
    _response_get('https://www.ip.cn', 'high', {})