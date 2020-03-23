# -*- coding: utf-8 -*-

import os
import scrapy
from newsSpider.items import NewsspiderItem

class newsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):

        #　通过某节点作为根节点进行大类链接遍历
        for each in response.xpath("//div[@id='tab01']/div[@data-sudaclick!='citynav']"):
            # 获取大类链接和大类标题
            #encode('utf-8') string编码为bytes
            parentUrl = each.xpath('./h3/a/@href').extract()[0]
            #parentTitle = each.xpath('./h3/a/text()').extract()[0].encode('utf-8')
            parentTitle = each.xpath('./h3/a/text()').extract()[0]
            # 设置大类存储路径
            parentpath = './data/' + parentTitle
            #parentpath = parentTitle
            if not os.path.exists(parentpath):
                os.makedirs(parentpath)

            #　遍历小类链接
            for other in each.xpath("./ul/li/a"):

                #　获取以大类链接开头的小类链接
                if other.xpath('./@href').extract()[0].startswith(parentUrl):
                    #　注意item的位置，不同的位置会导致不同的结果。尽量不要把item的数据在外循环和内循环里面分别获取，如必须这样做，则创建空列表添加item来解决。
                    item = NewsspiderItem()
                    subUrl = other.xpath('./@href').extract()[0]
                    subTitle = other.xpath('./text()').extract()[0]
                    subpath = parentpath + '/' + subTitle
                    item['parentUrl'] = parentUrl
                    item['parentTitle'] = parentTitle
                    item['subUrl'] = subUrl
                    item['subTitle'] = subTitle
                    item['subpath'] = subpath

                    if not os.path.exists(subpath):
                        os.makedirs(subpath)

                    #　发送小类链接请求，使用meta参数把item数据传递到回调函数里面，通过response.meta['']得到数据
                    yield scrapy.Request(url=item['subUrl'],meta={'meta_1':item},callback=self.second_parse)


    def second_parse(self,response):

        # 获取meta参数里面键为'meta_1'的值
        meta_1 = response.meta['meta_1']
        items = []
        #　遍历小类里面的子链接
        for each in response.xpath('//a/@href'):
            #　获取的子链接，以大类链接开头，以.shtml结尾
            if each.extract().encode('utf-8').startswith(meta_1['parentUrl'].encode('utf-8')) and each.extract().encode('utf-8').endswith('.shtml'.encode('utf-8')):
                item = NewsspiderItem()
                item['parentUrl'] = meta_1['parentUrl']
                item['parentTitle'] = meta_1['parentTitle']
                item['subUrl'] = meta_1['subUrl']
                item['subTitle'] = meta_1['subTitle']
                item['subpath'] = meta_1['subpath']
                item['sonUrl'] = each.extract()
                items.append(item)


        # 发送子链接请求
        for each in items:
            yield scrapy.Request(each['sonUrl'],meta={'meta_2':each},callback=self.detail_parse)

    def detail_parse(self,response):
        item = response.meta['meta_2']
        # 获取标题和内容不为空的子链接
        #if len(response.xpath("//div[@id='top_bar']/div[1]/div[1]/text()")) != 0 and len(response.xpath("//div[@class='article']/p/text()")) != 0:
            # item['head'] = response.xpath("//h1[@class='main-title']"))
        item['head'] = ''.join(response.xpath("//div[@id='top_bar']/div[1]/div[1]/text()").extract())
        item['time'] = ''.join(response.xpath("//div[@id='top_bar']/div/div[2]/span/text()").extract())
        item['content'] = ''.join(response.xpath("//div[@id='artibody']/p/text()").extract())
        #$x('//div[@id="top_bar"]/div/div[2]/span')
        #   item['head'] = response.xpath("//h1[@class='main-title']/text()").extract()[0].encode('utf-8')
        #   item['content'] = ''.join(response.xpath("//div[@class='article']/p/text()").extract()).encode('utf-8')
        #   yield item

        #scrapy crawl news
        yield item