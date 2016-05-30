#encoding=utf-8
import copy
import json
import re
import traceback

import MySQLdb
from scrapy import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider

from tmall.items import TmallproductItem


#from scrapy.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.spiders.crawl import CrawlSpider, Rule
class tamllproduct_spider(Spider):
    name = 'product'
    
    allowed_domain = ['detail.tmall.com/']
    
    start_urls = []
    
    #字典
    brandid_isdecoration = {}
    '''
    for brandId in file(r"D:\coding\workspace\Projects\tmall\tmall\spiders\tmall_brand_is_new_version.txt"):
        brandId = brandId.strip()
        start_urls.append("https://list.tmall.com//search_product.htm?brand=%s" % (brandId))
        break
    '''
    index = 1 
    for line in file(r"tmall/spiders/tmall_brand_is_new_version.txt"):
        index = index +1
        brandId = line
        start_urls.append("https://list.tmall.com//search_product.htm?brand=%s" % (brandId))
        if index>600000 :
            break
    '''
    start_urls = ['https://detail.tmall.com/item.htm?id=42445783565']
    
    begin = 500001
    scop = 100000
    i = 0
    while(i<=scop):
        url = 'http://www.china-10.com/product/%d.html' % (begin+i)
        start_urls.append(url)
        i = i + 1
    
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,db='spider_db',charset='utf8')
    cur = conn.cursor()
    sql = 'select product_id from tmall_product_id_list'
    cur.execute(sql)
    rs = cur.fetchmany(50)
    for r in rs:
        url = 'https://detail.tmall.com/item.htm?id=%s' % r
        start_urls.append(url)
        
    
    cur.close()
    conn.close()
    '''

    #匹配一串数字
    rule_getpid = re.compile('[\d]+')
    #获取店铺id
    rule_getuserid = re.compile(r'userid=[\d]+')
    #去掉字符串中的空白符号
    rule_removeblank = re.compile(r'[\r\n\t]')
    #匹配品牌名称
    rule_brandname = re.compile(u'\u54c1\u724c')
    #匹配品牌型号
    rule_producttype = re.compile(u'\u578b\u53f7')
    #判断url是否有http头
    rule_httphead = re.compile('http')
    
    def __init__(self):
        
        self.url_specialjudge = 'https://rate.tmall.com/listTagClouds.htm?itemId=%s'
        
        self.url_judgementnum = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s'
        
        self.url_product = 'https://detail.tmall.com/item.htm?id=%s'
        
        self.url_search_hotword = 'https://suggest.taobao.com/sug?area=getdetailsuggest&nid=%s'
        
        ############################################
        self.brandIdPattern = re.compile(r"brand=[0-9]+")  # brandPattern re
        self.brandIdLength = len("brand=")
        
        self.productIdPattern = re.compile(r"\Wid=[0-9]+")  # product_id  \W匹配 “&”
        self.productIdLength = len("_id=")  # 截取的时候，去掉前四位
        self.pageUrl = "https://list.tmall.com//search_product.htm?brand=%s&s=%s"
        
    def parseProduct(self,response):
        
        item = response.meta["data"]
        sel = Selector(response)
        #产品id
        item['product_id'] = self.rule_getpid.findall(response.url)[0]
        #产品名称,去掉空白符
        product_name = sel.xpath(".//div[@class='tb-detail-hd']/h1/text()").extract()[0]
        item['product_name'] = self.rule_removeblank.sub('',product_name)
        #brandid
        item['brand_id'] = response.headers['at_brid']
        #userid==shopid
        content = sel.xpath(".//head/meta[@name='microscope-data']/@content").extract()
        if content:
            word = self.rule_getuserid.findall(content[0])
            if word:
                item['shop_id'] = word[0].split('=')[-1]
            else:
                item['shop_id'] = ''
        else:
            item['shop_id'] = ''
        #product_point    
        product_point = sel.xpath(".//div[@class='tb-detail-hd']/p/text()").extract()[0]
        item['product_point'] = self.rule_removeblank.sub('',product_point)
        
        #product_data
        product_data_temp = sel.xpath(".//ul[@id = 'J_AttrUL']/li/text()").extract()
        product_data =[]
        item['product_type'] = ''
        item['brand_name'] = ''
        for pd in product_data_temp:
            pd_temp = pd.replace(u'\xa0','')
            if self.rule_brandname.findall(pd_temp):
                item['brand_name'] = pd_temp.split(':')[-1]
            elif self.rule_producttype.findall(pd_temp):
                item['product_type'] = pd_temp.split(':')[-1]
            product_data.append(pd_temp)
        item['product_data'] = product_data
        
        item['category_id'] = ''
        item['category_name'] = ''
        item['product_judgementnum'] = ''
        item['product_searchword'] = ''
        item['product_specialjudge'] = ''
        item['url'] = response.url
        
        #group_img
        group_imgs = sel.xpath("//ul[@id='J_UlThumb']/li/a/img/@src").extract()
        for img in group_imgs:
            item['image_urls'].append('https:'+ img.replace('60x60','300x300'))
        
        request =  Request(self.url_specialjudge%(item["product_id"]),
                           callback = self.parse_specialjudge, priority=123456
                          )
        request.meta["data"] = copy.deepcopy(item)
        
        yield request
            
        
    def parse_specialjudge(self,response):
        
        item = response.meta["data"]
        jsondata = '{'+response.body[2:]+'}'
        liResult = json.loads(jsondata, encoding="GBK")
        result = liResult['tags']["tagClouds"]
        specialjudge = ''
        for r in result:
            specialjudge = specialjudge + r['tag'] + ','
            
        print specialjudge
        item['product_specialjudge'] = specialjudge
        
        
        request =  Request(self.url_judgementnum%(item["product_id"]),
                           callback = self.parse_judgementnum
                          )
        request.meta["data"] = copy.deepcopy(item)
        
        yield request
        
    def parse_judgementnum(self,response):    
        
        item = response.meta["data"]
        try:
            jsondata = response.body[11:-1]
            liResult = json.loads(jsondata, encoding="GBK")
            result = liResult['dsr']['rateTotal']
            item['product_judgementnum'] = result
        except Exception,ex:
            item['product_judgementnum'] = ''
        request =  Request(self.url_search_hotword%(item["product_id"]),
                           callback = self.parse_searchword
                          )
        request.meta["data"] = copy.deepcopy(item)
        
        yield request
        
    def parse_searchword(self,response):
        
        item = response.meta["data"]
        result1 = json.loads(response.body, encoding="utf-8")
        if not result1['result']:
            yield item
        else:
            result2 = json.loads(result1['result'][0]['record'][0]['detail_value'])
            searchword = []
            for r in result2['result']:
                searchword.append(r[0])
            item['product_searchword'] = searchword
            item['category_id'] = result2['result'][0][0].split('|')[-1]
            item['category_name'] = result2['result'][0][0].split('|')[0]
            
            yield item
        
    def parse(self, response):
        select = Selector(response)
        brandId = self.getBrandId(response.url)

        itemList = select.css(".product")
        if len(itemList) > 1:#当前有产品，才需要处理
            for productItem in itemList:
                productId = self.productIdPattern.findall(productItem.extract())[0]  # 三个一样的id，取第一个
                product_id = productId[self.productIdLength:]
                product_salepermonth = productItem.css(".productStatus")[0].xpath(".//span/em/text()").extract()[0]
                try:
                    product_price = productItem.xpath("./div/p/em/@title").extract()[0]
                except Exception, e:
                    product_price = ""
                    print e
                
                #单图下载
                item = TmallproductItem()
                #是不是装修类
                item["is_decoration"] = 'yes'
                
                if productItem.xpath(".//img/@src").extract():
                    image_url = productItem.xpath(".//img/@src").extract()[0]
                elif productItem.xpath(".//img/@data-ks-lazyload").extract():
                    image_url = productItem.xpath(".//img/@data-ks-lazyload").extract()[0]
                if image_url:
                    image_url = 'https:'+ image_url
                item['image_urls'] = [image_url]
                item["product_salepermonth"] = product_salepermonth
                item["product_id"] = product_id
                #item["brand_id"] = brandId
                item["product_price"] = product_price
                
                
                request = Request(self.url_product%(item['product_id']),callback=self.parseProduct)
                request.meta["data"] = copy.deepcopy(item)
                yield request
            
            pages = select.css(".ui-page-s-len").xpath("./text()").extract()[0]
            totalPage = int(pages.split("/")[1])
            if totalPage > 1:
                for pageNo in xrange(1, totalPage):
                    
                    #每页60个产品，参数s=60，表示请求第二页, s=120表示请求第三页
                    #self.pageUrl = "https://list.tmall.com//search_product.htm?brand=%s&s=%s"
                    requestUrl = self.pageUrl % (brandId, pageNo * 60)
                    yield Request(requestUrl, callback=self.parse, priority=123456)
                    pass
        pass
    
    def getProductId(self, url):
        match = self.productIdPattern.search(url)
        if match and match.group():
            itemId = match.group()[self.productIdLength:]
        else:
            return None
        return itemId
        pass
    
    def getBrandId(self, url):
        match = self.brandIdPattern.search(url)
        if match and match.group():
            id = match.group()[self.brandIdLength:]
        else:
            return None
        return id
        pass
        
        