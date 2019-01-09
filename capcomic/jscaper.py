
#######################################################################

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

def wait(bs, **kwargs):
    timeout = 30

    for key, val in kwargs.items():
        key = key.lower()

        if key == r'id':
            WebDriverWait(bs, timeout).until(ec.presence_of_element_located((By.ID, val)))
            return bs.find_element_by_id(val)

        if key == r'tagname':
            WebDriverWait(bs, timeout).until(ec.presence_of_element_located((By.TAG_NAME, val)))
            return bs.find_element_by_tag_name(val)

    return None

#######################################################################

def get(bs, url, **kwargs):
    bs.get(url)
    return wait(bs, **kwargs)

#######################################################################
