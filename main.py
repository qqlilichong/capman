
######################################################

import requests
from bs4 import BeautifulSoup

######################################################


HEADERS_UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 ' \
             'QQBrowser/9.7.13021.400'

HTTP_PROXY = {
    'http': '192.168.200.1:1080',
    'https': '192.168.200.1:1080',
}


######################################################


def http_get(url):
    return requests.get(
        url,
        headers={
            'User-Agent': HEADERS_UA,
        },
        proxies=HTTP_PROXY,
    )


######################################################


html = http_get('http://hao360.cn')
html.encoding = 'gbk'
bsObj = BeautifulSoup(html.text, 'html5lib')
result = bsObj.findAll('div')
for item in result:
    print(item)


######################################################
