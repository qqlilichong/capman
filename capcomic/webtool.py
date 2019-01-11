
#######################################################################

import re
import os
import json
import base64
import multiprocessing
import configparser

import bs4
import requests
from urllib.parse import urljoin

#######################################################################

def reducer(dlist, handler, maxps=32):
    result = None
    try:
        ps = len(dlist)
        if not ps:
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
        if url.startswith(r'data:'):
            result = fset(filename, base64.b64decode(url.split(r',')[1]))
            return

        resp = http_get(url)
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
        result = bs4create(http_get(url).text)
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
