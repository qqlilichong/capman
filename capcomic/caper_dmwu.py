
#######################################################################

import re
import os
import jscaper
import webtool

#######################################################################

class CaperDMWU:
    def __init__(self, main, path):
        self.__bs = jscaper.newbs()
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
        webtool.fmkdir(self.__path)
        imgfile = '%s' % (self.__pageidx + 1)
        return os.path.join(self.__path, r'%s.jpg' % imgfile.zfill(4))

    def __gomain(self):
        result = None
        try:
            chap = jscaper.getbss(self.__bs, self.__main, r'div#chapterpager.chapterpager')
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
            img = jscaper.getbss(self.__bs, imgframe, r'img#cp_image')
            img = jscaper.getbtn(self.__bs, img.get_attribute(r'src'), r'img')

            # 保存图片
            jscaper.save(self.__bs, img.get_attribute(r'src'), self.__imgfile())
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
        for link in webtool.bs4get(url).find(r'ul', id=r'detail-list-select-1').findAll(r'a'):
            title = link.get_text()
            if re.match(rm, title):
                lis.append(webtool.http_urljoin(url, link[r'href']))

        if rev == 'True':
            lis.reverse()

        params = list()
        num = 0
        for link in lis:
            num += 1
            params.append((link, os.path.join(path, fmt % str(num).zfill(int(fmtf)))))

        webtool.reducer(params, docap, 8)
        result = True
    finally:
        if not result:
            print(r'failed.')

        return result

#######################################################################
