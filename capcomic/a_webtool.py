
#######################################################################################################

from libcap import t_ptree, a_http, a_httpmr

#######################################################################################################

def mainbus(cfgfile):
    ini = t_ptree.PTini()
    ini.read(cfgfile)
    beans = {beanid: ini[beanid].copy() for beanid in ini.smatch(r'(bean.\w+)').keys()}
    metas = dict()
    metas.update(a_http.meta())
    metas.update(a_httpmr.meta())
    a_httpmr.farm(beans, metas)

#######################################################################################################

if __name__ == '__main__':
    mainbus(r'configer_beans.ini')

#######################################################################################################
