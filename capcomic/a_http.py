
#######################################################################################################

import asyncio
import aiohttp
import a_file
import t_xpath

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
                if r.status != 200:
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

def __request_headers():
    return {
        r'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400'
    }

async def hsession(task, headers=__request_headers(), sema=1000):
    async with aiohttp.ClientSession() as s:
        await task({
            r'status': 0,
            r'session': s,
            r'headers': headers,
            r'semaphore': asyncio.Semaphore(sema),
        })

#######################################################################################################
