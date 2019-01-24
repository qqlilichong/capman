
#######################################################################

import os
import webtool

import javlib
import stocklib
import caper_dmwu

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

def capstock():
    stocklib.start_collect()

#######################################################################

def caper():
    cfg = webtool.IniDict()
    cfg.read(os.path.join(os.path.dirname(__file__), r'caper.ini'))
    for maker in cfg.resection(r'^DMWU_(\w+)$').keys():
        caper_dmwu.capman(cfg[maker][r'url'],
                          os.path.join(cfg[r'OUTPUT'][r'path'], cfg[maker][r'title']),
                          cfg[maker][r'match'],
                          cfg[maker][r'format'],
                          cfg[maker][r'reverse'])
    print('caper bye ...')

#######################################################################

if __name__ == "__main__":
    caper()

#######################################################################
