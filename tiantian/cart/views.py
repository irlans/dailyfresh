from django.shortcuts import render,redirect
from page.login_check import *
from django.http import HttpResponseRedirect,JsonResponse
from cart.models import *
from goods.models import *
from django.db.models import Sum
# Create your views here.

@login_check
def cart(request):
    uid = request.session.get('userid')
    goodsinfo_list = Cartinfo.objects.filter(userInfo_id=uid)
    count = cart_count(request)
    content={
        'goodsinfo_list':goodsinfo_list,
        'count':count
    }
    return render(request,'page/cart.html',content)

def cart_count(requet):
    uid = requet.session.get('userid')
    count = 0
    if uid:
        ret = Cartinfo.objects.filter(userInfo_id=uid).aggregate(num=Sum('count'))
        count = ret['num']
        if count == None:
            count = 0
    return count


@login_check
def cart_add(request,goodsid,count):
    userid = request.session.get('userid')
    goodsid = int(goodsid)
    count = int(count)

    cart_match = Cartinfo.objects.filter(userInfo_id=userid,goodsinfo_id=goodsid)
    if len(cart_match)==1:
        cart = cart_match[0]
        cart.count = cart.count+count
    else:
        cart = Cartinfo()
        cart.userInfo_id = userid
        cart.goodsinfo_id = goodsid
        cart.count = count
    cart.save()
    if request.is_ajax():
        count = cart_count(request)
        return JsonResponse({'count':count})
    else:
        return redirect('/tiantian/cart')


def delete(request,gid):
    userid = request.session.get('userid')
    info = Cartinfo.objects.filter(userInfo_id=userid,goodsinfo_id=gid)
    info.delete()
    count = cart_count(request)
    data = {'flag':1,'count':count}
    return JsonResponse(data)

def alter(request,gid,num):
    cart = Cartinfo.objects.get(goodsinfo_id=int(gid))
    cart.count = num
    cart.save()
    data = {'flag':1}
    return JsonResponse(data)


