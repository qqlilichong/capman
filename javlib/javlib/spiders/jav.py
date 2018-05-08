
#################################################################

import re
import scrapy

#################################################################


class JavLibSpy(scrapy.Spider):
    name = 'javlibspy'
    start_urls = ['https://www.jianshu.com/p/3d1eb40187ad']
    img_templ = 'https://upload-images.jianshu.io/upload_images/%s?imageMogr2/auto-orient/strip|imageView2/2/w/700'

    #################################################################

    def parse(self, response):
        for img in response.xpath("//div[@class='image-view']/img[1]/@data-original-src").extract():
            img_name = re.search('//upload-images.jianshu.io/upload_images/(.*)$', img)
            if not img_name:
                continue
            yield {
                'img_url': self.img_templ % img_name.group(1),
                'img_name': img_name.group(1),
            }

    #################################################################


#################################################################
