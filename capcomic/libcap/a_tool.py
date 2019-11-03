
#######################################################################################################

import uuid
import copy
import shelve
import hashlib
import asyncio
import inspect
import multiprocessing
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

#######################################################################################################

async def tmr(*tasks):
    taskqueue = list()
    for task in tasks:
        taskqueue.append(asyncio.create_task(task))
    return await asyncio.gather(*taskqueue)

#######################################################################################################

def tloop(task):
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

def tzf(data, width=3, inc=1):
    data = int(data) + inc
    return str(data).zfill(width)

#######################################################################################################

def tuuid():
    result = None
    try:
        result = hashlib.sha1(str(uuid.uuid1()).encode()).hexdigest()
    finally:
        return result

#######################################################################################################

def tjoinurl(url, path):
    result = None
    try:
        result = urljoin(url, path)
    finally:
        return result

#######################################################################################################

def fixpath(path):
    path = path.replace('\\', '/')
    path = path.replace(r'..', r'')
    path = path.replace(r'./', r'/')
    psp = path.split(r':/')
    if len(psp) == 2:
        pl = list()
        for s in psp[1].split(r'/'):
            for i in (r':', r'*', r'?', r'"', r'<', r'>', r'|'):
                s = s.replace(i, r'')
            pl.append(s)
        path = r'%s:/%s' % (psp[0], r'/'.join(pl))
    path = path.strip()
    path = path.strip(r'.')
    path = path.strip()
    return path

#######################################################################################################

def dc(obj):
    return copy.deepcopy(obj)

#######################################################################################################

def mrmt(dlist, handler, maxps=32):
    result = None
    try:
        ps = len(dlist)
        if not ps:
            result = []
            return

        if ps > maxps:
            ps = maxps

        with ThreadPoolExecutor(max_workers=ps) as ios:
            plist = [ios.submit(handler, d) for d in dlist]
            wait(plist, return_when=ALL_COMPLETED)
            result = [p.result() for p in plist]
    finally:
        return result

#######################################################################################################

def mrmp(dlist, handler, maxps=32):
    result = None
    try:
        ps = len(dlist)
        if not ps:
            result = []
            return

        if ps > maxps:
            ps = maxps

        ios = multiprocessing.Pool(ps)
        plist = [ios.apply_async(handler, (d,)) for d in dlist]
        ios.close()
        ios.join()
        result = [p.get() for p in plist]
    finally:
        return result

#######################################################################################################

def dbsave(datafile, key, value):
    result = None
    try:
        db = shelve.open(datafile, writeback=True)
        db[key] = value
        db.close()
        result = True
    finally:
        return result

#######################################################################################################

def dbload(datafile, key):
    result = None
    try:
        db = shelve.open(datafile)
        result = db[key].copy()
        db.close()
    finally:
        return result

#######################################################################################################
