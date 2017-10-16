# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
from sqlalchemy.engine import create_engine

class MafengwoPipeline(object):
    def process_item(self, item, spider):
        return item

class SaveSQLPipeline(object):
    """
    将获取的景点数据保存到MySQL
    """
    def __init__(self):
        username = 'root' # 数据库的用户名
        password = '123456' # 数据库的密码
        hostname = '127.0.0.1' # ip
        database = 'testdata' # 数据库名              #//用户名:密码@主机地址/数据库名
        self._con = create_engine('mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(username, password, hostname, database))
        self._count = 0
        
    def process_item(self, item, spider):
        self._count += 1
        p = self._count*100/(15*2500)
        print('\r当前进度是 {:8.5}%'.format(p), end='')
        if item:
            item_df = pd.DataFrame([['','','','','']], columns=['名称', '城市', '代码', '简介', '图片'])
            item_df.ix[0, '名称'] = item['name']
            item_df.ix[0, '代码'] = item['code']
            item_df.ix[0, '图片'] = item['pic']
            item_df.ix[0, '简介'] = item['desc']
            item_df.ix[0, '城市'] = item['city']
            item_df.to_sql('tourist', self._con, if_exists='append', index=False)
        return item
