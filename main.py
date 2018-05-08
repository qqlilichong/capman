
######################################################

import re
import requests
from bs4 import BeautifulSoup

######################################################


HEADERS_UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 ' \
             'QQBrowser/9.7.13021.400'

HTTP_PROXY = {
    'http': '192.168.200.1:1080',
    'https': '192.168.200.1:1080',
}


######################################################


def http_get(url):
    return requests.get(
        url,
        headers={
            'User-Agent': HEADERS_UA,
        },
        #proxies=HTTP_PROXY,
    )


def http_download(url, filename):
    resp = http_get(url)
    if not resp:
        return False

    with open(filename, 'wb') as file:
        for chunk in resp.iter_content(1024 * 64):
            file.write(chunk)
    return True


######################################################


img_templ = 'https://upload-images.jianshu.io/upload_images/%s?imageMogr2/auto-orient/strip|imageView2/2/w/700'
html = http_get('https://www.jianshu.com/p/3d1eb40187ad')
bsObj = BeautifulSoup(html.text, 'html5lib')
for item in bsObj.findAll('div', {'class': 'image-view'}):
    img = item.find('img')
    if not img:
        continue

    img_name = re.search('//upload-images.jianshu.io/upload_images/(.*)$', img['data-original-src'])
    if not img_name:
        continue

    print(img_name.group(1))


######################################################
