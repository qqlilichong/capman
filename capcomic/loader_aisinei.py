
#######################################################################

import os
import re
import t_webtool as t

#######################################################################

def pagecount(total):
    ep = 20
    return int(int(total) / ep) + 1

#######################################################################

def subject(title):
    title = re.match(r'(.*)\[.*\]', title)[1]
    title = title.strip()
    return title

#######################################################################

def mapper_image(params):
    def work():
        result = None
        try:
            result = t.http_download(params[r'url'], params[r'image'])
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % params[r'url'])
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
            bs = t.bs4get(params[r'url'])
            if not bs:
                return

            # caper all images.
            images = dict()
            for img in bs.findAll(r'img'):
                if r'aid' not in img.attrs:
                    continue
                images[img[r'file']] = os.path.join(params[r'dst'], img[r'aid'] + r'.jpg')

            result = images
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % params[r'url'])
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
            bs = t.bs4get(params[r'url'])
            if not bs:
                return

            details = dict()
            for div in bs.findAll(r'div', r'bus_vtem'):
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

def loader_main():
    params = dict()
    params[r'url'] = r'https://www.aisinei.org/forum-xiuren-%s.html'
    params[r'dst'] = r'D:/TOSHIBA/AISINEI/%s' % r'XIUREN秀人网'
    mapper_product(params)
    fail = t.rmempty(params[r'dst'])
    if fail:
        print(r'[Bad] : %s' % fail)

    print(r'Done.')

#######################################################################

if __name__ == "__main__":
    loader_main()

#######################################################################
