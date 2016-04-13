# encoding=utf-8
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from azw.items import AzwItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='azw.log',
                filemode='a')

class SpiderTmall(Spider):
    name = 'azw'
    
    allowed_domain = ['tmall.com']
    start_urls = []

    def __init__(self):
        pass
    
    def parse(self, response):
        select = Selector(response)
        
        item = AzwItem()
        yield item
        pass
    
