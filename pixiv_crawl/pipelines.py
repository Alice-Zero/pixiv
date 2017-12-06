# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import json
import os
"""存储图片的META，供后续的页面展示等使用"""


class PixivMetaPipeline(object):
    def process_item(self, item, spider):
        settings = spider.settings
        os.chdir(settings['IMAGES_STORE'])
        img_path = str(item['rank']) + '_' + item['title'] + '_' + item['user_name']
        for ch in ('\\', '/', ':', '*', '?', '\"', '<', '>', '|'):
            img_path = img_path.replace(ch, 'O')
        img_path = 'full/' + img_path
        if (item['work_dis'] == 'manga')and(not os.path.exists(img_path)): os.mkdir(img_path)
        for i, image_path in enumerate(item['image_paths']):
            suffix = image_path[-(len(image_path) - image_path.rfind('.')):]
            if item['work_dis'] == 'manga':
                image_path_new = img_path + '/p' + str(i) + suffix
            else:
                image_path_new = img_path + suffix
            os.rename(image_path, image_path_new)
            item['image_paths'][i] = image_path_new
        self.file.write(json.dumps(dict(item)) + "\n")
        return item

    def open_spider(self, spider):
        settings = spider.settings
        file_path = settings['IMAGES_STORE'] + '/meta.json'
        self.file = open(file_path, 'w')
        self.file.write('[')
        return

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()
        return


class PixivImagesPipeline(ImagesPipeline):
    """抽取ITEM中的图片地址，并下载"""

    def get_media_requests(self, item, info):
        try:
            for image_url in item['img_urls']:
                yield scrapy.Request(
                    image_url,
                    headers={
                        'Referer':
                        item['url'],  #添加Referer，否则会返回403错误
                        'User-Agent':
                        'Mozilla/5.0 (Macintosh; '
                        'Intel Mac OS X 10_10_5) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/45.0.2454.101 Safari/537.36'
                    })
        except KeyError:
            raise DropItem("Item contains no images")

    def item_completed(self, results, item, info):
        #image_paths这段都没看懂，Python好高深，大概意思是获取results列表中获取到图片的地址
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("无法处理的图片展示页面")
        item['image_paths'] = image_paths
        return item
