# 数据容器文件

import scrapy

class SpiderItem(scrapy.Item):
    pass

class NcsecondhandhouseItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 总价(万)
    totalprice = scrapy.Field()
    # 单价
    unitprice = scrapy.Field()
    # 户型
    types = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 朝向
    orientation = scrapy.Field()
    # 装修
    fitment = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 竣工
    becompleted = scrapy.Field()
    # 小区
    plot = scrapy.Field()
    # 区域
    region = scrapy.Field()
    # 封面
    cover = scrapy.Field()
    # 来源
    laiyuan = scrapy.Field()

