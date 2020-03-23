# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NewsspiderPipeline(object):
    def process_item(self, item, spider):
        # 设置保存的文件名，把子链接去掉'http://'和'.shtml'，把'/'替换成‘_’，保存为txt文件格式
        self.filename = item['sonUrl'][7:-6].replace('/', '_') + '.txt'
        self.file = open(item['subpath'] + '/' + self.filename, 'w')
        #self.file.write(item['sonUrl'] + '\n' + item['head'] + '\n' + item['time'] + '\n' + item['content'])
        self.file.write(item['parentUrl'] + '\n' + item['parentTitle'] + '\n'
                        + item['subUrl'] + '\n' + item['subTitle'] + '\n'
                        +item['sonUrl'] + '\n' + item['head'] + '\n' + item['time'] + '\n' + item['content'])
        self.file.close()

        return item
