from django.conf.urls import url
from order.views import *
from cart.views import *
urlpatterns = [
    url(r'^order/$',order),
    url(r'^order/order_handle/$',order_handle),
    url(r'^order_show(\d*)/$',show),
    url(r'^pay(\d+)/$',pay),
]