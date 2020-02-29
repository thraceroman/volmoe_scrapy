# volmoe_scrapy
先建空仓,后写代码的形式,同样是那个爬取volmoe网站的scrapy项目

### 0.5:按一本为一个item逻辑去实现,并且带有详情页内容爬取,其中遇到的问题  
(1)xpath的跳级模糊拿取时,是会有平行项出现的,尽量先用scrapy shell 进行尝试,其中还有extarct的疑问,什么时候是多个结果  
(2)详情页跳转时,是用scrapy.Request(跳转页url,爬取逻辑,带的数据)  
(3)如此跳转时,scrapy多线程会出现问题,此中原理还有疑问  
(4)一般,spider中只写爬取的逻辑,爬取到的内容再进行修正或保存,在pipelines中进行,正则表达式的使用,和列表的批量操作的写法,用高阶函数?

### 待实现的:0.5  
(1)爬取详情页中的下载地址,这又是一个循环,这里会有线程问题(应该)
>https://volmoe.com/down/10231/1001/0/2/1-0/ 这里是火凤燎原(10231),第一卷(1001,卷都是1打头,话是3打头,3521就是第521话),普通线路(0,2是vip线),epub格式下载(2,1是mobi格式)
(2)分页的实现,两种,一个是类似详情页跳转(直接用scrapy shell进行尝试即可),把下一页的url写入scrapy.Request进行callback=self.parse;另一个是用scrapy框架中的

### 待实现的:0.6
下载页的内容获取,如果直接用爬虫的话只会得到javascript:display_codeinfo( 'e401', 0 ),而不会获取真实的下载页  
原因:只有以用户登录时才会得到下载页面的网址,即可以添加带有用户的cookies,或者发送post请求,但是如何在详情页里发送请求?

### 0.7:使用scarpy的imagepipeline进行图片下载注意事项
1.item的限定格式,必要有images image_urls image_results image_paths 可有image_name  
2.spider中只需要把地址列表放入image_urls中即可,处理是pipelines他自己进行  
3.pipelines中要导ImagesPipeline 和相关的总共3个包,并且其自依赖的是Pillow这个第三方库,需要先pip  
4.同时settings中要开启IMAGES_STORE设置  
5.重载get_media_requests item_completed方法,此时是在IMAGES_STORE\\full下,并且文件名都是默认的  
6.格式化的下载,需要重载file_path方法,在path中写入每一个的样式

### 0.8:使用scrapy_redis进行增量爬虫
1.安装redis server,导scrapy_redis模块  
2.在settings中进行相应配置  
&emsp;DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'  
&emsp;SCHEDULER = 'scrapy_redis.scheduler.Scheduler'  
&emsp;#坑啊,,一定要答对字,这里就是把persist打成了presist,导致一直被清空~~~~~~~~~~~~~~  
&emsp;SCHEDULER_PERSIST = True  
&emsp;REDIS_URL = 'redis://127.0.0.1:6379'  
3.redis查看  
- redis-cli启动
- keys * 查询所有键
- tpye photo2:dupefilter 查询类型
- zcard llen scard看长度
- lrange listname 0 -1 看list的内容
- zrange zsetname 0 -1 看zset的内容
- smembers setname      看set的内容

### 0.81:m3u8的爬取
仍有些问题:
- 爬的时候,play是详情页的网址,这个用shell应该可以找到原因;
- python3的编码问题,转中文算是转不了彻底    

### 0.82:rrys rss的爬取
>http://rss.rrys.tv/rss/feed/26992 悠长假期的磁力链爬取
http://www.rrys2019.com/search/index?keyword=%E6%82%A0%E9%95%BF%E5%81%87%E6%9C%9F
xpath('//div[@class="middle-box"]//ul//li[1]//a/@href').extract_first()
'http://www.rrys2019.com'
加的时候需要判断是否有此资源,可能会none
跳转
xpath('//div[@class="middle-box"]//div[@class="resource-tit"]//h2//a/@href').extract_first()
跳转
xpath('//item')
分组
xpath('.//title/text()').extract_first()
xpath('.//ed2k/text()').extract_first()
xpath('.//magent/text()').extract_first()
xpath('.//pan/text()').extract_first()

>http://pcs.baidu.com/rest/2.0/pcs/file?app_id=778750&method=download&path=/Charlie Chaplin/古/第一季/S01EP11_SP1-笑うカンガルー/S01EP11_SP1-笑うカンガルー.mp4&devuid=百度网盘

>http://pcs.baidu.com/rest/2.0/pcs/file?method=download&devuid=百度网盘&app_id=778750&path=/雪崩_12294950.pdf

### 0.84:爬80s的云播地址
一个简单的requests爬取,额,其实用scrapy也行,直接用shell
data = {'Input':'搜索','search_typeid':'1','skey':'的新生活'}
data = {'Input':'%E6%90%9C%E7%B4%A2','search_typeid':'1','skey':'%E7%9A%84%E6%96%B0%E7%94%9F%E6%B4%BB'}
r = requests.post('http://www.8080s.net/movie/search',data=data)

shell
req = scrapy.FormRequest('http://www.8080s.net/movie/search',formdata=data) 
fetch(req)
ju = response.xpath('//div[@class="clearfix noborder"]//a/@href').extract_first() 
fetch('http://www.8080s.net' + ju)
暂时只能到此,下面的拿不出来,这是因为在线播放是另一个网页,嵌在按钮里,其实就是后面再来/play/f-1
fetch('http://www.8080s.net' + ju + '/play/f-1')

### 0.84待解决:
- 真正的m3u8地址还没爬取到,好像是因为在JavaScript中,拿不出来,用selenium试试
- 搜索词错误的情况如何提示
### 0.85: 80s云播地址爬取完毕
结果是m3u8地址,其中最后一步的js其实就是再经过一次跳转,不过此时跳转到的网址已经是域外的,需要在requests中加入dont_filter=True参数
同时,解决了乱码问题,问题原因是那边用的是ISO的编码,而自己这边是utf-8编码

### 0.9 微博爬取(ajax渲染,数据在json中)
https://m.weibo.cn/u/3214549521
一页10个
https://m.weibo.cn/detail/4475784733009599 每个的内容页
首页,是主页,微博,视频,相册这四个里面的微博的主页观察containerid和u的区别,就是在前面加了107603,具体是个啥
头 100505 主页 230283 微博 107603 相册 107803
https://m.weibo.cn/api/container/getIndex?type=uid&value=3214549521&containerid=1076033214549521
这返回的是个json,其中cardlistInfo中有个since_id记录的是下一页的首个内容id 4475788642893839
a = json.loads(response.text)
a['data']['cardlistInfo']['since_id']
下一页
https://m.weibo.cn/api/container/getIndex?type=uid&value=3214549521&containerid=1076033214549521&since_id=4475788642893839
### 待解决:
- 每条微博的具体内容
- 微博的搜索页面
找人(综合就是weibo 找人就是user 文章就是article 视频就是video 图片就是pic 话题就是 topic)
https://s.weibo.com/user?q=zuzuzuzuzuyangyang
1593400812

### 反爬手段
- headers,proxy,cookies
- 验证码
- js参数加密
- 字体加密

### 爬虫的另一套逻辑:使用selenium自动化工具,这个,不是男人的浪漫,无视掉
> https://www.jianshu.com/p/1b63c5f3c98e