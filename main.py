
######################################################

import requests
from urllib.parse import urljoin
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


def http_download(url, filename):
    resp = http_get(url)
    if not resp:
        return False

    with open(filename, 'wb') as file:
        for chunk in resp.iter_content(1024 * 64):
            file.write(chunk)
    return True


######################################################


class JavLibDetail:

    ######################################################

    def __init__(self, url):
        self.bs = None
        self.url = url

        resp = http_get(url)
        if resp:
            self.bs = BeautifulSoup(resp.text, 'html5lib')

    ######################################################

    def id(self):
        if not self.bs:
            return None

        finder = self.bs.find('div', {
            'id': 'video_id',
            'class': 'item',
        })
        if not finder:
            return None

        finder = finder.find('td', {
            'class': 'text',
        })
        if not finder:
            return None

        return finder.string

    ######################################################

    def preview(self):
        if not self.bs:
            return None

        finder = self.bs.find('img', {
            'id': 'video_jacket_img'
        })
        if not finder:
            return None

        if not finder.has_attr('src'):
            return None

        return urljoin(self.url, finder['src'])

    ######################################################


######################################################
