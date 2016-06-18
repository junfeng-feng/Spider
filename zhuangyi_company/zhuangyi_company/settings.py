# -*- coding: utf-8 -*-

# Scrapy settings for zhuangyi_company project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhuangyi_company'

SPIDER_MODULES = ['zhuangyi_company.spiders']
NEWSPIDER_MODULE = 'zhuangyi_company.spiders'

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'zhuangyi.pipelines.ZhuangyiCompanyPipeline': 300,
}

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