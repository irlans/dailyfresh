from django.db import models
from page.models import *
from goods.models import *
# Create your models here.


class Cartinfo(models.Model):
    userInfo = models.ForeignKey(userinfo)              #用户
    goodsinfo = models.ForeignKey(Goods_info)           #商品
    count = models.IntegerField()                       #数量
