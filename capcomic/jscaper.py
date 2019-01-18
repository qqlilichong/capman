
#######################################################################

import uuid
import webtool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

def newbs():
    options = webdriver.ChromeOptions()
    for crx in webtool.flist(__file__, r'.crx'):
        options.add_extension(crx)
    return webdriver.Chrome(chrome_options=options)

#######################################################################

def wait(bs, **kwargs):
    timeout = 30

    for key, val in kwargs.items():
        key = key.lower()

        if key == r'id':
            WebDriverWait(bs, timeout).until(ec.presence_of_element_located((By.ID, val)))
            return bs.find_element_by_id(val)

        if key == r'name':
            WebDriverWait(bs, timeout).until(ec.presence_of_element_located((By.NAME, val)))
            return bs.find_element_by_name(val)

        if key == r'tagname':
            WebDriverWait(bs, timeout).until(ec.presence_of_element_located((By.TAG_NAME, val)))
            return bs.find_element_by_tag_name(val)

        if key == r'css':
            WebDriverWait(bs, timeout).until(ec.presence_of_element_located((By.CSS_SELECTOR, val)))
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
    return webtool.http_download(img.get_attribute(r'src'), filename)

#######################################################################