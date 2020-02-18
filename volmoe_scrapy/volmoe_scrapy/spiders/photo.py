# -*- coding: utf-8 -*-
import scrapy
# import wget
import requests
import re


class PhotoSpider(scrapy.Spider):
    name = 'photo'
    allowed_domains = ['68aiav.com']
    # 首页和vodlist是一样的层级结构
    start_urls = ['http://www.68aiav.com/vodlist/56']

    def parse(self, response):
        #找到分类头层,注意是要以有多个的那层
        title_li = response.xpath('//div[@class="wrap mt20"]//li')
        for title in title_li:
            # 建一个字典,
            item = {}
            item['title'] = title.xpath('.//h3/text()').extract_first()
            item['date'] = title.xpath('.//dt/text()').extract_first()
            item['href'] = title.xpath('.//a/@href').extract_first()
            item['href'] = response.url + item['href']
            item['img'] = "http:"+ title.xpath('.//img/@data-original').extract_first()
            # img_name = re.findall('.*?/(\d+).html',item['href'])
            # 结尾一定要带\\
            img_file = 'D:\\code\\photo\\' + item['title'][:6] +'.jpg'
            img = requests.get(item['img'])
            open(img_file, 'wb').write(img.content)
            # wget有时会被网站发现,可以在wget中加代理,但是这里怎么加
            # wget.download(item['img'],img_file)
            print(item)