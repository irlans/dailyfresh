from django.conf.urls import url
from goods.views import *
urlpatterns = [
    url(r'^$',goods_index),
    url(r'^(\d+)$',goods_detail),
    url(r'^list/(\d+)/(\d+)/(\d+)$',goods_list),
    url(r'^find/(\d+)/(\d+)/(\d+)$',findInfo),
    #url(r'^infopage$',infopage),
]