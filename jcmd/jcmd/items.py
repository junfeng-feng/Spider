# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class JcmdItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
#分类
class categoryItem(Item):
    
    category_id = Field()
    category_name = Field()
    category_father_id = Field()
    category_father_name = Field()
    category_child_id = Field()
    category_child_name = Field()
    category_level = Field()
    url = Field()


#品牌
class brandItem(Item):
    
    brand_id = Field()
    brand_chname = Field()
    brand_enname = Field()
    category_id = Field()
    category_name = Field()
    brand_introduction = Field()
    brand_info = Field()
    brand_word = Field()
    brand_address = Field()
    brand_leader = Field()
    brand_phone = Field()
    brand_website = Field()
    brand_year = Field()
    logo = Field()
    img = Field()
    url = Field()
    image_urls = Field()
    images = Field()
    
#门店    
class shopItem(Item):
    
    shop_id = Field()
    shop_name = Field()
    brand_id = Field()
    brand_name = Field()
    category_id = Field()
    category_name = Field()
    shop_type = Field()
    shop_phone = Field()
    shop_person = Field()
    shop_site = Field()
    shop_address = Field()
    shop_introduction = Field()
    image_urls = Field()
    images = Field()
    url = Field()
    