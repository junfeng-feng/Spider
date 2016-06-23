# -*- coding: utf-8 -*-

BOT_NAME = 'zhuangyi_company'

SPIDER_MODULES = ['zhuangyi_company.spiders']
NEWSPIDER_MODULE = 'zhuangyi_company.spiders'

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'zhuangyi_company.pipelines.ZhuangyiCompanyPipeline': 300,
}

# mysql config
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'spider_db'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_PORT = 3306

#delay
DOWNLOAD_DELAY = 1
CONCURRENT_ITEMS = 16
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

#images
IMAGES_STORE = r'./img'
IMAGES_EXPIRES = 90

DOWNLOADER_MIDDLEWARES = {  
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,  
        'zhuangyi_company.spiders.rotate_useragent.RotateUserAgentMiddleware' :400  
    } 