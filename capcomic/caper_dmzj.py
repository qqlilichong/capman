
#######################################################################

import os
import jscaper
import webtool
from selenium import webdriver

#######################################################################

def js():
    return r'''
        function dmzj_select(idx) {
            var obj = document.getElementById("page_select");
            obj.options[idx].selected = true;
            select_page();
        }
    
    '''

#######################################################################

dmzj_main = r''
def go_main(bs):
    return jscaper.get(bs, dmzj_main, id=r'page_select')

#######################################################################

def get_options(browser):
    return go_main(browser).find_elements_by_tag_name(r'option')

#######################################################################

def get_imgurl(bs, pageidx):
    options = get_options(bs)
    es = js()
    es += r'dmzj_select(%s);' % pageidx
    bs.execute_script(es)
    bs.get(webtool.http_urljoin(bs.current_url, options[pageidx].get_attribute(r'value')))
    return jscaper.wait(bs, tagname=r'img').get_attribute(r'src')

#######################################################################

def capman(url, rootpath):
    global dmzj_main
    dmzj_main = url

    bs = webdriver.Chrome()
    try:
        for imgidx in range(0, len(get_options(bs))):
            imgid = '%s' % (imgidx + 1)
            imgid = imgid.zfill(4)

            es = jscaper.js()
            es += r'caper_appendimg("%s", "%s")' % (get_imgurl(bs, imgidx), imgid)
            bs.execute_script(es)

            webtool.http_download(jscaper.wait(bs, id=imgid).get_attribute(r'src'),
                                  os.path.join(rootpath, r'%s.jpg' % imgid))

    finally:
        bs.close()

#######################################################################
