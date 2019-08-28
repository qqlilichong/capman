
#######################################################################################################

import t_xpath
import a_tool
import a_http

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

class RXP:
    def __init__(self, cfg):
        self.cfg = cfg
        self.pin = dict()

    def task(self):
        return a_http.htext(a_http.hctx(self.cfg[r'param.context'],
                                        url=self.cfg[r'param.url'],
                                        xpath=self.__task,
                                        farmer=self))

    async def __task(self, ctx):
        self.pin = dict()
        vl = [k for k in self.cfg.keys() if k.find(r'pin.') != -1]
        result = dict()
        for node in t_xpath.xselects(ctx[r'xp'], self.cfg[r'param.select']):
            nd = {v: t_xpath.xnode(node, self.cfg[v]) for v in vl}
            if nd:
                result[nd[r'pin.id']] = nd

        self.pin = result
        return True

#######################################################################################################
