
#######################################################################################################

import os
import re
import shutil
import aiofiles

#######################################################################################################

async def fget(file, fmode=r'rb'):
    result = None
    try:
        if not file:
            return

        async with aiofiles.open(file, mode=fmode) as f:
            result = await f.read()
    finally:
        return result

#######################################################################################################

async def fset(file, content, fmode=r'wb'):
    result = None
    try:
        if not file:
            return

        if not content:
            return

        async with aiofiles.open(file, mode=fmode) as f:
            result = await f.write(content)
    finally:
        return result

#######################################################################################################

async def fmkd(file):
    result = None
    try:
        os.makedirs(file, exist_ok=True)
        result = True
    finally:
        return result

#######################################################################################################

async def fsize(file):
    result = None
    try:
        if not os.path.isdir(file):
            result = os.path.getsize(file)
    finally:
        return result

#######################################################################################################

async def fexists(file):
    result = None
    try:
        result = os.path.exists(file)
    finally:
        return result

#######################################################################################################

async def frm(file):
    result = None
    try:
        if not await fexists(file):
            return

        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

        result = True
    finally:
        return result

#######################################################################################################

async def frmempty(path):
    result = list()
    try:
        while True:
            pl = [root for root, _, _ in os.walk(path) if not os.listdir(root)]
            if not pl:
                break

            for p in pl:
                os.rmdir(p)
                result.append(p)
    finally:
        return result

#######################################################################################################

async def fmatch(file, mode):
    result = None
    try:
        ma = re.compile(mode)
        fl = list()
        for filename in os.listdir(file):
            if ma.match(filename):
                fl.append(os.path.join(file, filename))

        result = fl
    finally:
        return result

#######################################################################################################
