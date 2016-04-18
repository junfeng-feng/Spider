# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    
    shop_flag = scrapy.Field()
    # shop
    shop_id= scrapy.Field()
    shop_name= scrapy.Field()
    shop_star = scrapy.Field()
    shop_common_price = scrapy.Field()
    shop_img= scrapy.Field()
    shop_area= scrapy.Field()
    shop_domain= scrapy.Field()
    shop_address= scrapy.Field()
    shop_telphone= scrapy.Field()
    
    shop_open_time= scrapy.Field()
    shop_tag= scrapy.Field()
    shop_map_attitude= scrapy.Field()
    shop_contact_man= scrapy.Field()
    shop_subway_line= scrapy.Field()
    shop_bus_line= scrapy.Field()
    shop_description = scrapy.Field()
    city_id = scrapy.Field()
    
    #rate
    rate_id= scrapy.Field()
    user_photo = scrapy.Field()
    user_nickname= scrapy.Field()
    rate_content= scrapy.Field()
    rate_img= scrapy.Field()
    rate_datetime= scrapy.Field()

    pass
