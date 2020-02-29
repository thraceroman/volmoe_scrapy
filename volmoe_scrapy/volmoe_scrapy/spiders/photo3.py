# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.parse
import codecs

class Photo3Spider(scrapy.Spider):
    name = 'photo3'
    allowed_domains = ['68aiav.com']
    start_urls = ['http://www.68aiav.com/vodtag/JULIA']

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
            # http://www.68aiav.com/vod/122987.html 这个会有中文解码问题,从play_url开始
            # 下级的是 http://www.68aiav.com/play/122987-5-1.html

            # 得到的url_2是/Public/player/player5.html?url=\\x68\\x74\\x74形式,
            # 中文部分是\\xe8\\xae\\xa9\\xe5\\xa5\\xb3开始的,这是unicode码
            # 911解码上对应的是\u8BA9\u5973
            # 即,,问题是如何把3个\x转成2个\u
            url_2 = urllib.parse.unquote(url_1)
            item['play2'] = 'www.68aiav.com' + url_2
            # 真正的m3u8地址在url后面,还需要一步解码
            # 注意,视频2区的不是m3u8格式的,字符串解码是一样的,不过地址无法看
            # 还有些其中带有中文,\x20\xe8\xae\xa9\xe5\xa5\xb3\xe6\x95\x99\xe5\xb8\x88\xe5\xa4\xa7\xe6\xa1\xa5\xe6\x9c\xaa\xe4\xb9\x85\xe6\xbd\xae\xe5\x90\xb9\xe5\x90\xa7\x20\xe5\xa4\xa7\xe6\xa9\x8b\xe6\x9c\xaa\xe4\xb9\x85\x20\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97\xe5\xb9\x95\x2f\x69\x6e\x64\x65\x78\x2e\x6d\x33\x75\x38
            # 直接解码中文会成乱码,è®©这里表示的其实是'\xe8\xae\xa9',
            url_3 = codecs.decode(url_2.split('=')[1],'unicode_escape')
            # 即,只需要encode,这里面,居然是要用ISO-8859-1,
            url_4 = url_3.encode('ISO-8859-1').decode('utf-8')
            item['m3u8'] = url_4
            # yield item
            # 这里的所有逻辑也可以放在pipeline中
            # 表m3u8 http://videocdn2.quweikm.com:8091/20181125/A77nMnXk/index.m3u8
            # 里m3u8 1000kb/hls/index.m3u8 有的是500kb/hls/index.m3u8
            # 里还有key,有的key是完整的,有的是只有最后的key
            if item['m3u8'].endswith('.m3u8'):
                yield scrapy.Request(
                    item['m3u8'],
                    callback=self.m3u8_url_li,
                    meta={'item':item},
                    # 从这里开始,其实就已经不是域内网页了,
                    dont_filter=True
                )
            # http://cdn3.senhaige.com:8091/20180803/fOrTzIdd/index.m3u8 这个访问不了 报error
            # print(item['m3u8'])
        
    def m3u8_url_li(self,response):
        item = response.meta['item']
        # 这里!!!!有的index文件里面最后一行会手贱的打空行,所以不能用[-1]
        text = response.text.split('\n')[2]
        # 还有可能会结尾有问题hls/index.m3u8#EXT-X-TARGETDURATION:2
        item['m3u8_li'] = response.urljoin(text).split('#')[0]

        yield item
        # yield scrapy.Request(
        #     item['m3u8_li'],
        #     callback=self.m3u8_url_key,
        #     meta={'item':item},
        #     dont_filter=True
        # )
    # def m3u8_url_key(self,response):
    #     item = response.meta['item']
    #     key_if = re.findall('URI="(.*?)"',response.text)
    #     if key_if != []:
    #         key = re.findall('URI="(.*?)"',response.text)[0]
    #         item['m3u8_key'] = response.urljoin(key)
    #         # 这里用的逻辑是所有的页面内容全在spider中写,key和m3u8的内容也一并放在item中,
    #         # pipeline中只有把这两个拿出来写入本地的逻辑
    #         # 也可以把拿key等的逻辑写在pipeline中,看pipeline中进行跳转时方法怎么写参数
    #         item['m3u8_index_text'] = response.text
    #         yield scrapy.Request(
    #             item['m3u8_key'],
    #             callback=self.m3u8_url_key_text,
    #             meta={'item':item},
    #             dont_filter=True
    #         )
    #     else:
    #         # 测试,实际的时候要在这里加yield item
    #         # yield item
    #         print('这个没加密:'+item['m3u8_li'])    

    # def m3u8_url_key_text(self,response):
    #     item = response.meta['item']
    #     item['m3u8_key_text'] = response.text
    #     # 测试
    #     print(item['title'])
    #     print(item['m3u8_li'])
    #     print(item['m3u8_key']+'  '+str(len(item['m3u8_index_text'])))
    #     # yield item    

        

