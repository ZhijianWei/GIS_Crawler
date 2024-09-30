
# <div align="center">Automatically scrape web geographic location names and latitude/longitude information
## <div align="center"><b><a href="https://github.com/ZhijianWei/GIS_Crawler/blob/main/README.md">English</a> | <a href="https://github.com/ZhijianWei/GIS_Crawler/blob/main/READMEzh.md">简体中文</a></b></div>

#### Author: Zhijian Wei (Nanjing Agricultural University), if you have any questions, please feel free to contact me at ``18151936092@163.com``📧
**If this set of algorithms helps you, you can give this project a Star ⭐, or recommend it to your friends, thank you!😊**

## 💻Introduction
#### This spider is designed to collect geographic location (country, state/province, city) names and latitude/longitude information from websites that contain geographic information. This data can be used for various applications, such as map services, location analysis, etc. I have added detailed Chinese comments to this spider, making it suitable for beginners and quick calls.

### * Website:<br>
_A website example: https://chi.timegenie.com, similar websites that provide time zone and geographic location data can be used_ 
### * Data Type:<br>
_First, visit a specific part of the website (/latitude_longitude/) to get a list of countries, then further obtain information about states or provinces, and then get information about cities.<br>_
### * Data Fields:<br>
_name: The name of the geographic location<br>
parent: The name of the parent geographic location, for example, the parent of a state is the country<br>
type: Data type, used to distinguish the level of data<br>
sname: Standardized geographic location name, part of the URL<br>
lng: Longitude<br>
lat: Latitude<br>_

## 🔧Dependencies

* Scrapy and its related libraries
* Selenium
* pymongo
* pymysql
<br>
<br>

## ⚡Instructions 

### * **Modify the Spider**:

If you want to scrape a website similar to the example website https://example.com, you can simply adjust the parsing rules in _GIS_Crawler.py_:

```python
class GIS_Crawler(scrapy.Spider):
    name = 'Cname'
    allowed_domains = ['https://example.com']   # Update to the new website's domain
    start_urls = ['https://example.com']   # Update to the new website's start URL

def start_requests(self):
    url = self.allowed_domains[0] + '/some/path'  # Update to the new website's path
    yield scrapy.Request(url, callback=self.parse, meta={'type': 0}, dont_filter=True)

def parse(self, response):
    # Update the XPath selector to match the new website's HTML structure
    items = response.xpath('//div[@class="item"]')
    for item in items:
        name = item.xpath('.//h2/text()').get()  # Example XPath
        # Create Item and extract data
        vdgeoItem = VdgeospiderItem()
        vdgeoItem['name'] = name

        # Other fields...

        yield vdgeoItem
```

#### **💥Special Instructions💥**
#### * If you need to modify a website that is very different from the example, you need to adjust `settings.py` (download delay, number of concurrent requests) and `middlewares.py` (custom request headers, Cookies processing).

#### * If you encounter basic anti-crawling mechanisms (such as the need for User-Agent, prohibition of too many requests, etc.), you need to adjust the relevant settings in `settings.py`. If you encounter complex anti-crawling strategies (such as IP blocking, the need for captcha, dynamic tokens, etc.), you need to modify `middlewares.py`.

#### * If the scraped data needs to be cleaned, you need to add the corresponding processing function in `pipelines.py`. If you need to change the storage database, you need to configure the new database connection and storage logic in `pipelines.py`.

#### * Comply with the law, check the target website's robots.txt rules first<br><br>
  
### * **Run the Spider**:
Run the spider in the project root directory (the directory containing the `scrapy.cfg` file) using the command line:

```bash
scrapy crawl Cname
```

### * **Store Data**:
```bash
scrapy crawl Cname -o output.json -t json
```
This will output the scraped data in JSON format to the `output.json` file.
