# -*- coding: utf-8 -*-

BOT_NAME = 'tmallrate'

SPIDER_MODULES = ['tmallrate.spiders']
NEWSPIDER_MODULE = 'tmallrate.spiders'


ITEM_PIPELINES = {
#     'scrapy.pipelines.images.ImagesPipeline': 1,
    'tmallrate.pipelines.TmallratePipeline': 300,
}


#增大并发item, request, perdomain
# CONCURRENT_ITEMS = 64
# CONCURRENT_REQUESTS = 2
# CONCURRENT_REQUESTS_PER_DOMAIN = 2

#mysql config
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'spider_db'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_PORT = 3306

DOWNLOAD_DELAY = 0.05

# IMAGES_STORE = r'D:\ProgramingIDE\workspace\SuperSpider\tmallrate\img'

# IMAGES_EXPIRES = 90

COOKIES_ENABLED=False