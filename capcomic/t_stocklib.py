
#######################################################################

import re
import t_webtool

#######################################################################

class StockModel:
    def __init__(self, sid):
        self.__model = None
        self.__load(sid)

    def __str__(self):
        result = '\n***********************************\n'
        try:
            for k, v in self.__trand(self.__model).items():
                result += '\n[%s]\n' % k
                for ppk, ppv in self.__trand(v).items():
                    result += '%s = "%s"\n' % (ppk, ppv)
        finally:
            result += '\n***********************************\n'
            return result

    def __load(self, sid):
        result = None
        try:
            model = dict()
            info = t_webtool.bs4get(r'http://data.eastmoney.com/stockdata/%s.html' % sid).text

            # 基本信息
            model[r'_jbxx_'] = self.jbxx(info)

            # 行业指标
            model[r'_hyzb_'] = self.hyzb(info)

            # 财务指标
            model[r'_cwzb_'] = self.cwzb(info)

            # 重点关注
            model[r'_zdgz_'] = self.zdgz(info)

            # 核心题材
            model[r'_hxtc_'] = self.hxtc(info)

            # 其他指标
            model[r'_qtzb_'] = self.qtzb(model)

            self.__model = model
            result = True
        finally:
            return result

    def jbxx(self, info):
        data = t_webtool.mkd(
            ID=self.__vak(info, r'hypmData', r'Code'),
            NAME=self.__vak(info, r'hypmData', r'Name'),
            PRICE=self.__var(info, r'gdzjcData')[r'Close'],
            VOL=r'%.2f' % (float(self.__vak(info, r'defaultKdata', r'a')) / 10000),
        )
        return data

    def hyzb(self, info):
        data = t_webtool.mkd(
            PROFIT=self.__vak(info, r'hypmData', r'Profit'),
            PERATION=self.__vak(info, r'hypmData', r'PERation'),
            PBRATION=self.__vak(info, r'hypmData', r'PBRation'),
            ROE=self.__vak(info, r'hypmData', r'ROE'),
        )

        data[r'PROFIT'] = '%.2f' % (float(data[r'PROFIT']) / 100000000)
        return data

    def cwzb(self, info):
        data = self.__var(info, r'cwzbData')
        for k, v in data.items():
            data[k] = '%.3f' % float(v)

        data[r'NETSHARE'] = '%.2f' % (float(data[r'NETSHARE']) / 10000)
        data[r'TOTALSHARE'] = '%.2f' % (float(data[r'TOTALSHARE']) / 10000)
        return data

    def zdgz(self, info):
        data = dict()
        for d in self.__vars(info, r'zdgzData'):
            data[r'%s(%s)' % (d[r'rq'].split(r'T')[0], t_webtool.mkid()[:4])] = r'%s : %s' % (d[r'sjlx'], d[r'sjms'])
        return data

    def hxtc(self, info):
        data = dict()
        for d in self.__vars(info, r'hxtxData'):
            data[r'(%s)[%s]' % (d[r'MainPoint'].zfill(4), d[r'KeyWords'])] = d[r'MainPointCon']
        return data

    @staticmethod
    def qtzb(model):
        pr = float(model[r'_jbxx_'][r'PRICE'])
        ns = float(model[r'_cwzb_'][r'NETSHARE'])
        ts = float(model[r'_cwzb_'][r'TOTALSHARE'])
        data = dict()
        data[r'NETVAL'] = '%.2f' % (pr * ns)
        data[r'TOTALVAL'] = '%.2f' % (pr * ts)
        return data

    @staticmethod
    def __trand(d):
        return dict(sorted({StockModel.__trans(k): v for k, v in d.items()}.items()))

    @staticmethod
    def __trans(key):
        data = t_webtool.mkd(
            _jbxx_=r'1.基本信息',
            ID=r'1.1~股票代码',
            NAME=r'1.2~股票名称',
            PRICE=r'1.3~股票价格(元)',
            VOL=r'1.4~成交量(万元)',

            _hyzb_=r'2.行业指标',
            PERATION=r'2.1~市盈率',
            PBRATION=r'2.2~市净率',
            PROFIT=r'2.3~净利润(亿)',
            ROE=r'2.4~ROE(%)',

            _cwzb_=r'3.财务指标',
            DRIEPA=r'3.1~每股净资产(元)',
            DRIEPS=r'3.2~基本每股收益(元)',
            PROPERCASH=r'3.3~每股现金流(元)',
            DRPCAPRES=r'3.4~每股公积金(元)',
            NETSHARE=r'3.5~流通股本(亿股)',
            TOTALSHARE=r'3.6~总股本(亿股)',

            _qtzb_=r'4.其他指标',
            NETVAL=r'4.1~流通市值(亿)',
            TOTALVAL=r'4.2~总市值(亿)',

            _zdgz_=r'5.重点关注',

            _hxtc_=r'6.核心题材'
        )

        if key not in data.keys():
            return key

        return data[key]

    @staticmethod
    def __va(txt, val):
        return re.findall(r'var %s\s*=\s*(.*);' % val, txt)[0]

    @staticmethod
    def __vars(txt, val):
        return eval(StockModel.__va(txt, val))

    @staticmethod
    def __var(txt, val):
        return StockModel.__vars(txt, val)[0]

    @staticmethod
    def __vaks(txt, val, key):
        return re.findall(r'"%s"\s*:\s*"(.*?)"' % key, StockModel.__va(txt, val))

    @staticmethod
    def __vak(txt, val, key):
        return StockModel.__vaks(txt, val, key)[0]

#######################################################################

def start_collect():
    st = StockModel(r'601186')
    print(st)

#######################################################################
