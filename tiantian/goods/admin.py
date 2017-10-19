from django.contrib import admin
from goods.models import *
# Register your models here.
class goods_typeAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']

class goods_infoAdmin(admin.ModelAdmin):
    list_per_page = 15

    list_display = [
        'id',
        'gtitle',
        'gprice',
        'gunit',
        'gclick',
        'gstock',
        'gtypeinfo'
    ]

admin.site.register(Goods_types,goods_typeAdmin)
admin.site.register(Goods_info,goods_infoAdmin)