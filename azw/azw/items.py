# -*- coding: utf-8 -*-
import scrapy

class AzwItem(scrapy.Item):
    # define the fields for your item here like:
    title_id = scrapy.Field()
    title_name = scrapy.Field()
    title_introduction = scrapy.Field()
    title_category = scrapy.Field()
    title_url = scrapy.Field()
    content_uuid_list = scrapy.Field()
    content_uuid = scrapy.Field()
    content_name = scrapy.Field()
    content_text = scrapy.Field()
    
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
