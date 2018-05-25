
######################################################

from .sp_javlib_detail import *
from .db_javlib import *

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

            jdb = JavLibDB()
            if not jdb.connect():
                return

            if not jdb.update(jdetail.dbmodel()):
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
