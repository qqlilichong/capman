
#######################################################################################################

from libcap import t_ptree, a_http, a_httpmr
from libctrl import view_default, ctrl_lsm, ctrl_mtr
from libuser import uc_fixtitle, uc_newpin

#######################################################################################################

def mainbus(config):
    metas = dict()
    metas.update(a_http.meta())
    metas.update(a_httpmr.meta())

    metas.update(view_default.meta())
    metas.update(ctrl_lsm.meta())
    metas.update(ctrl_mtr.meta())

    metas.update(uc_fixtitle.meta())
    metas.update(uc_newpin.meta())

    ini = t_ptree.PTini()
    ini.read(config)
    beans = {beanid: ini[beanid].copy() for beanid in ini.smatch(r'(bean.\w+)').keys()}
    mb = ini[r'main']
    metas[mb[r'control']](mb, beans, metas)

#######################################################################################################

if __name__ == '__main__':
    mainbus(r'configer_beans.ini')

#######################################################################################################
