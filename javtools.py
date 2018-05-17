
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

def jav_filter_parse_page(**kwargs):
    title = kwargs['title']
    if re.match('.*（ブルーレイディスク）', title):
        print('jav_filter_parse_page, INFO, %s <%s> %s' % (kwargs['page'], kwargs['jid'], title))
        return None

    return kwargs

######################################################

class JavLibSearch:
    def __init__(self, cache=None):
        self.mainpage = 'http://www.javlibrary.com/ja/'
        self.result = None
        self.api = None
        self.cache = cache

        if self.cache:
            self.load(self.cache)

    ######################################################

    def ready(self):
        if self.result and self.api:
            return True

        return None

    ######################################################

    def load(self, filename, enc='utf-8'):
        result = None

        try:
            jdict = jseri(file_read(filename, 'r', encoding=enc))
            self.result = jdict['result']
            self.api = jdict['api']

            result = True
            return

        finally:
            if not result:
                self.result = None
                self.api = None

            return result

    ######################################################

    def save(self, filename, enc='utf-8'):
        return file_create(filename, jformat(api=self.api, result=self.result), 'w', encoding=enc)

    ######################################################

    def __str__(self):
        result = ''

        try:
            icount = 0
            if self.result:
                icount = len(self.result)

            info = 'JavLibSearch(%s) %s items found' % (self.api, icount)
            if icount > 0:
                info += ' $$LOST$$==> %s' % javlib_check_lost(self.result)

            result = info
            return

        finally:
            return result

    ######################################################

    @staticmethod
    def mapper_parse_page(page):
        result = None

        try:
            pages = {}
            for finder in bsget(page).findAll('div', 'video'):
                finder = finder.a
                jid = finder.find('div', 'id').get_text().strip()
                fd = jav_filter_parse_page(
                    jid=jid,
                    title=finder.find('div', 'title').get_text().strip(),
                    image=http_urljoin(page, finder.img['src']),
                    page=http_urljoin(page, finder['href']),
                )

                if fd:
                    pages[jid] = fd

            result = pages
            return

        finally:
            if not result:
                print('mapper_parse_page, ERROR, %s' % page)

            return result

    ######################################################

    def getkeyword(self, keyword):
        result = None

        try:
            self.result = {}
            self.api = http_urljoin(self.mainpage, 'vl_searchbyid.php?&keyword=%s' % keyword)

            pagelist = self.parse_pagelist()
            reducelist = reactor_reduce(pagelist, self.mapper_parse_page)
            if len(pagelist) != len(reducelist):
                return

            for jdict in reducelist:
                self.result.update(jdict)

            if self.cache:
                self.save(self.cache)

            result = True
            return

        finally:
            if not result:
                self.result = None
                self.api = None

            return result

    ######################################################

    def parse_pagelist(self):
        result = None

        try:
            finder = bsget(self.api).find('a', 'page last')
            pagecount = int(re.match('.*page=(\d+)', finder['href']).group(1))

            pagelist = []
            for i in range(1, pagecount + 1):
                pagelist.append(self.api + '&page=%s' % i)

            result = pagelist
            return

        finally:
            return result

    ######################################################

    @staticmethod
    def mapper_parse_detail(info):
        result = None

        try:
            jid, jitem, imgfile = info

            detail = JavLibDetail(jitem['page'])
            if not detail.ready():
                print('mapper_parse_detail, ERROR, detail = %s' % jid)
                return

            if not detail.saveimg(imgfile):
                print('mapper_parse_detail, ERROR, image = %s' % jid)
                return

            result = jid
            return

        finally:
            return result

    ######################################################

    def build(self, path):
        result = None

        try:
            file_mkdir(path)

            details = []
            for jid, jitem in self.result.items():
                imgfile = os.path.join(path, jid + '.jpg')
                if not os.path.exists(imgfile):
                    details.append((jid, jitem, imgfile))

            if not reactor_reduce(details, self.mapper_parse_detail):
                return

            result = True
            return

        finally:
            return result

######################################################
