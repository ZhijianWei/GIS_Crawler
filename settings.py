# -*- coding: utf-8 -*-

# 本文件为Scrapy设置文件，用于GIS_Crawler项目，包含一些重要或常用的设置。

# 更多设置请参考官方文档：
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'GIS_Crawler'  # 定义爬虫项目的名称

SPIDER_MODULES = ['GIS_Crawler.spiders']  # 指定存储爬虫代码的模块位置
NEWSPIDER_MODULE = 'GIS_Crawler.spiders'  # 指定新爬虫的默认模块

# 通过用户代理识别自己，负责任地爬取（默认的用户代理）
#USER_AGENT = 'GIS_Crawler (+http://www.yourdomain.com)'  # 可以通过设置此项来自定义用户代理字符串

# 是否遵守robots.txt规则
ROBOTSTXT_OBEY = False  # 设置为False表示不遵守robots.txt文件的规则

# 配置Scrapy执行的最大并发请求数（默认为16）
#CONCURRENT_REQUESTS = 32  # 可以通过此项来调整并发请求的数量

# 配置对同一网站的请求之间的延迟（默认为0秒）
#DOWNLOAD_DELAY = 3  # 设置请求延迟，以秒为单位
# 下面两个设置只会生效一个：
#CONCURRENT_REQUESTS_PER_DOMAIN = 16  # 每个域名的并发请求数
#CONCURRENT_REQUESTS_PER_IP = 16  # 每个IP的并发请求数

# 禁用cookies（默认启用）
#COOKIES_ENABLED = False  # 禁用cookies

# 禁用Telnet控制台（默认启用）
#TELNETCONSOLE_ENABLED = False  # 禁用Telnet控制台

# 覆盖默认的请求头
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# 开启或禁用爬虫中间件
# SPIDER_MIDDLEWARES = {
#    'GIS_Crawler.middlewares.GIS_CrawlerSpiderMiddleware': 543,
# }

# 开启或禁用下载器中间件
# DOWNLOADER_MIDDLEWARES = {
#    'GIS_Crawler.middlewares.GIS_CrawlerDownloaderMiddleware': 543,
# }

# 开启或禁用扩展
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# 配置项目中的Item Pipelines
ITEM_PIPELINES = {
    'GIS_Crawler.pipelines.MySqlPipeLine': 300,  # 启用MySQL Pipeline，并设置优先级
    # 'GIS_Crawler.pipelines.MongoPipeline': 300,  # 注释掉的MongoDB Pipeline
}

# 开启和配置下载器中间件
DOWNLOADER_MIDDLEWARES = {
    'GIS_Crawler.middlewares.SeleniumMiddleware': 543,  # 自定义的Selenium下载器中间件
}

# MongoDB的连接设置
MONGO_URI = 'localhost'  # MongoDB服务器地址
MONGO_DB = 'COVID19'  # MongoDB数据库名称

# MySQL的连接设置
MYSQL_HOST = 'localhost'  # MySQL服务器地址
MYSQL_DB = 'covid19'  # MySQL数据库名称
MYSQL_USER = 'root'  # MySQL用户名
MYSQL_PASSWORD = '123456'  # MySQL密码
MYSQL_PORT = 3306  # MySQL端口

# Selenium的超时设置
SELENIUM_TIMEOUT = 20  # Selenium超时时间（秒）

# PhantomJS服务参数
PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']  # PhantomJS服务参数，禁止加载图片，启用磁盘缓存