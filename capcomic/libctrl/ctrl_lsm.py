
#######################################################################################################

import os
import re
from libcap import a_tool, a_http, t_xpath

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def forum_count(url):
    result = None

    async def forum(ctx, _):
        nonlocal result
        for node in t_xpath.xselects(ctx[r'xp'], r'//div[@class="pg"]//a[@class="last"]'):
            result = int(re.search(r'(\d+)', t_xpath.xtext(node)).group(1))
            return
        result = 1

    async def routine(context):
        context[r'url'] = url
        await a_http.htext(context, forum)

    a_tool.tloop(a_http.hsession(routine))

    if not result:
        raise Exception(r'forum_count error.')

    return result

#######################################################################################################

def products():
    return {
        r'109': {
            r'name': r'头条女神 Goddes',
        },

        r'55': {
            r'name': r'美媛馆 MyGirl',
        }
    }

#######################################################################################################

def plist(mainbean, beans):
    url = beans[mainbean][r'url']
    saveroot = beans[mainbean][r'saveroot']

    pros = products()
    for pid, info in pros.items():
        info[r'url'] = a_tool.tjoinurl(url, (r'forum-%s' % pid) + r'-%s.html')
        info[r'forum'] = info[r'url'] % 1
        info[r'saveroot'] = os.path.join(saveroot,)


    forum_count(r'https://www.lsm.me/forum-109-1.html')
    return dict()
    # return {
    #     r'109': {
    #         r'name': r'头条女神 Goddes',
    #         r'count': 29,
    #     }
    # }

#######################################################################################################

def control(mainbean, beans, metas, view):
    dlist = list()
    for pid, info in plist(mainbean, beans).items():
        for i in range(1, info[r'count'] + 1):
            ibeans = a_tool.dc(beans)
            ibeans[mainbean][r'meta.main'] = r'true'
            ibeans[mainbean][r'param.url'] = info[r'url'] % i
            ibeans[mainbean][r'cookie.saveroot'] = info[r'saveroot']
            dlist.append((ibeans, metas))

    for r in a_tool.mrmp(dlist, view, 8):
        if not r:
            raise Exception(r'Error.')

    return True

#######################################################################################################
