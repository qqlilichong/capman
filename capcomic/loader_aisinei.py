
#######################################################################

import os
import re
import time
import t_webtool as t

#######################################################################

def pagecount(total):
    ep = 20
    return int(int(total) / ep) + 1

#######################################################################

def subject(title):
    return re.match(r'(.*)\[.*\]', title)[1].strip()

#######################################################################

def mapper_image(params):
    def work():
        result = None
        try:
            if not t.http_download(params[r'url'], params[r'image']):
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

def mapper_detail(params):
    def work():
        result = None
        try:
            imgs = t.bs4get(params[r'url']).findAll(r'img')
            if not imgs:
                return

            # caper all images.
            imagelist = list()
            for img in imgs:
                if r'aid' in img.attrs:
                    imagelist.append(img[r'file'])
                    continue

                if r'title' in img.attrs:
                    imagelist.append(img[r'src'])
                    continue

            if not imagelist:
                return

            images = dict()
            index = 0
            for img in imagelist:
                images[img] = os.path.join(params[r'dst'], r'%s.jpg' % t.zf(index))
                index += 1

            result = images
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

def mapper_productpage(params):
    def work():
        result = None
        try:
            divs = t.bs4get(params[r'url']).findAll(r'div', r'bus_vtem')
            if not divs:
                return

            details = dict()
            for div in divs:
                link = div.a
                dst = os.path.join(params[r'dst'], subject(link[r'title']))

                # ignore exists detail.
                if not os.path.exists(dst):
                    details[link[r'href']] = dst
                    t.fmkdir(dst)

            result = details
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
    result = None
    try:
        url = params[r'url'] % 1
        bs = t.bs4get(url)
        if not bs:
            return

        # make product all pages.
        pagecnt = pagecount(bs.find(r'em', r'bus_num').get_text())
        pagelist = [params[r'url'] % i for i in range(1, pagecnt + 1)]

        # make product all details.
        pin = [{r'url': url, r'dst': params[r'dst']} for url in pagelist]
        details = dict()
        for data in t.reducer(pin, mapper_productpage):
            details.update(data)

        # make product detail images.
        pin = [{r'url': k, r'dst': v} for k, v in details.items()]
        images = dict()
        for data in t.reducer(pin, mapper_detail):
            images.update(data)

        # make product detail images.
        pin = [{r'url': k, r'image': v} for k, v in images.items()]
        t.reducer(pin, mapper_image)

        result = True
    finally:
        return result

#######################################################################

def productlist():
    result = list()

    k = r'Goddes头条女神'
    v = r'https://www.aisinei.org/forum-goddes-%s.html'
    result.append((k, v))

    k = r'TuiGirl推女郎'
    v = r'https://www.aisinei.org/forum-tuigirl-%s.html'
    result.append((k, v))

    return result

#######################################################################

def loader_main():
    k, v = productlist()[-1]

    params = dict()
    params[r'dst'] = r'D:/TOSHIBA/AISINEI/%s' % k
    params[r'url'] = v
    mapper_product(params)
    fail = t.rmempty(params[r'dst'])
    if fail:
        print(r'[Bad] : %s' % fail)

#######################################################################

if __name__ == "__main__":
    loader_main()
    print(r'Done.')

#######################################################################
