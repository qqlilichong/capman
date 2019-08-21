
#######################################################################

import os
import t_webtool
import t_javlib

#######################################################################

def update_cookie(website):
    os.environ[r't_cloudflare'] = r'true'

    def work():
        result = None
        try:
            if t_webtool.CFSession().reset(website).status_code == 200:
                result = True
        finally:
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def loader_main():
    dbinfo = t_webtool.mkd(db=r'javlib',
                           user=r'root',
                           passwd=r'admin')

    cfg = t_webtool.IniDict()
    proot = os.path.dirname(__file__)
    cfg.read(os.path.join(proot, r'configer_jmakers.ini'))
    proot = os.path.join(proot, cfg[r'CONFIG'][r'path'])
    website = cfg[r'CONFIG'][r'site']
    for maker, ma in cfg.resection(r'^JMAKER_(\w+)$').items():
        update_cookie(website)
        t_javlib.start_collect(proot,
                               dbinfo,
                               ma.group(1),
                               t_webtool.http_urljoin(website, cfg[maker][r'url']))

#######################################################################

if __name__ == "__main__":
    loader_main()
    print('bye...')

#######################################################################
