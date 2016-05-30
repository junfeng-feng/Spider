# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TmallItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TmallproductItem(Item):
    
    product_id = Field()
    shop_id = Field()
    brand_id = Field()
    brand_name = Field()
    category_id = Field()
    category_name = Field()
    category_id2 = Field()
    category_name2 = Field()
    brand_chname = Field()
    brand_enname = Field()
    product_name = Field()
    product_point = Field()
    product_price = Field()
    product_lower_price = Field()
    product_salepermonth = Field()
    product_judgementnum = Field()
    product_type = Field()
    product_data = Field()
    product_searchword = Field()
    product_specialjudge = Field()
    is_decoration = Field()
    image_urls = Field()
    images = Field()
    img = Field()
    group_img = Field()
    url = Field()
    