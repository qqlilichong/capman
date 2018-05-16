
######################################################
# Import Section.
import os
import re
import json
import bs4
import multiprocessing
from webtools import http_get, http_urljoin, http_download

######################################################
# Json serialization.
def jformat(*args, **kwargs):
    obj = None

    if args:
        obj = args

    elif kwargs:
        obj = kwargs

    return json.dumps(obj, ensure_ascii=False, indent=True)

    ######################################################

def jseri(text):
    return json.loads(text)

######################################################
# BeautifulSoup Creator.
def bscreator(text):
    return bs4.BeautifulSoup(text, 'html5lib')

    ######################################################

def bsget(url):
    return bscreator(http_get(url).text)

    ######################################################

def bshtml(file, enc='utf-8'):
    with open(file, encoding=enc) as src:
        return bscreator(src.read())

######################################################
#  Find all lost jav-id.
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

        try:
            if not self.parse():
                self.id = None
        except:
            self.id = None

    ######################################################

    def __str__(self):
        return jformat(
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

    ######################################################

    def parse(self):
        for item in bsget(self.url).findAll('div', id=re.compile('video_\w+')):
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

class JavLibSearch:
    def __init__(self, cache=None):
        self.api = None
        self.result = None
        self.cache = cache
        self.load(self.cache)

    ######################################################

    def get(self, keyword, mainpage='http://www.javlibrary.com/ja/'):
        self.api = http_urljoin(mainpage, 'vl_searchbyid.php?&keyword=%s' % keyword)
        self.result = {}

        try:
            for page in self.parse_pagelist():
                self.parse_page(page)

            if self.cache:
                self.save(self.cache)
        except:
            self.result = None

    ######################################################

    def save(self, file, enc='utf-8'):
        try:
            with open(file, 'w', encoding=enc) as fh:
                fh.write(jformat(api=self.api, result=self.result))
                return True
        except:
            return None

    ######################################################

    def load(self, file, enc='utf-8'):
        try:
            with open(file, 'r', encoding=enc) as fh:
                jdict = jseri(fh.read())
                self.api = jdict['api']
                self.result = jdict['result']
                return True
        except:
            return None

    ######################################################

    def __str__(self):
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

    def parse_page(self, page):
        for finder in bsget(page).findAll('div', 'video'):
            finder = finder.a
            self.result[finder.find('div', 'id').get_text().strip()] = {
                'title': finder.find('div', 'title').get_text().strip(),
                'image': http_urljoin(page, finder.img['src']),
                'page': http_urljoin(page, finder['href']),
            }

    ######################################################

    @staticmethod
    def fork_capdetail(page, imgfile):
        info = JavLibDetail(page)
        if not info.id:
            print('JavLibSearch build, ERROR, info.id = %s', info.id)
            return None

        if not http_download(info.image, imgfile):
            print('JavLibSearch build, ERROR, img = %s', info.id)
            return None

        return True

    ######################################################

    def build(self, path):
        reactor = multiprocessing.Pool(8)
        for jid, jitem in self.result.items():
            img = os.path.join(path, jid + '.jpg')
            if os.path.exists(img):
                continue

            reactor.apply_async(self.fork_capdetail, (jitem['page'], img))

        reactor.close()
        reactor.join()

######################################################
