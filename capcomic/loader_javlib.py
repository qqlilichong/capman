
#######################################################################

import os
import t_webtool
import t_javlib
import t_jscaper

#######################################################################

def update_cookie(website):
    bs = t_jscaper.newbs(False, False, True)

    def work():
        result = None
        try:
            if t_jscaper.getbss(bs, website, r'div#toplogo'):
                cookiedict = {c[r'name']: c[r'value'] for c in bs.get_cookies()}
                cookies = [r'%s=%s' % (k, v) for k, v in cookiedict.items()]
                os.environ[r't_cookie'] = r'; '.join(cookies)
                result = True
        finally:
            return result

    data = None
    while data is None:
        data = work()

    bs.close()
    bs.quit()
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
