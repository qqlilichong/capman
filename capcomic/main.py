
#######################################################################

import os
import re
import javlib
import webtool
import configparser
import caper_dmzj

#######################################################################

def capjav():
    dbinfo = {
        r'db': r'javlib',
        r'user': r'root',
        r'passwd': r'admin',
    }

    jpath = os.path.dirname(__file__)
    jcfg = configparser.ConfigParser()
    jcfg.read(os.path.join(jpath, r'jmakers.ini'), encoding=r'utf-8')
    rootpath = os.path.join(jpath, jcfg.get(r'CONFIG', r'jlib'))
    rootsite = jcfg.get(r'CONFIG', r'site')

    for section in jcfg.sections():
        jmaker = re.match(r'^JMAKER_(\w+)$', section)
        if not jmaker:
            continue

        if jcfg.get(section, r'use') != r'true':
            continue

        url = webtool.http_urljoin(rootsite, jcfg.get(section, r'url'))
        javlib.start_collect(rootpath, dbinfo, jmaker.group(1), url)

    print('capjav bye ...')


#######################################################################

if __name__ == "__main__":
    caper_dmzj.capman(r'https://manhua.dmzj.com/tzbexysdpj/71082.shtml', r'y:/01')

#######################################################################
