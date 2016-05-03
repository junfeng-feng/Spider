# -*- coding: utf-8 -*-


BOT_NAME = 'tmallshop'

SPIDER_MODULES = ['tmallshop.spiders']
NEWSPIDER_MODULE = 'tmallshop.spiders'

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
     'scrapy.pipelines.images.ImagesPipeline': 1,
    'tmallshop.pipelines.TmallshopPipeline': 300,
}

# 增大并发item, request, perdomain
# CONCURRENT_ITEMS = 512
# CONCURRENT_REQUESTS = 8
# CONCURRENT_REQUESTS_PER_DOMAIN = 64

# mysql config
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'spider_db'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_PORT = 3306

#delay
DOWNLOAD_DELAY = 0.1

#images
IMAGES_STORE = r'./img'
IMAGES_EXPIRES = 90
COOKIES_ENABLES=False