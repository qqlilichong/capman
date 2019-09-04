
#######################################################################################################

import os
import re
import a_tool
import a_http
import t_xpath
import t_beans

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def farm(beans, metas):
    async def farmbus(bs, tasks):
        result = list()
        for ctx in await a_tool.tmr(*tasks):
            result += bs.transform(ctx[r'farmer'])
        return result

    async def mainbus(context):
        bs = t_beans.Beans(beans, metas, context)
        tasks = bs.starts()
        while tasks:
            tasks = await farmbus(bs, tasks)

    a_tool.tloop(a_http.hsession(mainbus))

#######################################################################################################

class FarmerBase:
    def __init__(self, bean):
        self.bean = bean
        self.pin = dict()
        self.debug = r''

    def newctx(self, **kwargs):
        ctx = self.bean[r'param.context'].copy()
        ctx.update(kwargs)
        ctx[r'farmer'] = self
        ctx[r'except'] = self.exceptbus
        return ctx

    async def exceptbus(self, ctx):
        await ctx[r'log'](ctx, self.debug)
        ctx[r'retry'] = True

#######################################################################################################

class FarmerXP(FarmerBase):
    def task(self):
        self.debug = r'%s@%s' % (self.bean[r'param.beanid'], self.bean[r'param.select'])
        return a_http.htext(self.newctx(url=self.bean[r'param.url']),
                            self.__work)

    async def __work(self, ctx, _):
        ctx[r'workstack'] = self.debug
        self.pin = dict()
        result = dict()
        vl = [k for k in self.bean.keys() if k.find(r'pin.') != -1]
        for node in t_xpath.xselects(ctx[r'xp'], self.bean[r'param.select']):
            nd = {v: t_xpath.xnode(node, self.bean[v]) for v in vl}
            if nd:
                result[nd[r'pin.id']] = nd
        self.pin = result
        return True

#######################################################################################################

class FarmerFile(FarmerBase):
    def task(self):
        self.debug = r'%s@%s' % (self.bean[r'param.beanid'], self.bean[r'param.name'])
        return a_http.hsave(self.newctx(url=self.bean[r'param.url'], file=self.__filename()),
                            self.__work)

    def __filename(self):
        filename = r''
        for d in self.bean[r'param.file'].split(r'|'):
            for t in re.findall(r'<(.*?)>', d):
                d = d.replace(r'<%s>' % t, self.bean[t])
            filename = os.path.join(filename, d)
        return filename

    async def __work(self, ctx, _):
        ctx[r'workstack'] = self.debug
        self.pin = dict()
        self.pin = {
            ctx[r'file']: {
                r'pin.file': ctx[r'file']
            }
        }
        return True

#######################################################################################################
