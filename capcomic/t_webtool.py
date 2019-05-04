
#######################################################################

import re
import os
import json
import uuid
import base64
import hashlib
import multiprocessing
import configparser

import bs4
import requests
from urllib.parse import urljoin

#######################################################################

def zf(data, width=3, inc=1):
    data = int(data) + inc
    return str(data).zfill(width)

#######################################################################

def mkid():
    result = None
    try:
        result = hashlib.sha1(str(uuid.uuid1()).encode()).hexdigest()
    finally:
        return result

#######################################################################

def reducer(dlist, handler, maxps=32):
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

def flist(filename, fi):
    result = None
    try:
        files = list()
        dirname = os.path.dirname(filename)
        for file in os.listdir(dirname):
            if file.endswith(fi):
                files.append(os.path.join(dirname, file))

        result = files
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

def rmempty(path):
    def work():
        r = []
        for root, dirs, files in os.walk(path):
            if not os.listdir(root):
                r.append(root)
        return r

    result = list()
    while True:
        data = work()
        if not data:
            break

        for d in data:
            result.append(d)
            os.rmdir(d)

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

def http_get(url, headers=None, err=None):
    result = None
    try:
        def_headers = {
            r'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 '
                'QQBrowser/9.7.13021.400',
        }

        if headers:
            def_headers.update(headers)

        resp = requests.get(url, timeout=30, headers=def_headers)
        if not resp.ok:
            if err:
                err(resp)
            return

        result = resp
    finally:
        return result

#######################################################################

def http_download(url, filename, headers=None, err=None):
    result = None
    try:
        if url.startswith(r'data:'):
            result = fset(filename, base64.b64decode(url.split(r',')[1]))
            return

        resp = http_get(url, headers, err)
        if not resp:
            return

        len1 = int(resp.headers.get(r'content-length'))
        if not len1:
            result = 0
            return

        len2 = len(resp.content)
        if not len2:
            return

        if len1 != len2:
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
        resp.encoding = requests.utils.get_encodings_from_content(resp.text)[0]
        result = bs4create(resp.text)
    finally:
        return result

#######################################################################

class IniDict:
    def __init__(self, enc=r'utf-8'):
        self.__data = dict()
        self.__enc = enc

    def __getitem__(self, item):
        result = None
        try:
            result = self.__data[item]
        finally:
            return result

    def read(self, filename):
        result = None
        try:
            cfg = configparser.ConfigParser()
            cfg.read(filename, encoding=self.__enc)
            result = self.__update(cfg)
        finally:
            return result

    def __update(self, cfg):
        result = None
        try:
            self.__data = {section: None for section in cfg.sections()}
            for key in self.__data.keys():
                self.__data[key] = {k: v for k, v in cfg.items(key)}

            result = self.__data
        finally:
            return result

    def resection(self, ma):
        result = None
        try:
            data = dict()
            for key in self.__data.keys():
                m = re.match(ma, key)
                if m:
                    data[key] = m

            result = data
        finally:
            return result

#######################################################################
