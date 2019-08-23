
#######################################################################################################

import a_tool
import a_http
import t_xpath

#######################################################################################################

class ReducerXP:
    def __init__(self, config):
        self.config = config
        self.config[r'result'] = dict()

    async def workwork(self, ctx):
        vl = [k for k in self.config.keys() if k.find(r'v.') != -1]

        result = dict()
        for node in t_xpath.xselects(ctx[r'xp'], self.config[r'select']):
            nd = {v: t_xpath.xnode(node, self.config[v]) for v in vl}
            if nd:
                result[nd[r'v.id']] = nd

        self.config[r'result'] = result
        return True

#######################################################################################################

def mrfactory(name, config):
    clsfactory = [ReducerXP]
    for cls in clsfactory:
        if cls.__name__ == name:
            return cls(config)
    return None

#######################################################################################################

async def mainbus(context):
    cfg1 = {
        r'url': r'https://www.jisilu.cn/',
        r'class': r'ReducerXP',
        r'select': r'//div[@class="text2"]/a',
        r'v.id': r'@href',
        r'v.text': r'text()',
    }

    farmer = mrfactory(cfg1[r'class'], cfg1)
    c2 = a_http.hctx(context, url=cfg1[r'url'], xpath=farmer.workwork)
    for result in await a_tool.tmr(a_http.hcontent(c2)):
        print(result[r'url'])

#######################################################################################################

if __name__ == '__main__':
    a_tool.tloop(a_http.hsession(mainbus))

#######################################################################################################
