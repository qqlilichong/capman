
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

    def reparamval(self, data):
        paramlist = data.split(r'|')
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
                result[key.replace(kid, r'')] = self.reparamval(self.bean[key])
        self.bean.update(result)

    def repinvalre(self, bact):
        reidx = int(bact.getparam(r'reidx', 0))
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

    def extpin(self, tag):
        def user_reparamval():
            for k, v in bact.view.items():
                val = self.reparamval(k)
                result[val] = {v: val}

        def user_lastfill():
            lastitem = None
            for i in self.pin.values():
                lastitem = i
            if not lastitem:
                return

            pid = None
            redata = None
            review = None
            lastnum = 0
            reidx = int(bact.getparam(r'reidx', 0))
            uid = bact.getparam(r'uid', r'pin.id')
            for k, v in bact.view.items():
                pid = lastitem[uid]
                lastnum = int(re.findall(k, pid)[reidx])
                review = v
                redata = v % lastnum
            if not lastnum:
                return

            for i in range(1, lastnum):
                val = pid.replace(redata, review % i)
                result[val] = {uid: val}

        extpmap = {
            r'reparamval': user_reparamval,
            r'lastfill': user_lastfill,
        }

        kid = r'extp.%s' % tag
        result = dict()
        for key in self.bean.keys():
            if not key.startswith(kid):
                continue
            bact = t_beans.BeanAct(self.bean[key])
            if not bact.isprouser():
                continue
            if bact.act in extpmap.keys():
                extpmap[bact.act]()
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
            nd = {pin: self.fixnode(t_xpath.xnode(node, self.bean[pin])) for pin in pinlist}
            if not nd:
                continue
            for k in joinlist:
                nd[k] = a_tool.tjoinurl(ctx[r'url'], nd[k])
            result[nd[r'pin.id']] = nd

        self.extpin(r'addhead')
        self.pin.update(result)
        self.extpin(r'addtail')
        self.repin()
        return True

    @staticmethod
    def fixnode(txt):
        if not txt:
            return txt
        result = txt
        result = re.sub('(<.*>)', r'', result)
        result = re.sub('(\r\n)', r'', result)
        result = re.sub('(\n)', r'', result)
        return result

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
