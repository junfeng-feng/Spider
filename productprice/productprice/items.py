# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


#齐家百科内容类
class ProductItem(Item):
    product_id = Field()
    product_price = Field()

#齐家百科
    
    