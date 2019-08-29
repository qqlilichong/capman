
#######################################################################################################

import os
import re
import t_xpath
import a_tool
import a_http

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

class FarmerXP:
    def __init__(self, cfg):
        self.cfg = cfg
        self.pin = dict()

    def task(self):
        return a_http.htext(a_http.hctx(self.cfg[r'param.context'],
                                        url=self.cfg[r'param.url'],
                                        farmer=self), self.__work)

    async def __work(self, ctx, _):
        ctx[r'workstack'] = r'[%s]{%s}<%s>' % (self.cfg[r'meta.id'], ctx[r'url'], self.cfg[r'param.select'])

        self.pin = dict()
        result = dict()
        vl = [k for k in self.cfg.keys() if k.find(r'pin.') != -1]
        for node in t_xpath.xselects(ctx[r'xp'], self.cfg[r'param.select']):
            nd = {v: t_xpath.xnode(node, self.cfg[v]) for v in vl}
            if nd:
                result[nd[r'pin.id']] = nd
        self.pin = result
        return True

#######################################################################################################

class FarmerFile:
    def __init__(self, cfg):
        self.cfg = cfg
        self.pin = dict()

    def __filename(self):
        filename = r''
        for d in self.cfg[r'param.file'].split(r'|'):
            for t in re.findall(r'<(.*?)>', d):
                d = d.replace(r'<%s>' % t, self.cfg[t])
            filename = os.path.join(filename, d)
        return filename

    def task(self):
        return a_http.hsave(a_http.hctx(self.cfg[r'param.context'],
                                        url=self.cfg[r'param.url'],
                                        file=self.__filename(),
                                        farmer=self), self.__work)

    async def __work(self, ctx, _):
        ctx[r'workstack'] = r'[%s]{%s}<%s>' % (self.cfg[r'meta.id'], ctx[r'url'], self.cfg[r'param.name'])

        self.pin = {
            ctx[r'file'] : {
                ctx[r'file']: ctx[r'url']
            }
        }
        return True

#######################################################################################################
