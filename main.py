
######################################################

import re
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
        file.write(resp.content)
    return True


######################################################


class JavLibDetail:

    ######################################################

    def __init__(self, url):
        self.bs = None
        self.id = None
        self.title = None
        self.image = None
        self.date = None
        self.length = None
        self.maker = None
        self.maker_uri = None
        self.label = None
        self.label_uri = None
        self.cast = None
        self.cast_uri = None

        resp = http_get(url)
        if resp:
            self.bs = BeautifulSoup(resp.text, 'html5lib')
            self.url = url
            self.parseset = {
                'video_id': self.parse_id,
                'video_title': self.parse_title,
                'video_jacket': self.parse_image,
                'video_date': self.parse_date,
                'video_length': self.parse_length,
                'video_maker': self.parse_maker,
                'video_label': self.parse_label,
                'video_cast': self.parse_cast,
            }
            self.parse()

    ######################################################

    def parse(self):
        if not self.bs:
            return None

        finder = self.bs.findAll('div',
                                 id=re.compile('video_\w+'))
        if not finder:
            return None

        for item in finder:
            if not item.has_attr('id'):
                continue

            item_id = item['id']
            if item_id not in self.parseset:
                continue

            if not self.parseset[item_id](item):
                self.id = None
                return None

        return True

    ######################################################

    def parse_id(self, item):
        finder = item.findAll('td', {
            'class': 'text',
        })
        if not finder:
            return None

        self.id = finder[-1].get_text().strip()
        return self.id

    ######################################################

    def parse_image(self, item):
        finder = item.find('img')
        if not finder:
            return None

        self.image = urljoin(self.url, finder['src'].strip())
        return self.image

    ######################################################

    def parse_title(self, item):
        finder = item.find('a')
        if not finder:
            return None

        self.title = finder.get_text().strip()
        return self.title

    ######################################################

    def parse_date(self, item):
        finder = item.findAll('td', {
            'class': 'text',
        })
        if not finder:
            return None

        self.date = finder[-1].get_text().strip()
        return self.date

    ######################################################

    def parse_length(self, item):
        finder = item.findAll('td')
        if not finder:
            return None

        self.length = finder[-1].get_text().strip()
        return self.length

    ######################################################

    def parse_maker(self, item):
        finder = item.findAll('td', {
            'class': 'text',
        })
        if not finder:
            return None

        self.maker = finder[-1].get_text().strip()
        self.maker_uri = item.find('a')
        if self.maker_uri:
            self.maker_uri = self.maker_uri['href']

        return self.maker

    ######################################################

    def parse_label(self, item):
        finder = item.findAll('td', {
            'class': 'text',
        })
        if not finder:
            return None

        self.label = finder[-1].get_text().strip()
        self.label_uri = item.find('a')
        if self.label_uri:
            self.label_uri = self.label_uri['href']

        return self.label

    ######################################################

    def parse_cast(self, item):
        finder = item.findAll('td', {
            'class': 'text',
        })
        if not finder:
            return None

        self.cast = finder[-1].get_text().strip()
        self.cast_uri = item.find('a')
        if self.cast_uri:
            self.cast_uri = self.cast_uri['href']

        return self.cast

    ######################################################


######################################################

pageurl = ''
jav = JavLibDetail(pageurl)
print(jav.id)
print(jav.title)
print(jav.image)
print(jav.date)
print(jav.length)
print(jav.maker)
print(jav.maker_uri)
print(jav.label)
print(jav.label_uri)
print(jav.cast)
print(jav.cast_uri)
