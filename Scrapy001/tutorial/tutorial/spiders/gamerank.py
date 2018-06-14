# coding:utf8

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
import json 
from urllib.parse import urljoin
import codecs

from tutorial.items import GamerankItem
import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver


class Gamerank(scrapy.Spider):
    name = 'quotes'

    def __init__(self):
        self.driver = webdriver.Chrome()
        super(Gamerank, self).__init__()
        dispatcher.connect(self.close_spider, signals.spider_closed)   # 信号量，当爬虫关闭时，执行自定义函数

    def close_spider(self, spider):  # 自定义函数
        self.driver.quit()


    def start_requests(self):
        start_urls = "http://blog.jobbole.com/all-posts/"
        yield scrapy.Request(url=start_urls, callback=self.parse)
    def parse(self, response):
        item = GamerankItem()
        for each_ga in response.css('div.post'):
            item["rank"] = each_ga.xpath('div[@class="post-meta"]/p/a[2]/text()').extract_first()
            item["game"] = each_ga.xpath('div[@class="post-meta"]/span/p/text()').extract_first()
            yield item

        # next_page = response.xpath('//*[@id="archive"]/div[21]/a[4]/@href').extract_first()
        # a = next_page.split('/')[-2]
        # if 0 < int(a) < 5:
        #     yield scrapy.Request(next_page, callback=self.parse)

