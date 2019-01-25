
#######################################################################

import os
import webtool
import javlib

#######################################################################

def capman():
    dbinfo = webtool.mkd(db=r'javlib',
                         user=r'root',
                         passwd=r'admin')

    cfg = webtool.IniDict()
    proot = os.path.dirname(__file__)
    cfg.read(os.path.join(proot, r'configer_jmakers.ini'))
    proot = os.path.join(proot, cfg[r'CONFIG'][r'path'])
    for maker, ma in cfg.resection(r'^JMAKER_(\w+)$').items():
        javlib.start_collect(proot,
                             dbinfo,
                             ma.group(1),
                             webtool.http_urljoin(cfg[r'CONFIG'][r'site'], cfg[maker][r'url']))

#######################################################################

if __name__ == "__main__":
    capman()
    print('bye...')

#######################################################################
