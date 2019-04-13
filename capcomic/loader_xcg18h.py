
#######################################################################

import os
import t_webtool

#######################################################################

def mapper_imagedown(url, file):
    headers = {
        r'Host': r'img.177pic.info'
    }
    return t_webtool.http_download(url, file, headers)

#######################################################################

def loader_main():
    if True:
        os.environ[r'HTTP_PROXY'] = r'http://192.168.200.1:1080'
        os.environ[r'HTTPS_PROXY'] = os.environ[r'HTTP_PROXY']

    img_begin = 6
    img_end = 791
    dir_dst = r'./xcg18h'

    t_webtool.fmkdir(dir_dst)

    for idx in range(img_begin, img_end + 1):
        idx = str(idx).zfill(3)
        file_dst = os.path.join(dir_dst, r'%s.jpg' % idx)
        url = r'http://img.177pic.info/uploads/2013/11h/P%s.jpg' % idx
        if not mapper_imagedown(url, file_dst):
            print(r'[ERROR] : %s' % url)
            return None

    return True

#######################################################################

if __name__ == "__main__":
    if loader_main():
        print(r'loader done.')

#######################################################################
