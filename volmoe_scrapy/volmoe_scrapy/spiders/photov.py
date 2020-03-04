# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import codecs
import urllib.parse
from volmoe_scrapy.items import PhvScrapyItem



class PhotovSpider(CrawlSpider):
    name = 'photov'
    allowed_domains = ['68aiav.com']
    start_urls = ['http://www.68aiav.com/vodtag/無碼破解版/']

    rules = (
        Rule(LinkExtractor(allow=r'/vod/\d+\.html'),callback='get_play_url'),
        Rule(LinkExtractor(allow=r'/index-\d\.html'),follow=True)
    )
  
    def get_play_url(self,response):
        item = PhvScrapyItem()
        item['title'] = response.xpath('//div[@class="wrap mt20"]//dd[@class="film_title"]/text()').extract_first()
        item['play'] = response.xpath('//div[@class="wrap mt20"]//li/a/@href').extract_first()
        item['play'] = response.urljoin(item['play'])
        item['image_urls'] = response.xpath('//div[@class="wrap mt20"]//img/@data-original').extract_first()
        item['image_urls'] = 'http:' + item['image_urls']
         # 以链接提取器的形式拿url,直接是完整的
        # item['play'] = LinkExtractor(allow=r'/play/\d+-\d-\d\.html').extract_links(response)[0].url
        # item['play'] = LinkExtractor(restrict_xpaths='//div[@class="wrap mt20"]//li/a').extract_links(response)[0].url
        # print(item['play'])

        yield scrapy.Request(
            item['play'],
            callback=self.get_m3u8_url, #获取m3u8的地址
            meta={"item":item}
        )
        
    def get_m3u8_url(self,response):
        item = response.meta['item']
        url_if = re.findall('<script>var player=unescape\("(.*?)"\);',response.body.decode())
        if url_if == []:
            print('这里到底发生了什么??'+item['play'])
        else:
            url_1 = url_if[0]
            url_2 = urllib.parse.unquote(url_1)
            # item['play2'] = 'www.68aiav.com' + url_2
            url_3 = codecs.decode(url_2.split('=')[1],'unicode_escape')
            url_4 = url_3.encode('ISO-8859-1').decode('utf-8')
            item['m3u8'] = url_4
            # print(item['title'])
            # 只有yield或者return item后,才会收集到item也就是输出
            yield item
