# -*- coding: utf-8 -*-
import scrapy
# import wget
import requests
import re
import os


class PhotoSpider(scrapy.Spider):
    name = 'photo'
    allowed_domains = ['68aiav.com']
    # 首页和vodlist是一样的层级结构
    # start_urls = ['http://www.68aiav.com']
    start_urls = ['http://www.68aiav.com/vodlist/56']
    # http://www.68aiav.com/vodtag/259LUXU/index-2.html
    # start_urls = ['http://www.68aiav.com/newslist/38']

    def parse(self, response):
        # 找到分类头层,注意是要以有多个的那层,vodlist
        title_li = response.xpath('//div[@class="wrap mt20"]//li')
        for title in title_li:
            # 建一个字典,
            item = {}
            item['title'] = title.xpath('.//h3/text()').extract_first()
            item['date'] = title.xpath('.//dt/text()').extract_first()
            item['href'] = title.xpath('.//a/@href').extract_first()
            # 注意这里的url,只有是首页的时候可以
            item['href'] = response.url + item['href']
            item['img'] = "http:"+ title.xpath('.//img/@data-original').extract_first()
            # img_name = re.findall('.*?/(\d+).html',item['href'])
            # 结尾一定要带\\
            img_file = 'D:\\code\\photo\\' + item['title'][:6] +'.jpg'
            img = requests.get(item['img'])
            with open(img_file,'wb') as img_out:
                img_out.write(img.content)
            # wget有时会被网站发现,可以在wget中加代理,但是这里怎么加
            # wget.download(item['img'],img_file)
            print(item)

        # newslist的层级结构,需要剔除
        # title_li = response.xpath('//div[@class="wrap mt20"]//li/a[text()!=""]')
        # for title in title_li:
        #     # 建一个字典,
        #     item = {}
        #     # 这里已经直接剔除了前两个广告的标题
        #     item['title'] = title.xpath('./text()').extract_first()
        #     # 注意这里需要匹配,其中有前两个是不符合要求的(页面里他们是红色大号的,也就是a直接下层的text为空)
        #     item['date'] = title.xpath('./span/text()').extract_first()
        #     item['href'] = title.xpath('./@href').extract_first()
        #     item['href'] = 'http://www.68aiav.com' + item['href']
        #     # print(item)
        #     # 详情页
        #     yield scrapy.Request(
        #         item['href'],
        #         callback=self.parse_detail,
        #         meta = {'item':item}
        #     )

    def parse_detail(self,response):
        item = response.meta['item']
        item['img'] = response.xpath('//div[@class="wrap mt20"]//img/@src').extract()
        # print(item)
        # 下载图片,这里其实应该放在piplines里
        img_dir = 'D:\\code\\photo\\' + item['title'][:10]
        os.mkdir(img_dir)
        for img_url in item['img']:
            img = requests.get(img_url)
            img_file = img_dir + '\\' + img_url[-7:]
            with open(img_file,'wb') as handler:
                handler.write(img.content)
            print(img_url[-7:])
        

