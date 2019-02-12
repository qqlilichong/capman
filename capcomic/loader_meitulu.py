
#######################################################################

import os
import re
import t_webtool

#######################################################################

def __pagelist(url):
    nums = list()

    bs = t_webtool.bs4get(url)
    for link in bs.find(r'div', r'text-c').findAll(r'a'):
        if not link.has_attr(r'href'):
            continue

        num = link.get_text()
        if not num.isnumeric():
            continue

        nums.append(int(num))

    pl = [url]
    for i in range(2, max(nums) + 1):
        pl.append(t_webtool.http_urljoin(url, r'./%s.html' % i))
    return pl

#######################################################################

def __mapper_collecter(param):
    def work():
        result = None
        try:
            ret = dict()

            for li in t_webtool.bs4get(param[r'url']).find(r'ul', r'img').findAll(r'li'):
                title = li.find(r'p', r'p_title').get_text().strip()
                title = title.replace(r' ', r'')
                title = title.replace(r'\\', r'')
                title = title.replace(r'/', r'')
                title = title.replace(r'"', r'')
                title = title.replace(r"'", r'')
                for label in re.findall(r'(\[.*\])', title):
                    title = title.replace(label, r'')

                pid = re.findall(r'/(\d+)/', li.a.img[r'src'])[-1]

                title = r'[%s]%s' % (pid.zfill(6), title)
                path = os.path.join(param[r'path'], title)
                if os.path.exists(path):
                    continue

                pc = int(re.findall(r'图片.*?(\d+).*', li.get_text())[0])
                for i in range(0, pc + 1):
                    key = t_webtool.http_urljoin(li.a.img[r'src'], r'./%s' % r'%s.jpg' % i)
                    ret[key] = dict()
                    ret[key][r'url'] = key
                    ret[key][r'path'] = path
                    ret[key][r'file'] = r'%s.jpg' % str(i).zfill(4)
                    ret[key][r'header'] = {r'Referer': param[r'referer'] % key}

            result = ret
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % param)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def __mapper_downloader(param):
    def work():
        result = None
        try:
            ret = dict()
            ig = False

            def onerr(resp):
                if resp.status_code == 403 or resp.status_code == 404:
                    nonlocal ig
                    ig = True

            t_webtool.fmkdir(param[r'path'])
            if not t_webtool.http_download(param[r'url'],
                                           os.path.join(param[r'path'], param[r'file']),
                                           param[r'header'],
                                           onerr):
                if ig:
                    print(r'[IG]%s' % param[r'url'])
                    result = ret
                return

            result = ret
        finally:
            if result is None:
                print(r'[ERROR] : %s.' % param)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def capman(url, path, referer):
    params = dict()
    for p in t_webtool.reducer([{
        r'url': url,
        r'path': path,
        r'referer': referer,
    } for url in __pagelist(url)], __mapper_collecter):
        params.update(p)

    t_webtool.reducer(params.values(), __mapper_downloader)
    return True

#######################################################################

def loader_main():
    cfg = t_webtool.IniDict()
    proot = os.path.dirname(__file__)
    cfg.read(os.path.join(proot, r'configer_mei.ini'))
    proot = os.path.join(proot, cfg[r'CONFIG'][r'path'])

    for maker, ma in cfg.resection(r'^MEITULU_(\w+)$').items():
        url = cfg[maker][r'url']
        path = os.path.join(proot, cfg[maker][r'title'])
        referer = t_webtool.http_urljoin(url, r'/img.html?img=%s')
        capman(url, path, referer)

#######################################################################

if __name__ == "__main__":
    loader_main()
    print('bye...')

#######################################################################
