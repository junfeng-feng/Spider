# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    
    shop_flag = scrapy.Field()
    shop_type = scrapy.Field()
    # shop
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    shop_img = scrapy.Field()
    
    shop_area = scrapy.Field()  # 杨浦区,五角场/大学区
    shop_domain = scrapy.Field()  # 上海家装
    shop_category = scrapy.Field()  # 分类
    shop_cityname = scrapy.Field()  # 上海
    shop_tag = scrapy.Field()
    
    shop_address = scrapy.Field()
    shop_telphone = scrapy.Field()
    
    shop_open_time = scrapy.Field()
    shop_map_attitude = scrapy.Field()
    shop_contact_man = scrapy.Field()
    shop_bus_line = scrapy.Field()
    shop_description = scrapy.Field()
    city_id = scrapy.Field()
    
    # rate
    rate_id = scrapy.Field()
    user_photo = scrapy.Field()
    user_nickname = scrapy.Field()
    rate_content = scrapy.Field()
    rate_img = scrapy.Field()
    rate_datetime = scrapy.Field()

    # images
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
