
######################################################

import re

from webtools import \
    http_get, \
    http_download, \
    http_urljoin \

from bs4 import BeautifulSoup

######################################################





######################################################








######################################################


class JavLibDetail:

    ######################################################

    def __init__(self, url):
        self.bs = None
        self.url = None
        self.parseset = None

        self.id = None
        self.title = None
        self.image = None
        self.date = None
        self.length = None
        self.maker = None
        self.label = None
        self.cast = None

        try:
            resp = http_get(url)
            if not resp:
                return

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

            if not self.parse():
                self.id = None

        except:
            self.id = None

    ######################################################

    def parse(self):
        for item in self.bs.findAll('div', id=re.compile('video_\w+')):
            handler = item['id']
            if handler not in self.parseset:
                continue

            if not self.parseset[handler](item):
                return None

        return True

    ######################################################

    def parse_id(self, item):
        self.id = item.find('td', 'text').get_text().strip()
        return self.id

    ######################################################

    def parse_image(self, item):
        self.image = http_urljoin(self.url, item.img['src'].strip())
        return self.image

    ######################################################

    def parse_title(self, item):
        self.title = item.a.get_text().strip()
        return self.title

    ######################################################

    def parse_date(self, item):
        self.date = item.find('td', 'text').get_text().strip()
        return self.date

    ######################################################

    def parse_length(self, item):
        self.length = item.find('td', '').get_text().strip()
        return self.length

    ######################################################

    def parse_maker(self, item):
        finder = item.find('td', 'text').a
        self.maker = (finder.get_text().strip(), finder['href'])
        return self.maker

    ######################################################

    def parse_label(self, item):
        finder = item.find('td', 'text').a
        self.label = (finder.get_text().strip(), finder['href'])
        return self.label

    ######################################################

    def parse_cast(self, item):
        self.cast = []
        for star in item.findAll('span', 'star'):
            self.cast.append((star.a.get_text().strip(), star.a['href']))
        return self.cast

    ######################################################


######################################################


def javlib_parse_html(file, path):
    pagedict = {}
    try:
        with open(file, encoding='utf-8') as source:
            for finder in BeautifulSoup(source.read(), 'html5lib').findAll('div', 'video'):
                finder = finder.a
                item = {
                    'title': finder.find('div', 'title').get_text().strip(),
                    'image': http_urljoin(path, finder.img['src']),
                    'page': http_urljoin(path, finder['href']),
                }
                pagedict[finder.find('div', 'id').get_text().strip()] = item
    except:
        return None

    return pagedict


######################################################


def javlib_check_lost(pagedict):
    chk = re.compile('^(\w+)([_-]+)(\w+)$')

    jid_max = chk.match(max(pagedict))
    if not jid_max:
        print('javlib_check_lost, ERROR, not jid_max')
        return None

    jid_min = chk.match(min(pagedict))
    if not jid_min:
        print('javlib_check_lost, ERROR, not jid_min')
        return None

    result = []
    jid_header = jid_max.group(1)
    jid_mid = jid_max.group(2)
    jid_width = len(jid_max.group(3))
    jid_beg = int(jid_min.group(3))
    jid_end = int(jid_max.group(3)) + 1
    for jnum in range(jid_beg, jid_end):
        jnum = '%s%s%s' % (jid_header, jid_mid, str(jnum).zfill(jid_width))
        if jnum not in pagedict:
            result.append(jnum)
            continue

    return result


######################################################

pageurl = 'http://www.javlibrary.com/ja/?v=javlilaf5y'
jav = JavLibDetail(pageurl)
print(jav.id)

pd = javlib_parse_html('./res/snis.html', pageurl)
print(javlib_check_lost(pd))
