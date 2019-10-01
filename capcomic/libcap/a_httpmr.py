
#######################################################################################################

import os
import re
from libcap import a_tool, a_http, t_xpath, t_beans

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

    def reparam(self, paramlist):
        result = list()
        for p in paramlist:
            for k in re.findall(r'<(.*?)>', p):
                p = p.replace(r'<%s>' % k, self.bean[k])
            result.append(p)
        return result

    async def exceptbus(self, ctx):
        await ctx[r'log'](ctx, self.debug)
        ctx[r'retry'] = True

    @staticmethod
    async def logbus(ctx, log):
        await ctx[r'log'](ctx, log, 1)

#######################################################################################################

class FarmerXP(FarmerBase):
    def task(self):
        self.debug = r'%s@%s' % (self.bean[r'param.beanid'], self.bean[r'param.select'])
        return a_http.htext(self.newctx(url=self.bean[r'param.url']), *self.tasklist())

    def tasklist(self):
        return [self.__xp_work]

    def __param_joinurl(self):
        joinlist = [r'pin.id']
        if r'param.joinurl' in self.bean.keys():
            joinlist = [k for k in self.bean[r'param.joinurl'].split(r'&')]
        return joinlist

    async def __xp_work(self, ctx, _):
        ctx[r'workstack'] = self.debug

        joinlist = self.__param_joinurl()
        self.pin = dict()
        result = dict()
        pinlist = [k for k in self.bean.keys() if k.find(r'pin.') != -1]
        for node in t_xpath.xselects(ctx[r'xp'], self.bean[r'param.select']):
            nd = {pin: t_xpath.xnode(node, self.bean[pin]) for pin in pinlist}
            if not nd:
                continue
            for k in joinlist:
                nd[k] = a_tool.urljoin(ctx[r'url'], nd[k])
            result[nd[r'pin.id']] = nd
        self.pin = result
        return True

#######################################################################################################

class FarmerNavi(FarmerXP):
    def tasklist(self):
        return super().tasklist() + [self.__navi_work]

    def __param_navi(self):
        if r'param.navi' not in self.bean.keys():
            return

        bact = t_beans.BeanAct(self.bean[r'param.navi'])
        idx = 0
        if bact.param:
            idx = int(bact.param[0])

        for k, v in bact.view.items():
            for pin in self.pin.values():
                pin[v] = re.findall(bact.act, pin[k])[idx]

    async def __navi_work(self, ctx, _):
        self.pin[ctx[r'url']] = {
            r'pin.id': ctx[r'url']
        }
        self.__param_navi()
        return True

#######################################################################################################

class FarmerFile(FarmerBase):
    def task(self):
        self.debug = r'%s@%s' % (self.bean[r'param.beanid'], self.bean[r'param.name'])
        return a_http.hsave(self.newctx(url=self.bean[r'param.url'], file=self.__filename()), *self.tasklist())

    def tasklist(self):
        return [self.__file_work]

    def __filename(self):
        filename = r''
        for p in self.reparam(self.bean[r'param.file'].split(r'|')):
            filename = os.path.join(filename, p)
        return filename

    async def __file_work(self, ctx, _):
        ctx[r'workstack'] = self.debug
        self.pin = dict()
        self.pin = {
            ctx[r'file']: {
                r'pin.file': ctx[r'file']
            }
        }
        return True

#######################################################################################################
