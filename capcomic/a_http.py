
#######################################################################################################

import asyncio
import aiohttp
import t_xpath
import a_tool
import a_file
import a_httpmr

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

async def wxpath(ctx, _):
    if r'xpath' not in ctx:
        return True

    if r'text' in ctx:
        ctx[r'xp'] = t_xpath.xhtml(ctx[r'text'])
    elif r'content' in ctx:
        ctx[r'xp'] = t_xpath.xhtml(ctx[r'content'])
    else:
        raise Exception()

    return await ctx[r'xpath'](ctx)

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
    clen = int(ctx[r'Content-Length'])
    if not clen:
        raise Exception()

    flen = await a_file.fset(ctx[r'file'], ctx[r'content'])
    if not flen:
        raise Exception()

    if clen != flen:
        raise Exception()

    return True

#######################################################################################################

async def hget(ctx, *workflow):
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

async def hsave(ctx):
    return await hget(ctx, wgetcontent, wsavefile)

async def htext(ctx):
    return await hget(ctx, wgettext, wxpath)

async def hcontent(ctx):
    return await hget(ctx, wgetcontent, wxpath)

#######################################################################################################

def hctx(context, **kwargs):
    ctx = dict()
    ctx.update(context)
    ctx.update(kwargs)
    return ctx

def hfarmer(cfg):
    return cfg[r'param.context'][r'meta'][cfg[r'meta.id']](cfg).task()

#######################################################################################################

async def __logbus(ctx, info, level=5):
    print(r'{%s}[%s]: %s' % (ctx[r'url'], level, info))

async def __exceptbus(ctx):
    await ctx[r'log'](ctx, ctx[r'workstack'])

def __request_headers():
    return {
        r'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400'
    }

def __meta():
    tbl = dict()
    tbl.update(meta())
    tbl.update(a_httpmr.meta())
    return tbl

async def hsession(task, headers=__request_headers(), sema=1000):
    async with aiohttp.ClientSession() as s:
        await task({
            r'meta': __meta(),
            r'session': s,
            r'semaphore': asyncio.Semaphore(sema),
            r'headers': headers,
            r'status': 0,
            r'okcode': 200,
            r'ok': False,
            r'workstack': r'hsession',
            r'log': __logbus,
            r'except': __exceptbus,
        })

#######################################################################################################
