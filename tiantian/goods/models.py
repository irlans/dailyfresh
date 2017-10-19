from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Goods_types(models.Model):
    ttitle = models.CharField(max_length=20,unique=True)            #标题
    isdelete = models.BooleanField(default=False)                   #是否删除
    def __str__(self):
        return self.ttitle

class Goods_info(models.Model):
    gtitle = models.CharField(max_length=100,unique=True)           #标题
    gpic = models.ImageField(upload_to='img/goods')                 #图片
    gprice = models.DecimalField(max_digits=5,decimal_places=2)     #价格
    gunit = models.CharField(max_length=20,default='500g')          #单位
    gclick = models.IntegerField(default=0)                         #点击量
    gintroduction = models.CharField(max_length=200)                #简介
    gstock = models.IntegerField(default=0)                         #库存
    gcontent = HTMLField()                                          #内容
    gtypeinfo = models.ForeignKey(Goods_types)                      #所属类型
    isdelete = models.BooleanField(default=False)                   #是否删除
    def __str__(self):
        return self.gtitle