
######################################################

from .sp_javlib_mapper import *
from .sp_javlib_filter import *

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
