# encoding=utf-8
import re
from scrapy.spiders import Spider
from productprice.items import ProductItem


class SpiderTmall(Spider):
    def __init__(self):
        self.pricePattern = re.compile(r"<b>.*?<")#结果类似<b>89.00<
    name = 'productprice'
    allowed_domain = ['china-10.com']
    start_urls = []
    
    start_id = 1136894
    end_id = 2000000
    
    for product_id in xrange(start_id, end_id):
        start_urls.append("http://www.china-10.com/ajaxstream/product/?action=productbaojia&productid=%s" % (product_id))
        
    
    def parse(self, response):
        item = ProductItem()
        item["product_id"] = response.url.split("=")[-1]#从url获取product_id
        if len(response.body) < 10: #如果body太小则没有数据
            item["product_price"] = None
            return item
        
        match = self.pricePattern.search(response.body)
        item["product_price"] = match.group()[3:-1]#去掉前面的<b>和后面的<
        
        return item
        
