# -*- coding: utf-8 -*-
import random
import time
import scrapy
from sun.items import SunItem
from scrapy import Request
from scrapy.http.response.html import HtmlResponse

class FincSpider(scrapy.Spider):
    name = 'finc1'
    allowed_domains = ['finance.591hx.com']
    start_urls = ['http://finance.591hx.com/list/jj.shtml/']
    def start_requests(self):
        yield Request("http://finance.591hx.com/list/jj.shtml/", headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})

    def parse(self, response):
        #获取首页的目录
        contents = response.xpath(".//div[@class='line']/ul/li")

        for content in contents:
            item = SunItem()
            url = content.xpath(".//a/@href").get()
            item['url'] = url
            yield scrapy.Request(item['url'], meta={'item': item}, callback=self.detail)
            # 翻页操作
            # return
        print("========准备翻页========")
        next_url = response.xpath("//div[@class='page']/a[last()]/@href").getall()
        next_url = "".join(next_url)
        if not next_url:
            print("===结束===")
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse)
            print("=====翻页成功======")
    def detail(self, response):
        # 接收上级已爬取的数据
        print("========已经进入内页=========")
        item = response.meta['item']
        # 一级内页数据提取
        title = response.xpath("//div[@class='news bc mt12']/h1/text()").getall()
        item['title'] = "".join(title).strip()

        item['cont'] = response.xpath("//div[@class='newsContainer']/p/text()").getall()
        item['cont'] = "".join(item['cont']).strip()
        yield item

        time.sleep(random.randint(1, 3))
        print("=======延时结束========")