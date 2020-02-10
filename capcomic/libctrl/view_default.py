
#######################################################################################################

from libcap import a_http, a_httpmr, a_tool

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def view(param):
    beans, metas, cmap = param

    async def caper(context):
        await a_httpmr.farm(context, beans, metas)

    a_tool.tloop(a_http.hsession(caper,
                                 sema=cmap[r'sema'],
                                 hgetb=cmap[r'hgetb']))
    return beans

#######################################################################################################
