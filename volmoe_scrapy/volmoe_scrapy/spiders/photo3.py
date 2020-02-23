# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.parse
import codecs

class Photo3Spider(scrapy.Spider):
    name = 'photo3'
    allowed_domains = ['68aiav.com']
    start_urls = ['http://www.68aiav.com/vodtag/未久']

    def parse(self, response):
        title_li = response.xpath('//div[@class="wrap mt20"]//li')
        for title in title_li:
            item = {}
            item['title'] = title.xpath('.//h3/text()').extract_first()
            item['date'] = title.xpath('.//dt/text()').extract_first()
            item['href'] = title.xpath('.//a/@href').extract_first()
            item['href'] = 'http://www.68aiav.com' + item['href']
            item['img'] = "http:"+ title.xpath('.//img/@data-original').extract_first()

            yield scrapy.Request(
                item["href"],
                callback=self.play_url, #跳转到播放器页面
                meta = {"item":item} 
            )
            
    def play_url(self,response):
        item = response.meta['item']
        # <a href="/play/137159-5-1.html" target="_blank">全集</a>
        item['play'] = response.xpath('//div[@class="wrap mt20"]//li/a/@href').extract_first()
        item['play'] = 'http://www.68aiav.com' +item['play']
        yield scrapy.Request(
            item['play'],
            callback=self.m3u8_url, #获取m3u8的地址
            meta={"item":item}
        )
    def m3u8_url(self,response):
        item = response.meta['item']
        # m3u8 = response.xpath('//')
        # 得到的url_1是%2f%50%75%62%6c%69%63%2f%7形式,
        # ?????有的时候会报这里有问题,有的时候不会??????
        url_if = re.findall('<script>var player=unescape\("(.*?)"\);',response.body.decode())
        if url_if == []:
            print(item['play'])
        else:
            url_1 = url_if[0]
            # 需要进行unescape解码
            # 得到的url_2是/Public/player/player5.html?url=\\x68\\x74\\x74形式,
            url_2 = urllib.parse.unquote(url_1)
            item['play2'] = 'www.68aiav.com' + url_2
            # 真正的m3u8地址在url后面,还需要一步解码
            # 注意,视频2区的不是m3u8格式的,字符串解码是一样的,不过地址无法看
            # 还有些其中带有中文,\x20\xe8\xae\xa9\xe5\xa5\xb3\xe6\x95\x99\xe5\xb8\x88\xe5\xa4\xa7\xe6\xa1\xa5\xe6\x9c\xaa\xe4\xb9\x85\xe6\xbd\xae\xe5\x90\xb9\xe5\x90\xa7\x20\xe5\xa4\xa7\xe6\xa9\x8b\xe6\x9c\xaa\xe4\xb9\x85\x20\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97\xe5\xb9\x95\x2f\x69\x6e\x64\x65\x78\x2e\x6d\x33\x75\x38
            # 直接解码中文会成乱码,暂时还木偶办法
            url_3 = codecs.decode(url_2.split('=')[1],'unicode_escape')
            item['m3u8'] = url_3
            yield item
        

        

