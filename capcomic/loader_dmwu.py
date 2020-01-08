
#######################################################################

import re
import os
import t_jscaper
import t_webtool

#######################################################################

class CaperDMWU:
    def __init__(self, main, path):
        self.__bs = t_jscaper.newbs(True)
        self.__main = main
        self.__path = path
        self.__pagecount = self.__refresh()
        self.__pageidx = 0

    def close(self):
        self.__bs.quit()

    def __select(self):
        items = self.__main.split(r'/')
        items = [i for i in items if i]
        return self.__main.replace(items[-1], r'%s-p%s' % (items[-1], self.__pageidx + 1))

    def __imgfile(self):
        t_webtool.fmkdir(self.__path)
        imgfile = '%s' % (self.__pageidx + 1)
        return os.path.join(self.__path, r'%s.jpg' % imgfile.zfill(4))

    def __gomain(self):
        result = None
        try:
            chap = t_jscaper.getbss(self.__bs, self.__main, r'div#chapterpager.chapterpager')
            result = chap.find_elements_by_tag_name(r'a')
        finally:
            return result

    def __refresh(self):
        chaps = None
        while not chaps:
            chaps = self.__gomain()

        return int(re.match(r'.*-p(\d+)/', chaps[-1].get_attribute(r'href')).group(1))

    def next(self):
        result = None
        try:
            if self.__pageidx >= self.__pagecount:
                result = True
                return

            # 选择图片
            imgframe = self.__select()

            # 跳转到图片框架
            img = t_jscaper.getbss(self.__bs, imgframe, r'img#cp_image')
            img = t_jscaper.getbtn(self.__bs, img.get_attribute(r'src'), r'img')

            # 保存图片
            t_jscaper.save(self.__bs, img.get_attribute(r'src'), self.__imgfile())
            self.__pageidx += 1

        finally:
            return result

#######################################################################

def docap(param):
    url, path = param
    caper = CaperDMWU(url, path)
    try:
        while not caper.next():
            pass
    finally:
        caper.close()

def capman(url, path, rm, fmt, fmtf, rev):
    result = None
    try:
        lis = list()
        for link in t_webtool.bs4get(url).find(r'div', id=r'chapterlistload').findAll(r'a'):
            title = link.get_text()
            if re.match(rm, title):
                lis.append(t_webtool.http_urljoin(url, link[r'href']))

        if rev == 'True':
            lis.reverse()

        params = list()
        num = 0
        for link in lis:
            num += 1
            params.append((link, os.path.join(path, fmt % str(num).zfill(int(fmtf)))))

        t_webtool.reducer(params, docap, 8)
        result = True
    finally:
        if not result:
            print(r'failed.')

        return result

#######################################################################

def loader_main():
    cfg = t_webtool.IniDict()
    cfg.read(os.path.join(os.path.dirname(__file__), r'configer_dmwu.ini'))
    for maker in cfg.resection(r'^DMWU_(\w+)$').keys():
        capman(cfg[maker][r'url'],
               os.path.join(cfg[r'OUTPUT'][r'path'], cfg[maker][r'title']),
               cfg[maker][r'match'],
               cfg[maker][r'format'],
               cfg[maker][r'formatfill'],
               cfg[maker][r'reverse'])

#######################################################################

if __name__ == "__main__":
    loader_main()
    print('bye...')

#######################################################################
