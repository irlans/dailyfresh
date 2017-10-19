from django.conf.urls import url
from cart.views import *
urlpatterns = [
    url(r'^cart/(\d+)/(\d+)$',cart_add),              #1商品ID,2商品数量
    url(r'^cart/$',cart),
    url(r'^cart/delete/(\d+)',delete),
    url(r'^cart/alter/(\d+)/(\d+)$',alter)
]