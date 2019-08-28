
#######################################################################################################

import a_tool
import a_http

#######################################################################################################

async def mainbus(context):
    cfg = {
        r'meta.id': r'a_httpmr.RXP',
        r'param.context': context,
        r'param.url': r'https://gaoqing.fm/',
        r'param.select': r'//ul[@class="item-list nav"]/li',
        r'pin.id': r'img/@src',
        r'pin.text': r'div[@class="item-desc pull-left"]/p/a/text()',
    }

    for result in await a_tool.tmr(a_http.hfarmer(cfg)):
        print(result[r'url'])

#######################################################################################################

if __name__ == '__main__':
    a_tool.tloop(a_http.hsession(mainbus))

#######################################################################################################
