
#######################################################################################################

import sys
import uuid
import hashlib
import asyncio
import inspect
from urllib.parse import urljoin

#######################################################################################################

async def tzf(data, width=3, inc=1):
    data = int(data) + inc
    return str(data).zfill(width)

#######################################################################################################

async def tuuid():
    result = None
    try:
        result = hashlib.sha1(str(uuid.uuid1()).encode()).hexdigest()
    finally:
        return result

#######################################################################################################

async def tjoinurl(url, path):
    result = None
    try:
        result = urljoin(url, path)
    finally:
        return result

#######################################################################################################

async def tmr(*tasks):
    taskqueue = list()
    for task in tasks:
        taskqueue.append(asyncio.create_task(task))
    return await asyncio.gather(*taskqueue)

#######################################################################################################

def tloop(task):
    if sys.platform == r'win32':
        asyncio.set_event_loop(asyncio.ProactorEventLoop())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    loop.run_until_complete(asyncio.sleep(1))

#######################################################################################################

def metatbl(tbl):
    return {
        r'%s.%s' % (tbl[r'__name__'], k): v for k, v in tbl.items()
        if not k.startswith(r'_') and (inspect.isfunction(v) or inspect.isclass(v))
    }

#######################################################################################################
