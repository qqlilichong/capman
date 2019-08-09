
#######################################################################################################

import a_tool
import a_http

#######################################################################################################

async def exceptbus(_):
    print(r'Except...')

async def mainbus(context):
    context[r'url'] = r'https://image.suning.cn/public/v3/images/new-down-img.png?v=st0001'
    context[r'except'] = exceptbus

    c1 = dict()
    c1.update(context)
    c1[r'file'] = r'y:/abc1.png'

    c2 = dict()
    c2.update(context)
    c2[r'file'] = r'y:/abc2.png'

    for result in await a_tool.tmr(a_http.hsave(c1), a_http.hsave(c2)):
        print(result[r'url'], result[r'status'])

#######################################################################################################

if __name__ == '__main__':
    a_tool.tloop(a_http.hsession(mainbus))

#######################################################################################################
