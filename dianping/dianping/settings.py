# -*- coding: utf-8 -*-

# Scrapy settings for dianping project
#

BOT_NAME = 'dianping'

SPIDER_MODULES = ['dianping.spiders']
NEWSPIDER_MODULE = 'dianping.spiders'

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'dianping.pipelines.DianpingPipeline': 300,
}

# mysql config
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'spider_db'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_PORT = 3306

#delay
DOWNLOAD_DELAY = 2
COOKIES_ENABLES=False


HTTP_PROXY = 'http://127.0.0.1:8123'

#images
IMAGES_STORE = r'./img'
IMAGES_EXPIRES = 90

DOWNLOADER_MIDDLEWARES = {  
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,  
        'dianping.spiders.rotate_useragent.RotateUserAgentMiddleware' :400  
    } 