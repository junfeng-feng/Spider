# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JiuzhengItem(scrapy.Item):
    # define the fields for your item here like:
    question_id = scrapy.Field()
    question_title = scrapy.Field()
    question_category = scrapy.Field()
    question_description = scrapy.Field()
    is_question = scrapy.Field()
    
    
    answer_id = scrapy.Field()
    answer_content = scrapy.Field()
    is_best = scrapy.Field()
    
    imageStatus = scrapy.Field()
    
    # images
#     image_urls = scrapy.Field()
#     images = scrapy.Field()
    pass
