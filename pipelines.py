
# -*- coding: utf-8 -*-

# 定义项目中的两个Item Pipeline类，一个用于将抓取的数据存储到MongoDB中，另一个用于存储到MySQL数据库中。
# 每个类都实现了`__init__`、`from_crawler`、`open_spider`、`process_item`和`close_spider`方法，用于在爬虫的不同阶段执行特定的操作
# 要激活这个Pipeline，需要在项目的设置中添加到ITEM_PIPELINES
# 更多信息请参考文档: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo  # 导入pymongo库，用于操作MongoDB
import pymysql  # 导入pymysql库，用于操作MySQL数据库


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        """
        MongoPipeline的初始化方法。

        :param mongo_uri: MongoDB服务器的URI。
        :param mongo_db: 要操作的MongoDB数据库名称。
        """
        self.mongo_uri = mongo_uri  # MongoDB服务器URI
        self.mongo_db = mongo_db  # MongoDB数据库名称

    @classmethod
    def from_crawler(cls, crawler):
        """
        类方法，用于从Crawler对象创建Pipeline实例。
        :param crawler: Crawler对象。
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),  # 从Crawler的设置中获取MongoDB的URI
            mongo_db=crawler.settings.get('MONGO_DB')  # 从Crawler的设置中获取MongoDB的数据库名称
        )

    def open_spider(self, spider):
        """
        当爬虫开启时调用的方法。
        :param spider: 爬虫实例。
        """
        self.client = pymongo.MongoClient(self.mongo_uri)  # 创建MongoDB客户端连接
        self.db = self.client[self.mongo_db]  # 选择MongoDB数据库

    def process_item(self, item, spider):
        """
        处理每个Item的方法。
        :param item: 爬取到的Item对象。
        :param spider: 爬虫实例。
        """
        self.db[item.collection].insert(dict(item))  # 将Item插入到对应的MongoDB集合中
        return item  # 返回Item对象

    def close_spider(self, spider):
        """
        当爬虫关闭时调用的方法。
        :param spider: 爬虫实例。
        """
        self.client.close()  # 关闭MongoDB客户端连接


class MySqlPipeline(object):
    def __init__(self, host, database, user, password, port):
        """
        MySqlPipeline的初始化方法。

        :param host: MySQL服务器的主机名或IP地址。
        :param database: 要操作的MySQL数据库名称。
        :param user: MySQL数据库的用户名。
        :param password: MySQL数据库的密码。
        :param port: MySQL服务器的端口号。
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        """
        类方法，用于从Crawler对象创建Pipeline实例。
        :param crawler: Crawler对象。
        """
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),  # 从Crawler的设置中获取MySQL的主机名或IP地址
            database=crawler.settings.get('MYSQL_DB'),  # 从Crawler的设置中获取MySQL的数据库名称
            user=crawler.settings.get('MYSQL_USER'),  # 从Crawler的设置中获取MySQL的用户名
            password=crawler.settings.get('MYSQL_PASSWORD'),  # 从Crawler的设置中获取MySQL的密码
            port=crawler.settings.get('MYSQL_PORT')  # 从Crawler的设置中获取MySQL的端口号
        )

    def open_spider(self, spider):
        """
        当爬虫开启时调用的方法。
        :param spider: 爬虫实例。
        """
        self.db = pymysql.connect(  # 创建MySQL数据库连接
            self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()  # 创建MySQL数据库游标

    def close_spider(self, spider):
        """
        当爬虫关闭时调用的方法。
        :param spider: 爬虫实例。
        """
        self.db.close()  # 关闭MySQL数据库连接

    def process_item(self, item, spider):
        """
        处理每个Item的方法。
        :param item: 爬取到的Item对象。
        :param spider: 爬虫实例。
        """
        data = dict(item)  # 将Item对象转换为字典
        keys = ', '.join(data.keys())  # 获取所有字段名，并用逗号连接成一个字符串
        values = ', '.join(['%s'] * len(data))  # 获取与字段数量相同的占位符字符串
        sql = 'insert into {table}({keys}) values ({values}) on duplicate key update'.format(  # 构建插入数据的SQL语句
            table=item.table, keys=keys, values=values)
        update = ','.join([" {key}=%s".format(key=key) for key in data])  # 构建更新数据的SQL语句
        sql += update
        try:
            if self.cursor.execute(sql, tuple(data.values())*2):  # 执行SQL语句
                print('successful')  # 打印成功信息
                self.db.commit()  # 提交事务
        except pymysql.MySQLError as e:  # 捕获MySQL错误
            print(e)  # 打印错误信息
            self.db.rollback()  # 回滚事务
        return item  # 返回Item对象



