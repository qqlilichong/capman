
#######################################################################

import os
import time
import t_webtool as t

#######################################################################

def website(path, xid):
    return r'https://xcg123.herokuapp.com/series/%s/%s' % (path, xid)

#######################################################################

def mapper_image(params):
    if t.fexists(params[r'file']):
        return t.mkd(result=r'fexists')

    headers = {
        r'Host': r'img.177pic.info'
    }
    while not t.http_download(params[r'url'], params[r'file'], headers):
        time.sleep(1)

    return t.mkd(result=r'ok')

#######################################################################

def mapper_chapter(params):
    url = r'%s/%s' % (website(r'chapter', params[r'BOOK']), params[r'Id'])
    imageset = t.jloads(t.http_get(url).text)
    if not imageset[r'Successful']:
        return None

    cidx = t.zf(imageset[r'Data'][r'Index'])
    dst = os.path.join(params[r'DST'], cidx)
    t.fmkdir(dst)

    index = 0
    for image in imageset[r'Data'][r'Images']:
        if not mapper_image({
            r'url': image[r'Path'],
            r'file': os.path.join(dst, '%s-%s.jpg' % (cidx, t.zf(index))),
        }):
            return None
        index += 1

    return t.mkd(result=r'ok')

#######################################################################

def mapper_chapterset(params):
    url = website(r'show', params[r'BOOK'])
    chapterset = t.jloads(t.http_get(url).text)
    if not chapterset[r'Successful']:
        return None

    for chapter in chapterset[r'Data'][r'Chapters']:
        chapter.update(params)
        if not mapper_chapter(chapter):
            return None

    return t.mkd(result=r'ok')

#######################################################################

def loader_main():
    book = r''
    title = r''

    return mapper_chapterset({
        r'BOOK': book,
        r'DST': r'../../../XCG18H/%s/%s' % (book, title)
    })

#######################################################################

if __name__ == "__main__":
    if loader_main():
        print(r'loader done.')

#######################################################################
