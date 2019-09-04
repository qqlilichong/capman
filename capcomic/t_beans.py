
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

#######################################################################################################
