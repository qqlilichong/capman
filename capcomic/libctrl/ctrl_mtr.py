
#######################################################################################################

from libcap import a_tool

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def control(mb, beans, metas):
    ibeans = a_tool.dc(beans)
    mainbean = mb[r'bean']
    ibeans[mainbean][r'meta.main'] = r'true'
    ibeans[mainbean][r'param.url'] = r'https://www.meituri.com/a/31406/'
    ibeans[mainbean][r'cookie.saveroot'] = r'%s/test' % mb[r'saveroot']
    metas[mb[r'view']]((ibeans, metas))
    return True

#######################################################################################################
