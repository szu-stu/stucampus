#coding:utf-8
from django.db import models

# Create your models here.

AREA = (
    ('C', u'南区'),
    ('A', u'西南'),
    ('B', u'斋区'),
)
GIFT_TYPE = (
    ('01', u'食物'),
    ('02', u'服装配饰'),
    ('03', u'钟表首饰'),
    ('04', u'化妆品'),
    ('05', u'运动户外'),
    ('06', u'电器数码'),
    ('07', u'小玩意'),
    ('08', u'手工物件'),
    ('09', u'二次元'),
    ('10', u'图书音像'),
    ('11', u'学习资源'),
    ('12', u'其它'),
)
AIM_GROUP = (
    ('male', u'男性'),
    ('female', u'女性'),
    ('both', u'男女不限'),
)
class GiftSystem_user(models.Model):
    stu_no = models.CharField("学号", max_length=10)
    name = models.CharField("名字", max_length=100)
    phone = models.CharField("手机", max_length=11, null=True)
    area = models.CharField("居住区域", max_length=1, choices=AREA, default=u'南区', null=True)
    wechat = models.CharField("微信号", max_length=50, null=True)
    def __str__(self):
        return self.stu_no
    class Meta:
        permissions = (
            ('manager', '礼物系统管理员'),
        )
class Gift(models.Model):
    giftId = models.CharField("礼物ID", max_length=10, null=True)
    name = models.CharField("礼物名", max_length=100)
    type = models.CharField("礼物类别", choices=GIFT_TYPE, max_length=15)
    description = models.TextField("礼物描述", max_length=1000)
    isAnonymous = models.BooleanField("匿名", default=False)
    own = models.ForeignKey("GiftSystem_user", null=True)
    isExchange = models.BooleanField("是否为交换礼物", default=True)
    isUsed = models.BooleanField("是否已完成交换或赠与", default=False)
    isGet = models.BooleanField("是否已收取礼物", default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "礼物"
        verbose_name_plural = verbose_name
        permissions = (
            ('manager', '礼物系统管理员'),
        )
class ExchangeGift(models.Model):
    gift = models.OneToOneField("Gift", null=True)
    aimGroup = models.CharField("希望送给", choices=AIM_GROUP, max_length=6, null=True)
    def __str__(self):
        return self.gift.name
    class Meta:
        verbose_name = "可互换礼物"
        verbose_name_plural = verbose_name
        permissions = (
            ('manager', '礼物系统管理员'),
        )

class ChangeResult(models.Model):
    exchangegift = models.OneToOneField("ExchangeGift", null=True)
    wangGiftType = models.CharField("回礼类型", max_length=50)
    getGiftId = models.CharField("回礼ID", max_length=10, null=True)
    def __str__(self):
        return self.exchangegift.gift.name
    class Meta:
        verbose_name = u'互换结果'
        verbose_name_plural = verbose_name
        permissions = (
            ('manager', '礼物系统管理员'),
        )

class GivenGift(models.Model):
    gift = models.OneToOneField("Gift")
    givenPerson = models.CharField("收礼者", max_length=100)
    givenPhone = models.CharField("收礼者手机号", max_length=11)
    givenAdress = models.CharField("收礼者具体地址", max_length=1000)
    def __str__(self):
        return self.gift.name
    class Meta:
        verbose_name = "被赠予礼物"
        verbose_name_plural = verbose_name
        permissions = (
            ('manager', '礼物系统管理员'),
        )
