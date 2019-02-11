
#######################################################################

import os
import t_webtool
import t_javlib

#######################################################################

def loader_main():
    dbinfo = t_webtool.mkd(db=r'javlib',
                           user=r'root',
                           passwd=r'admin')

    cfg = t_webtool.IniDict()
    proot = os.path.dirname(__file__)
    cfg.read(os.path.join(proot, r'configer_jmakers.ini'))
    proot = os.path.join(proot, cfg[r'CONFIG'][r'path'])
    for maker, ma in cfg.resection(r'^JMAKER_(\w+)$').items():
        t_javlib.start_collect(proot,
                               dbinfo,
                               ma.group(1),
                               t_webtool.http_urljoin(cfg[r'CONFIG'][r'site'], cfg[maker][r'url']))

#######################################################################

if __name__ == "__main__":
    loader_main()
    print('bye...')

#######################################################################
