#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import socks
import requests
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9011, username='username', password='password')
socket.socket = socks.socksocket
print(requests.get('https://www.baidu.com/').text)