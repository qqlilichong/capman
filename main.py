
######################################################

import configparser
from captain.sp_javlib_search import *

######################################################

if __name__ == '__main__':
    jpath = os.path.dirname(__file__)
    jcfg = configparser.ConfigParser()
    jcfg.read(os.path.join(jpath, 'jmakers.ini'), encoding='utf-8')

    def make_jfilterflow(section):
        jfilterflow = []
        for key, val in jcfg.items(section):
            jfilter = re.match('^(\d+)\.jfilter\.(.*)$', key)
            if jfilter:
                jfilterflow.append((jfilter.group(1), jfilter.group(2), val))

        jfilterflow.sort(key=lambda f: int(f[0]))
        return [(f[1], f[2]) for f in jfilterflow]

    def start_capman(jlib, site):
        for section in jcfg.sections():
            jmaker = re.match('^JMAKER_(\w+)$', section)
            if not jmaker:
                continue

            if jcfg.get(section, 'use') != 'true':
                continue

            jfilterflow = make_jfilterflow(section)
            if not jfilterflow:
                continue

            scrapy_javlib_maker(jlib,
                                http_urljoin(site, jcfg.get(section, 'url')),
                                jmaker.group(1),
                                jfilterflow)

    start_capman(os.path.join(jpath, jcfg.get('CONFIG', 'jlib')),
                 jcfg.get('CONFIG', 'site'))
    print('capman bye!')
    exit(0)

######################################################
