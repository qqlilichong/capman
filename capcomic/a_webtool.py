
#######################################################################################################

import time
from libcap import t_ptree, a_http, a_httpmr
from libctrl import view_default, ctrl_lsm

#######################################################################################################

def mainbus(config):
    time_begin = time.time()

    metas = dict()
    metas.update(a_http.meta())
    metas.update(a_httpmr.meta())
    metas.update(view_default.meta())
    metas.update(ctrl_lsm.meta())

    ini = t_ptree.PTini()
    ini.read(config)
    beans = {beanid: ini[beanid].copy() for beanid in ini.smatch(r'(bean.\w+)').keys()}
    mainbean = ini[r'main'][r'bean']
    view = metas[ini[r'main'][r'view']]
    control = metas[ini[r'main'][r'control']]
    control(mainbean, beans, metas, view)

    print(r'runtime : %s' % (time.time() - time_begin))

#######################################################################################################

if __name__ == '__main__':
    mainbus(r'configer_beans.ini')

#######################################################################################################
