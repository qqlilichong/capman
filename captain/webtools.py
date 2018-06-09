
######################################################

import bs4
import requests
import urllib.parse
from .mantools import *

######################################################

HTTP_HUA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
           'AppleWebKit/537.36 (KHTML, like Gecko) ' \
           'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 ' \
           'QQBrowser/9.7.13021.400'

HTTP_PROXY = {
    # 'http': '192.168.200.1:1080',
    # 'https': '192.168.200.1:1080',

    # 'http': '127.0.0.1:1080',
    # 'https': '127.0.0.1:1080',
}

######################################################

def http_get(url):
    result = None

    try:
        resp = requests.get(
            url,
            headers={'User-Agent': HTTP_HUA},
            timeout=30,
            # proxies=HTTP_PROXY,
        )

        if not resp.ok:
            return

        result = resp
        return

    finally:
        return result

######################################################

def http_download(url, filename):
    result = None

    try:
        resp = http_get(url)
        if not resp:
            return

        fs = resp.headers.get('content-length')
        if not fs:
            return

        fs = int(fs)
        if fs == 0:
            return

        if not file_create(filename, resp.content):
            return

        if file_size(filename) != fs:
            return

        result = True
        return

    finally:
        if not result:
            file_remove(filename)

        return result

######################################################

def http_urljoin(path, url):
    result = None

    try:
        result = urllib.parse.urljoin(path, url)

    finally:
        return result

######################################################

def bscreator(text):
    result = None

    try:
        result = bs4.BeautifulSoup(text, 'html5lib')

    finally:
        return result

######################################################

def bsget(url):
    result = None

    try:
        resp = http_get(url)
        if not resp:
            return

        result = bscreator(resp.text)
        return

    finally:
        return result

######################################################
