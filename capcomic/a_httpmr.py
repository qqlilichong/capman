
#######################################################################################################

import os
import re
import t_xpath
import a_tool
import a_http

def meta():
    return a_tool.metatbl(globals())

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

class BeanStock:
    def __init__(self, beans, context):
        self.context = context
        self.beans = beans

    def starts(self):
        return [self.newtask(self.newbean(beanid)) for beanid, bean in self.beans.items() if r'meta.main' in bean.keys()]

    def newbean(self, beanid):
        bean = self.beans[beanid].copy()
        bean[r'param.beanid'] = beanid
        bean[r'param.context'] = self.context
        return bean

    def newtask(self, bean):
        return self.context[r'meta'][bean[r'meta.class']](bean).task()

    def transform(self, farmer):
        if r'meta.link' not in farmer.bean.keys():
            return list()

        beanparse = farmer.bean[r'meta.link'].split(r'?')
        beanmap = dict()
        for pv in beanparse[1].split(r'&'):
            pv = pv.split(r'=')
            beanmap[pv[0]] = pv[1]

        tasks = list()
        for fv in farmer.pin.values():
            nb = self.newbean(beanparse[0])
            for k, v in beanmap.items():
                nb[v] = fv[k]
            tasks.append(self.newtask(nb))

        return tasks

    async def farming(self, tasks):
        result = list()
        for ctx in await a_tool.tmr(*tasks):
            result += self.transform(ctx[r'farmer'])
        return result

#######################################################################################################

def farming(beans):
    async def mainbus(context):
        bs = BeanStock(beans, context)
        tasks = bs.starts()
        while tasks:
            tasks = await bs.farming(tasks)
    a_tool.tloop(a_http.hsession(mainbus))

#######################################################################################################
