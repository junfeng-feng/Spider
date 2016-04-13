# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmallrateItem(scrapy.Item):
    # define the fields for your item here like:
    product_id = scrapy.Field()
    rate_id = scrapy.Field()
    user_nickname = scrapy.Field()
    user_name_star_flag = scrapy.Field()
    rate_content = scrapy.Field()
    rate_content_time = scrapy.Field()
    rate_content_append = scrapy.Field()
    rate_append_time = scrapy.Field()
    
    shop_url = scrapy.Field() #店铺的url
    pass
