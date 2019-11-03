
#######################################################################################################

from libcap import a_tool

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def plist():
    return {
        r'109': {
            r'name': r'头条女神 Goddes',
            r'count': 29,
        }
    }

#######################################################################################################

def control(mainbean, beans, metas, view):
    dlist = list()
    for pid, info in plist().items():
        for i in range(1, info[r'count'] + 1):
            ibeans = a_tool.dc(beans)
            ibeans[mainbean][r'meta.main'] = r'true'
            ibeans[mainbean][r'param.url'] = ibeans[mainbean][r'param.url'].replace(r'<_>', r'%s-%s' % (pid, i))
            ibeans[mainbean][r'cookie.saveroot'] = ibeans[mainbean][r'cookie.saveroot'].replace(r'<_>', info[r'name'])
            dlist.append((ibeans, metas))

    for r in a_tool.mrmp(dlist, view, 8):
        if not r:
            raise Exception(r'Error.')

    return True

#######################################################################################################
