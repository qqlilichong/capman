# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#################################################################

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

#################################################################


class JavlibPipeline(ImagesPipeline):

    #################################################################

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        return 'blog/jianshu/' + item['img_name']

    #################################################################

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['img_url'], meta={'item': item})

    #################################################################

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images.')
        print('ok : ' + image_paths[0])

    #################################################################


#################################################################
