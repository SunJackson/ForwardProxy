import requests
sessions = requests.session()
payload = {'url': 'https://www.ip.cn', 'proxy_level': 'high'}
sessions.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
# r = sessions.get('http://127.0.0.1', params=payload)
r = sessions.get('http://127.0.0.1/demo/?url=https%3A%2F%2Ftaian.anjuke.com%2Fprop%2Fview%2FA1384899365&proxy_level=high')

print(sessions.headers)
print(r.status_code)
print(r.text)