
#######################################################################

import os
import re
import webtool

#######################################################################

class JavLibDetail:
    def __init__(self, url):
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
        self.load(url)

    def load(self, url):
        self.model = None
        try:
            model = webtool.mkd(
                video_url=webtool.http_urlfpath(url)
            )

            for div in webtool.bs4get(url).findAll(r'div', id=re.compile(r'video_\w+')):
                divid = div[r'id']
                if divid in self.divs:
                    model[divid] = self.divs[divid](div)

            self.model = model
        finally:
            return self.model

    def saveimg(self, filename):
        result = None
        try:
            if not webtool.fmkdir(os.path.dirname(filename)):
                return

            if not webtool.http_download(self.model['video_jacket'], filename):
                return

            result = True
        finally:
            return result

    @staticmethod
    def video_id(div):
        return div.find(r'td', r'text').get_text().strip()

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
            href = it[r'href']
            result.append((re.match(r'.*\?(.*)', href).group(1), href, it.get_text().strip()))
        return result

#######################################################################
