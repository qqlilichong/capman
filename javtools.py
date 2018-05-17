
######################################################

import re
from webtools import *

######################################################

def javlib_check_lost(pagedict):
    result = None

    try:
        chk = re.compile('^(\w+)([_-]+)(\w+)$')

        key_max = max(pagedict)
        jid_max = chk.match(key_max)
        if not jid_max:
            print('javlib_check_lost, ERROR, jid_max')
            return

        key_min = min(pagedict)
        jid_min = chk.match(key_min)
        if not jid_min:
            print('javlib_check_lost, ERROR, jid_min')
            return

        jid_header = jid_max.group(1)
        jid_mid = jid_max.group(2)
        jid_width = len(jid_max.group(3))
        jid_beg = int(jid_min.group(3))
        jid_end = int(jid_max.group(3)) + 1

        losts = []
        for jnum in range(jid_beg, jid_end):
            jnum = '%s%s%s' % (jid_header, jid_mid, str(jnum).zfill(jid_width))
            if jnum not in pagedict:
                losts.append(jnum)
                continue

        report = ['%s <%s, %s> %s' % (key_min, jid_end - jid_beg, len(losts), key_max)]
        report.extend(losts)

        result = report
        return

    finally:
        return result

######################################################

class JavLibDetail:
    def __init__(self, url):
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

class JavLibSearch:
    def __init__(self, cache=None):
        self.mainpage = 'http://www.javlibrary.com/ja/'
        self.api = None
        self.result = None
        self.cache = cache
        self.load(self.cache)

    ######################################################

    def load(self, filename, enc='utf-8'):
        result = None

        try:
            jdict = jseri(file_read(filename, 'r', encoding=enc))
            self.api = jdict['api']
            self.result = jdict['result']

            result = True
            return

        finally:
            if not result:
                self.api = None
                self.result = None

            return result

    ######################################################

    def save(self, filename, enc='utf-8'):
        result = None

        try:
            if not file_create(
                    filename,
                    jformat(api=self.api, result=self.result),
                    'w',
                    encoding=enc):
                return

            result = True
            return

        finally:
            if not result:
                self.api = None
                self.result = None

            return result

    ######################################################

    @staticmethod
    def mapper_parse_page(page):
        result = {}

        try:
            for finder in bsget(page).findAll('div', 'video'):
                finder = finder.a
                result[finder.find('div', 'id').get_text().strip()] = {
                    'title': finder.find('div', 'title').get_text().strip(),
                    'image': http_urljoin(page, finder.img['src']),
                    'page': http_urljoin(page, finder['href']),
                }

        except:
            print('mapper_parse_page, ERROR, %s', page)
            return None

        return result

    ######################################################

    def getkeyword(self, keyword):
        self.api = http_urljoin(self.mainpage, 'vl_searchbyid.php?&keyword=%s' % keyword)
        self.result = {}

        try:
            for jdict in reactor_reduce(self.parse_pagelist(), self.mapper_parse_page):
                self.result.update(jdict)

            if self.cache:
                self.save(self.cache)
        except:
            self.result = None



    ######################################################



    ######################################################

    def __str__(self):
        icount = 0
        if self.result:
            icount = len(self.result)

        info = 'JavLibSearch(%s) %s items found' % (self.api, icount)
        if icount > 0:
            info += ' $$LOST$$==> %s' % javlib_check_lost(self.result)

        return info

    ######################################################

    def parse_pagelist(self):
        finder = bsget(self.api).find('a', 'page last')
        pagecount = int(re.match('.*page=(\d+)', finder['href']).group(1))

        pagelist = []
        for i in range(1, pagecount + 1):
            pagelist.append(self.api + '&page=%s' % i)

        return pagelist

    ######################################################

    @staticmethod
    def mapper_parse_detail(info):
        try:
            jid, jitem, imgfile = info

            detail = JavLibDetail(jitem['page'])
            if not detail.id:
                print('mapper_parse_detail, ERROR, detail = %s', jid)
                return None

            if not http_download(detail.image, imgfile):
                print('mapper_parse_detail, ERROR, image = %s', jid)
                return None

            return jid

        except:
            return None

    ######################################################

    def build(self, path):
        details = []
        for jid, jitem in self.result.items():
            imgfile = os.path.join(path, jid + '.jpg')
            if os.path.exists(imgfile):
                continue
            details.append((jid, jitem, imgfile))

        reactor_reduce(details, self.mapper_parse_detail)

######################################################
