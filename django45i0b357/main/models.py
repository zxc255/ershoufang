#coding:utf-8
__author__ = "ila"
from django.db import models

from .model import BaseModel

from datetime import datetime



class yonghu(BaseModel):
    __doc__ = u'''yonghu'''
    __tablename__ = 'yonghu'

    __loginUser__='yonghuzhanghao'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='yonghuzhanghao'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    yonghuzhanghao=models.CharField ( max_length=255,null=False,unique=True, verbose_name='用户账号' )
    xingming=models.CharField ( max_length=255,null=False, unique=False, verbose_name='姓名' )
    mima=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码' )
    xingbie=models.CharField ( max_length=255, null=True, unique=False, verbose_name='性别' )
    shouji=models.CharField ( max_length=255, null=True, unique=False, verbose_name='手机' )
    touxiang=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    '''
    yonghuzhanghao=VARCHAR
    xingming=VARCHAR
    mima=VARCHAR
    xingbie=VARCHAR
    shouji=VARCHAR
    touxiang=Text
    '''
    class Meta:
        db_table = 'yonghu'
        verbose_name = verbose_name_plural = '用户'
class ncsecondhandhouse(BaseModel):
    __doc__ = u'''ncsecondhandhouse'''
    __tablename__ = 'ncsecondhandhouse'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='是'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    orientation=models.CharField ( max_length=255, null=True, unique=False, verbose_name='朝向' )
    fitment=models.CharField ( max_length=255, null=True, unique=False, verbose_name='装修' )
    area=models.CharField ( max_length=255, null=True, unique=False, verbose_name='面积' )
    becompleted=models.CharField ( max_length=255, null=True, unique=False, verbose_name='竣工' )
    plot=models.CharField ( max_length=255, null=True, unique=False, verbose_name='小区' )
    region=models.CharField ( max_length=255, null=True, unique=False, verbose_name='区域' )
    cover=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    laiyuan=models.TextField   (  null=True, unique=False, verbose_name='来源' )
    title=models.CharField ( max_length=255, null=True, unique=False, verbose_name='标题' )
    totalprice=models.FloatField   (  null=True, unique=False, verbose_name='总价(万)' )
    unitprice=models.FloatField   (  null=True, unique=False, verbose_name='单价' )
    types=models.CharField ( max_length=255, null=True, unique=False, verbose_name='户型' )
    floor=models.CharField ( max_length=255, null=True, unique=False, verbose_name='楼层' )
    '''
    orientation=VARCHAR
    fitment=VARCHAR
    area=VARCHAR
    becompleted=VARCHAR
    plot=VARCHAR
    region=VARCHAR
    cover=Text
    laiyuan=Text
    title=VARCHAR
    totalprice=Float
    unitprice=Float
    types=VARCHAR
    floor=VARCHAR
    '''
    class Meta:
        db_table = 'ncsecondhandhouse'
        verbose_name = verbose_name_plural = '南昌二手房'
class ncsecondhandhouseforecast(BaseModel):
    __doc__ = u'''ncsecondhandhouseforecast'''
    __tablename__ = 'ncsecondhandhouseforecast'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    totalprice=models.FloatField   (  null=True, unique=False, verbose_name='总价' )
    region=models.CharField ( max_length=255, null=True, unique=False, verbose_name='区域' )
    '''
    totalprice=Float
    region=VARCHAR
    '''
    class Meta:
        db_table = 'ncsecondhandhouseforecast'
        verbose_name = verbose_name_plural = '房价预测'
class forum(BaseModel):
    __doc__ = u'''forum'''
    __tablename__ = 'forum'



    __authTables__={}
    __foreEndListAuth__='是'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255, null=True, unique=False, verbose_name='帖子标题' )
    content=models.TextField   ( null=False, unique=False, verbose_name='帖子内容' )
    parentid=models.BigIntegerField  (  null=True, unique=False, verbose_name='父节点id' )
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    username=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户名' )
    avatarurl=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    isdone=models.CharField ( max_length=255, null=True, unique=False, verbose_name='状态' )
    istop=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='是否置顶' )
    toptime=models.DateTimeField  (  null=True, unique=False, verbose_name='置顶时间' )
    typename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='分类名称' )
    cover=models.TextField   (  null=True, unique=False, verbose_name='封面' )
    isanon=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='是否匿名(1:是,0:否)' )
    delflag=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='是否删除(1:是,0:否)' )
    '''
    title=VARCHAR
    content=Text
    parentid=BigInteger
    userid=BigInteger
    username=VARCHAR
    avatarurl=Text
    isdone=VARCHAR
    istop=Integer
    toptime=DateTime
    typename=VARCHAR
    cover=Text
    isanon=Integer
    delflag=Integer
    '''
    class Meta:
        db_table = 'forum'
        verbose_name = verbose_name_plural = '在线交流'
class forumtype(BaseModel):
    __doc__ = u'''forumtype'''
    __tablename__ = 'forumtype'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    typename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='分类名称' )
    '''
    typename=VARCHAR
    '''
    class Meta:
        db_table = 'forumtype'
        verbose_name = verbose_name_plural = '在线交流类型'
class forumreport(BaseModel):
    __doc__ = u'''forumreport'''
    __tablename__ = 'forumreport'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    forumid=models.BigIntegerField  (  null=True, unique=False, verbose_name='论坛id' )
    title=models.CharField ( max_length=255, null=True, unique=False, verbose_name='帖子标题' )
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='举报用户id' )
    username=models.CharField ( max_length=255, null=True, unique=False, verbose_name='举报用户名' )
    reporteduserid=models.BigIntegerField  ( null=False, unique=False, verbose_name='被举报用户id' )
    reportedusername=models.CharField ( max_length=255, null=True, unique=False, verbose_name='被举报用户名' )
    reason=models.TextField   ( null=False, unique=False, verbose_name='举报原因' )
    picture=models.TextField   (  null=True, unique=False, verbose_name='图片补充' )
    handleadvise=models.TextField   (  null=True, unique=False, verbose_name='处理建议' )
    status=models.CharField ( max_length=255, null=True, unique=False,default='处理中', verbose_name='状态' )
    reporttype=models.CharField ( max_length=255, null=True, unique=False,default='主题帖举报', verbose_name='举报类型' )
    '''
    forumid=BigInteger
    title=VARCHAR
    userid=BigInteger
    username=VARCHAR
    reporteduserid=BigInteger
    reportedusername=VARCHAR
    reason=Text
    picture=Text
    handleadvise=Text
    status=VARCHAR
    reporttype=VARCHAR
    '''
    class Meta:
        db_table = 'forumreport'
        verbose_name = verbose_name_plural = '在线交流举报'
class newstype(BaseModel):
    __doc__ = u'''newstype'''
    __tablename__ = 'newstype'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    typename=models.CharField ( max_length=255,null=False, unique=False, verbose_name='分类名称' )
    '''
    typename=VARCHAR
    '''
    class Meta:
        db_table = 'newstype'
        verbose_name = verbose_name_plural = '房产资讯分类'
class news(BaseModel):
    __doc__ = u'''news'''
    __tablename__ = 'news'



    __authTables__={}
    __thumbsUp__='是'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='是'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='是'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255,null=False, unique=False, verbose_name='标题' )
    introduction=models.TextField   (  null=True, unique=False, verbose_name='简介' )
    typename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='分类名称' )
    name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='发布人' )
    headportrait=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    clicknum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='点击次数' )
    clicktime=models.DateTimeField  (auto_now=True,  null=True, unique=False, verbose_name='最近点击时间' )
    thumbsupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='赞' )
    crazilynum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='踩' )
    storeupnum=models.IntegerField  (  null=True, unique=False,default='0', verbose_name='收藏数' )
    picture=models.TextField   ( null=False, unique=False, verbose_name='图片' )
    content=models.TextField   ( null=False, unique=False, verbose_name='内容' )
    '''
    title=VARCHAR
    introduction=Text
    typename=VARCHAR
    name=VARCHAR
    headportrait=Text
    clicknum=Integer
    clicktime=DateTime
    thumbsupnum=Integer
    crazilynum=Integer
    storeupnum=Integer
    picture=Text
    content=Text
    '''
    class Meta:
        db_table = 'news'
        verbose_name = verbose_name_plural = '房产资讯'
class storeup(BaseModel):
    __doc__ = u'''storeup'''
    __tablename__ = 'storeup'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    refid=models.BigIntegerField  (  null=True, unique=False, verbose_name='商品id' )
    tablename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='表名' )
    name=models.CharField ( max_length=255,null=False, unique=False, verbose_name='名称' )
    picture=models.TextField   (  null=True, unique=False, verbose_name='图片' )
    type=models.CharField ( max_length=255, null=True, unique=False,default='1', verbose_name='类型' )
    inteltype=models.CharField ( max_length=255, null=True, unique=False, verbose_name='推荐类型' )
    remark=models.CharField ( max_length=255, null=True, unique=False, verbose_name='备注' )
    '''
    userid=BigInteger
    refid=BigInteger
    tablename=VARCHAR
    name=VARCHAR
    picture=Text
    type=VARCHAR
    inteltype=VARCHAR
    remark=VARCHAR
    '''
    class Meta:
        db_table = 'storeup'
        verbose_name = verbose_name_plural = '收藏表'
