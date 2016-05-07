# -*- coding: utf-8 -*-
import scrapy

class ShejibenItem(scrapy.Item):
    designer_id = scrapy.Field()
    designer_name = scrapy.Field()
    designer_phone_no = scrapy.Field()
    designer_email = scrapy.Field()
    designer_sex = scrapy.Field()
    designer_position = scrapy.Field()
    apartment = scrapy.Field()
    style = scrapy.Field()
    program = scrapy.Field()
    average_price = scrapy.Field()
    work_years = scrapy.Field()
    introduction = scrapy.Field()
    head_photo = scrapy.Field()
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    company_id = scrapy.Field()
    company_name = scrapy.Field()
    
    # images
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
