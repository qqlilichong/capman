
#######################################################################

import re
import t_webtool
import t_dbe
import t_tushare

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
            info = t_webtool.http_get(r'http://data.eastmoney.com/stockdata/%s.html' % sid)
            info.encoding = r'gbk'
            info = info.text

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
        price = self.__vak(info, r'defaultKdata', r'c')
        if price == r'-':
            price = r'0'

        vol = self.__vak(info, r'defaultKdata', r'a')
        if vol == r'-':
            vol = r'0'

        hy = r'-'
        stock = self.__vad(info, r'stock')
        if r'hyName' in stock.keys():
            hy = r'%s(%s-%s)' % (stock[r'hyName'], stock[r'hyCode'], stock[r'hyCodeInt'])

        return t_webtool.mkd(
            ID=self.__vak(info, r'defaultKdata', r'code'),
            NAME=self.__vak(info, r'defaultKdata', r'name'),
            PRICE=price.zfill(7),
            VOL=r'%.2f' % (float(vol) / 10000),
            HY=hy,
        )

    def hyzb(self, info):
        data = dict()
        if not self.__vabase(info, r'hypmDatainfo'):
            return data

        data = t_webtool.mkd(
            PROFIT=self.__vak(info, r'cwzyData', r'retainedProfits'),
            PERATION=self.__vak(info, r'hypmDatainfo', r'PE9'),
            PBRATION=self.__vak(info, r'hypmDatainfo', r'PB8'),
            ROE=self.__vak(info, r'hypmDatainfo', r'ROE'),
        )

        if data[r'PROFIT'] and data[r'PROFIT'] != r'-':
            data[r'PROFIT'] = '%.2f' % (float(data[r'PROFIT']) / 10000)

        return data

    def cwzb(self, info):
        data = self.__var(info, r'cwzbData')
        for k, v in data.items():
            if v:
                data[k] = '%.3f' % float(v)
            else:
                data[k] = r'-'

        data[r'NETSHARE'] = '%.2f' % (float(data[r'NETSHARE']) / 10000)
        data[r'TOTALSHARE'] = '%.2f' % (float(data[r'TOTALSHARE']) / 10000)
        return data

    def zdgz(self, info):
        data = dict()
        if not self.__vabase(info, r'zdgzData'):
            return data

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
        data[r'NETVAL'] = data[r'NETVAL'].zfill(8)
        data[r'TOTALVAL'] = '%.2f' % (pr * ts)
        data[r'TOTALVAL'] = data[r'TOTALVAL'].zfill(8)
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
            HY=r'1.5~行业名称',

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
    def __vabase(txt, val):
        return re.findall(r'var %s\s*=\s*(.*)' % val, txt)

    @staticmethod
    def __va(txt, val):
        result = StockModel.__vabase(txt, val)
        return result[0]

    @staticmethod
    def __vars(txt, val):
        result = StockModel.__va(txt, val)
        result = result.replace(r';', r'')
        return eval(result)

    @staticmethod
    def __var(txt, val):
        result = StockModel.__vars(txt, val)
        return result[0]

    @staticmethod
    def __vaks(txt, val, key):
        result = StockModel.__va(txt, val)
        result = result.replace(r'"', r'')
        return re.findall(r'\W+%s\s*:\s*([\*\-\w]+|[-+]?[0-9]*\.?[0-9]+),' % key, result)

    @staticmethod
    def __vak(txt, val, key):
        result = StockModel.__vaks(txt, val, key)
        return result[0]

    @staticmethod
    def __vad(txt, key):
        txt = re.findall(r'var %s\s*=\s*(.*?);' % key, txt, re.MULTILINE | re.DOTALL)[0]
        return {cc[0].strip(): cc[1].strip()
                for cc in re.findall(r'(\w+)\s*:\s*"(\w+)"', txt, re.MULTILINE | re.DOTALL)}

    def dbmodel(self):
        result = None
        try:
            dbmodel = dict()
            dbmodel.update(self.__model[r'_jbxx_'])
            dbmodel.update(self.__model[r'_hyzb_'])
            dbmodel.update(self.__model[r'_cwzb_'])
            dbmodel.update(self.__model[r'_qtzb_'])
            dbmodel[r'zdgz'] = t_webtool.jdumps(**self.__model[r'_zdgz_'])
            dbmodel[r'hxtc'] = t_webtool.jdumps(**self.__model[r'_hxtc_'])
            result = dbmodel
        finally:
            return result

#######################################################################

def __mapper_collect(param):
    def work():
        result = None
        try:
            dbs = t_dbe.DBEngine()
            if not dbs.connect(**param[r'dbinfo']):
                print(r'[ERROR] : DBEngine.')
                return

            print(r'[COLLECT] : %s' % param[r'code'])
            dbmodel = StockModel(param[r'code']).dbmodel()
            dbs.replace(r'detail', **dbmodel)
            dbs.commit()

            result = True
        finally:
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def start_collect(dbinfo):
    t_webtool.reducer([{r'code': code, r'dbinfo': dbinfo} for code in t_tushare.codes_hs()],
                      __mapper_collect, 16)

#######################################################################
