
#######################################################################

import os
import webtool

import javlib
import caper_dmzj

#######################################################################

def capjav():
    dbinfo = webtool.mkd(db=r'javlib',
                         user=r'root',
                         passwd=r'admin')

    cfg = webtool.IniDict()
    proot = os.path.dirname(__file__)
    cfg.read(os.path.join(proot, r'jmakers.ini'))
    proot = os.path.join(proot, cfg[r'CONFIG'][r'path'])
    for maker, ma in cfg.resection(r'^JMAKER_(\w+)$').items():
        javlib.start_collect(proot,
                             dbinfo,
                             ma.group(1),
                             webtool.http_urljoin(cfg[r'CONFIG'][r'site'], cfg[maker][r'url']))

    print('capjav bye ...')

#######################################################################

def caper():
    cfg = webtool.IniDict()
    cfg.read(os.path.join(os.path.dirname(__file__), r'caper.ini'))
    for maker, ma in cfg.resection(r'^DMZJ_(\w+)$').items():
        for path, url in cfg[maker].items():
            caper_dmzj.capman(url,
                              os.path.join(cfg[r'OUTPUT'][r'path'], ma.group(1), path))

    print('caper bye ...')

#######################################################################

if __name__ == "__main__":
    caper()

#######################################################################
