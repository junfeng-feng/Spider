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

from meilele.items import MeileleItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='meilele.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'meilele'
    
    allowed_domain = ['meilele.com']
    start_urls = [
#                   "http://zx.meilele.com/ask/10092.html",
#                 "http://zx.meilele.com/ask/15097.html",
#                 "http://zx.meilele.com/ask/35547.html",
#                 "http://zx.meilele.com/ask/290.html",
                  ]

    for id in xrange(1, 100000):
        start_urls.append("http://zx.meilele.com/ask/%s.html" % id)
        
    def __init__(self):
        self.digitalPattern = re.compile("[0-9]+")
        self.pageUrl = "http://zx.meilele.com/ask/?act=getMoreAnswer&page=%s&id=%s"
        pass
    
    def parse(self, response):
        if response.status == 404:
            # 如果返回404，可以直接返回，不需要处理
            logging.info("response.status:" + response.status)
            return
                
        select = Selector(response)
        if "question_id" in response.meta:
            isNextPage = response.meta["question_id"]
        else:
            isNextPage = "firstPage"
        
        if isNextPage == "firstPage":
            # 第一页只处理问题
            question_id = self.digitalPattern.findall(response.url)[0]
            
            item = MeileleItem()
            item["question_id"] = question_id
            
            # pages 翻页
            try:
                logging.info("# pages 取页码")
                totoal_answers = select.css(".ans_left").xpath(".//text()")[1].extract()
                totoal_answers = self.digitalPattern.findall(totoal_answers)[0]
                pages = int(totoal_answers) / 5 + 1  # page从1开始计算
                 
                for page in xrange(1, pages + 1):  # xrange[)
                    requestUrl = self.pageUrl % (page, question_id)
                    
#                     logging.info("--------------------requestUrl：" + requestUrl)
                    request = Request(url=requestUrl, callback=self.parse, priority=123456)
                    request.meta["question_id"] = question_id
                    yield request
                    pass
            except Exception, e:
                print e
            
            item["question_title"] = "".join(select.css(".ask_de_con").xpath(".//div")[1].xpath(".//text()").extract()).strip()
            try:
                item["question_description"] = "".join(select.css(".descre").xpath(".//p/text()").extract())
            except Exception, e:
                item["question_description"] = ""
                print e
            
            
            try:
                big_category = ">".join(select.css(".w_position").xpath(".//a/text()").extract()[2:])
            except Exception, e:
                big_category = ""
                print e
           
            item["question_category"] = big_category
            
            item["image_urls"] = []
            try:
                # 问题的图片，如果是list
                item["image_urls"] = select.xpath(".//div[@class='descre']").xpath(".//p[@class='img']/a/@href").extract()
            except Exception, e:
                pass
                
            item["is_question"] = "yes"
            yield item
            
        else:
            # 抓取答案
            # other answer
            ask_answer_li_list = json.loads(response.body, encoding="utf-8")["result"]
            
            allNo = self.digitalPattern.findall(response.url)
            pageNo = allNo[0]
            askId = allNo[1]
            index = 0
            for li in ask_answer_li_list:
                index += 1
                item = MeileleItem()
                item["question_id"] = response.meta["question_id"]
                item["answer_id"] = askId + "-" + pageNo + "-" + str(index)
                
                item["answer_content"] = li["ask_content"]
                if li["ask_best"] == "1":
                    item["is_best"] = "yes"
                else:
                    item["is_best"] = "no"
                
                if li["ask_image"] != False:
                    item["image_urls"] = [li["ask_image"]]
                
                item["is_question"] = "no"
                yield item
                pass
            pass
        pass
