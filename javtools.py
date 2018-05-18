
######################################################

import re
from webtools import *

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

######################################################

class JavLibFilter:

    ######################################################

    def __init__(self, filterlist):
        self.filterflow = None
        self.filtermap = mkdict(
            EXNAME=self.filter_exname,
            SONE_TITLE=self.filter_sone_title,
        )

        self.makeflow(filterlist)

    ######################################################

    def makeflow(self, filterlist):
        result = None

        try:
            filterflow = []
            for fname in filterlist:
                filterflow.append(self.filtermap[fname])

            self.filterflow = filterflow

            result = True
            return

        finally:
            if not result:
                self.filterflow = None

            return result

    ######################################################

    def flowing(self, **jpage):
        result = None

        try:
            for flow in self.filterflow:
                jpage = flow(jpage)
                if not jpage:
                    return

            result = jpage
            return

        finally:
            return result

    ######################################################

    @staticmethod
    def filter_exname(jpage):
        if not re.match('^\d+$', jpage['jnumer']):
            return None

        return jpage

    ######################################################

    @staticmethod
    def filter_sone_title(jpage):
        if re.match('.*（ブルーレイディスク）', jpage['title']):
            return None

        return jpage

    ######################################################

######################################################

class JavLibSearchMapper:

    ######################################################

    @staticmethod
    def parse_spagelist(spagelist):
        return reactor_reduce(spagelist, JavLibSearchMapper.parse_spage)

    ######################################################

    @staticmethod
    def parse_jpagelist(jpagelist):
        return reactor_reduce(jpagelist, JavLibSearchMapper.parse_jpage)

    ######################################################

    @staticmethod
    def parse_spage(param):
        result = None
        spage, filterflow = param

        try:
            jpages = {}
            for finder in bsget(spage).findAll('div', 'video'):
                finder = finder.a
                vid = re.match('^(\w+)(\W+)(\w+)$', finder.find('div', 'id').get_text().strip())
                if not vid:
                    continue

                fdict = filterflow.flowing(
                    jid=vid.group(0).strip(),
                    jtyper=vid.group(1).strip(),
                    jmider=vid.group(2).strip(),
                    jnumer=vid.group(3).strip(),
                    title=finder.find('div', 'title').get_text().strip(),
                    preview=http_urljoin(spage, finder.img['src']),
                    detail=http_urljoin(spage, finder['href']),
                )

                if fdict:
                    jpages[fdict['jid']] = fdict

            result = jpages
            return

        finally:
            if not result:
                print('parse_spage, ERROR, %s' % spage)

            return result

    ######################################################

    @staticmethod
    def parse_jpage(param):
        result = None
        jpage, imgfile = param

        try:
            jdetail = JavLibDetail(jpage['detail'])
            if not jdetail.ready():
                return

            if not jdetail.saveimg(imgfile):
                return

            result = jdetail
            return

        finally:
            if not result:
                file_remove(imgfile)
                print('parse_jpage, ERROR, image = %s' % jpage['jid'])

            return result

    ######################################################

######################################################

class JavLibSearch:

    ######################################################

    def __init__(self, cache=None):
        self.jpages = None
        self.search = None
        self.filter = None
        self.cache = cache

        if self.cache:
            self.load(self.cache)

    ######################################################

    def ready(self):
        if self.jpages and self.search:
            return True

        return None

    ######################################################

    def __str__(self):
        result = ''

        try:
            jidrange = {}
            for jpage in self.jpages.values():
                jtyper = jpage['jtyper']
                jnumer = jpage['jnumer']

                if jtyper not in jidrange:
                    jidrange[jtyper] = [jpage['jmider'], jnumer, jnumer]
                    continue

                if int(jnumer) < int(jidrange[jtyper][1]):
                    jidrange[jtyper][1] = jnumer
                    continue

                if int(jnumer) > int(jidrange[jtyper][2]):
                    jidrange[jtyper][2] = jnumer
                    continue

            report = []
            for jtyper, info in jidrange.items():
                report.append(self.check_lost(jtyper, info[0], info[1], info[2]))

            result = '\n'.join(report)
            return

        finally:
            return result

    ######################################################

    def load(self, filename, enc='utf-8'):
        result = None

        try:
            jdict = jseri(file_read(filename, 'r', encoding=enc))
            self.jpages = jdict['jpages']
            self.search = jdict['search']
            self.filter = jdict['filter']

            result = True
            return

        finally:
            if not result:
                self.jpages = None
                self.search = None
                self.filter = None

            return result

    ######################################################

    def save(self, filename, enc='utf-8'):
        return file_create(
            filename,
            jformat(jpages=self.jpages,
                    search=self.search,
                    filter=self.filter),
            'w',
            encoding=enc
        )

    ######################################################

    def check_lost(self, jtyper, jminder, jbeg, jend):
        result = None

        try:
            losts = []
            for jnumer in range(int(jbeg), int(jend) + 1):
                jid = '%s%s%s' % (jtyper, jminder, str(jnumer).zfill(len(jend)))
                if jid not in self.jpages:
                    losts.append(jid)
                    continue

            result = str([jtyper, '%s <%s> %s' % (jbeg, len(losts), jend)] + losts)
            return

        finally:
            return result

    ######################################################

    def get(self, search, filterlist=list()):
        result = None

        try:
            self.jpages = {}
            self.search = search
            self.filter = filterlist

            spagelist = self.parse_spagelist()
            jpageslist = JavLibSearchMapper.parse_spagelist(spagelist)
            if len(spagelist) != len(jpageslist):
                return

            for jpages in jpageslist:
                self.jpages.update(jpages)

            if self.cache:
                self.save(self.cache)

            result = True
            return

        finally:
            if not result:
                self.jpages = None
                self.search = None
                self.filter = None

            return result

    ######################################################

    def parse_spagelist(self):
        result = None

        try:
            pagecount = int(
                re.match(
                    '.*page=(\d+)',
                    bsget(self.search).find('a', 'page last')['href']
                ).group(1)
            )

            spagelist = []
            for i in range(1, pagecount + 1):
                spagelist.append(('%s&page=%s' % (self.search, i), JavLibFilter(self.filter)))

            result = spagelist
            return

        finally:
            return result

    ######################################################

    def build(self, path):
        result = None

        try:
            jpagelist = []
            for jpage in self.jpages.values():
                imgfile = os.path.join(path, jpage['jtyper'])
                file_mkdir(imgfile)
                imgfile = os.path.join(imgfile, jpage['jid'] + '.jpg')
                if not file_exists(imgfile):
                    jpagelist.append((jpage, imgfile))

            jdetailist = JavLibSearchMapper.parse_jpagelist(jpagelist)
            if len(jdetailist) != len(jpagelist):
                return

            result = True
            return

        finally:
            return result

    ######################################################

######################################################
