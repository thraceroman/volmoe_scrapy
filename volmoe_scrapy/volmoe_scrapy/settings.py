# -*- coding: utf-8 -*-

# Scrapy settings for volmoe_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'volmoe_scrapy'

SPIDER_MODULES = ['volmoe_scrapy.spiders']
NEWSPIDER_MODULE = 'volmoe_scrapy.spiders'

LOG_LEVEL = "WARNING"

# 使用redis进行去重或分布式操作,只有这4行就能进行简单的增量爬虫,用shell时,,提示这里关闭,,是什么问题?
# DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# # 坑啊,,一定要答对字,这里就是把persist打成了presist,导致一直被清空~~~~~~~~~~~~~~
# SCHEDULER_PERSIST = True
# REDIS_URL = 'redis://127.0.0.1:6379'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'volmoe_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False
# DEPTH_LIMIT = 6
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'volmoe_scrapy.middlewares.VolmoeScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'volmoe_scrapy.middlewares.VolmoeScrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'volmoe_scrapy.pipelines.VolmoeScrapyPipeline': 300,
   'volmoe_scrapy.pipelines.VodtagScrapyPipeline':300
   # 这里是把item存入redis,而不是指纹
   # 'scrapy_redis.pipelines.RedisPipeline':400,
   # 'volmoe_scrapy.pipelines.PhScrapyPipeline': 300
}
IMAGES_STORE = 'D:\\code\\photo'

# 顺序输出?
FEED_EXPORT_FIELDS = ["title", "play", "m3u8"]
#下载超时退出
DOWNLOAD_TIMEOUT = 10

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
