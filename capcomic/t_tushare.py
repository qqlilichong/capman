
#######################################################################

import tushare as ts

#######################################################################

def __newts():
    return ts.pro_api(r'51d04c570c7dc69b069b60e0d3f45816045498689318d85090ba89aa')

#######################################################################

def qcodes(ex):
    result = None
    try:
        codes = list()
        for info in __newts().stock_basic(exchange=ex, list_status='L', fields='symbol').values:
            codes.append(info[0])

        result = codes
    finally:
        return result

#######################################################################

def codes_sh():
    return qcodes(r'SSE')

def codes_sz():
    return qcodes(r'SZSE')

def codes_hs():
    return codes_sh() + codes_sz()

#######################################################################
