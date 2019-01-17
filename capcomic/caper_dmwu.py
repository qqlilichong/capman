
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
        self.__bs.close()

    def __select(self):
        items = self.__main.split(r'/')
        items = [i for i in items if i]
        return self.__main.replace(items[-1], r'%s-p%s' % (items[-1], self.__pageidx + 1))

    def __imgfile(self):
        webtool.fmkdir(self.__path)
        imgfile = '%s' % (self.__pageidx + 1)
        return os.path.join(self.__path, r'%s.jpg' % imgfile.zfill(4))

    def __gomain(self):
        return jscaper.getbss(self.__bs, self.__main, r'div#chapterpager.chapterpager')

    def __refresh(self):
        chaps = self.__gomain().find_elements_by_tag_name(r'a')
        return int(re.match(r'.*-p(\d+)/', chaps[-1].get_attribute(r'href')).group(1))

    def next(self):
        if self.__pageidx >= self.__pagecount:
            return None

        # 选择图片
        imgframe = self.__select()

        # 跳转到图片框架
        img = jscaper.getbss(self.__bs, imgframe, r'img#cp_image')
        img = jscaper.getbtn(self.__bs, img.get_attribute(r'src'), r'img')

        # 保存图片
        jscaper.save(self.__bs, img.get_attribute(r'src'), self.__imgfile())
        self.__pageidx += 1
        return True

#######################################################################

def capman(url, path):
    caper = CaperDMWU(url, path)
    try:
        while caper.next():
            pass
    finally:
        caper.close()

#######################################################################
