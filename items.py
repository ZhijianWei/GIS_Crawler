# -*- coding: utf-8 -*-

# 定义Scrapy项目中用于存储抓取数据的容器模型
#
# 更多信息请参考Scrapy官方文档:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy  # 导入Scrapy库，以便使用Scrapy提供的类和方法


class GIS_CrawlerItem(scrapy.Item):
    """
    GIS_CrawlerItem类用于定义爬虫抓取到的数据结构。
    它继承自Scrapy的Item类，可以定义多个字段来存储不同类型的数据。
    """

    # 定义数据存储的目标集合或表名
    # 注意：实际上Scrapy不会自动创建数据库表，这个字段通常用于Item Pipeline中的数据存储逻辑
    collection = scrapy.Field()  # 定义一个名为'collection'的字段
    table = 'dict_geo'  # 指定表名

    # 定义要抓取的字段及其类型
    name = scrapy.Field()  # 定义一个名为'name'的字段，用于存储地名或其他名称
    parent = scrapy.Field()  # 定义一个名为'parent'的字段，可能用于存储父级名称或分类
    sname = scrapy.Field()  # 定义一个名为'sname'的字段，可能用于存储标准化的名称
    lng = scrapy.Field()  # 定义一个名为'lng'的字段，用于存储经度信息
    lat = scrapy.Field()  # 定义一个名为'lat'的字段，用于存储纬度信息
    type = scrapy.Field()  # 定义一个名为'type'的字段，可能用于存储类型信息

    # pass表示类定义结束，没有更多的方法或属性要添加
    # 在Python类定义中，pass是一个空操作符，用于占位，表示类定义结束
    pass