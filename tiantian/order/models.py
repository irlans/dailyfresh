from django.db import models
from page.models import *
# Create your models here.


class OrderInfo(models.Model):
    oid = models.CharField(max_length=100,primary_key=True)
    userinfo = models.ForeignKey(userinfo)
    odate = models.DateTimeField(auto_now_add=True)
    oispay = models.BooleanField(default=False)
    ottotal = models.DecimalField(max_digits=10,decimal_places=2)
    oaddress = models.CharField(max_length=150)

class OrderDetailInfo(models.Model):
    goodsinfo = models.ForeignKey('goods.Goods_info')
    orderinfo = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    count = models.IntegerField()