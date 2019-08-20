
#######################################################################################################

import a_tool
import a_http
import a_file

#######################################################################################################

async def exceptbus(_):
    print(r'Except...')

async def xpathbus(_):
    return True

async def mainbus(context):
    context[r'except'] = exceptbus

    c1 = dict()
    c1.update(context)
    c1[r'url'] = r'https://image.suning.cn/public/v3/images/new-down-img.png?v=st0001'
    c1[r'file'] = r'y:/abc1.png'

    c2 = dict()
    c2[r'url'] = r'https://gaoqing.fm/'
    c2[r'xpath'] = xpathbus
    c2.update(context)

    for result in await a_tool.tmr(a_http.hcontent(c2)):
        print(result[r'url'])

#######################################################################################################

if __name__ == '__main__':
    a_tool.tloop(a_http.hsession(mainbus))

#######################################################################################################
