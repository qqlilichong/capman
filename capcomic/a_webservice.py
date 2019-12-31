
#######################################################################################################

import os
import subprocess
from aiohttp import web
from libcap import a_file

#######################################################################################################

async def a_findsnf(req):
    result = r'unknown error.'
    try:
        rootpath = r'D:/EMU'
        mamodel = r'^.*\.%s$' % req.query[r'key']

        fdict = dict()
        flist = [(os.path.basename(f).split(r'.')[0].lower(), f) for f in a_file.fmatch(rootpath, mamodel)]
        for name, file in flist:
            if name not in fdict.keys():
                fdict[name] = list()
            fdict[name].append(file)

        data = r''
        for fl in fdict.values():
            if len(fl) > 1:
                data += '%s\n' % str(fl)

        result = data
    finally:
        return web.Response(text=result)

#######################################################################################################

async def a_runbat(req):
    result = r'unknown error.'
    try:
        cmdline = req.query[r'key']
        result = subprocess.check_output(cmdline, shell=True).decode(r'gbk')
    finally:
        return web.Response(text=result)

#######################################################################################################

def mainbus():
    app = web.Application()
    app.router.add_get(r'/findsnf', a_findsnf)
    app.router.add_get(r'/runbat', a_runbat)
    web.run_app(app, host=r'0.0.0.0', port=8080)

#######################################################################################################

if __name__ == '__main__':
    mainbus()

#######################################################################################################
