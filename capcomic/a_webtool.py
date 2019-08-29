
#######################################################################################################

import a_tool
import a_http

#######################################################################################################

async def mainbus(context):
    c1 = {
        r'meta.id': r'a_httpmr.FarmerXP',
        r'param.context': context,
        r'param.url': r'https://www.1905.com/vod/',
        r'param.select': r'//section[@id="rthk"]//a[@class="pic-pack-outer"]',
        r'pin.id': r'img/@src',
        r'pin.text': r'h3/text()',
    }

    c2 = {
        r'meta.id': r'a_httpmr.FarmerFile',
        r'param.context': context,
        r'param.file': r'g:/sf|<param.name>|<param.name>.jpg',
        r'param.name': r'hehe',
        r'param.url': r'https://www.runoob.com/wp-content/uploads/2015/01/cpp-mini-logo.png',
    }

    for result in await a_tool.tmr(a_http.hfarmer(c1), a_http.hfarmer(c2)):
        print(result[r'farmer'].pin)

#######################################################################################################

if __name__ == '__main__':
    a_tool.tloop(a_http.hsession(mainbus))

#######################################################################################################
