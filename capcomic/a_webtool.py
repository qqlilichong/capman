
#######################################################################################################

import time
from libcap import t_ptree, a_http, a_httpmr, a_tool

#######################################################################################################

class CapLSM:
    @staticmethod
    def subproc(param):
        beans, metas = param

        async def caper(context):
            await a_httpmr.farm(context, beans, metas)

        a_tool.tloop(a_http.hsession(caper))
        return beans

    @staticmethod
    def mainbus(beans, metas):
        mainkey = None
        for key, bean in beans.items():
            if r'meta.main' in bean.keys():
                mainkey = key
                break
        if not mainkey:
            return

        dlist = list()
        for pid, info in CapLSM.plist().items():
            for i in range(1, info[r'count'] + 1):
                ibeans = a_tool.dc(beans)
                ibeans[mainkey][r'param.url'] = ibeans[mainkey][r'param.url'].replace(r'<_>', r'%s-%s' % (pid, i))
                ibeans[mainkey][r'cookie.saveroot'] = ibeans[mainkey][r'cookie.saveroot'].replace(r'<_>', info[r'name'])
                dlist.append((ibeans, metas))

        for r in a_tool.mrmp(dlist, CapLSM.subproc, 8):
            if not r:
                raise Exception(r'Error.')

    @staticmethod
    def plist():
        return {
            r'109': {
                r'name': r'头条女神 Goddes',
                r'count': 29,
            }
        }

#######################################################################################################

def mainbus(config):
    time_begin = time.time()
    metas = dict()
    metas.update(a_http.meta())
    metas.update(a_httpmr.meta())
    ini = t_ptree.PTini()
    ini.read(config)
    beans = {beanid: ini[beanid].copy() for beanid in ini.smatch(r'(bean.\w+)').keys()}
    CapLSM.mainbus(beans, metas)
    print(r'runtime : %s' % (time.time() - time_begin))

#######################################################################################################

if __name__ == '__main__':
    mainbus(r'configer_beans.ini')

#######################################################################################################
