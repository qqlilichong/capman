
#######################################################################

import os
import jscaper
import webtool

#######################################################################

class CaperDMZJ:
    def __init__(self, main, path):
        self.__bs = jscaper.newbs()
        self.__main = main
        self.__path = path
        self.__pagecount = len(self.__refresh())
        self.__pageidx = 0

    def close(self):
        self.__bs.close()

    def __select(self):
        sc = r'''
            function dmzj_select(idx) {
                var obj = document.getElementById("page_select");
                obj.options[idx].selected = true;
                select_page();
            }
        ''' + (r'dmzj_select(%s);' % self.__pageidx)
        return jscaper.exejsbid(self.__bs, sc, r'center_box')

    def __imgfile(self):
        webtool.fmkdir(self.__path)
        imgfile = '%s' % (self.__pageidx + 1)
        return os.path.join(self.__path, r'%s.jpg' % imgfile.zfill(4))

    def __gomain(self):
        return jscaper.getbid(self.__bs, self.__main, r'page_select')

    def __refresh(self):
        return self.__gomain().find_elements_by_tag_name(r'option')

    def next(self):
        if self.__pageidx >= self.__pagecount:
            return None

        # 刷新主页
        pages = self.__refresh()

        # 下拉选择图片
        self.__select()

        # 得到图片框架
        imgframe = webtool.http_urljoin(self.__bs.current_url, pages[self.__pageidx].get_attribute(r'value'))

        # 跳转到图片框架
        img = jscaper.getbtn(self.__bs, imgframe, r'img')

        # 保存图片
        jscaper.save(self.__bs, img.get_attribute(r'src'), self.__imgfile())
        self.__pageidx += 1
        return True

#######################################################################

def capman(url, path):
    caper = CaperDMZJ(url, path)
    try:
        while caper.next():
            pass
    finally:
        caper.close()

#######################################################################
