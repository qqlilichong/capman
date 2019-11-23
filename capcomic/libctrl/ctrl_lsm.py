
#######################################################################################################

import os
import re
from libcap import a_tool, a_http, t_xpath

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def products():
    return {
        r'109': {
            r'name': r'头条女神 Goddes',
        },

        r'39': {
            r'name': r'推女郎 TuiGirl',
        }
    }

#######################################################################################################

class Prot:
    def __init__(self, mb, pid, info):
        self.mb = mb
        self.pid = pid
        self.url = self.geturl(1)
        self.saveroot = os.path.join(mb[r'saveroot'], info[r'name'])
        self.pages = list()

    def geturl(self, idx):
        return a_tool.tjoinurl(self.mb[r'url'], (r'forum-%s' % self.pid) + (r'-%s.html' % idx))

    @staticmethod
    async def getpc(ctx):
        for node in t_xpath.xselects(ctx[r'xp'], r'//div[@class="pg"]//a[@class="last"]'):
            return int(re.search(r'(\d+)', t_xpath.xtext(node)).group(1))
        pidxs = list()
        for node in t_xpath.xselects(ctx[r'xp'], r'//div[@class="pg"]//a/text()'):
            if node.isnumeric():
                pidxs.append(int(node))
        if pidxs:
            return max(pidxs)
        return 1

    async def parse(self, ctx, _):
        pc = await self.getpc(ctx)
        self.pages = [self.geturl(i) for i in range(1, pc + 1)]

    def newtask(self, context):
        ctx = context.copy()
        ctx[r'url'] = self.url
        return a_http.htext(ctx, self.parse)

    @staticmethod
    def init(prots):
        async def routine(context):
            await a_tool.tmr(*[prot.newtask(context) for prot in prots])
        a_tool.tloop(a_http.hsession(routine))

#######################################################################################################

def plist(mb):
    # init all products.
    prots = [Prot(mb, pid, info) for pid, info in products().items()]
    Prot.init(prots)
    return prots

#######################################################################################################

def control(mb, beans, metas):
    dlist = list()
    for prot in plist(mb):
        for page in prot.pages:
            ibeans = a_tool.dc(beans)
            mainbean = mb[r'bean']
            ibeans[mainbean][r'meta.main'] = r'true'
            ibeans[mainbean][r'param.url'] = page
            ibeans[mainbean][r'cookie.saveroot'] = prot.saveroot
            dlist.append((ibeans, metas))

    for r in a_tool.mrmp(dlist, metas[mb[r'view']], 8):
        if not r:
            raise Exception(r'Error.')

    return True

#######################################################################################################
