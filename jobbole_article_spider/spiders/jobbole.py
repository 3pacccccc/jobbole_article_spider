# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy
from scrapy.http import Request

from jobbole_article_spider.common.get_md5 import get_md5
from jobbole_article_spider.items import jobbole_article_spider_item


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']


    def parse(self,response):
        post_nodes = response.css('#archive .post-thumb')
        for post_node in post_nodes:
            post_url = post_node.css('a::attr(href)').extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url),  callback=self.parse_detail)       #进入文章的url并调用parse——detail函数进行解析


        # next_page_url = response.css('.next.page-numbers::attr(href)').extract()[0]        #获取下一页的url
        # yield Request(url=parse.urljoin(response.url, next_page_url), callback=self.parse)     #进入下一页并调用parse进行解析从而获取到所有文章的url





    def parse_detail(self, response):
        title = response.css('.entry-header h1::text').extract()[0]
        date = response.css('.entry-meta p::text').extract_first().replace('·', '').strip()
        tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        tag = [element for element in tag_list if not element.strip().endswith('评论')]    #提取文章的标签，如果有‘*评论’出现，则删除
        tags = ','.join(tag)
        content = response.css('.entry').extract()
        praise_nums = int(response.css('.post-adds h10::text').extract()[0])
        collect_nums_str = response.css('.bookmark-btn::text').extract()[0]
        collect_nums_match = re.match('.*?(\d+).*', collect_nums_str)
        if collect_nums_match:
            collect_nums = int(collect_nums_match.group(1))
        else:
            collect_nums = 0                #取出收藏数，收藏数为' 3 收藏'字样，或者为' 收藏‘，有数字则取出数字，没数字取为0
        comment_nums_str = response.css('a[href="#article-comment"] span::text').extract()[0]
        comment_nums_re = re.match('.*?(\d+).*', comment_nums_str)
        if comment_nums_re:
            comment_nums = int(comment_nums_re.group(1))
        else:
            comment_nums = 0                #提取规则与collect_nums同理

        url_object_id = get_md5(response.url)
        image_urls = response.css('.entry img::attr(src)').extract()



        #将所得到的数据载入到item当中
        jobbole_item = jobbole_article_spider_item()
        jobbole_item['title'] = title
        jobbole_item['date'] = date
        jobbole_item['tags'] = tags
        jobbole_item['content'] = content
        jobbole_item['praise_nums'] = praise_nums
        jobbole_item['collect_nums'] = collect_nums
        jobbole_item['comment_nums'] = comment_nums
        jobbole_item['url_object_id'] = url_object_id
        jobbole_item['image_urls'] = image_urls
        return jobbole_item
