# -*- coding: utf-8 -*-
import scrapy
from volmoe_scrapy.items import PhScrapyItem

class Photo2Spider(scrapy.Spider):
    name = 'photo2'
    allowed_domains = ['68aiav.com']
    start_urls = ['http://www.68aiav.com/newslist/44']

    def parse(self, response):
        title_li = response.xpath('//div[@class="wrap mt20"]//li/a[text()!=""]')
        for title in title_li:
            # 建一个字典,
            item = PhScrapyItem()
            # 这里已经直接剔除了前两个广告的标题
            item['title'] = title.xpath('./text()').extract_first()
            # 注意这里需要匹配,其中有前两个是不符合要求的(页面里他们是红色大号的,也就是a直接下层的text为空)
            item['date'] = title.xpath('./span/text()').extract_first()
            item['href'] = title.xpath('./@href').extract_first()
            item['href'] = 'http://www.68aiav.com' + item['href']
            # 替代之前的自己建文件夹
            item['image_name'] = item['title'][:10]
            # print(item)
            # 详情页
            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,
                meta = {'item':item}
            )
    def parse_detail(self,response):
        item = response.meta['item']
        # print(item)
        # img必须的image_name,image_urls
        item['image_urls'] = response.xpath('//div[@class="wrap mt20"]//img/@src').extract()
        # 测试:只要前5张的
        # item['image_urls'] = item['image_urls'][:1]
        # print(item)
        # 之后的操作,下载图片和图片的命名,都在pipeline中实现
        yield item