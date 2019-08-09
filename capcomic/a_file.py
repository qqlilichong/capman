
#######################################################################################################

import aiofiles

#######################################################################################################

async def fset(filename, content, fmode=r'wb'):
    result = None
    try:
        if not filename:
            return

        if not content:
            return

        async with aiofiles.open(filename, mode=fmode) as f:
            result = await f.write(content)
    finally:
        return result

#######################################################################################################
