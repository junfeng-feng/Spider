# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class FangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Fang_Item(Item):
    site = Field()
    title = Field()
    shortDescription = Field()
    category = Field()
    style = Field()
    tag = Field()
    origin_url = Field()
    new_url = Field()
    mb = Field()
    pixel = Field()
    size = Field()
    format  = Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass