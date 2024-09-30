# -*- coding: utf-8 -*-

import scrapy  # 导入Scrapy库，用于创建爬虫
from GIS_Crawler_WZJ.items import GIS_CrawlerItem  # 导入项目中定义的Item
from scrapy.selector import Selector  # 导入Scrapy的选择器，用于解析响应内容
from time import sleep  # 导入time库的sleep函数，可能用于在请求间添加延迟

class GIS_Crawler(scrapy.Spider):
    name = 'Cname'  # 定义爬虫名称
    allowed_domains = ['https://example.com']  # 定义允许爬取的域名列表
    start_urls = ['https://example.com']  # 定义起始URL列表

    def start_requests(self):
        # 该方法在爬虫开始时调用，用于生成初始请求
        url = self.allowed_domains[0] + '/latitude_longitude/'  # 构建初始请求的URL
        yield scrapy.Request(url, callback=self.parse, meta={'type': 0}, dont_filter=True)  # 生成请求并指定解析方法

    def parse(self, response):
        # 该方法用于解析爬虫响应
        countries = response.xpath(
            '/html/body/div/div[2]/div[1]/a[@class="links"]').extract()  # 使用XPath选择器提取国家链接
        for country in countries:
            countryItem = GIS_CrawlerItem()  # 创建一个新的Item实例
            countryNode = Selector(text=country)  # 使用选择器包装国家元素
            nextUrl = countryNode.xpath('//@href').extract_first().strip()  # 提取国家链接
            countryItem['name'] = countryNode.xpath(
                '//h5//text()').extract_first()  # 提取国家名称
            countryItem['parent'] = ''  # 设置父级字段
            countryItem['type'] = response.meta.get('type')  # 获取meta中的类型信息
            countryItem['sname'] = nextUrl.split('/')[-1]  # 提取链接中的最后一部分作为sname
            countryItem['lng'] = ''  # 设置经度字段
            countryItem['lat'] = ''  # 设置纬度字段

            if nextUrl:  # 如果存在下一级URL
                yield scrapy.Request(self.allowed_domains[0] + nextUrl, callback=self.parse_state, meta={'type': 1}, dont_filter=True)  # 生成新的请求

            yield countryItem  # 将提取到的国家信息yield出去

    def parse_state(self, response):
        # 该方法用于解析州/省级别的响应
        lngLatEle = response.xpath(
            '/html/body/div/div[2]/div[1]/div[@class="searchMatch"]').extract_first()  # 提取包含经纬度信息的元素
        if lngLatEle:
            cities = response.xpath(
                '/html/body/div/div[2]/div[1]/*[@class="links" and not(@itemprop="breadcrumb")]').extract()  # 提取城市链接
            title = response.xpath(
                '/html/body/div/div[2]/div[1]/h1[@class="description"]//text()').extract_first()  # 提取标题

            i = 0  # 初始化计数器
            for index in range(len(cities)):  # 遍历城市链接
                if i == index:
                    cityItem = GIS_CrawlerItem()  # 创建一个新的Item实例
                    url = Selector(text=cities[index]).xpath(
                        '//@href').extract_first().strip()  # 提取城市链接
                    cityItem['name'] = Selector(text=cities[index]).xpath(
                        '//h5//text()').extract_first()  # 提取城市名称
                    cityItem['parent'] = title  # 设置父级字段
                    cityItem['type'] = response.meta.get('type')  # 获取meta中的类型信息
                    cityItem['sname'] = url.split('/')[-1]  # 提取链接中的最后一部分作为sname
                    cityItem['lng'] = Selector(
                        text=cities[index + 2]).xpath('//span//text()').extract_first().strip()  # 提取经度
                    cityItem['lat'] = Selector(
                        text=cities[index + 2]).xpath('//h5//text()').extract_first().strip()  # 提取纬度
                    i += 3  # 更新计数器
                    yield cityItem  # 将提取到的城市信息yield出去

        else:
            states = response.xpath(
                '/html/body/div/div[2]/div[1]/a[@class="links" and not(@itemprop="breadcrumb")]').extract()  # 提取州/省链接
            title = response.xpath(
                '/html/body/div/div[2]/div[1]/h1[@class="description"]//text()').extract_first()  # 提取标题
            for state in states:
                stateItem = GIS_CrawlerItem()  # 创建一个新的Item实例
                stateNode = Selector(text=state)  # 使用选择器包装州/省元素
                nextUrl = stateNode.xpath('//@href').extract_first().strip()  # 提取州/省链接
                stateItem['name'] = stateNode.xpath(
                    '//h5//text()').extract_first()  # 提取州/省名称
                stateItem['parent'] = title  # 设置父级字段
                stateItem['type'] = response.meta.get('type')  # 获取meta中的类型信息
                stateItem['sname'] = nextUrl.split('/')[-1]  # 提取链接中的最后一部分作为sname
                stateItem['lng'] = ''  # 设置经度字段
                stateItem['lat'] = ''  # 设置纬度字段

                if nextUrl:  # 如果存在下一级URL
                    yield scrapy.Request(self.allowed_domains[0] + nextUrl, callback=self.parse_city, meta={'type': 2},  dont_filter=True)  # 生成新的请求
                yield stateItem  # 将提取到的州/省信息yield出去

    def parse_city(self, response):
        # 该方法用于解析城市级别的响应
        cities = response.xpath(
            '/html/body/div/div[2]/div[1]/*[@class="links" and not(@itemprop="breadcrumb")]').extract()  # 提取城市链接
        title = response.xpath(
            '/html/body/div/div[2]/div[1]/h1[@class="description"]//text()').extract_first()  # 提取标题
        i = 0  # 初始化计数器
        for index in range(len(cities)):  # 遍历城市链接
            if i == index:
                cityItem = GIS_CrawlerItem()  # 创建一个新的Item实例
                url = Selector(text=cities[index]).xpath(
                    '//@href').extract_first().strip()  # 提取城市链接
                cityItem['name'] = Selector(text=cities[index]).xpath(
                    '//h5//text()').extract_first()  # 提取城市名称
                cityItem['parent'] = title  # 设置父级字段
                cityItem['type'] = response.meta.get('type')  # 获取meta中的类型信息
                cityItem['sname'] = url.split('/')[-1]  # 提取链接中的最后一部分作为sname
                cityItem['lng'] = Selector(
                    text=cities[index + 2]).xpath('//span//text()').extract_first().strip()  # 提取经度
                cityItem['lat'] = Selector(
                    text=cities[index + 2]).xpath('//h5//text()').extract_first().strip()  # 提取纬度
                i += 3  # 更新计数器
                yield cityItem  # 将提取到的城市信息yield出去