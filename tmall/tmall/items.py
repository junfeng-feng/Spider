# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item

# 齐家百科内容类
class TmallCategoryItem(Item):
    
    flag = Field()
    #category
    category_id = Field()
    category_name = Field()
    category_level = Field()
    category_level1 = Field()
    category_level2 = Field()
    category_level3 = Field()
    related_product_num = Field()
    #dict
    category_pro = Field() # {pro_name:[prov_value_list],}

    #brand
    #images
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
