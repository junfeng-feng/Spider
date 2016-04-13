# -*- coding: utf-8 -*-

import scrapy


class TmallshopItem(scrapy.Item):
    # define the fields for your item here like:
    shop_id = scrapy.Field()
    category_id = scrapy.Field()
    brand_id = scrapy.Field()
    
    shop_type = scrapy.Field()
    shop_name = scrapy.Field()
    company_name = scrapy.Field()
    shop_area = scrapy.Field()
    shop_logo = scrapy.Field()
    shop_commodity_num = scrapy.Field()
    
    description_consist_score = scrapy.Field()
    service_attitude_score = scrapy.Field()
    logistics_service_score = scrapy.Field()
    description_consist_cmp = scrapy.Field()
    service_attitude_cmp = scrapy.Field()
    logistics_service_cmp = scrapy.Field()
    
    
#      not important
    open_years = scrapy.Field() 
    shop_url = scrapy.Field()
     
    # images
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass

