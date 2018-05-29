
######################################################

import re
from .webtools import *

######################################################

class JavLibDetail:

    ######################################################

    def __init__(self, url):
        self.url = url
        self.parseset = mkdict(
            video_id=self.parse_id,
            video_title=self.parse_title,
            video_jacket=self.parse_image,
            video_date=self.parse_date,
            video_length=self.parse_length,
            video_maker=self.parse_maker,
            video_label=self.parse_label,
            video_cast=self.parse_cast,
        )

        self.id = None
        self.title = None
        self.image = None
        self.date = None
        self.length = None
        self.maker = None
        self.label = None
        self.cast = None
        self.parse()

    ######################################################

    def ready(self):
        if self.id:
            return True

        return None

    ######################################################

    def __str__(self):
        result = ''

        try:
            jstr = jformat(
                url=self.url,
                id=self.id,
                title=self.title,
                image=self.image,
                date=self.date,
                length=self.length,
                maker=self.maker,
                label=self.label,
                cast=self.cast,
            )
            if not jstr:
                return

            result = jstr
            return

        finally:
            return result

    ######################################################

    def parse(self):
        result = None

        try:
            for item in bsget(self.url).findAll('div', id=re.compile('video_\w+')):
                handler = item['id']
                if handler in self.parseset:
                    self.parseset[handler](item)

            result = True
            return

        finally:
            if not result:
                self.id = None

            return result

    ######################################################

    def parse_id(self, item):
        self.id = item.find('td', 'text').get_text().strip()

    ######################################################

    def parse_image(self, item):
        self.image = http_urljoin(self.url, item.img['src'].strip())

    ######################################################

    def parse_title(self, item):
        self.title = item.a.get_text().strip()

    ######################################################

    def parse_date(self, item):
        self.date = item.find('td', 'text').get_text().strip()

    ######################################################

    def parse_length(self, item):
        self.length = item.find('td', '').get_text().strip()

    ######################################################

    def parse_maker(self, item):
        finder = item.find('td', 'text').a
        href = http_urljoin(self.url, finder['href'])
        self.maker = [(re.match('.*m=(\w+)', href).group(1), finder.get_text().strip(), href)]

    ######################################################

    def parse_label(self, item):
        finder = item.find('td', 'text').a
        if finder:
            href = http_urljoin(self.url, finder['href'])
            self.label = [(re.match('.*l=(\w+)', href).group(1), finder.get_text().strip(), href)]
        else:
            self.label = [('NOLABEL', 'NOLABEL', 'NOLABEL')]

    ######################################################

    def parse_cast(self, item):
        self.cast = []
        for star in item.findAll('span', 'star'):
            star = star.a
            href = http_urljoin(self.url, star['href'])
            self.cast.append((re.match('.*s=(\w+)', href).group(1), star.get_text().strip(), href))

    ######################################################

    def saveimg(self, filename):
        return http_download(self.image, filename)

    ######################################################

######################################################
