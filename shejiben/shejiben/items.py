# -*- coding: utf-8 -*-
import scrapy

class ShejibenItem(scrapy.Item):
    #标记
    flag =  scrapy.Field()
    
    #设计师
    designer_id = scrapy.Field()
    designer_name = scrapy.Field()
    signature = scrapy.Field()
    consulting_number = scrapy.Field()
    view_number = scrapy.Field()
    designer_position = scrapy.Field()
    address = scrapy.Field()
    style = scrapy.Field()
    experience = scrapy.Field()
    fee = scrapy.Field()
    certification_rewords = scrapy.Field()
    introduction = scrapy.Field()
    head_photo = scrapy.Field()
    followers_number = scrapy.Field()
    renqi = scrapy.Field()
    follows = scrapy.Field()
    
    #设计师评论
    designer_id = scrapy.Field()
    rate_id = scrapy.Field()
    rate_content = scrapy.Field()
    rate_img = scrapy.Field()
    rate_addr = scrapy.Field()
    rate_datetime = scrapy.Field()
    user_name = scrapy.Field()
    user_photo = scrapy.Field()
    

    #设计师博客
    designer_id = scrapy.Field()
    blog_id = scrapy.Field()
    blog_title = scrapy.Field()
    blog_datetime = scrapy.Field()
    view_number = scrapy.Field()
    blog_content = scrapy.Field()
    blog_img = scrapy.Field()
    blog_author = scrapy.Field()    
    
    # images
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
