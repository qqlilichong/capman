
#######################################################################

import uuid
import t_webtool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec

#######################################################################

def js():
    return r'''
        function caper_urlblob(url, cb) {
            var xhr = new XMLHttpRequest();
            xhr.open("get", url, true);
            xhr.responseType = "blob";
            xhr.onload = function() {
                if (this.status == 200)
                {
                    cb(this.response);
                }
            };

            xhr.send();
        }

        function caper_appendimg(url, imgid) {
            let reader = new FileReader();

            reader.onload = function(e) {
                var img = document.createElement("img");
                img.id = imgid;
                img.src = e.target.result;
                document.body.appendChild(img);
            }

            caper_urlblob(url, function(blob) {
                reader.readAsDataURL(blob);
            });
        }
    '''

#######################################################################

def timeout():
    return 10

#######################################################################

def newbs(hl=False, crx=False, dc=False, did=r'chrome'):
    dr = None

    if did == r'chrome':
        options = webdriver.ChromeOptions()

        if hl:
            options.add_argument(r'--headless')
            options.add_argument(r'--disable-gpu')

        if crx:
            for crx in t_webtool.flist(__file__, r'.crx'):
                options.add_extension(crx)

        pls = None
        if dc:
            pls = DesiredCapabilities.CHROME
            pls[r'pageLoadStrategy'] = r'none'

        dr = webdriver.Chrome(chrome_options=options,
                              desired_capabilities=pls,
                              executable_path=r'../chrome/chromedriver')

    dr.implicitly_wait(timeout())
    dr.minimize_window()
    return dr

#######################################################################

def wait(bs, **kwargs):
    for key, val in kwargs.items():
        key = key.lower()

        if key == r'id':
            WebDriverWait(bs, timeout()).until(ec.presence_of_element_located((By.ID, val)))
            return bs.find_element_by_id(val)

        if key == r'name':
            WebDriverWait(bs, timeout()).until(ec.presence_of_element_located((By.NAME, val)))
            return bs.find_element_by_name(val)

        if key == r'tagname':
            WebDriverWait(bs, timeout()).until(ec.presence_of_element_located((By.TAG_NAME, val)))
            return bs.find_element_by_tag_name(val)

        if key == r'css':
            WebDriverWait(bs, timeout()).until(ec.presence_of_element_located((By.CSS_SELECTOR, val)))
            return bs.find_element_by_css_selector(val)

    return None

#######################################################################

def get(bs, url, **kwargs):
    bs.get(url)
    return wait(bs, **kwargs)

def getbid(bs, url, val):
    return get(bs, url, id=val)

def getbna(bs, url, val):
    return get(bs, url, name=val)

def getbtn(bs, url, val):
    return get(bs, url, tagname=val)

def getbss(bs, url, val):
    return get(bs, url, css=val)

#######################################################################

def exejs(bs, sc, **kwargs):
    bs.execute_script(js() + sc)
    return wait(bs, **kwargs)

def exejsbid(bs, sc, val):
    return exejs(bs, sc, id=val)

def exejsbna(bs, sc, val):
    return exejs(bs, sc, name=val)

def exejsbtn(bs, sc, val):
    return exejs(bs, sc, tagname=val)

def exejsbss(bs, sc, val):
    return exejs(bs, sc, css=val)

#######################################################################

def save(bs, url, filename):
    gid = str(uuid.uuid4())
    img = exejs(bs, r'caper_appendimg("%s", "%s")' % (url, gid), id=gid)
    return t_webtool.http_download(img.get_attribute(r'src'), filename)

#######################################################################
