# encoding=utf-8
import re
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import Request
import logging
import json
import chardet

from tmall.items import TmallCategoryItem

#===============================================================================
# SpiderTmall
# 根据给定的一级分类，抓取对应的子分类和所有品牌
#===============================================================================
class SpiderTmall(CrawlSpider):
    name = 'tmall'
    
    allowed_domain = ['tmall.com']
    start_urls = []
    
    # read cat id list from file
    # 50000000~50221126的所有有效的分类id
    # #只需要第一次跑一遍，之后，就不用再重复抓取
#     catIdList = eval(file("tmall/spiders/catid.txt").read()) 
#     for catid in catIdList:
#         start_urls.append("https://list.tmall.com/search_product.htm?cat=%s" % (catid))

    # 50000000~50221126 done
    # 54402802~ 54500000 done
    # 55000000~55311317 done
#     for catid in xrange(55311317, 56000000):
#         start_urls.append("https://list.tmall.com/search_product.htm?cat=%s" % (catid))
            
    for catid in file("./tmall/spiders/catid.list"):
        catid = catid.strip()
        start_urls.append("https://list.tmall.com/search_product.htm?cat=%s" % (catid))

    def __init__(self):
        logging.info("spider init")
        self.catPattern = re.compile(r"cat=[0-9]+")  # cat re
        self.catPrefixLen = len("cat=")
        self.brandPattern = re.compile(r"brand=[0-9]+")  # brandPattern re
        self.brandPrefixLen = len("brand=")
        pass
    
    def parse(self, response):
        select = Selector(response)
        
        item = TmallCategoryItem()
        item["related_product_num"] = select.css(".j_ResultsNumber").xpath("./span/text()")[0].extract()
        item["category_id"] = self.getCatId(response.url)
        
        catSel = select.xpath("//li[@data-tag='cat']")
        category_level = len(catSel)
        # 级别
        item["category_level"] = category_level
        item["category_level1"] = ""
        item["category_level2"] = ""
        item["category_level3"] = ""
        
        # 通过li获取所有级分类名称，最后一级是本身，最底层的分级 category_name
        for index in xrange(category_level):
            catName = catSel[index].xpath(".//a/text()")[0].extract()  # 取得li/a里面的text
            if index == category_level - 1:
                item["category_name"] = catName
            else:
                item["category_level%s" % (index + 1)] = catName
            pass
        
        # 分类对应的属性
        item["category_pro"] = {}
        proList = select.css(".propAttrs").css(".j_Prop")
        for pro in proList:
            attrKey = pro.xpath(".//div[@class='attrKey']/text()")[0]
            
            attrKey = attrKey.extract().strip()
            liList = pro.xpath("./div[@class='attrValues']//li/a/text()")
            valueList = []
            for value in liList:
                valueList.append(value.extract().strip())
                pass
            item["category_pro"][attrKey] = valueList
            pass
        item["flag"] = "category"
        # 生成分类的item
        yield item
    
        # 请求品牌更多的连接
        brandUrl = "https://list.tmall.com/ajax/allBrandShowForGaiBan.htm?cat=%s" % (item["category_id"])
        request = Request(brandUrl, callback=self.brandJsonCallBack, priority=123456)
        request.meta["category_id"] = item["category_id"]
        yield request
        
        
        # 获取子集分类id，调用callback自身
        catUrl = "https://list.tmall.com/search_product.htm?cat=%s" 
        
        #如果有子分类
        cateAttrs = select.css(".cateAttrs")
        if len(cateAttrs) > 0:
            catIdList = self.catPattern.findall(cateAttrs.extract()[0])
            for catidstr in catIdList:
                catid = catidstr[self.catPrefixLen:]
                print catid
                requestUrl = catUrl % (catid)
                request = Request(requestUrl, callback=self.parse, priority=12345678)
                yield request
            pass
        pass
    
    def brandJsonCallBack(self, response):
        item = TmallCategoryItem()
        category_id = response.meta["category_id"]
        respList = json.loads(response.body.decode("GBK").encode("utf-8"))
        
        image_urls = []
        brandList = []
        for dictItem in respList:
            href = dictItem["href"]
            brand_id = self.getBrandid(href)
            
            title = dictItem["title"].split("/")
            # 如果只有英文，则中文名称也采用英文
            if len(title) < 2:
                title.append(title[0])
                
            brand_en = title[0]
            brand_zh = title[1]
            
            # 没有img则跳过此品牌
            if len(dictItem["img"]) == 0:
                continue
            
            img_url = "http://img.alicdn.com/bao/uploaded/" + dictItem["img"]
            
            image_urls.append(img_url)
            
            brand = {"brand_id":brand_id, "brand_en":brand_en, "brand_zh":brand_zh}
            brandList.append(brand)
            pass
        
        item["image_urls"] = image_urls
        item["flag"] = "brand"
        item["category_pro"] = {}
        item["category_pro"]["品牌"] = brandList
        
        item["category_id"] = category_id
        # 生成品牌的id
        yield item
        pass
    
    #===========================================================================
    # 通过正则表达式从url获取cat id 
    #===========================================================================
    def getCatId(self, url):
        match = self.catPattern.search(url)
        if match and match.group():
            category_id = match.group()[self.catPrefixLen:]
        else:
            return None
        return category_id
        pass

    def getBrandid(self, url):
        match = self.brandPattern.search(url)
        if match and match.group():
            brand_id = match.group()[self.brandPrefixLen:]
        else:
            return None
        return brand_id
        pass    

