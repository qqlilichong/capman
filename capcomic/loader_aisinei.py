
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
    m = re.match(r'(.*)\[.*\]', title)
    if not m:
        return title.strip()
    return m[1].strip()

#######################################################################

def website():
    return r'https://www.aisinei.net/'

#######################################################################

def mapper_image(params):
    def work():
        result = None
        url = t.http_urljoin(website(), params[r'url'])
        try:
            ig = False

            def onerr(resp):
                if resp.status_code == 404:
                    nonlocal ig
                    ig = True

            if not t.http_download(url,
                                   params[r'image'],
                                   None,
                                   onerr):
                if ig:
                    result = True
                    print(r'[404] : %s.' % url)
                return

            result = True
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % url)
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

    k = r'TuiGirl推女郎'
    v = r'/forum-tuigirl-%s.html'
    result.append((k, v))

    k = r'UGirls尤果网'
    v = r'/forum-ugirls-%s.html'
    result.append((k, v))

    k = r'UGirls尤果圈'
    v = r'/forum-youguoquan-%s.html'
    result.append((k, v))

    k = r'ROSI'
    v = r'/forum-rosi-%s.html'
    result.append((k, v))

    k = r'BeautyLeg'
    v = r'/forum-beautyleg-%s.html'
    result.append((k, v))

    k = r'Goddes头条女神'
    v = r'/forum-goddes-%s.html'
    result.append((k, v))

    k = r'DDY_Pantyhose'
    v = r'/forum-ddypantyhoseart-%s.html'
    result.append((k, v))

    k = r'颜女神'
    v = r'/forum-yannvshen-%s.html'
    result.append((k, v))

    k = r'DISI第四印象'
    v = r'/forum-disi-%s.html'
    result.append((k, v))

    k = r'3AGirl'
    v = r'/forum-3agirl-%s.html'
    result.append((k, v))

    k = r'108TV酱'
    v = r'/forum-108tv-%s.html'
    result.append((k, v))

    k = r'QingDouKe青豆客'
    v = r'/forum-qingdouke-%s.html'
    result.append((k, v))

    k = r'Kelagirls克拉女神'
    v = r'/forum-kelagirls-%s.html'
    result.append((k, v))

    k = r'GIRLT果团网'
    v = r'/forum-girlt-%s.html'
    result.append((k, v))

    k = r'TGOD推女神'
    v = r'/forum-tgod-%s.html'
    result.append((k, v))

    k = r'SLADY猎女神'
    v = r'/forum-slady-%s.html'
    result.append((k, v))

    k = r'XIUREN秀人网'
    v = r'/forum-xiuren-%s.html'
    result.append((k, v))

    k = r'MyGirl美媛馆'
    v = r'/forum-mygirl-%s.html'
    result.append((k, v))

    k = r'BoLoli波萝社'
    v = r'/forum-bololi-%s.html'
    result.append((k, v))

    k = r'MiStar魅妍社'
    v = r'/forum-mistar-%s.html'
    result.append((k, v))

    k = r'MFStar模范学院'
    v = r'/forum-mfstar-%s.html'
    result.append((k, v))

    k = r'UXING优星馆'
    v = r'/forum-uxing-%s.html'
    result.append((k, v))

    k = r'IMISS爱蜜社'
    v = r'/forum-imiss-%s.html'
    result.append((k, v))

    k = r'FEILIN嗲囡囡'
    v = r'/forum-feilin-%s.html'
    result.append((k, v))

    k = r'TASTE顽味生活'
    v = r'/forum-taste-%s.html'
    result.append((k, v))

    k = r'MiiTao蜜桃社'
    v = r'/forum-miitao-%s.html'
    result.append((k, v))

    k = r'YouWu尤物馆'
    v = r'/forum-youwu-%s.html'
    result.append((k, v))

    k = r'WingS影私荟'
    v = r'/forum-wings-%s.html'
    result.append((k, v))

    k = r'LeYuan星乐园'
    v = r'/forum-leyuan-%s.html'
    result.append((k, v))

    k = r'HuaYan花の颜'
    v = r'/forum-huayan-%s.html'
    result.append((k, v))

    k = r'MintYe薄荷叶'
    v = r'/forum-mintye-%s.html'
    result.append((k, v))

    k = r'DKGirl御女郎'
    v = r'/forum-dkgirl-%s.html'
    result.append((k, v))

    k = r'CANDY糖果画报'
    v = r'/forum-candy-%s.html'
    result.append((k, v))

    k = r'YOUMI尤蜜荟'
    v = r'/forum-youmi-%s.html'
    result.append((k, v))

    k = r'MTMENG模特联盟'
    v = r'/forum-mtmeng-%s.html'
    result.append((k, v))

    k = r'MICAT猫萌榜'
    v = r'/forum-micat-%s.html'
    result.append((k, v))

    k = r'HuaYang花漾'
    v = r'/forum-huayang-%s.html'
    result.append((k, v))

    k = r'XINGYAN星颜社'
    v = r'/forum-xingyan-%s.html'
    result.append((k, v))

    k = r'XIAOYU语画界'
    v = r'/forum-xiaoyu-%s.html'
    result.append((k, v))

    return result

#######################################################################

def loader_main():
    for k, v in productlist():
        print(r'[PRODUCT] : %s' % k)
        params = dict()
        params[r'dst'] = r'D:/TOSHIBA/AISINEI/%s' % k
        params[r'url'] = t.http_urljoin(website(), v)
        mapper_product(params)
        fail = t.rmempty(params[r'dst'])
        if fail:
            print(r'[Bad] : %s' % fail)

#######################################################################

if __name__ == "__main__":
    loader_main()
    print(r'Done.')

#######################################################################
