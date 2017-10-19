from django.shortcuts import render
from goods.models import *
from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from cart.views import *
# Create your views here.


def goods_index(request):
    goodsTypeList = Goods_types.objects.all()
    # 根据商品类找商品，并根据ID和点击来分类
    typelist1 = goodsTypeList[0].goods_info_set.order_by('-id')[0:4]
    typelist11 = goodsTypeList[0].goods_info_set.order_by('-gclick')[0:4]

    typelist2 = goodsTypeList[1].goods_info_set.order_by('-id')[0:4]
    typelist22 = goodsTypeList[1].goods_info_set.order_by('-gclick')[0:4]

    typelist3 = goodsTypeList[2].goods_info_set.order_by('-id')[0:4]
    typelist33 = goodsTypeList[2].goods_info_set.order_by('-gclick')[0:4]

    typelist4 = goodsTypeList[3].goods_info_set.order_by('-id')[0:4]
    typelist44 = goodsTypeList[3].goods_info_set.order_by('-gclick')[0:4]

    typelist5 = goodsTypeList[4].goods_info_set.order_by('-id')[0:4]
    typelist55 = goodsTypeList[4].goods_info_set.order_by('-gclick')[0:4]

    typelist6 = goodsTypeList[5].goods_info_set.order_by('-id')[0:4]
    typelist66 = goodsTypeList[5].goods_info_set.order_by('-gclick')[0:4]

    count = cart_count(request)
    content = {
        'typelist1': typelist1, 'typelist11': typelist11,
        'typelist2': typelist2, 'typelist22': typelist22,
        'typelist3': typelist3, 'typelist33': typelist33,
        'typelist4': typelist4, 'typelist44': typelist44,
        'typelist5': typelist5, 'typelist55': typelist55,
        'typelist6': typelist6, 'typelist66': typelist66,
        'count':count
    }
    return render(request,'page/index.html',content)


def goods_detail(request,id):
    goods_info = Goods_info.objects.get(id=id)
    typeid = goods_info.gtypeinfo_id                     #商品页面根据商品来查找种类
    type = Goods_types.objects.filter(id=typeid)[0]

    #推荐商品
    recommend = Goods_types.objects.filter(id=typeid)[0].goods_info_set.order_by('id')[::-1]

    #商品点击量增加
    goods_info.gclick +=1
    goods_info.save()

    count = cart_count(request)
    content={
        'goods_info':goods_info,        #商品信息
        'type':type,                    #商品种类
        'recommend':recommend[0:2],      #荐商品
        'count':count
    }
    response = render(request, 'page/detail.html', content)

    #将最近浏览保存到cookie
    recent = request.COOKIES.get('Recent','')
    if recent != '':
        recent1 = recent.split(',')
        if recent1.count(id)>=1:
            recent1.remove(id)
        recent1.insert(0,id)
        if len(recent1)>=6:
            del recent1[5]
        recent = ','.join(recent1)
    else:
        recent = str(id)
    response.set_cookie('Recent',recent)

    return response


def goods_list(request,tid,index,sort):
    type = Goods_types.objects.filter(id=tid)[0]
    infolist_bynew = type.goods_info_set.order_by('-id')[0:2]
    infolist = type.goods_info_set.all()
    #根据排序种类排序
    if sort=='1':
        infolist = infolist.order_by('-id')
    elif sort=='2':
        infolist = infolist.order_by('gprice')
    elif sort=='3':
        infolist = infolist.order_by('-gclick')

    #对商品列表分类
    paginator = Paginator(infolist,5)
    page_list = paginator.page(index).object_list
    page = paginator.page(index)

    content = {
        'type':type,
        'infolist':page_list,
        'infolist_bynew':infolist_bynew,
        'page':page,
        'paginator':paginator,
        'sort':sort

    }
    return render(request,'page/list.html',content)

def findInfo(request,tid,index,sort):
    keyword = request.GET.get('keyword')
    goodslist = Goods_info.objects.all()
    goods_recommend = goodslist.order_by('-id')[0:2]
    if tid == '0':
        goodslist = Goods_info.objects.all()
    else:
        goodslist = Goods_types.objects.filter(id=tid)[0].goods_info_set
    #匹配关键字的queryset列表
    goods_find_list = goodslist.filter(
        Q(gtitle__icontains=keyword)|Q(gcontent__icontains=keyword)|Q(gintroduction__contains=keyword)
    )

    #根据排序种类排序
    if sort=='1':
        goods_find_list = goods_find_list.order_by('-id')
    elif sort=='2':
        goods_find_list = goods_find_list.order_by('gprice')
    elif sort=='3':
        goods_find_list = goods_find_list.order_by('-gclick')

    #分页
    paginator=Paginator(goods_find_list,2)
    page = paginator.page(index)

    content={
        'tid':tid,
        'goods_recommend':goods_recommend,
        'paginator':paginator,
        'page':page,
        'sort':sort,
        'keyword':keyword,
    }

    return render(request,'page/find.html',content)

'''
def infopage(request):
    return HttpResponse('xxx')
'''