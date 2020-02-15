# -*- coding: utf-8 -*-
import scrapy


class PhotoSpider(scrapy.Spider):
    name = 'photo'
    allowed_domains = ['68aiav.com']
    start_urls = ['http://www.68aiav.com/newslist/41']

    def parse(self, response):
        pass
