
######################################################

import requests
import urllib.parse

######################################################

HEADERS_UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 ' \
             'QQBrowser/9.7.13021.400'

HTTP_PROXY = {
    #'http': '192.168.200.1:1080',
    #'https': '192.168.200.1:1080',

    'http': '127.0.0.1:1080',
    'https': '127.0.0.1:1080',
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


def http_download(url, filename):
    resp = http_get(url)
    if not resp:
        return None

    with open(filename, 'wb') as file:
        file.write(resp.content)
    return True


######################################################


def http_urljoin(path, url):
    return urllib.parse.urljoin(path, url)


######################################################
