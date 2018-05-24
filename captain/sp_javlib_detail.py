
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
        self.maker = (finder.get_text().strip(), finder['href'])

    ######################################################

    def parse_label(self, item):
        finder = item.find('td', 'text').a
        self.label = (finder.get_text().strip(), finder['href'])

    ######################################################

    def parse_cast(self, item):
        self.cast = []
        for star in item.findAll('span', 'star'):
            self.cast.append((star.a.get_text().strip(), star.a['href']))

    ######################################################

    def saveimg(self, filename):
        return http_download(self.image, filename)

    ######################################################

    def dbmodel(self):
        result = None

        try:
            model = dict(id=self.id)

            model['detail'] = mkdict(
                title=self.title,
                image=self.image,
                date=self.date,
                length=self.length
            )

            model['maker'] = [(
                re.match('.*m=(\w+)', self.maker[1]).group(1),
                http_urljoin(self.url, self.maker[1]),
                self.maker[0]
            )]

            model['label'] = [(
                re.match('.*l=(\w+)', self.label[1]).group(1),
                http_urljoin(self.url, self.label[1]),
                self.label[0]
            )]

            model['cast'] = []
            for mm in self.cast:
                model['cast'].append((
                    re.match('.*s=(\w+)', mm[1]).group(1),
                    http_urljoin(self.url, mm[1]),
                    mm[0]
                ))

            result = model
            return

        finally:
            return result

    ######################################################

######################################################
