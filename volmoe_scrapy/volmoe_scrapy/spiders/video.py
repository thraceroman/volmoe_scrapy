# -*- coding: utf-8 -*-
import scrapy


class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['8080s.net']
    start_urls = ['http://www.8080s.net/movie/search']

    # 带参数的启动爬虫,只需要在构造函数上加上参数即可,
    # 命令行是 scrapy crawl video -a keyword='我是大哥大'
    def __init__(self,keyword=None,**kwargs):
        super(VideoSpider,self).__init__(**kwargs)
        self.keyword = keyword

    # 初始请求,提交搜索的post请求
    def start_requests(self):
        data = {
            'Input':'搜索',
            'search_typeid':'1',
            'skey':self.keyword
        }
        for url in self.start_urls:
            yield scrapy.FormRequest(
            url,
            formdata=data,
            callback=self.parse
            )

    def parse(self, response):
        # 拿详情页的地址
        # /ju/27038
        ju = response.xpath('//div[@class="clearfix noborder"]//a/@href').extract_first()
        url = 'http://www.8080s.net' +ju +'/play/f-1'
        # 这里,其实详情页的页面上还没有云播的页面,就是f-1页面,
        # 但是抓包的时候已经分析出来了,网址是/play/f-1
        # 之后从这个页面中拿到每集的播放页地址,再从地址中拿到m3u8
        yield scrapy.Request(
            url,
            callback=self.every_parse
        )

    def every_parse(self,response):
        lis = response.xpath('//a')
        for li in lis:
            item = {}
            item['title'] = li.xpath('./text()').extract_first()
            href = li.xpath('./@href').extract_first()
            item['href'] = 'http://www.8080s.net' + href
            yield scrapy.Request(
                item['href'],
                callback=self.m3u8,
                meta={'item':item}
            )
    def m3u8(self,response):
        item = response.meta['item']
        # 能拿到这个网址,虽然不是m3u8的,但是同样可以播放
        item['play'] = response.xpath('//div[@id="olpcode"]/iframe/@src').extract_first()
        # https://feifei.feifeizuida.com/share/4f8a318403063fea751813e0991d5bf6
        
        # 20190921/18284_793345db/index.m3u8在javascript的var中,直接拿拿不到,有什么办法???
        # 观察发现,还有这个的poster地址,替换替换应该可以,但是poster也拿不出来
        # item['m3u8'] = response.xpath('')
        # https://feifei.feifeizuida.com/20190921/18284_793345db/index.m3u8
        print(item['title']+item['play'])