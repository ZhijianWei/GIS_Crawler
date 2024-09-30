
# -*- coding: utf-8 -*-

# 本文件为爬虫中间件，用于处理动态网页内容的加载，用Selenium库来模拟浏览器操作，以便获取JavaScript动态生成的内容。
# 更多信息请参考文档:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy  # 导入Scrapy库
from selenium import webdriver  # 导入Selenium的webdriver，用于浏览器自动化
from selenium.common.exceptions import TimeoutException  # 导入Selenium的超时异常
from selenium.webdriver.common.by import By  # 导入Selenium的By类，用于定位元素
from selenium.webdriver.support.ui import WebDriverWait  # 导入WebDriverWait，用于等待条件成立
from selenium.webdriver.support import expected_conditions as EC  # 导入expected_conditions，用于定义等待条件
from scrapy.http import HtmlResponse  # 导入Scrapy的HtmlResponse，用于返回网页响应
from logging import getLogger  # 导入Python的logging库，用于获取日志记录器
from time import sleep  # 导入time库的sleep函数，可能用于暂停执行

class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        """
        初始化Selenium中间件。

        :param timeout: 超时时间设置。
        :param service_args: 启动Selenium服务时传递的参数列表。
        """
        self.logger = getLogger(__name__)  # 获取日志记录器
        self.timeout = timeout  # 设置超时时间
        self.browser = webdriver.PhantomJS(service_args=service_args)  # 创建PhantomJS浏览器实例
        self.browser.set_window_size(1400, 700)  # 设置浏览器窗口大小
        self.browser.set_page_load_timeout(self.timeout)  # 设置页面加载超时时间
        self.wait = WebDriverWait(self.browser, self.timeout)  # 创建WebDriverWait实例

    def __del__(self):
        """
        析构函数，确保在对象销毁时关闭浏览器。
        """
        self.browser.close()  # 关闭浏览器

    def process_request(self, request, spider):
        """
        处理请求，使用Selenium获取动态加载的页面内容。

        :param request: Scrapy的请求对象。
        :param spider: 爬虫实例。
        """
        self.logger.debug('PhantomJs is Starting')  # 记录调试信息
        type = request.meta.get('type', 1)  # 从请求元数据中获取类型，默认为1
        try:
            # 访问URL
            self.browser.get(request.url)  # 使用Selenium访问请求的URL

            self.wait.until(EC.presence_of_element_located(  # 等待页面元素出现
                (By.CSS_SELECTOR, '.headerWrap .content')))  # 指定CSS选择器
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)  # 返回页面内容
        except TimeoutException:
            # 超时异常处理
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        """
        类方法，用于从爬虫实例创建中间件实例。

        :param crawler: 爬虫实例。
        """
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),  # 从爬虫设置中获取超时时间
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))  # 从爬虫设置中获取PhantomJS服务参数



