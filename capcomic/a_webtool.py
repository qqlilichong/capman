
#######################################################################################################

import a_tool
import a_http

#######################################################################################################

async def exceptbus(_):
    print(r'Except...')

async def mainbus(context):
    context[r'file'] = r'y:/abc.png'
    context[r'url'] = r'https://image.suning.cn/public/v3/images/new-down-img.png?v=st0001'
    context[r'except'] = exceptbus
    for result in await a_tool.tmr(a_http.hget(context, a_http.wgetcontent, a_http.wsavefile)):
        print(result[r'url'], result[r'status'])

#######################################################################################################

if __name__ == '__main__':
    a_tool.tloop(a_http.hsession(mainbus))

#######################################################################################################
