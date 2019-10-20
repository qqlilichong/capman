
#######################################################################################################

import re
from libcap import a_tool, a_http, a_file, t_xpath, t_beans

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
        self.reparam()

    def newctx(self, **kwargs):
        ctx = self.bean[r'param.context'].copy()
        ctx.update(kwargs)
        ctx[r'farmer'] = self
        ctx[r'except'] = self.exceptbus
        self.reheaders(ctx[r'headers'])
        return ctx

    def reheaders(self, headers):
        kid = r'param.headers.'
        for key, val in self.bean.items():
            if key.startswith(kid):
                headers[key.replace(kid, r'')] = val

    def reparamval(self, key):
        paramlist = self.bean[key].split(r'|')
        result = list()
        for p in paramlist:
            for k in re.findall(r'<(.*?)>', p):
                p = p.replace(r'<%s>' % k, self.bean[k])
            result.append(p)
        return r''.join(result)

    def reparam(self):
        kid = r'reparam.'
        result = dict()
        for key in self.bean.keys():
            if key.startswith(kid):
                result[key.replace(kid, r'')] = self.reparamval(key)
        self.bean.update(result)

    def repinvalre(self, bact):
        reidx = 0
        if r'reidx' in bact.param:
            reidx = int(bact.param[r'reidx'])

        for k, v in bact.view.items():
            for pin in self.pin.values():
                pin[v] = re.findall(bact.act, pin[k])[reidx]

    def repinval(self, key):
        bact = t_beans.BeanAct(self.bean[key])
        if bact.isprore():
            self.repinvalre(bact)

    def repin(self):
        kid = r'repin.'
        for key in self.bean.keys():
            if key.startswith(kid):
                self.repinval(key)

    def extpin(self):
        kid = r'extp.'
        result = dict()
        for key in self.bean.keys():
            if key.startswith(kid):
                pid = self.reparamval(key)
                result[pid] = {r'pin.id': pid}
        self.pin.update(result)

    def skip(self, ctx):
        if r'param.skip' not in self.bean.keys():
            return
        if not a_file.fexists(a_tool.fixpath(self.bean[r'param.skip'])):
            return None
        return a_http.hnull(ctx)

    async def exceptbus(self, ctx):
        await ctx[r'log'](ctx, self.debug)
        ctx[r'retry'] = True

    @staticmethod
    async def logbus(ctx, log):
        await ctx[r'log'](ctx, log, 1)

#######################################################################################################

class FarmerXP(FarmerBase):
    def task(self):
        ctx = self.newctx(url=self.bean[r'param.url'])
        self.debug = r'%s@%s' % (self.bean[r'param.beanid'], self.bean[r'param.select'])
        tpass = self.skip(ctx)
        if tpass:
            return tpass
        return a_http.htext(ctx, *self.tasklist())

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
                nd[k] = a_tool.tjoinurl(ctx[r'url'], nd[k])
            result[nd[r'pin.id']] = nd

        self.extpin()
        self.pin.update(result)
        self.repin()
        return True

#######################################################################################################

class FarmerFile(FarmerBase):
    def task(self):
        file = a_tool.fixpath(self.bean[r'param.file'])
        ctx = self.newctx(url=self.bean[r'param.url'], file=file)
        self.debug = r'[get]%s@%s' % (self.bean[r'param.beanid'], file)
        tpass = self.skip(ctx)
        if tpass:
            return tpass
        return a_http.hsave(ctx, *self.tasklist())

    def tasklist(self):
        return [self.__file_work]

    def __igs(self):
        if r'param.igs' not in self.bean.keys():
            return list()
        return [int(i) for i in self.bean[r'param.igs'].split(r'|')]

    async def __file_work(self, ctx, _):
        ctx[r'workstack'] = self.debug
        self.pin = dict()
        self.pin = {
            ctx[r'file']: {
                r'pin.file': ctx[r'file']
            }
        }
        return True

    async def exceptbus(self, ctx):
        if ctx[r'status'] in self.__igs():
            ctx[r'retry'] = False
        else:
            await super().exceptbus(ctx)

#######################################################################################################
