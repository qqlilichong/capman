
#######################################################################################################

import os
import re
from libcap import a_tool, a_http, t_xpath

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def products():
    return {
        # r'132': {
        #     r'name': r'轰趴猫 PartyCat',
        # },
        #
        # r'133': {
        #     r'name': r'猎女神 SLY',
        # },
        #
        # r'80': {
        #     r'name': r'魅妍社 MiStar',
        # },
        #
        # r'82': {
        #     r'name': r'模范学院 MFStar',
        # },
        #
        # r'99': {
        #     r'name': r'爱尤物 UGirls APP',
        # },
        #
        # r'106': {
        #     r'name': r'尤物馆 YouWu',
        # },
        #
        # r'109': {
        #     r'name': r'头条女神 Goddes',
        # },
        #
        # r'112': {
        #     r'name': r'激萌文化 Kimoe',
        # },
        #
        # r'119': {
        #     r'name': r'DK御女郎 DKGirl',
        # },
        #
        # r'122': {
        #     r'name': r'尤蜜荟 YOUMI',
        # },
        #
        # r'125': {
        #     r'name': r'模特联盟 MTMENG',
        # },
        #
        # r'130': {
        #     r'name': r'星颜社 XINGYAN',
        # },
        #
        # r'55': {
        #     r'name': r'美媛馆 MyGirl',
        # },
        #
        # r'135': {
        #     r'name': r'语画界 XIAOYU',
        # },
        #
        # r'136': {
        #     r'name': r'雅拉伊 YALAYI',
        # },
        #
        # r'81': {
        #     r'name': r'优星馆 UXING',
        # },
        #
        # r'85': {
        #     r'name': r'嗲囡囡 FeiLin',
        # },
        #
        # r'104': {
        #     r'name': r'顽味生活 Taste',
        # },
        #
        # r'107': {
        #     r'name': r'影私荟 WingS',
        # },
        #
        # r'110': {
        #     r'name': r'美腿宝贝 Legbaby',
        # },
        #
        # r'113': {
        #     r'name': r'波萝社 BoLoli',
        # },
        #
        # r'120': {
        #     r'name': r'薄荷叶 MintYe',
        # },
        #
        # r'124': {
        #     r'name': r'克拉女神 KeLa',
        # },
        #
        # r'126': {
        #     r'name': r'猫萌榜 MICAT',
        # },
        #
        # r'131': {
        #     r'name': r'熊川纪信 XCJX',
        # },
        #
        # r'40': {
        #     r'name': r'秀人网 XiuRen',
        # },
        #
        # r'134': {
        #     r'name': r'尤美 YOUMEI',
        # },
        #
        # r'79': {
        #     r'name': r'兔几盟 Tukmo',
        # },
        #
        # r'83': {
        #     r'name': r'爱蜜社 IMiss',
        # },
        #
        # r'89': {
        #     r'name': r'DDY Pantyhose',
        # },
        #
        # r'105': {
        #     r'name': r'蜜桃社 MiiTao',
        # },
        #
        # r'108': {
        #     r'name': r'星乐园 LeYuan',
        # },
        #
        # r'111': {
        #     r'name': r'花の颜 HuaYan',
        # },
        #
        # r'116': {
        #     r'name': r'村长的宝物 CUZ',
        # },
        #
        # r'121': {
        #     r'name': r'糖果画报 CANDY',
        # },
        #
        # r'123': {
        #     r'name': r'萌缚 MF',
        # },
        #
        # r'128': {
        #     r'name': r'花漾show HuaYang',
        # },
        #
        # r'59': {
        #     r'name': r'推女神 TGOD',
        # },
        #
        # r'54': {
        #     r'name': r'爱丝 AISS',
        # },

        r'39': {
            r'name': r'推女郎 TuiGirl',
        },

        # r'UGirls': {
        #     r'name': r'尤果网 UGirls',
        # },
        #
        # r'84': {
        #     r'name': r'中国腿模',
        # },
        #
        # r'87': {
        #     r'name': r'51Modo',
        # },
        #
        # r'86': {
        #     r'name': r'IShow',
        # },
        #
        # r'44': {
        #     r'name': r'VGirl',
        # },
        #
        # r'37': {
        #     r'name': r'Rosi',
        # },
        #
        # r'38': {
        #     r'name': r'Ru1mm',
        # },
        #
        # r'36': {
        #     r'name': r'Pans',
        # },
        #
        # r'43': {
        #     r'name': r'Sityle',
        # },
    }

#######################################################################################################

class Prot:
    def __init__(self, mb, pid, info):
        self.mb = mb
        self.pid = pid
        self.url = self.geturl(1)
        self.saveroot = os.path.join(mb[r'saveroot'], info[r'name'])
        self.pages = list()

    def geturl(self, idx):
        return a_tool.tjoinurl(self.mb[r'url'], (r'forum-%s' % self.pid) + (r'-%s.html' % idx))

    @staticmethod
    async def getpc(ctx):
        for node in t_xpath.xselects(ctx[r'xp'], r'//div[@class="pg"]//a[@class="last"]'):
            return int(re.search(r'(\d+)', t_xpath.xtext(node)).group(1))
        pidxs = list()
        for node in t_xpath.xselects(ctx[r'xp'], r'//div[@class="pg"]//a/text()'):
            if node.isnumeric():
                pidxs.append(int(node))
        if pidxs:
            return max(pidxs)
        return 1

    async def parse(self, ctx, _):
        pc = await self.getpc(ctx)
        self.pages = [self.geturl(i) for i in range(1, pc + 1)]

    def newtask(self, context):
        ctx = context.copy()
        ctx[r'url'] = self.url
        return a_http.htext(ctx, self.parse)

    @staticmethod
    def init(prots):
        async def routine(context):
            await a_tool.tmr(*[prot.newtask(context) for prot in prots])
        a_tool.tloop(a_http.hsession(routine))

#######################################################################################################

def plist(mb):
    # init all products.
    cfg = products()
    prots = [Prot(mb, pid, info) for pid, info in cfg.items()]
    Prot.init(prots)
    return prots

#######################################################################################################

def control(mb, beans, metas):
    dlist = list()
    for prot in plist(mb):
        for page in prot.pages:
            ibeans = a_tool.dc(beans)
            mainbean = mb[r'bean']
            ibeans[mainbean][r'meta.main'] = r'true'
            ibeans[mainbean][r'param.url'] = page
            ibeans[mainbean][r'cookie.saveroot'] = prot.saveroot
            dlist.append((ibeans, metas))

    for r in a_tool.mrmp(dlist, metas[mb[r'view']], 1):
        if not r:
            raise Exception(r'Error.')

    return True

#######################################################################################################
