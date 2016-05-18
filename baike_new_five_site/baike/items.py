# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BaikeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#齐家百科内容类
class Baike_Qijia_Item(Item):
    title_id = Field()
    title_name = Field()
    title_introduction = Field()
    title_category = Field()
    title_url = Field()
    content_uuid_list = Field()
    content_uuid = Field()
    content_name = Field()
    content_text = Field()
    image_urls = Field()
    images = Field()
#齐家百科
    
    