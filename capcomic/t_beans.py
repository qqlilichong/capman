
#######################################################################################################

class BeanAct:
    def __init__(self, act):
        self.act = r''
        self.param = list()
        self.view = dict()
        self.__update(act)

    def __update(self, act):
        beanmain = act.split(r'/')
        beanfunc = beanmain[0].split(r':')
        self.act = beanfunc[0]
        self.param = beanfunc[1:]
        for v in beanmain[1].split(r'|'):
            v = v.split(r'->')
            self.view[v[0]] = v[1]

#######################################################################################################

class Beans:
    def __init__(self, beans, metas, context):
        self.beans = beans
        self.metas = metas
        self.context = context

    def starts(self):
        return [self.newtask(self.newbean(beanid)) for beanid, bean in self.beans.items() if r'meta.main' in bean.keys()]

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
        nbs = list()
        for pin in farmer.pin.values():
            nb = self.newbean(bact.act)
            for k, v in bact.view.items():
                nb[v] = pin[k]
            nbs.append(nb)

        for k, v in farmer.bean.items():
            if not k.startswith(r'cookie.'):
                continue
            for nb in nbs:
                nb[k] = v

        return [self.newtask(nb) for nb in nbs]

#######################################################################################################
