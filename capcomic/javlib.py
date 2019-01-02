
#######################################################################

import os
import re
import webtool

#######################################################################

def video_id(vid):
    return vid.strip().upper()

def video_type(vid):
    return re.findall(r'[a-zA-Z]+', vid)[0]

#######################################################################

class JavLibDetail:
    def __init__(self, url, kind):
        self.__divs = webtool.mkd(
            video_id=self.__video_id,
            video_title=self.__video_title,
            video_jacket=self.__video_jacket,
            video_date=self.__video_date,
            video_length=self.__video_length,
            video_maker=self.__video_items,
            video_label=self.__video_items,
            video_cast=self.__video_items,
        )

        self.__model = None
        self.__load(url, kind)

    def __getattr__(self, item):
        result = None
        try:
            result = self.__model[r'video_%s' % item]
        finally:
            return result

    def __load(self, url, kind):
        self.__model = None
        try:
            model = dict()
            for div in webtool.bs4get(url).findAll(r'div', id=re.compile(r'video_\w+')):
                divid = div[r'id']
                if divid in self.__divs:
                    model[divid] = self.__divs[divid](div)

            self.__model = self.__update(model, kind)
        finally:
            return self.__model

    def saveimg(self, rootpath):
        result = None
        filename = None
        try:
            if not self.__model:
                return

            if not webtool.fmkdir(os.path.join(rootpath, self.__model[r'video_relpath'])):
                return

            filename = os.path.join(rootpath, self.__model[r'video_localfile'])
            result = webtool.http_download(self.__model[r'video_jacket'], filename)
        finally:
            if not result:
                webtool.fremove(filename)

            return result

    def savemodel(self, dbs):
        result = None
        try:
            if not self.__model:
                return

            tnames = {
                r'maker': None,
                r'label': None,
                r'cast': None,
            }

            for tname in tnames.keys():
                vals = list()
                for model in self.__model[r'video_%s' % tname]:
                    if not dbs.replace(tname, **model):
                        return
                    vals.append(model[r'id'])
                tnames[tname] = r','.join(vals)

            if not dbs.replace(r'detail',
                               id=self.__model[r'video_localfile'],
                               url=self.__model[r'video_url'],
                               title=self.__model[r'video_title'],
                               image=self.__model[r'video_jacket'],
                               date=self.__model[r'video_date'],
                               length=self.__model[r'video_length'],
                               **tnames):
                return

            if not dbs.commit():
                return

            result = True
        finally:
            return result

    @staticmethod
    def __update(model, kind):
        model[r'video_kind'] = kind
        model[r'video_title'], model[r'video_url'] = model[r'video_title']
        model[r'video_number'] = re.findall(r'\d+', model[r'video_id'])[0]
        model[r'video_relpath'] = r'%s/%s' % (model[r'video_kind'], video_type(model[r'video_id']))
        model[r'video_localfile'] = r'%s/%s.jpg' % (model[r'video_relpath'], model[r'video_id'])
        return model

    @staticmethod
    def __video_id(div):
        return video_id(div.find(r'td', r'text').get_text())

    @staticmethod
    def __video_title(div):
        return div.a.get_text().strip(), div.a[r'href']

    @staticmethod
    def __video_jacket(div):
        return div.img[r'src'].strip()

    @staticmethod
    def __video_date(div):
        return div.find(r'td', r'text').get_text().strip()

    @staticmethod
    def __video_length(div):
        return div.find(r'td', r'').get_text().strip()

    @staticmethod
    def __video_items(div):
        result = list()
        for it in div.findAll(r'a'):
            result.append(webtool.mkd(
                id=re.match(r'.*\?(.*)', it[r'href']).group(1),
                url=r'',
                name=it.get_text().strip()
            ))
        return result

#######################################################################

class JavLibSearch:
    def __init__(self, url, kind, dbinfo):
        self.__kind = kind
        self.__dbinfo = dbinfo
        self.__load(url)

    def __load(self, url):
        result = None
        try:
            result = self.__detailcollect(url)
        finally:
            return result

    def __detailcollect(self, url):
        typeset = self.__typecollect(self.__pageselector(url))
        print('[LOG] - TypeCollect %s : %s' % (self.__kind, typeset))

        searchurls = list()
        for t in typeset:
            searchurl = webtool.http_urljoin(url, r'vl_searchbyid.php?keyword=%s' % t)
            searchurls += [(t, url) for url in self.__pageselector(searchurl)]

        self.__videocollect(searchurls)
        return True

    @staticmethod
    def __pageselector(url):
        pagetotal = 1
        link = webtool.bs4get(url).find(r'div', r'page_selector').find(r'a', r"page last")
        if link:
            pagetotal = int(re.match(r'.*page=(\d+)', link[r'href']).group(1))

        return [url + r'&page=%s' % num for num in range(1, pagetotal + 1)]

    @staticmethod
    def __typecollect(urls):
        typeset = set()
        for data in webtool.reducer(urls, mapper_search_type):
            typeset |= data
        return typeset

    @staticmethod
    def __videocollect(urls):
        videolist = list()
        for data in webtool.reducer(urls, mapper_search_video):
            videolist += data
        return videolist

#######################################################################

def mapper_search_type(url):
    def work():
        result = None
        try:
            typeset = set()
            for div in webtool.bs4get(url).findAll(r'div', r'video'):
                typeset.add(video_type(video_id(div.find(r'div', r'id').get_text())))

            result = typeset
        finally:
            if result is None:
                print(r'Error : %s' % url)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################

def mapper_search_video(param):
    vfilter, url = param

    def work():
        result = None
        try:
            videolist = list()
            for div in webtool.bs4get(url).findAll(r'div', r'video'):
                if re.match(r'^%s.*' % vfilter, video_id(div.find(r'div', r'id').get_text())):
                    videolist.append(webtool.http_urljoin(url, div.a[r'href']))

            result = videolist
        finally:
            if result is None:
                print(r'Error : %s' % url)
            return result

    data = None
    while data is None:
        data = work()
    return data

#######################################################################
