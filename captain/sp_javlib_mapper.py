
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
        def run_task():
            result = None
            spage, filterflow = param

            try:
                jpages = {}

                def makefdict(jid, title, preview, detail):
                    vid = re.match('^(\w+)(\W+)(\w+)$', jid)
                    if not vid:
                        return None

                    return filterflow.flowing(
                        jid=vid.group(0).strip(),
                        jtyper=vid.group(1).strip(),
                        jmider=vid.group(2).strip(),
                        jnumer=vid.group(3).strip(),
                        title=title,
                        preview=preview,
                        detail=detail,
                    )

                spages = bsget(spage).findAll('div', 'video')
                if not spages:
                    jdetail = JavLibDetail(spage)
                    if jdetail.ready():
                        fdict = makefdict(jdetail.id,
                                          jdetail.title,
                                          jdetail.image,
                                          jdetail.url)
                        if fdict:
                            jpages[fdict['jid']] = fdict

                for finder in spages:
                    finder = finder.a
                    fdict = makefdict(finder.find('div', 'id').get_text().strip(),
                                      finder.find('div', 'title').get_text().strip(),
                                      http_urljoin(spage, finder.img['src']),
                                      http_urljoin(spage, finder['href']))
                    if fdict:
                        jpages[fdict['jid']] = fdict

                result = jpages
                return

            finally:
                if not result:
                    print('parse_spage, ERROR, %s' % spage)

                return result

        taskok = None
        while not taskok:
            taskok = run_task()
        return taskok

    ######################################################

    @staticmethod
    def parse_jpage(param):
        def run_task():
            result = None
            jpage, imgfile, imgpath = param

            try:
                jdetail = JavLibDetail(jpage['detail'])
                if not jdetail.ready():
                    return

                if not jdetail.saveimg(imgfile):
                    return

                jdb = JavLibDB()
                if not jdb.connect():
                    return

                jdetail.id = '%s/%s' % (imgpath, jdetail.id)
                result = jdb.update(jdetail)
                jdb.close()
                return

            finally:
                if not result:
                    file_remove(imgfile)
                    print('parse_jpage, ERROR, image = %s' % jpage['jid'])

                return result

        taskok = None
        while not taskok:
            taskok = run_task()
        return taskok

    ######################################################

######################################################
