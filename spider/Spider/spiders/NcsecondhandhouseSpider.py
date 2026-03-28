# # -*- coding: utf-8 -*-

# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import NcsecondhandhouseItem
import time
from datetime import datetime,timedelta
import datetime as formattime
import re
import random
import platform
import json
import os
import urllib
from urllib.parse import urlparse
import requests
import emoji
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from selenium.webdriver import ChromeOptions, ActionChains
from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# 南昌二手房
class NcsecondhandhouseSpider(scrapy.Spider):
    name = 'ncsecondhandhouseSpider'
    spiderUrl = 'https://nc.lianjia.com/ershoufang/pg{}/'
    start_urls = spiderUrl.split(";")
    protocol = ''
    hostname = ''
    realtime = False


    def __init__(self,realtime=False,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realtime = realtime=='true'

    def start_requests(self):

        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '48yv847n_ncsecondhandhouse') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        pageNum = 1 + 1

        for url in self.start_urls:
            if '{}' in url:
                for page in range(1, pageNum):

                    next_link = url.format(page)
                    yield scrapy.Request(
                        url=next_link,
                        callback=self.parse
                    )
            else:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse
                )

    # 列表解析
    def parse(self, response):
        _url = urlparse(self.spiderUrl)
        self.protocol = _url.scheme
        self.hostname = _url.netloc
        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '48yv847n_ncsecondhandhouse') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        list = response.css('div#content div.leftContent ul.sellListContent li[class~="LOGCLICKDATA"]')
        for item in list:
            fields = NcsecondhandhouseItem()

            if '(.*?)' in '''div.totalPrice.totalPrice2 span::text''':
                try:
                    fields["totalprice"] = float( re.findall(r'''div.totalPrice.totalPrice2 span::text''', item.extract(), re.DOTALL)[0].strip())
                except:
                    pass
            else:
                try:
                    fields["totalprice"] = float( self.remove_html(item.css('div.totalPrice.totalPrice2 span::text').extract_first()))
                except:
                    pass
            if '(.*?)' in '''div.unitPrice::attr(data-price)''':
                try:
                    fields["unitprice"] = float( re.findall(r'''div.unitPrice::attr(data-price)''', item.extract(), re.DOTALL)[0].strip())
                except:
                    pass
            else:
                try:
                    fields["unitprice"] = float( self.remove_html(item.css('div.unitPrice::attr(data-price)').extract_first()))
                except:
                    pass
            if '(.*?)' in '''li[class~="LOGCLICKDATA"] div[class~="info"] div.title a::attr(href)''':
                try:
                    fields["laiyuan"] = str( re.findall(r'''li[class~="LOGCLICKDATA"] div[class~="info"] div.title a::attr(href)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["laiyuan"] = str( self.remove_html(item.css('''li[class~="LOGCLICKDATA"] div[class~="info"] div.title a::attr(href)''').extract_first()))

                except:
                    pass
            detailUrlRule = item.css('li[class~="LOGCLICKDATA"] div[class~="info"] div.title a::attr(href)').extract_first()
            if self.protocol in detailUrlRule or detailUrlRule.startswith('http'):
                pass
            elif detailUrlRule.startswith('//'):
                detailUrlRule = self.protocol + ':' + detailUrlRule
            elif detailUrlRule.startswith('/'):
                detailUrlRule = self.protocol + '://' + self.hostname + detailUrlRule
            else:
                detailUrlRule = self.protocol + '://' + self.hostname + '/' + detailUrlRule
            yield scrapy.Request(url=detailUrlRule, meta={'fields': fields},  callback=self.detail_parse, dont_filter=True)

    # 详情解析
    def detail_parse(self, response):
        fields = response.meta['fields']
        try:
            if '(.*?)' in '''div.sellDetailHeader div.title-wrapper div.content div.title h1.main::text''':
                fields["title"] = str( re.findall(r'''div.sellDetailHeader div.title-wrapper div.content div.title h1.main::text''', response.text, re.S)[0].strip())

            else:
                if 'title' != 'xiangqing' and 'title' != 'detail' and 'title' != 'pinglun' and 'title' != 'zuofa':
                    fields["title"] = str( self.remove_html(response.css('''div.sellDetailHeader div.title-wrapper div.content div.title h1.main::text''').extract_first()))

                else:
                    try:
                        fields["title"] = str( emoji.demojize(response.css('''div.sellDetailHeader div.title-wrapper div.content div.title h1.main::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.overview div.content div.houseInfo div.room div.mainInfo::text''':
                fields["types"] = str( re.findall(r'''div.overview div.content div.houseInfo div.room div.mainInfo::text''', response.text, re.S)[0].strip())

            else:
                if 'types' != 'xiangqing' and 'types' != 'detail' and 'types' != 'pinglun' and 'types' != 'zuofa':
                    fields["types"] = str( self.remove_html(response.css('''div.overview div.content div.houseInfo div.room div.mainInfo::text''').extract_first()))

                else:
                    try:
                        fields["types"] = str( emoji.demojize(response.css('''div.overview div.content div.houseInfo div.room div.mainInfo::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.overview div.content div.houseInfo div.room div.subInfo::text''':
                fields["floor"] = str( re.findall(r'''div.overview div.content div.houseInfo div.room div.subInfo::text''', response.text, re.S)[0].strip())

            else:
                if 'floor' != 'xiangqing' and 'floor' != 'detail' and 'floor' != 'pinglun' and 'floor' != 'zuofa':
                    fields["floor"] = str( self.remove_html(response.css('''div.overview div.content div.houseInfo div.room div.subInfo::text''').extract_first()))

                else:
                    try:
                        fields["floor"] = str( emoji.demojize(response.css('''div.overview div.content div.houseInfo div.room div.subInfo::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.overview div.content div.houseInfo div.type div.mainInfo::text''':
                fields["orientation"] = str( re.findall(r'''div.overview div.content div.houseInfo div.type div.mainInfo::text''', response.text, re.S)[0].strip())

            else:
                if 'orientation' != 'xiangqing' and 'orientation' != 'detail' and 'orientation' != 'pinglun' and 'orientation' != 'zuofa':
                    fields["orientation"] = str( self.remove_html(response.css('''div.overview div.content div.houseInfo div.type div.mainInfo::text''').extract_first()))

                else:
                    try:
                        fields["orientation"] = str( emoji.demojize(response.css('''div.overview div.content div.houseInfo div.type div.mainInfo::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.overview div.content div.houseInfo div.type div.subInfo::text''':
                fields["fitment"] = str( re.findall(r'''div.overview div.content div.houseInfo div.type div.subInfo::text''', response.text, re.S)[0].strip())

            else:
                if 'fitment' != 'xiangqing' and 'fitment' != 'detail' and 'fitment' != 'pinglun' and 'fitment' != 'zuofa':
                    fields["fitment"] = str( self.remove_html(response.css('''div.overview div.content div.houseInfo div.type div.subInfo::text''').extract_first()))

                else:
                    try:
                        fields["fitment"] = str( emoji.demojize(response.css('''div.overview div.content div.houseInfo div.type div.subInfo::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.overview div.content div.houseInfo div.area div.mainInfo::text''':
                fields["area"] = str( re.findall(r'''div.overview div.content div.houseInfo div.area div.mainInfo::text''', response.text, re.S)[0].strip())

            else:
                if 'area' != 'xiangqing' and 'area' != 'detail' and 'area' != 'pinglun' and 'area' != 'zuofa':
                    fields["area"] = str( self.remove_html(response.css('''div.overview div.content div.houseInfo div.area div.mainInfo::text''').extract_first()))

                else:
                    try:
                        fields["area"] = str( emoji.demojize(response.css('''div.overview div.content div.houseInfo div.area div.mainInfo::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.overview div.content div.houseInfo div.area div.subInfo::text''':
                fields["becompleted"] = str( re.findall(r'''div.overview div.content div.houseInfo div.area div.subInfo::text''', response.text, re.S)[0].strip())

            else:
                if 'becompleted' != 'xiangqing' and 'becompleted' != 'detail' and 'becompleted' != 'pinglun' and 'becompleted' != 'zuofa':
                    fields["becompleted"] = str( self.remove_html(response.css('''div.overview div.content div.houseInfo div.area div.subInfo::text''').extract_first()))

                else:
                    try:
                        fields["becompleted"] = str( emoji.demojize(response.css('''div.overview div.content div.houseInfo div.area div.subInfo::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.overview div.content div.aroundInfo div.communityName a.info::text''':
                fields["plot"] = str( re.findall(r'''div.overview div.content div.aroundInfo div.communityName a.info::text''', response.text, re.S)[0].strip())

            else:
                if 'plot' != 'xiangqing' and 'plot' != 'detail' and 'plot' != 'pinglun' and 'plot' != 'zuofa':
                    fields["plot"] = str( self.remove_html(response.css('''div.overview div.content div.aroundInfo div.communityName a.info::text''').extract_first()))

                else:
                    try:
                        fields["plot"] = str( emoji.demojize(response.css('''div.overview div.content div.aroundInfo div.communityName a.info::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div.overview div.content div.aroundInfo div.areaName span.info a[target="_blank"]::text''':
                fields["region"] = str( re.findall(r'''div.overview div.content div.aroundInfo div.areaName span.info a[target="_blank"]::text''', response.text, re.S)[0].strip())

            else:
                if 'region' != 'xiangqing' and 'region' != 'detail' and 'region' != 'pinglun' and 'region' != 'zuofa':
                    fields["region"] = str( self.remove_html(response.css('''div.overview div.content div.aroundInfo div.areaName span.info a[target="_blank"]::text''').extract_first()))

                else:
                    try:
                        fields["region"] = str( emoji.demojize(response.css('''div.overview div.content div.aroundInfo div.areaName span.info a[target="_blank"]::text''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''div#topImg div#thumbnail2 ul.smallpic li:nth-child(1)::attr(data-src)''':
                fields["cover"] = str( re.findall(r'''div#topImg div#thumbnail2 ul.smallpic li:nth-child(1)::attr(data-src)''', response.text, re.S)[0].strip())

            else:
                if 'cover' != 'xiangqing' and 'cover' != 'detail' and 'cover' != 'pinglun' and 'cover' != 'zuofa':
                    fields["cover"] = str( self.remove_html(response.css('''div#topImg div#thumbnail2 ul.smallpic li:nth-child(1)::attr(data-src)''').extract_first()))

                else:
                    try:
                        fields["cover"] = str( emoji.demojize(response.css('''div#topImg div#thumbnail2 ul.smallpic li:nth-child(1)::attr(data-src)''').extract_first()))

                    except:
                        pass
        except:
            pass
        return fields

    # 数据清洗
    def pandas_filter(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost/spider48yv847n?charset=UTF8MB4')
        df = pd.read_sql('select * from ncsecondhandhouse limit 50', con = engine)

        # 重复数据过滤
        df.duplicated()
        df.drop_duplicates()

        #空数据过滤
        df.isnull()
        df.dropna()

        # 填充空数据
        df.fillna(value = '暂无')

        # 异常值过滤

        # 滤出 大于800 和 小于 100 的
        a = np.random.randint(0, 1000, size = 200)
        cond = (a<=800) & (a>=100)
        a[cond]

        # 过滤正态分布的异常值
        b = np.random.randn(100000)
        # 3σ过滤异常值，σ即是标准差
        cond = np.abs(b) > 3 * 1
        b[cond]

        # 正态分布数据
        df2 = pd.DataFrame(data = np.random.randn(10000,3))
        # 3σ过滤异常值，σ即是标准差
        cond = (df2 > 3*df2.std()).any(axis = 1)
        # 不满⾜条件的⾏索引
        index = df2[cond].index
        # 根据⾏索引，进⾏数据删除
        df2.drop(labels=index,axis = 0)

    # 去除多余html标签
    def remove_html(self, html):
        if html == None:
            return ''
        pattern = re.compile(r'<[^>]+>', re.S)
        return pattern.sub('', html).strip()

    # 数据库连接
    def db_connect(self):
        type = self.settings.get('TYPE', 'mysql')
        host = self.settings.get('HOST', 'localhost')
        port = int(self.settings.get('PORT', 3306))
        user = self.settings.get('USER', 'root')
        password = self.settings.get('PASSWORD', '123456')

        try:
            database = self.databaseName
        except:
            database = self.settings.get('DATABASE', '')

        if type == 'mysql':
            connect = pymysql.connect(host=host, port=port, db=database, user=user, passwd=password, charset='utf8')
        else:
            connect = pymssql.connect(host=host, user=user, password=password, database=database)
        return connect

    # 断表是否存在
    def table_exists(self, cursor, table_name):
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]

        if table_name in table_list:
            return 1
        else:
            return 0

    # 数据缓存源
    def temp_data(self):

        connect = self.db_connect()
        cursor = connect.cursor()
        sql = '''
            insert into `ncsecondhandhouse`(
                id
                ,title
                ,totalprice
                ,unitprice
                ,types
                ,floor
                ,orientation
                ,fitment
                ,area
                ,becompleted
                ,plot
                ,region
                ,cover
                ,laiyuan
            )
            select
                id
                ,title
                ,totalprice
                ,unitprice
                ,types
                ,floor
                ,orientation
                ,fitment
                ,area
                ,becompleted
                ,plot
                ,region
                ,cover
                ,laiyuan
            from `48yv847n_ncsecondhandhouse`
            where(not exists (select
                id
                ,title
                ,totalprice
                ,unitprice
                ,types
                ,floor
                ,orientation
                ,fitment
                ,area
                ,becompleted
                ,plot
                ,region
                ,cover
                ,laiyuan
            from `ncsecondhandhouse` where
                `ncsecondhandhouse`.id=`48yv847n_ncsecondhandhouse`.id
            ))
            order by rand()
            limit 50;
        '''

        cursor.execute(sql)
        connect.commit()
        connect.close()
