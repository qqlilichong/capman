
#######################################################################

import os
import javlib
import webtool

#######################################################################

def capjav():
    dbinfo = {
        r'db': r'javlib',
        r'user': r'root',
        r'passwd': r'admin',
    }

    jcfg = webtool.IniDict()
    jpath = os.path.dirname(__file__)
    jcfg.read(os.path.join(jpath, r'jmakers.ini'))
    jcfg[r'CONFIG']
    rootpath = os.path.join(jpath, jcfg[r'CONFIG'][r'jlib'])
    rootsite = jcfg[r'CONFIG'][r'site']

    for key, m in jcfg.resection(r'^JMAKER_(\w+)$').keys():
        if jcfg[key][r'use'] != r'true':
            continue

        url = webtool.http_urljoin(rootsite, jcfg[key][r'url'])
        javlib.start_collect(rootpath, dbinfo, m.group(1), url)

    print('capjav bye ...')


#######################################################################

if __name__ == "__main__":
    capjav()
    #caper_dmzj.capman(r'https://manhua.dmzj.com/snsfdpj/10574.shtml', r'y:/capman')

#######################################################################
