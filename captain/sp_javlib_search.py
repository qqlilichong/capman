
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
            report = self.report()

            rlist = []
            for r in report:
                rlist.append(str(r))

            report = '\n'.join(rlist)

            result = report
            return

        finally:
            return result

    ######################################################

    def report(self):
        result = None

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

            result = report
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
        if not file_mkdir(os.path.dirname(filename)):
            return None

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

            result = [jtyper, '%s <%s> %s' % (jbeg, len(losts), jend)] + losts
            return

        finally:
            return result

    ######################################################

    def get(self, search, jfilterflow=list()):
        result = None

        try:
            self.jpages = {}
            self.search = search
            self.filter = jfilterflow

            spagelist = None
            while not spagelist:
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
            spagelist = []
            apage = bsget(self.search).find('a', 'page last')
            if not apage:
                spagelist.append((self.search, JavLibFilter(self.filter)))

            else:
                pagecount = int(re.match('.*page=(\d+)', apage['href']).group(1))

                for i in range(1, pagecount + 1):
                    spagelist.append(('%s&page=%s' % (self.search, i), JavLibFilter(self.filter)))

            result = spagelist
            return

        finally:
            return result

    ######################################################

    def build(self, pathmaker, jpath):
        result = None

        try:
            if len(self.jpages) == 0:
                return

            jpagelist = []
            for jpage in self.jpages.values():
                imgpath = os.path.join(pathmaker, jpage['jtyper'])
                file_mkdir(imgpath)
                imgfile = os.path.join(imgpath, jpage['jid'] + '.jpg')
                if not file_exists(imgfile):
                    imgpath = os.path.relpath(imgpath, jpath)
                    imgpath = imgpath.replace('\\', '/')
                    jpagelist.append((jpage, imgfile, imgpath))

            if len(jpagelist) > 0:
                jdetailist = JavLibSearchMapper.parse_jpagelist(jpagelist)
                if len(jdetailist) != len(jpagelist):
                    return

            result = True
            return

        finally:
            return result

    ######################################################

######################################################

def scrapy_javlib_maker(jlib, jurl, jmaker, jfilterflow):
    print('')
    print('**************** scrapy_javlib_maker %s ****************' % jmaker)
    path_maker = os.path.join(jlib, jmaker)

    print('')
    print('$finding jtypers ...')
    jenumtyper = JavLibSearch(os.path.join(path_maker, '%s.jmcache' % jmaker))
    if jenumtyper.ready():
        print('jmaker cache upspeed : [%s]' % jmaker)
    else:
        while not jenumtyper.ready():
            print('jmaker cache building : [%s]' % jmaker)
            jenumtyper.get(jurl, jfilterflow)
        print('jmaker cache ready : [%s]' % jmaker)

    jsdict = {}
    for ritem in jenumtyper.report():
        jtyper = ritem[0]
        jsdict[jtyper] = JavLibSearch(os.path.join(path_maker, '%s.jtcache' % jtyper))
        print('found jtyper : [%s]' % jtyper)

    print('')
    print('$building jtypers cache ...')
    for jtyper, jsearch in jsdict.items():
        if jsearch.ready():
            print('jtyper cache upspeed : [%s]' % jtyper)
            continue

        print('jtyper cache building : [%s]' % jtyper)

        jsurl = http_urljoin(jurl, 'vl_searchbyid.php?&keyword=%s' % jtyper)
        while not jsearch.ready():
            jsearch.get(jsurl, jfilterflow)

        print('jtyper cache ready : [%s]' % jtyper)

    print('')
    print('$building jtypers lib ...')
    for jtyper, jsearch in jsdict.items():
        print('----------------- [%s] -----------------' % jtyper)
        print(jsearch)
        print('')

        building = None
        while not building:
            print('$try build ...')
            building = jsearch.build(path_maker, jlib)

        print('-----------------  end  ------------------')
        print('')

    return True

######################################################
