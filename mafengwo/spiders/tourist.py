# -*- coding: utf-8 -*-

import time
import json
import scrapy
from mafengwo.items import MafengwoItem
from bs4 import BeautifulSoup

class TouristSpider(scrapy.Spider):
    """
    蚂蜂窝站点中国景点数据爬虫
    """
    name = "tourist"
    allowed_domains = ["mafengwo.cn"]
    start_urls = ['http://www.mafengwo.cn/jd/21536/gonglve.html']   # 中国的所有景点数据初始链接   

    def parse(self, response):
        """
        获取cookies，并生成中国所有景点页面数据的链接
        """
        tourist_base_url = 'http://www.mafengwo.cn/ajax/router.php'

        cookie_list = response.headers.getlist('Set-Cookie')  # 获取cookies
        def parse_cookies(cookie_list):
            """
            将列表型的cookies解析为字典，以便后续的使用
            """
            cookies = {}
            for cookie in cookie_list:
                key = cookie.decode().split(';')[0].split('=')[0].strip()
                value = cookie.decode().split(';')[0].split('=')[1].strip()
                cookies.update({key:value})
            return cookies
        cookies = parse_cookies(cookie_list)

        global_vars = {'cookies':cookies} # meta=global_vars仅仅是在本模块不同函数中传递的信息(与http请求无关)

        city_code = '21536'     # 中国的代码
        page_counts = 5      # 页数
        #params = {'iMddid':city_code, 'iPage':str(1), 'iTagId':'0', 'sAct':'KMdd_StructWebAjax|GetPoisByTag'}
        #yield scrapy.FormRequest(tourist_base_url, formdata=params, callback=self.parse_get_all_tourist_url, cookies=cookies, meta=global_vars)
        for page_count in range(1, page_counts+1):  # 获取所有页的景点数据
            time.sleep(2)
            params = {'iMddid':city_code, 'iPage':str(page_count), 'iTagId':'0', 'sAct':'KMdd_StructWebAjax|GetPoisByTag'}
            yield scrapy.FormRequest(tourist_base_url, formdata=params, callback=self.parse_get_all_tourist_url, cookies=cookies, meta=global_vars)

    def parse_get_all_tourist_url(self, response):
        """
        生成中国所有的景点链接

        """
        html_json = json.loads(response.body_as_unicode())['data']['list']
        import re
        tourist_code_list = re.findall('/poi/(\d*)\.html', html_json)
        #yield scrapy.Request("http://www.mafengwo.cn/poi/3474.html", callback=self.parse_tourist, cookies=response.meta['cookies'], meta={'code':3474})
        for tourist_code in tourist_code_list:
            time.sleep(2)
            url = 'http://www.mafengwo.cn/poi/{}.html'.format(tourist_code)
            yield scrapy.Request(url, callback=self.parse_tourist, cookies=response.meta['cookies'], meta={'code':tourist_code})

    def parse_tourist(self, response):
        """
        解析景点页面中景点的具体信息，使用MafengwoItem进行保存
        """
        item = MafengwoItem()
        try:
            item['name'] = response.css('div.title > h1::text')[0].extract() # 获取名字
            item['code'] = response.meta['code'] # 获取景点代码
            item['pic'] = response.css('div.pic-big > img::attr(src)')[0].extract() # 获取大图
            #item['desc'] = response.css('div.summary::text')[0].extract() # 获取描述 注意：有些会error
            #desc_texts = response.xpath('//div[@class="summary"]//text()').extract() # 获取描述标签
            #desc = ''
            #for desc_text in desc_texts:
            #    desc += desc_text.strip()
            item['desc'] = BeautifulSoup(response.text).find('div', class_='summary').get_text()
            item['city'] = response.css('div.item div.drop span.hd a::text')[0].extract() # 获取城市
        except Exception as e:
            print("\n{}: 获取信息失败".format(response.url))
            # scrapy.log.DEBUG("{}: 获取信息失败".format(response.url))
            return None
        return item
