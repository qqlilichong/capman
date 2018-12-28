
#######################################################################

import os
import json
import multiprocessing

import bs4
import requests
from urllib.parse import urljoin, urlparse

#######################################################################

def reducer(dlist, handler, maxps=32):
    result = None
    try:
        ps = len(dlist)
        if ps == 0:
            return

        if ps > maxps:
            ps = maxps

        ios = multiprocessing.Pool(ps)

        plist = list()
        for d in dlist:
            plist.append(ios.apply_async(handler, (d,)))

        ios.close()
        ios.join()

        rlist = list()
        for p in plist:
            rlist.append(p.get())

        result = rlist
    finally:
        return result

#######################################################################

def mkd(**kwargs):
    return kwargs

#######################################################################

def jdumps(**kwargs):
    result = None
    try:
        result = json.dumps(kwargs, ensure_ascii=False, indent=True)
    finally:
        return result

#######################################################################

def jloads(text):
    result = None
    try:
        result = json.loads(text)
    finally:
        return result

#######################################################################

def fmkdir(filename):
    result = None
    try:
        os.makedirs(filename, exist_ok=True)
        result = True
    finally:
        return result

#######################################################################

def fsize(filename):
    result = None
    try:
        result = os.path.getsize(filename)
    finally:
        return result

#######################################################################

def fexists(filename):
    result = None
    try:
        result = os.path.exists(filename)
    finally:
        return result

#######################################################################

def fremove(filename):
    result = None
    try:
        if not fexists(filename):
            return

        if os.path.isdir(filename):
            os.removedirs(filename)
        else:
            os.remove(filename)

        result = True
    finally:
        return result

#######################################################################

def fget(filename, fmode=r'rb'):
    result = None
    try:
        with open(filename, mode=fmode) as fh:
            result = fh.read()
    finally:
        return result

#######################################################################

def fset(filename, content, fmode=r'wb'):
    result = None
    try:
        with open(filename, mode=fmode) as fh:
            result = fh.write(content)
    finally:
        return result

#######################################################################

def http_get(url, headers=None):
    result = None
    try:
        def_headers = {
            r'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 '
                'QQBrowser/9.7.13021.400',
        }

        if not headers:
            headers = def_headers

        if url.startswith(r'//'):
            url = r'http:' + url

        resp = requests.get(url, timeout=30, headers=headers)
        if not resp.ok:
            return

        result = resp
    finally:
        return result

#######################################################################

def http_download(url, filename):
    result = None
    try:
        resp = http_get(url)
        if not resp:
            return

        len1 = int(resp.headers.get(r'content-length'))
        if not len1:
            return

        if len1 == 0:
            return

        len2 = len(resp.content)
        if len2 == 0:
            return

        if not fset(filename, resp.content):
            return

        if fsize(filename) != len2:
            return

        result = len2
    finally:
        if not result:
            fremove(filename)

        return result

#######################################################################

def http_urljoin(path, url):
    result = None
    try:
        result = urljoin(path, url)
    finally:
        return result

#######################################################################

def http_urlfpath(url):
    result = None
    try:
        meta = urlparse(url)
        result = url.replace(r'%s://%s' % (meta.scheme, meta.netloc), r'')
    finally:
        return result

#######################################################################

def bs4create(text, engine=r'html5lib'):
    result = None
    try:
        result = bs4.BeautifulSoup(text, engine)
    finally:
        return result

#######################################################################

def bs4get(url):
    result = None
    try:
        resp = http_get(url)
        if not resp:
            return

        result = bs4create(resp.text)
    finally:
        return result

#######################################################################
