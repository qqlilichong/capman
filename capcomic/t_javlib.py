
#######################################################################

import os
import re
import t_dbe
import t_webtool

#######################################################################

def video_id(vid):
    return vid.strip().upper()

def video_type(vid):
    return re.findall(r'[a-zA-Z]+', vid)[0]

#######################################################################

class JavLibDetail:
    def __init__(self, url):
        self.__divs = t_webtool.mkd(
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
        self.__load(url)

    def __getattr__(self, item):
        result = None
        try:
            result = self.__model[r'video_%s' % item]
        finally:
            return result

    def __load(self, url):
        self.__model = None
        try:
            model = dict()
            for div in t_webtool.bs4get(url).findAll(r'div', id=re.compile(r'video_\w+')):
                divid = div[r'id']
                if divid in self.__divs:
                    model[divid] = self.__divs[divid](div)

            self.__model = self.__update(model, url)
        finally:
            return self.__model

    def saveimg(self, filename):
        result = None
        try:
            if not self.__model:
                return

            result = t_webtool.http_download(self.__model[r'video_jacket'], filename)
            if result == 0:
                self.__model[r'video_jacket'] = self.__model[r'video_imgerror']
                result = t_webtool.http_download(self.__model[r'video_jacket'], filename)

        finally:
            if not result:
                t_webtool.fremove(filename)

            return result

    def savemodel(self, dbs, fid):
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
                               id=fid,
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
    def __update(model, url):
        model[r'video_title'], model[r'video_url'] = model[r'video_title']
        model[r'video_jacket'] = t_webtool.http_urljoin(url, model[r'video_jacket'])
        model[r'video_imgerror'] = t_webtool.http_urljoin(url, r'/img/noimagepl.gif')
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
            result.append(t_webtool.mkd(
                id=re.match(r'.*\?(.*)', it[r'href']).group(1),
                url=r'',
                name=it.get_text().strip()
            ))
        return result

#######################################################################

class JavLibSearch:
    @staticmethod
    def search(url, typedict):
        result = None
        try:
            tdict = dict()
            for key in JavLibSearch.__typecollect(url).keys():
                if key not in typedict.keys():
                    tdict[key] = key

            if not tdict:
                result = dict(), dict()
                return

            pagedict, tdict = JavLibSearch.__pagecollect(url, tdict)
            if not tdict:
                result = dict(), dict()
                return

            print('[LOG][JavLibSearch] - TypeCollect : %s.' % tdict.keys())
            videodict = JavLibSearch.__videocollect(pagedict)
            print('[LOG][JavLibSearch] - VideoCollect : %s.' % len(videodict))

            result = tdict, videodict
        finally:
            return result

    @staticmethod
    def __pageselector(url):
        result = list()
        try:
            pagetotal = 1
            link = t_webtool.bs4get(url).find(r'div', r'page_selector').find(r'a', r"page last")
            if link:
                pagetotal = int(re.match(r'.*page=(\d+)', link[r'href']).group(1))

            result = [url + r'&page=%s' % num for num in range(1, pagetotal + 1)]
        finally:
            return result

    @staticmethod
    def __typecollect(url):
        params = [{r'url': d} for d in JavLibSearch.__pageselector(url)]

        result = dict()
        for data in t_webtool.reducer(params, JavLibSearch.mapper_search_type):
            result.update(data)

        return result

    @staticmethod
    def __pagecollect(url, tdict):
        params = [{r'url': url, r'type': key} for key in tdict.keys()]

        result = dict()
        for data in t_webtool.reducer(params, JavLibSearch.mapper_search_page):
            result.update(data)

        tdict = dict()
        for t in result.values():
            tdict[t] = t

        return result, tdict

    @staticmethod
    def __videocollect(pagedict):
        params = [{r'url': key, r'type': val} for key, val in pagedict.items()]

        result = dict()
        for data in t_webtool.reducer(params, JavLibSearch.mapper_search_video):
            result.update(data)

        return result

    @staticmethod
    def mapper_search_page(param):
        def work():
            result = None
            try:
                searchurl = t_webtool.http_urljoin(param[r'url'], r'vl_searchbyid.php?keyword=%s' % param['type'])
                result = {url: param[r'type'] for url in JavLibSearch.__pageselector(searchurl)}
            finally:
                if result is None:
                    print(r'[ERROR] : %s.' % param)
                return result

        data = None
        while data is None:
            data = work()
        return data

    @staticmethod
    def mapper_search_type(param):
        def work():
            result = None
            try:
                ret = dict()
                for div in t_webtool.bs4get(param[r'url']).findAll(r'div', r'video'):
                    vtype = video_type(video_id(div.find(r'div', r'id').get_text()))
                    ret[vtype] = vtype

                result = ret
            finally:
                if result is None:
                    print(r'[ERROR] : %s.' % param)
                return result

        data = None
        while data is None:
            data = work()
        return data

    @staticmethod
    def mapper_search_video(param):
        def work():
            result = None
            try:
                ret = dict()
                for div in t_webtool.bs4get(param[r'url']).findAll(r'div', r'video'):
                    vid = video_id(div.find(r'div', r'id').get_text())
                    if re.match(r'^%s\W+\d+$' % param[r'type'], vid):
                        ret[vid] = t_webtool.http_urljoin(param[r'url'], div.a[r'href'])

                result = ret
            finally:
                if result is None:
                    print(r'[ERROR] : %s.' % param)
                return result

        data = None
        while data is None:
            data = work()
        return data

#######################################################################

class JavLibStore:
    @staticmethod
    def store(imgroot, kind, dbinfo, typedict, videodict):
        for t in typedict.keys():
            t_webtool.fmkdir(os.path.join(imgroot, kind, t))

        params = list()
        for vid, url in videodict.items():
            fid = r'%s/%s/%s.jpg' % (kind, video_type(vid), vid)
            filename = os.path.join(imgroot, fid)
            if not t_webtool.fexists(filename):
                params.append({
                    r'id': vid,
                    r'fid': fid,
                    r'url': url,
                    r'dbinfo': dbinfo,
                    r'file': filename,
                })

        result = dict()
        for data in t_webtool.reducer(params, JavLibStore.mapper_store_detail):
            result.update(data)

        return result

    @staticmethod
    def mapper_store_detail(param):
        def work():
            result = None
            try:
                ret = dict()

                dbs = t_dbe.DBEngine()
                if not dbs.connect(**param[r'dbinfo']):
                    print(r'[ERROR] : DBEngine.')
                    return

                jd = JavLibDetail(param[r'url'])
                if jd.id != param[r'id']:
                    print(r'[ERROR] video_id failed.')
                    return

                if not jd.saveimg(param[r'file']):
                    print(r'[ERROR] saveimg: %s.' % param[r'file'])
                    return

                if not jd.savemodel(dbs, param[r'fid']):
                    print(r'[ERROR] savemodel: %s.' % param[r'dbinfo'])
                    return

                result = ret
            finally:
                if result is None:
                    t_webtool.fremove(param[r'file'])
                    print(r'[ERROR] : %s.' % param)
                return result

        data = None
        while data is None:
            data = work()
        return data

#######################################################################

class JavLibTypeCache:
    def __init__(self, cachefile):
        self.__cachefile = cachefile

    def save(self, typedict):
        result = None
        try:
            if not t_webtool.fmkdir(os.path.dirname(self.__cachefile)):
                return

            result = t_webtool.fset(self.__cachefile, t_webtool.jdumps(**typedict).encode(r'utf-8'))
        finally:
            return result

    def load(self):
        result = None
        try:
            result = t_webtool.jloads(t_webtool.fget(self.__cachefile).decode(r'utf-8'))
        finally:
            if not result:
                result = dict()
            return result

#######################################################################

def loadtd(kind, typecache):
    typedict = typecache.load()

    pitems = list()
    for k, v in typedict.items():
        if v == kind:
            pitems.append(k)

    for k in pitems:
        typedict.pop(k)

    typecache.save(typedict)
    return typedict

def start_collect(rootpath, dbinfo, kind, url):
    print(r'[LOG] start_collect : %s' % kind)

    typecache = JavLibTypeCache(os.path.join(rootpath, r'typecache.json'))
    typedict = loadtd(kind, typecache)
    if kind in typedict.values():
        print(r'[LOG] start_collect_ignore : %s' % kind)
        return

    tdict, videodict = JavLibSearch.search(url, typedict)
    if tdict:
        JavLibStore.store(rootpath, kind, dbinfo, tdict, videodict)

        for key in tdict.keys():
            typedict[key] = kind

        typecache.save(typedict)

#######################################################################
