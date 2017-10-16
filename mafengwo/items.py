# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MafengwoItem(scrapy.Item):
    name = scrapy.Field()   # 景点名称
    code = scrapy.Field()   # 景点代码
    pic = scrapy.Field()    # 景点大图的地址
    desc = scrapy.Field()   # 景点的简介
    city = scrapy.Field()   # 景点所属城市
