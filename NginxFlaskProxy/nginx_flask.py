from flask import Flask, Response
from flask import request
import requests
from requests.exceptions import ConnectTimeout, ProxyError
from redis import Redis
import logging
import json

# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
logging.basicConfig(filename='logger.log', level=logging.INFO)
# gevent end

app = Flask(__name__)
app.debug = False
app.url_map.strict_slashes = False
r = Redis(host='10.30.1.20', port=6379)
_proxy_pool_map = {'low': 'GZYF_Test:Proxy_Pool',
                   'middle': 'GZYF_Test:Proxy_Pool:M',
                   'high': 'GZYF_Test:Proxy_Pool:H'
                   }


def _proxy(url, proxy_level):
    proxies = {}
    proxy = ''
    if proxy_level:
        _proxy = r.srandmember(_proxy_pool_map[proxy_level])
        if _proxy:
            proxy = _proxy.decode('utf-8')
            proxies = {"http": "http:{}".format(proxy), "https": "https:{}".format(proxy)}
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host' and value},
            data=request.get_data(),
            cookies=request.cookies,
            proxies=proxies,
            allow_redirects=True,
            timeout=60
        )
        response = Response(resp.content, resp.status_code)

    except ConnectTimeout:
        import traceback
        traceback.print_exc()
        response = Response('请求超时', 408)
    except ProxyError:
        import traceback
        traceback.print_exc()
        response = Response('代理错误', 407)
    log_json = {
        'status': response.status_code,
        'proxy': proxy,
        'url': url,
    }
    logging.info(json.dumps(log_json, ensure_ascii=True))
    return response


@app.route('/demo', methods=['GET', 'POST'])
def url_post():
    url = request.args.get('url')
    proxy_level = request.args.get('proxy_level', '')
    return _proxy(url, proxy_level)


if __name__ == '__main__':
    monkey.patch_all()
    # app.run(host='0.0.0.0', port=3031)
    http_server = WSGIServer(('0.0.0.0', 3031), app)
    http_server.serve_forever()
