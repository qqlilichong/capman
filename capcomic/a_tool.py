
#######################################################################################################

import sys
import asyncio

#######################################################################################################

def tloop(task):
    if sys.platform == r'win32':
        asyncio.set_event_loop(asyncio.ProactorEventLoop())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    loop.run_until_complete(asyncio.sleep(1))
    loop.close()

#######################################################################################################

async def tmr(*tasks):
    taskqueue = list()
    for task in tasks:
        taskqueue.append(asyncio.create_task(task))
    return await asyncio.gather(*taskqueue)

#######################################################################################################
