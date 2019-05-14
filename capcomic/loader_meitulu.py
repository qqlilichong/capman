
#######################################################################

import os
import time
import t_webtool as t

#######################################################################

def query_pgs(url):
    result = None
    try:
        data = [url]
        for x in t.exp(url).xpath(r'//*[@class = "pg"]//a[not(@class)]/@href'):
            data.append(t.http_urljoin(url, x))

        result = data
    finally:
        return result

#######################################################################

def query_pg_images(url):
    result = None
    try:
        data = list()
        for x in t.exp(url).xpath(r'//*[@class = "adw"]//img/@src'):
            data.append(t.http_urljoin(url, x))

        result = data
    finally:
        return result

#######################################################################

def query_product_page(url, dst):
    result = None
    try:
        threadinfos = dict()
        for group in t.exp(url, r'utf-8').xpath(r'//*[@class = "group"]'):
            link = group.xpath(r'.//*[@class = "bution"]//a')[0]
            threadurl = t.http_urljoin(url, t.expa(link, r'href'))
            thread = dict()
            thread[r'cover'] = t.exps(group.xpath(r'.//*[@class = "photo"]//img/@src'))
            thread[r'url'] = threadurl
            thread[r'subject'] = t.expt(link)
            thread[r'dst'] = dst
            for v in thread.values():
                if not v:
                    return
            threadinfos[threadurl] = thread

        result = threadinfos
    finally:
        return result

#######################################################################

def mapper_pg(params):
    def work():
        result = None
        try:
            # ignore exist thread.
            dst = os.path.join(params[r'dst'], params[r'subject'])
            if os.path.exists(dst):
                result = dict()
                return

            pgs = query_pgs(params[r'url'])
            if not pgs:
                return

            pginfos = dict()
            index = 0
            for pgurl in pgs:
                pginfo = dict()
                pginfo[r'url'] = pgurl
                pginfo[r'dst'] = dst
                pginfo[r'cover'] = params[r'cover']
                pginfo[r'pidx'] = t.zf(index)
                pginfos[pgurl] = pginfo
                index += 1

            t.fmkdir(dst)
            result = pginfos
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % params[r'url'])
                time.sleep(1)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def fiximg(url):
    data = [i for i in url.split(r'.jpg') if i]
    if len(data) != 1:
        url = data[0] + r'.jpg'

    url = url.replace(r'<br />', r'')
    url = url.replace(r'1178//', r'1178/T/')
    url = url.replace('\r\n', r'')
    url = url.replace('\n', r'')
    if url.endswith(r'/'):
        return None
    return url

def mapper_img(params):
    def work():
        result = None
        try:
            images = query_pg_images(params[r'url'])
            if not images:
                return

            imginfos = dict()

            # cover image.
            cover = dict()
            cover[r'url'] = params[r'cover']
            cover[r'dst'] = os.path.join(params[r'dst'], r'cover.jpg')
            imginfos[cover[r'url']] = cover

            # content images.
            index = 0
            for img in images:
                img = fiximg(img)
                if not img:
                    continue

                imginfo = dict()
                imginfo[r'url'] = img
                imginfo[r'dst'] = os.path.join(params[r'dst'],
                                               r'%s-%s.jpg' % (params[r'pidx'], t.zf(index)))
                imginfos[img] = imginfo
                index += 1

            result = imginfos
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % params[r'url'])
                time.sleep(1)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def mapper_get(params):
    def work():
        result = None
        try:
            ig = False

            def onerr(resp):
                if resp.status_code == 500:
                    nonlocal ig
                    ig = True

            if not t.http_download(params[r'url'], params[r'dst'],
                                   None,
                                   onerr):
                if ig:
                    result = True
                    print(r'[IGNORE] : %s.' % params[r'url'])
                return

            result = True
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % params[r'url'])
                time.sleep(1)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def mapper_product(params):
    def work():
        result = None
        try:
            result = query_product_page(params[r'url'], params[r'dst'])
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % params[r'url'])
                time.sleep(1)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def get(base, dst):
    productplist = list()
    pcount = t.exps(t.exp(base % r'1').xpath(r'//*[@class = "last"]/text()')).replace(r'.', r'')
    for i in range(1, int(pcount) + 1):
        params = dict()
        params[r'dst'] = dst
        params[r'url'] = base % i
        productplist.append(params)

    threadinfos = dict()
    for data in t.reducer(productplist, mapper_product):
        threadinfos.update(data)

    pginfos = dict()
    for data in t.reducer(threadinfos.values(), mapper_pg):
        pginfos.update(data)

    imginfos = dict()
    for data in t.reducer(pginfos.values(), mapper_img):
        imginfos.update(data)

    t.reducer(imginfos.values(), mapper_get)
    return True

#######################################################################

def productlist():
    result = list()

    k = r'头条女神 Goddes'
    v = r'https://www.lsm.me/forum-109-%s.html'
    result.append((k, v))

    return result

def loader_main():
    for k, v in productlist():
        print(r'[PRODUCT] : %s' % k)
        dst = r'D:/TOSHIBA/[套图]蕾丝猫/%s' % k
        get(v, dst)
        fail = t.rmempty(dst)
        if fail:
            print(r'[Bad] : %s' % fail)

#######################################################################

if __name__ == "__main__":
    loader_main()
    print('bye...')

#######################################################################
