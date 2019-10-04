
#######################################################################################################

from libcap import a_tool

#######################################################################################################

class BeanAct:
    def __init__(self, act):
        self.act = r''
        self.pro = r''
        self.param = list()
        self.view = dict()
        self.__update(act)

    @staticmethod
    def __sp(obj):
        result = dict()
        for v in obj.split(r'|'):
            v = v.split(r'->')
            result[v[0]] = v[1]
        return result

    def __update(self, act):
        beanmain = act.split(r'/?/')
        beanfunc = beanmain[0].split(r'/:/')
        if len(beanfunc) > 1:
            self.param = self.__sp(beanfunc[1])
        self.view = self.__sp(beanmain[1])
        self.__protocol(beanfunc[0])

    def __protocol(self, act):
        acts = act.split(r'/@/')
        if len(acts) == 2:
            self.pro = acts[0]
            self.act = acts[1]

    def isprobl(self):
        return self.pro == r'bl'

    def isprore(self):
        return self.pro == r're'

#######################################################################################################

class Beans:
    def __init__(self, beans, metas, context):
        self.beans = beans
        self.metas = metas
        self.context = context

    def starts(self):
        return [self.newtask(self.newbean(k)) for k, v in self.beans.items() if r'meta.main' in v.keys()]

    def newbean(self, beanid):
        bean = self.beans[beanid].copy()
        bean[r'param.beanid'] = beanid
        bean[r'param.context'] = self.context
        return bean

    def newtask(self, bean):
        return self.metas[bean[r'meta.class']](bean).task()

    def transform(self, farmer):
        if r'meta.link' not in farmer.bean.keys():
            return list()

        bact = BeanAct(farmer.bean[r'meta.link'])
        if not bact.isprobl():
            raise Exception()

        nbs = list()
        for pin in farmer.pin.values():
            nb = self.newbean(bact.act)
            for k, v in bact.view.items():
                nb[v] = pin[k]
            nb[r'meta.index'] = a_tool.tzf(len(nbs))
            nbs.append(nb)

        for k, v in farmer.bean.items():
            if not k.startswith(r'cookie.'):
                continue
            for nb in nbs:
                nb[k] = v

        return [self.newtask(nb) for nb in nbs]

#######################################################################################################
