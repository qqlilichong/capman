
#######################################################################################################

import os
import asyncio
import aiohttp
from libcap import t_xpath, a_tool, a_file
from fake_useragent import UserAgent

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
    if not a_file.fmkd(os.path.dirname(ctx[r'file'])):
        raise Exception()
    flen = await a_file.fset(ctx[r'file'], ctx[r'content'])
    if not flen:
        raise Exception()
    if clen != flen:
        raise Exception()
    return True

#######################################################################################################

# async def __hget(ctx, *workflow):
#     try:
#         async with ctx[r'semaphore']:
#             await ctx[r'hgetb'](ctx)
#             async with ctx[r'session'].get(ctx[r'url'],
#                                            headers=ctx[r'headers'],
#                                            timeout=ctx[r'timeout'],
#                                            verify_ssl=False) as r:
#                 ctx[r'status'] = r.status
#                 if ctx[r'status'] != ctx[r'okcode']:
#                     raise Exception()
#
#                 for work in workflow:
#                     ctx[r'workstack'] = work.__name__
#                     if not await work(ctx, r):
#                         break
#
#                 ctx[r'ok'] = True
#     except:
#         await ctx[r'except'](ctx)
#     finally:
#         return ctx

async def __hget(ctx, *workflow):
    async with ctx[r'semaphore']:
        await ctx[r'hgetb'](ctx)
        async with ctx[r'session'].get(ctx[r'url'],
                                       headers=ctx[r'headers'],
                                       timeout=ctx[r'timeout'],
                                       verify_ssl=False) as r:
            ctx[r'status'] = r.status
            if ctx[r'status'] != ctx[r'okcode']:
                raise Exception()

            for work in workflow:
                ctx[r'workstack'] = work.__name__
                if not await work(ctx, r):
                    break

            ctx[r'ok'] = True
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

async def hnull(ctx):
    return ctx

#######################################################################################################

async def __logbus(ctx, info, level=5):
    print(r'[%s][%s]{%s}: %s' % (level, ctx[r'status'], ctx[r'url'], info))

async def __exceptbus(ctx):
    await ctx[r'log'](ctx, ctx[r'workstack'])

async def __hgetb(_):
    pass

async def hsession(task,
                   headers=None,
                   timeout=None,
                   sema=32,
                   hgetb=None):
    # Default params.
    if not headers:
        headers = {r'User-Agent': str(UserAgent(use_cache_server=False,
                                                verify_ssl=False,
                                                path=r'fake_useragent.json').random)}
    if not timeout:
        timeout = aiohttp.ClientTimeout(total=20)
    if not hgetb:
        hgetb = __hgetb

    # Start session.
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as s:
        await task({
            r'session': s,
            r'semaphore': asyncio.Semaphore(sema),
            r'headers': headers,
            r'timeout': timeout,
            r'status': 0,
            r'okcode': 200,
            r'ok': False,
            r'retry': False,
            r'workstack': r'main',
            r'log': __logbus,
            r'except': __exceptbus,
            r'hgetb': hgetb,
        })

#######################################################################################################
