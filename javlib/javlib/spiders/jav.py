
import scrapy


class JavLibSpy(scrapy.Spider):
    name = 'javlibspy'
    start_urls = ['https://hao.360.cn']

    def parse(self, response):
        yield {'url': response.url}
