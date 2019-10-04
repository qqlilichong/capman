
#######################################################################################################

import os
import asyncio
import aiohttp
from libcap import t_xpath, a_tool, a_file

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

async def wxpath(ctx, _):
    if r'text' in ctx:
        ctx[r'xp'] = t_xpath.xhtml(ctx[r'text'])
    elif r'content' in ctx:
        ctx[r'xp'] = t_xpath.xhtml(ctx[r'content'])
    else:
        raise Exception()
    return True

async def wgettext(ctx, r):
    ctx[r'text'] = await r.text()
    return True

async def wgetcontent(ctx, r):
    for h in [r'Content-Length', r'Content-Type']:
        if h in r.headers:
            ctx[h] = r.headers[h]
    ctx[r'content'] = await r.read()
    return True

async def wsavefile(ctx, _):
    clen = len(ctx[r'content'])
    if r'Content-Length' in ctx.keys():
        clen = int(ctx[r'Content-Length'])
    if not clen:
        raise Exception()
    if not await a_file.fmkd(os.path.dirname(ctx[r'file'])):
        raise Exception()
    flen = await a_file.fset(ctx[r'file'], ctx[r'content'])
    if not flen:
        raise Exception()
    if clen != flen:
        raise Exception()
    return True

#######################################################################################################

async def __hget(ctx, *workflow):
    try:
        async with ctx[r'semaphore']:
            async with ctx[r'session'].get(ctx[r'url'], headers=ctx[r'headers']) as r:
                ctx[r'status'] = r.status
                if ctx[r'status'] != ctx[r'okcode']:
                    raise Exception()

                for work in workflow:
                    ctx[r'workstack'] = work.__name__
                    if not await work(ctx, r):
                        break

                ctx[r'ok'] = True
    except:
        await ctx[r'except'](ctx)
    finally:
        return ctx

async def hget(ctx, *workflow):
    while True:
        await __hget(ctx, *workflow)
        if ctx[r'ok']:
            break
        if not ctx[r'retry']:
            break
    return ctx

async def hsave(ctx, *workflow):
    return await hget(ctx, wgetcontent, wsavefile, *workflow)

async def htext(ctx, *workflow):
    return await hget(ctx, wgettext, wxpath, *workflow)

async def hcontent(ctx, *workflow):
    return await hget(ctx, wgetcontent, wxpath, *workflow)

#######################################################################################################

async def __logbus(ctx, info, level=5):
    print(r'[%s]{%s}: %s' % (level, ctx[r'url'], info))

async def __exceptbus(ctx):
    await ctx[r'log'](ctx, ctx[r'workstack'])

def __request_headers():
    ua = r'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    ua += r' AppleWebKit/537.36 (KHTML, like Gecko)'
    ua += r' Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400'
    return {
        r'User-Agent': ua
    }

async def hsession(task, headers=None, sema=1000):
    if not headers:
        headers = __request_headers()
    async with aiohttp.ClientSession() as s:
        await task({
            r'session': s,
            r'semaphore': asyncio.Semaphore(sema),
            r'headers': headers,
            r'status': 0,
            r'okcode': 200,
            r'ok': False,
            r'retry': False,
            r'workstack': r'main',
            r'log': __logbus,
            r'except': __exceptbus,
        })

#######################################################################################################