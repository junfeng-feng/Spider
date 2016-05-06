
# encoding=utf-8
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request
import logging
import json
import copy
import time
import uuid
import sys
from Finder.Finder_items import item
reload(sys)
sys.setdefaultencoding('utf-8')

from shijieben.items import ShejibenItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='dianping.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'dianping'
    
    allowed_domain = ['shiejiben.com']
    start_urls = [
                  ]

        
    for id in xrange(1, 100):
        start_urls.append("http://www.dianping.com/search/category/%s/90/g90p%s" % (id))
        
    def __init__(self):
        self.questionIdPatten = re.compile("[0-9]+")
        self.pageUrl = "http://www.dianping.com/search/category/%s/90/g90p%s"
        self.fw = file("pages.list", "a")
        
        pass
    
    def parse(self, response):
        #翻页请求，每10页，停30秒
        select = Selector(response)

