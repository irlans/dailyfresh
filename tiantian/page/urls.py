from django.conf.urls import url,include
from page.views import *
urlpatterns = [
    url(r'^login$',login,name='login'),
    url(r'^register$',register,name='register'),
    url(r'^register_handle$',register_handle,name='register_handle'),
    url(r'^login_handle$',login_handle,name='login_handle'),
    url(r'^user_center_info$',user_center_info,name='user_center_info'),
    url(r'^user_center_order$',user_center_order,name='user_center_order'),
    url(r'^user_center_site$',user_center_site,name='user_center_site'),
    url(r'^quite_login$',quite_login,name='quite_login'),
]