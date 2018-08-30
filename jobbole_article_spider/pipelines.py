# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.http import Request


from scrapy.pipelines.images import ImagesPipeline

class JobboleArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item



class jobbole_article_spider_pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(url=image_url, meta={'item': item})


    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok ]
        if not image_path:
            raise DropItem('item got no images')
        return item


    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem('item contains no images')
    #     return item


    # def item_completed(self, results, item, info):
    #     for ok, x in results:
    #         if ok:
    #             image_path = x['path']
    #     item['image_path'] = image_path
    #     return item

        # def file_path(self, request, response=None, info=None):
        #     item = request.meta['item']
        #     image_guid = request.url.split('/')[-1]
        #     filenames = 'full/%s/%s' % (item["title"], image_guid)
        #     return filenames

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split['/'][-1]
        filenames = 'full/%s/%s/' % (item['title'], image_guid)
        return filenames
