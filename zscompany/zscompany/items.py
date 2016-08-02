# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class ZscompanyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_id = Field()
    company_id = Field()
    company_name = Field()
    company_shortname = Field()
    service_zone = Field()
    price = Field()
    koubei = Field()
    service_content = Field()
    decoration_type_jia = Field()
    decoration_type_gong = Field()
    decoration_style = Field()
    city = Field()
    address = Field()
    company_des = Field()
    image_urls = Field()
    images = Field()
