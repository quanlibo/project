# -*- coding: utf-8 -*-
import scrapy
from ..items import QikanItem

class CareersSpider(scrapy.Spider):
    name = 'careers'
    # 允许的域名
    allowed_domains = ['https://link.springer.com/']

    # 重写 start_requests 方法做一个循环实现分页
    def start_requests(self):
        for page in range(1, 180):
            yield scrapy.Request(
                url="https://link.springer.com/search/page/" + str(
                    page) + "?facet-content-type=%22Journal%22&sortOrder=newestFirst", callback=self.parse)

    # 列表页
    def parse(self, response):
        all_li = response.xpath("//ol[@id='results-list']/li")
        for li in all_li:
            # 详情页地址
            href = 'https://link.springer.com' + li.xpath(".//h2/a[@class='title']/@href")[0].extract()
            print(href)
            # 请求详情页
            yield scrapy.Request(url=href, callback=self.parse_detaill)

    # 详情页
    def parse_detaill(self, response):
        # 实例化item
        item = QikanItem()
        # 标题
        title = response.xpath("//div[@class='col-main']/h1[@id='title']/text()")[0].extract()
        # 期刊名称
        qikan_name = response.xpath("//dl/dd[@id='abstract-about-title']/text()")[0].extract()
        # 出版者
        chuban = response.xpath("//dl/dd[@id='abstract-about-publisher']/text()")[0].extract()
        # 正文
        content = response.xpath("string(//div[@class='abstract-content formatted'])")[0].extract().replace('\n', '')
        # 覆盖
        coverage = response.xpath("//dl/dd[@id='abstract-about-journal-coverage']/text()")[0].extract()
        # 打印ISSN
        Online_ISSN = response.xpath("//dl/dd[@id='abstract-about-journal-online-issn']/text()")[0].extract()
        print(title, qikan_name, chuban, content, coverage, Online_ISSN)
