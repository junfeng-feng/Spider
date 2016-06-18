# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhuangyiCompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    designer_id = scrapy.Field()
    company_id = scrapy.Field()
    designer_name = scrapy.Field()
    position = scrapy.Field()
    good_at_filed = scrapy.Field()
    good_at_style = scrapy.Field()
    designer_introduction = scrapy.Field()
    head_img = scrapy.Field()
    
    
    company_id = scrapy.Field()
    company_name = scrapy.Field()
    company_shortname = scrapy.Field()
    company_koubei = scrapy.Field()
    service_zone = scrapy.Field()
    price = scrapy.Field()
    service_content = scrapy.Field()
    decoration_type_jia = scrapy.Field()
    decoration_type_gong = scrapy.Field()
    decoration_style = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    company_des = scrapy.Field()
    logo  = scrapy.Field()
    
    is_designer = scrapy.Field()
    
    # images
    image_urls = scrapy.Field()
    images = scrapy.Field()