
#######################################################################

import os
import javlib
import webtool
import caper_dmzj

#######################################################################

def capjav():
    dbinfo = {
        r'db': r'javlib',
        r'user': r'root',
        r'passwd': r'admin',
    }

    cfg = webtool.IniDict()
    jpath = os.path.dirname(__file__)
    cfg.read(os.path.join(jpath, r'jmakers.ini'))
    rootpath = os.path.join(jpath, cfg[r'CONFIG'][r'jlib'])
    rootsite = cfg[r'CONFIG'][r'site']

    for jmaker, ma in cfg.resection(r'^JMAKER_(\w+)$').items():
        if cfg[jmaker][r'use'] != r'true':
            continue

        url = webtool.http_urljoin(rootsite, cfg[jmaker][r'url'])
        javlib.start_collect(rootpath, dbinfo, ma.group(1), url)

    print('capjav bye ...')

#######################################################################

def capjav():
    cfg = webtool.IniDict()
    jpath = os.path.dirname(__file__)
    cfg.read(os.path.join(jpath, r'caper.ini'))

    for caper, ma in cfg.resection(r'^CAPER_(\w+)$').items():
        if ma.group(1) == r'DMZJ':
            output = cfg[caper]

#######################################################################

if __name__ == "__main__":
    capjav()
    #caper_dmzj.capman(r'https://manhua.dmzj.com/snsfdpj/10574.shtml', r'y:/capman')

#######################################################################
