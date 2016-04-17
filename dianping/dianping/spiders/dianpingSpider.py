# encoding=utf-8
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request
import logging
import json
import copy
import uuid
import sys
from scrapy.item import Item
reload(sys)
sys.setdefaultencoding('utf-8')

from dianping.items import DianpingItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='dianping.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'dianping'
    
    allowed_domain = ['dinaping.com']
    start_urls = [
#                   "http://www.dianping.com/search/category/1/90/g90p50"
                  ]

    for id in xrange(0, 2900):
        start_urls.append("http://www.dianping.com/search/category/%s/90/g90p50" % id)
        
    def __init__(self):
        self.questionIdPatten = re.compile("[0-9]+")
        self.pageUrl = ""
        self.fw=file("cityCode.list", "w")
        pass
    
    def parse(self, response):
        select = Selector(response)
        cityId = self.questionIdPatten.findall(response.url)[0]
        cityName = select.css(".city").xpath("./text()").extract()[0]
        
        self.fw.write("%s\t%s\n"%(cityId, cityName))
        self.fw.flush()
        
        if response.status == 403:
            sys.exit(0)
            return
        pass
