# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobboleArticleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class jobbole_article_spider_item(scrapy.Item):
    title = scrapy.Field()
    tags = scrapy.Field()
    praise_nums = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    comment_nums = scrapy.Field()
    collect_nums = scrapy.Field()
    url_object_id = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()



