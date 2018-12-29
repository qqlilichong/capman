
#######################################################################

import os
import re
import webtool

#######################################################################

class JavLibDetail:
    def __init__(self, url, kind):
        self.divs = webtool.mkd(
            video_id=self.video_id,
            video_title=self.video_title,
            video_jacket=self.video_jacket,
            video_date=self.video_date,
            video_length=self.video_length,
            video_maker=self.video_items,
            video_label=self.video_items,
            video_cast=self.video_items,
        )

        self.model = None
        self.load(url, kind)

    def load(self, url, kind):
        self.model = None
        try:
            model = dict()
            for div in webtool.bs4get(url).findAll(r'div', id=re.compile(r'video_\w+')):
                divid = div[r'id']
                if divid in self.divs:
                    model[divid] = self.divs[divid](div)

            self.model = self.update(model, url, kind)
        finally:
            return self.model

    def saveimg(self, rootpath):
        result = None
        filename = None
        try:
            if not self.model:
                return

            if not webtool.fmkdir(os.path.join(rootpath, self.model[r'video_relpath'])):
                return

            filename = os.path.join(rootpath, self.model[r'video_localfile'])
            result = webtool.http_download(self.model[r'video_jacket'], filename)
        finally:
            if not result:
                webtool.fremove(filename)

            return result

    def savemodel(self, dbs):
        result = None
        try:
            if not self.model:
                return

            for tname in (r'maker', r'label', r'cast'):
                for model in self.model[r'video_%s' % tname]:
                    if not dbs.replace(tname, **model):
                        return

            if not dbs.commit():
                return

            result = True
        finally:
            return result

    @staticmethod
    def update(model, url, kind):
        model[r'video_url'] = webtool.http_urlfpath(url)
        model[r'video_kind'] = kind
        model[r'video_type'] = re.findall(r'[a-zA-Z]+', model[r'video_id'])[0]
        model[r'video_number'] = re.findall(r'\d+', model[r'video_id'])[0]
        model[r'video_relpath'] = r'%s/%s' % (model[r'video_kind'], model[r'video_type'])
        model[r'video_localfile'] = r'%s/%s.jpg' % (model[r'video_relpath'], model[r'video_id'])
        return model

    @staticmethod
    def video_id(div):
        return div.find(r'td', r'text').get_text().strip().upper()

    @staticmethod
    def video_title(div):
        return div.a.get_text().strip()

    @staticmethod
    def video_jacket(div):
        return div.img[r'src'].strip()

    @staticmethod
    def video_date(div):
        return div.find(r'td', r'text').get_text().strip()

    @staticmethod
    def video_length(div):
        return div.find(r'td', r'').get_text().strip()

    @staticmethod
    def video_items(div):
        result = list()
        for it in div.findAll(r'a'):
            result.append(webtool.mkd(
                id=re.match(r'.*\?(.*)', it[r'href']).group(1),
                url=r'',
                name=it.get_text().strip()
            ))
        return result

#######################################################################
