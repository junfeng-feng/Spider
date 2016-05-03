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

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tmall.log',
                filemode='a')

#===============================================================================
# SpiderTmall
# 根据给定的一级分类，抓取对应的子分类和所有品牌
#===============================================================================
class SpiderTmall(CrawlSpider):
    name = 'tmall'
    
    allowed_domain = ['tmall.com']
    start_urls = []
    
    #一级分类ID list
    for catid in file("./tmall/spiders/catid.list"):
        catid = catid.strip().split()[0]
        start_urls.append("https://list.tmall.com/search_product.htm?cat=%s" % (catid))

    def __init__(self):
        logging.info("spider init")
        
        self.catPattern = re.compile(r"cat=[0-9]+")  # cat re
        self.catPrefixLen = len("cat=")
        self.brandPattern = re.compile(r"brand=[0-9]+")  # brandPattern re
        self.brandPrefixLen = len("brand=")
        
        self.catidIsDecrationSet = set([catid.strip().split()[0] 
                                            for catid in file("./tmall/spiders/catid.list")
                                                if catid.strip().split()[1] == "is_decoration"])
        pass
    
    def parse(self, response):
        select = Selector(response)
        item = TmallCategoryItem()
        
        item["category_id"] = self.getCatId(response.url)
        
        if "is_decoration" in response.meta:
            #子分类，带过来是否为装修类
            item["is_decoration"] = response.meta["is_decoration"]
        else:
            #一级分类，直接标示是否为装修类
            if item["category_id"] in self.catidIsDecrationSet:
                item["is_decoration"] = "yes"
            else:
                item["is_decoration"] = "no"
    
        # 获取子集分类id，调用callback自身
        catUrl = "https://list.tmall.com/search_product.htm?cat=%s" 
        #如果有子分类,地柜查找子分类
        cateAttrs = select.css(".cateAttrs")
        if len(cateAttrs) > 0:
            catIdList = self.catPattern.findall(cateAttrs.extract()[0])
            for catidstr in catIdList:
                catid = catidstr[self.catPrefixLen:]
                print catid
                requestUrl = catUrl % (catid)
                request = Request(requestUrl, callback=self.parse, priority=1234567)
                request.meta["is_decoration"] = item["is_decoration"]
                yield request
            pass

        item["related_product_num"] = ""
        try:
            item["related_product_num"] = select.css(".j_ResultsNumber").xpath("./span/text()")[0].extract().strip()
        except Exception,e:
            print e

        catSel = select.xpath("//li[@data-tag='cat']")
        category_level = len(catSel)
        # 级别
        item["category_level"] = category_level
        item["category_level1"] = ""
        item["category_level2"] = ""
        item["category_level3"] = ""
        
        item["category_name"] = ""
        # 通过li获取所有级分类名称，最后一级是本身，最底层的分级 category_name
        for index in xrange(category_level):
            try:
                catName = catSel[index].xpath(".//a/text()")[0].extract()  # 取得li/a里面的text
                if index == category_level - 1:
                    item["category_name"] = catName
                else:
                    item["category_level%s" % (index + 1)] = catName
                pass
            except Exception,e:
                print e
                
        # 分类对应的属性
        item["category_pro"] = {}
        proList = select.css(".propAttrs").css(".j_Prop")
        for pro in proList:
            try:
                attrKey = pro.xpath(".//div[@class='attrKey']/text()")[0]
                attrKey = attrKey.extract().strip()
                liList = pro.xpath("./div[@class='attrValues']//li/a/text()")
                valueList = []
                for value in liList:
                    valueList.append(value.extract().strip())
                    pass
                item["category_pro"][attrKey] = valueList
            except Exception,e:
                print e
            pass
        
        item["flag"] = "category"
        # 生成分类的item
        yield item
    
        # 请求品牌更多的连接
        brandUrl = "https://list.tmall.com/ajax/allBrandShowForGaiBan.htm?cat=%s" % (item["category_id"])
        request = Request(brandUrl, callback=self.brandJsonCallBack, priority=1234567)
        request.meta["category_id"] = item["category_id"]
        request.meta["is_decoration"] = item["is_decoration"]
        
        yield request
        pass
    
    def brandJsonCallBack(self, response):
        item = TmallCategoryItem()
        item["is_decoration"] =  response.meta["is_decoration"]
        
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
            
            #太多没有图片的，没有保存，被跳过
#             # 没有img则跳过此品牌
#             if len(dictItem["img"]) == 0:
#                 #问题在这里，没有图片，直接跳过
#                 continue
#                 pass

            brand = {"brand_id":brand_id, "brand_en":brand_en, "brand_zh":brand_zh}
            if len(dictItem["img"]) > 0:
                img_url = "http://img.alicdn.com/bao/uploaded/" + dictItem["img"]
                
                brand["brand_logo_url"] = img_url
                image_urls.append(img_url)
                
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

