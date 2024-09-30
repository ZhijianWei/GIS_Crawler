
# <div align="center">自动抓取web地理位置名称和经纬度信息
## <div align="center"><b><a href="https://github.com/ZhijianWei/GIS_Crawler/blob/main/README.md">English</a> | <a href="https://github.com/ZhijianWei/GIS_Crawler/blob/main/READMEzh.md">简体中文</a></b></div>


#### 作者：魏智健 (南京农业大学) ，如果有任何问题，请随时联系我``18151936092@163.com``📧
**如果这套算法对你有帮助，可以给本项目一个 Star ⭐ ，或者推荐给你的朋友们，谢谢！😊**




##  💻简介
#### 这个爬虫是为了从包含地理信息的网站收集关于地理位置（国家、州/省、城市）的名称和经纬度信息。这些数据可以用于各种应用，如地图服务、位置分析等。我为这个爬虫添加了详细的中文注释，适合入门和快速调用

### * 目标网站：<br>
_网站示例: https://chi.timegenie.com，类似这种提供时区和地理位置数据的网站都可以_
### * 爬取的数据类型：<br>
_首先访问网站的特定部分（/latitude_longitude/），从这里获取国家列表,之后进一步获取州或省份的信息，进一步获取州或省份的信息。<br>_
### * 数据字段：<br>
_name: 地理位置的名称<br>
parent: 父级地理位置的名称，例如，州的父级是国家<br>
type: 数据类型，用于区分数据的级别<br>
sname: 标准化的地理位置名称，URL的一部分<br>
lng: 经度<br>
lat: 纬度<br>_

## 🔧依赖库

* Scrapy 及其相关依赖库
* Selenium
* pymongo
* pymysql
<br>
<br>
##  ⚡使用说明

### * **修改爬虫**：

如果想爬取一个与示例网站类似的网站 https://example.com，可以在 _GIS_Crawler.py_ 中简单调整解析规则：

    class GIS_Crawler(scrapy.Spider):
    name = 'Cname'
    allowed_domains = ['https://example.com']  # 更新为新网站的域名
    start_urls = ['https://example.com']  # 更新为新网站的起始URL

代码中已经定义了一个 GIS_CrawlerItem，它指定了爬虫需要抓取的数据字段，例如名称、经度、纬度等。如果你需要抓取其他数据，可以在这个类中添加更多的字段。

    def start_requests(self):
        url = self.allowed_domains[0] + '/some/path'  # 更新为新网站的路径
        yield scrapy.Request(url, callback=self.parse, meta={'type': 0}, dont_filter=True)

    def parse(self, response):
        # 更新XPath选择器以匹配新网站的HTML结构
        items = response.xpath('//div[@class="item"]')
        for item in items:
            name = item.xpath('.//h2/text()').get()  # 示例XPath
            # 创建Item并提取数据
            vdgeoItem = VdgeospiderItem()
            vdgeoItem['name'] = name

            # 其他字段...

            yield vdgeoItem

####  **💥特别说明💥**
#### * 如需修改与示例差别很大的网站需要调整settings.py（下载延迟、并发请求数）和middlewares.py（自定义请求头、Cookies处理）。

#### * 如遇到基本反爬机制（如需要User-Agent、禁止过快请求等），需要在settings.py中调整相关设置，如果遇到复杂的反爬策略（如IP被封、需要验证码、动态令牌等），需要在middlewares.py进行修改。

#### * 如果抓取的数据需要清洗，需要在pipelines.py中添加相应的处理函数，如需要更改存储数据库，需要在pipelines.py中配置新的数据库连接和存储逻辑。

#### * 遵纪守法，先看目标网站的robots.txt规则<br><br><br>
 
### * **运行爬虫**：
在项目根目录下（包含 scrapy.cfg 文件的目录），使用命令行运行爬虫：

    scrapy crawl Cname
### * **存储数据**：
    scrapy crawl Cname -o output.json -t json
这将把抓取的数据以 JSON 格式输出到 output.json 文件中。

