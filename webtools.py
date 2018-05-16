
######################################################
# Import modules.
import os
import requests
import urllib.parse
import multiprocessing

######################################################
# HTTP settings.
HEADERS_UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 ' \
             'QQBrowser/9.7.13021.400'

HTTP_PROXY = {
    'http': '192.168.200.1:1080',
    'https': '192.168.200.1:1080',

    # 'http': '127.0.0.1:1080',
    # 'https': '127.0.0.1:1080',
}

######################################################
# HTTP GET.
def http_get(url):
    try:
        return requests.get(
            url,
            headers={
                'User-Agent': HEADERS_UA,
            },
            proxies=HTTP_PROXY,
            timeout=30,
        )
    except:
        return None

######################################################
# HTTP GET and save content.
def http_download(url, filename):
    try:
        resp = http_get(url)
        if resp:
            with open(filename, 'wb') as file:
                file.write(resp.content)
                return True

    except:
        if os.path.exists(filename):
            os.remove(filename)

    return None

######################################################
# Join URL.
def http_urljoin(path, url):
    return urllib.parse.urljoin(path, url)

######################################################
# Reducer with multiprocessing.
def reactor_reduce(dlist, handler, ps=32):
    result = []
    if len(dlist) == 0:
        return result

    ios = multiprocessing.Pool(ps)
    pres = []
    for d in dlist:
        pres.append(ios.apply_async(handler, (d,)))

    ios.close()
    ios.join()

    for p in pres:
        r = p.get()
        if r:
            result.append(r)

    return result

######################################################
