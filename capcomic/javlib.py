
#######################################################################

import os
import re
import webtool

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

            self.__model = self.__update(model, url, kind)
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
    def __update(model, url, kind):
        model[r'video_url'] = webtool.http_urlfpath(url)
        model[r'video_kind'] = kind
        model[r'video_type'] = re.findall(r'[a-zA-Z]+', model[r'video_id'])[0]
        model[r'video_number'] = re.findall(r'\d+', model[r'video_id'])[0]
        model[r'video_relpath'] = r'%s/%s' % (model[r'video_kind'], model[r'video_type'])
        model[r'video_localfile'] = r'%s/%s.jpg' % (model[r'video_relpath'], model[r'video_id'])
        return model

    @staticmethod
    def __video_id(div):
        return div.find(r'td', r'text').get_text().strip().upper()

    @staticmethod
    def __video_title(div):
        return div.a.get_text().strip()

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
