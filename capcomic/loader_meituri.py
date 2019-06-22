
#######################################################################

import re
import os
import time
import t_webtool as t

#######################################################################
# 查询厂商作品数量
def query_product_total(url, err=None):
    xx = t.exp(url, err=err)
    if xx is None:
        return None
    return t.exps(xx.xpath(r'//div[@class = "shoulushuliang"]/span/text()'))

#######################################################################
# 查询导航页中所有作品对象表
def query_navpage_threadobjtbl(url, err=None):
    xx = t.exp(url, err=err)
    if xx is None:
        return None
    return xx.xpath(r'//div[@class = "hezi"]/ul/li')

#######################################################################
# 将作品对象表转换为作品信息表
def __subjectstrip(text):
    if text.endswith(r'.'):
        return __subjectstrip(text[0:-1])
    return text

def __fixsubject(text):
    return __subjectstrip(text.replace('\\', r'-').replace('/', r'-')) \
        .replace('\t', r'') \
        .replace(r'?', r'') \
        .replace(r'|', r'') \
        .replace(r':', r'') \
        .replace(r'*', r'') \
        .replace(r'"', r'') \
        .replace(r'<', r'') \
        .replace(r'>', r'') \

def query_threadinfotbl(threadobjtbl, url, dst):
    result = None
    try:
        threadinfotbl = dict()
        for threadobj in threadobjtbl:
            link = t.http_urljoin(url, t.expa(threadobj, r'href', r'./a/'))
            subject = t.expt(threadobj, r'./p[@class = "biaoti"]/a/')
            tbl = dict()
            tbl[r'cover'] = t.expa(threadobj, r'src', r'./a/img/')
            tbl[r'url'] = link
            tbl[r'subject'] = r'[%s]%s' % (re.sub(r'\D', r'', link), __fixsubject(subject))
            tbl[r'dst'] = dst
            for v in tbl.values():
                if not v:
                    return
            threadinfotbl[link] = tbl

        result = threadinfotbl
    finally:
        return result

#######################################################################
# 查询作品所有页
def query_threadpages(url):
    result = None
    try:
        urls = [url]

        maxp = 1
        for x in t.exp(url).xpath(r'//div[@id = "pages"]/a/text()'):
            if not x.isnumeric():
                continue

            if int(x) > maxp:
                maxp = int(x)

        for i in range(2, maxp + 1):
            urls.append(t.http_urljoin(url, r'%s.html' % i))

        result = urls
    finally:
        return result

#######################################################################
# 查询作品页所有图片
def query_threadpageimages(url):
    result = None
    try:
        result = t.exp(url).xpath(r'//div[@class = "content"]/img/@src')
    finally:
        return result

#######################################################################

def mapper_threadinfo(params):
    def work():
        result = None
        try:
            # ignore exist thread.
            dst = os.path.join(params[r'dst'], params[r'subject'])
            if os.path.exists(dst):
                result = dict()
                return

            urls = query_threadpages(params[r'url'])
            if not urls:
                return

            threadpagetbl = dict()
            index = 0
            for link in urls:
                tbl = dict()
                tbl[r'url'] = link
                tbl[r'dst'] = dst
                tbl[r'cover'] = params[r'cover']
                tbl[r'pidx'] = t.zf(index)
                threadpagetbl[link] = tbl
                index += 1

            t.fmkdir(dst)
            result = threadpagetbl
        finally:
            if result is None:
                print(r'[mapper_threadinfo][ERROR] : %s.' % params[r'url'])
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

def mapper_threadpage(params):
    def work():
        result = None
        try:
            urls = query_threadpageimages(params[r'url'])
            if not urls:
                return

            imagetbl = dict()

            # cover image.
            imagetbl[params[r'cover']] = {
                r'url': params[r'cover'],
                r'dst': os.path.join(params[r'dst'], r'cover.jpg'),
            }

            # content images.
            index = 0
            for img in urls:
                img = fiximg(img)
                if not img:
                    continue

                tbl = dict()
                tbl[r'url'] = img
                tbl[r'dst'] = os.path.join(params[r'dst'],
                                           r'%s-%s.jpg' % (params[r'pidx'], t.zf(index)))
                imagetbl[img] = tbl
                index += 1

            result = imagetbl
        finally:
            if result is None:
                print(r'[mapper_threadpage][ERROR] : %s.' % params[r'url'])
                time.sleep(1)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def mapper_image(params):
    def work():
        result = None
        try:
            ig = False

            def onerr(resp):
                if resp.status_code == 500 or resp.status_code == 404 or resp.status_code == 403:
                    nonlocal ig
                    ig = True

            ilen = t.http_download(params[r'url'], params[r'dst'],
                                   None,
                                   onerr)
            if ilen == 0:
                result = True
                print(r'[mapper_image][IMGNULL] : %s.' % params[r'url'])
                return

            if not ilen:
                if ig:
                    result = True
                    print(r'[mapper_image][IGNORE] : %s.' % params[r'url'])
                return

            result = True
        finally:
            if result is None:
                print(r'[mapper_image][ERROR] : %s.' % params)
                time.sleep(1)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def mapper_navpage(params):
    def work():
        result = None
        try:
            ig = False

            def onerr(resp):
                if resp.status_code == 404:
                    nonlocal ig
                    ig = True

            threadobjtbl = query_navpage_threadobjtbl(params[r'url'], onerr)
            if not threadobjtbl:
                if ig:
                    print(r'[mapper_navpage][IGNORE] : %s.' % params[r'url'])
                    result = dict()
                    return

            result = query_threadinfotbl(threadobjtbl, params[r'url'], params[r'dst'])
        finally:
            if result is None:
                print(r'[mapper_navpage][ERROR] : %s.' % params[r'url'])
                time.sleep(1)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def query_navpagetbl(product, dst):
    pcount = int(int(query_product_total(product)) / len(query_navpage_threadobjtbl(product)))

    navpagetbl = list()
    navpagetbl.append({
        r'dst': dst,
        r'url': product,
    })

    for i in range(1, pcount + 1):
        navpagetbl.append({
            r'dst': dst,
            r'url': t.http_urljoin(product, r'index_%s.html' % i),
        })

    return navpagetbl

#######################################################################

def get(product, dst):
    navpagetbl = query_navpagetbl(product, dst)

    threadinfotbl = dict()
    for data in t.reducer(navpagetbl, mapper_navpage):
        threadinfotbl.update(data)

    threadpagetbl = dict()
    for data in t.reducer(threadinfotbl.values(), mapper_threadinfo):
        threadpagetbl.update(data)

    imagetbl = dict()
    for data in t.reducer(threadpagetbl.values(), mapper_threadpage):
        imagetbl.update(data)

    t.reducer(imagetbl.values(), mapper_image)
    return True

#######################################################################

def website():
    return r'https://www.meituri.com'

def productlist():
    result = list()

    k = r'丝意SIEE'
    v = r'/x/87/'
    result.append((k, v))

    k = r'语画界'
    v = r'/x/85/'
    result.append((k, v))

    k = r'尤美'
    v = r'/x/84/'
    result.append((k, v))

    k = r'CosPlay'
    v = r'/x/83/'
    result.append((k, v))

    k = r'森萝财团'
    v = r'/x/82/'
    result.append((k, v))

    k = r'蜜丝'
    v = r'/x/81/'
    result.append((k, v))

    k = r'Cosdoki'
    v = r'/x/80/'
    result.append((k, v))

    k = r'Girlz-High'
    v = r'/x/79/'
    result.append((k, v))

    k = r'台湾正妹'
    v = r'/x/78/'
    result.append((k, v))

    k = r'猎女神'
    v = r'/x/77/'
    result.append((k, v))

    k = r'OnlyTease'
    v = r'/x/76/'
    result.append((k, v))

    k = r'推女郎'
    v = r'/x/75/'
    result.append((k, v))

    k = r'美媛馆'
    v = r'/x/74/'
    result.append((k, v))

    k = r'尤物馆'
    v = r'/x/73/'
    result.append((k, v))

    k = r'魅妍社'
    v = r'/x/72/'
    result.append((k, v))

    k = r'蜜桃社'
    v = r'/x/71/'
    result.append((k, v))

    k = r'模范学院'
    v = r'/x/70/'
    result.append((k, v))

    k = r'星乐园'
    v = r'/x/69/'
    result.append((k, v))

    k = r'爱蜜社'
    v = r'/x/68/'
    result.append((k, v))

    k = r'嗲囡囡'
    v = r'/x/67/'
    result.append((k, v))

    k = r'波萝社'
    v = r'/x/66/'
    result.append((k, v))

    k = r'Misty'
    v = r'/x/65/'
    result.append((k, v))

    k = r'Wanibooks'
    v = r'/x/64/'
    result.append((k, v))

    k = r'尤果网'
    v = r'/x/63/'
    result.append((k, v))

    k = r'尤果圈爱尤物'
    v = r'/x/62/'
    result.append((k, v))

    k = r'影私荟'
    v = r'/x/61/'
    result.append((k, v))

    k = r'顽味生活'
    v = r'/x/60/'
    result.append((k, v))

    k = r'秀人网'
    v = r'/x/59/'
    result.append((k, v))

    k = r'尤蜜荟'
    v = r'/x/58/'
    result.append((k, v))

    k = r'Beautyleg'
    v = r'/x/57/'
    result.append((k, v))

    k = r'优星馆'
    v = r'/x/56/'
    result.append((k, v))

    k = r'御女郎'
    v = r'/x/55/'
    result.append((k, v))

    k = r'NS Eyes'
    v = r'/x/54/'
    result.append((k, v))

    k = r'ImageTV'
    v = r'/x/53/'
    result.append((k, v))

    k = r'YS Web'
    v = r'/x/52/'
    result.append((k, v))

    k = r'Hello Project Digital Books'
    v = r'/x/51/'
    result.append((k, v))

    k = r'BombTV'
    v = r'/x/50/'
    result.append((k, v))

    k = r'丽柜'
    v = r'/x/49/'
    result.append((k, v))

    k = r'PB写真集'
    v = r'/x/48/'
    result.append((k, v))

    k = r'4K-STAR'
    v = r'/x/47/'
    result.append((k, v))

    k = r'ISHOW爱秀'
    v = r'/x/46/'
    result.append((k, v))

    k = r'头条女神'
    v = r'/x/45/'
    result.append((k, v))

    k = r'动感之星'
    v = r'/x/44/'
    result.append((k, v))

    k = r'Graphis'
    v = r'/x/43/'
    result.append((k, v))

    k = r'Bejean On Line'
    v = r'/x/42/'
    result.append((k, v))

    k = r'51MODO'
    v = r'/x/41/'
    result.append((k, v))

    k = r'ImutoTV'
    v = r'/x/40/'
    result.append((k, v))

    k = r'推女神'
    v = r'/x/39/'
    result.append((k, v))

    k = r'DDY Pantyhose'
    v = r'/x/38/'
    result.append((k, v))

    k = r'爱丝'
    v = r'/x/37/'
    result.append((k, v))

    k = r'VYJ'
    v = r'/x/36/'
    result.append((k, v))

    k = r'MinisukaTV'
    v = r'/x/35/'
    result.append((k, v))

    k = r'网红馆'
    v = r'/x/34/'
    result.append((k, v))

    k = r'WPB写真'
    v = r'/x/33/'
    result.append((k, v))

    k = r'美腿宝贝'
    v = r'/x/32/'
    result.append((k, v))

    k = r'克拉女神'
    v = r'/x/31/'
    result.append((k, v))

    k = r'瑞丝馆'
    v = r'/x/30/'
    result.append((k, v))

    k = r'薄荷叶'
    v = r'/x/29/'
    result.append((k, v))

    k = r'Sabra'
    v = r'/x/28/'
    result.append((k, v))

    k = r'果团网'
    v = r'/x/27/'
    result.append((k, v))

    k = r'青豆客'
    v = r'/x/26/'
    result.append((k, v))

    k = r'花の颜'
    v = r'/x/25/'
    result.append((k, v))

    k = r'模特联盟'
    v = r'/x/24/'
    result.append((k, v))

    k = r'花漾'
    v = r'/x/23/'
    result.append((k, v))

    k = r'兔几盟'
    v = r'/x/22/'
    result.append((k, v))

    k = r'Juicy Honey'
    v = r'/x/21/'
    result.append((k, v))

    k = r'X-City'
    v = r'/x/20/'
    result.append((k, v))

    k = r'Princess Collection'
    v = r'/x/19/'
    result.append((k, v))

    k = r'LovePop'
    v = r'/x/18/'
    result.append((k, v))

    k = r'Digi-Gra'
    v = r'/x/17/'
    result.append((k, v))

    k = r'熊川纪信'
    v = r'/x/16/'
    result.append((k, v))

    k = r'星颜社'
    v = r'/x/15/'
    result.append((k, v))

    k = r'丝享家'
    v = r'/x/14/'
    result.append((k, v))

    k = r'丝足便当'
    v = r'/x/13/'
    result.append((k, v))

    k = r'异思趣向'
    v = r'/x/12/'
    result.append((k, v))

    k = r'The Black Alley'
    v = r'/x/11/'
    result.append((k, v))

    k = r'激萌文化'
    v = r'/x/10/'
    result.append((k, v))

    k = r'Young Animal Arashi'
    v = r'/x/9/'
    result.append((k, v))

    k = r'DGC'
    v = r'/x/8/'
    result.append((k, v))

    k = r'RQ-STAR'
    v = r'/x/7/'
    result.append((k, v))

    k = r'Young Animal'
    v = r'/x/6/'
    result.append((k, v))

    k = r'For-side'
    v = r'/x/5/'
    result.append((k, v))

    k = r'Weekly Playboy'
    v = r'/x/4/'
    result.append((k, v))

    k = r'Weekly Young Jump'
    v = r'/x/3/'
    result.append((k, v))

    k = r'网络美女'
    v = r'/x/2/'
    result.append((k, v))

    k = r'BWH'
    v = r'/x/1/'
    result.append((k, v))

    return result

def loader_main():
    for k, v in productlist():
        print(r'[PRODUCT] : %s' % k)
        dst = r'D:/TOSHIBA/[套图]美图日/%s' % k
        get(t.http_urljoin(website(), v), dst)
        fail = t.rmempty(dst)
        if fail:
            print(r'[Bad] : %s' % fail)

#######################################################################

if __name__ == "__main__":
    loader_main()
    print('bye...')

#######################################################################
