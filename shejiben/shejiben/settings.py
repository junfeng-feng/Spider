# -*- coding: utf-8 -*-

BOT_NAME = 'shejiben'

SPIDER_MODULES = ['shejiben.spiders']
NEWSPIDER_MODULE = 'shejiben.spiders'

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'shejiben.pipelines.ShejibenPipeline': 300,
}


# mysql config
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'spider_db'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_PORT = 3306

#delay
# DOWNLOAD_DELAY = 0.01
COOKIES_ENABLES=False


# HTTP_PROXY = 'http://127.0.0.1:8123'

#images
IMAGES_STORE = r'./img'
IMAGES_EXPIRES = 90

# DOWNLOADER_MIDDLEWARES = {  
#         'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,  
#         'dianping.spiders.rotate_useragent.RotateUserAgentMiddleware' :400  
#     } 