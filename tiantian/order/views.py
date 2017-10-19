from django.shortcuts import render,redirect
from cart.models import *
from page.models import *
from django.db import transaction
from page.login_check import *
from order.models import *
from datetime import datetime
from django.core.paginator import Paginator
# Create your views here.

@login_check
def order(request):
    user = userinfo.objects.get(id=request.session.get('userid'))
    cart_ids = request.GET.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids ]
    cars = Cartinfo.objects.filter(id__in=cart_ids1)
    cart_ids = ','.join(cart_ids)
    content={
        'cars':cars,
        'cart_ids':cart_ids,
        'user':user
    }
    return render(request,'page/place_order.html',content)

@login_check
@transaction.atomic
def order_handle(request):
    tran_id = transaction.savepoint()
    address = request.POST.get('address')
    carts_id = request.POST.get('carts_id')
    carts_ids = []
    if carts_id!='':
        carts_ids = [int(id) for id in carts_id.split(',')]
    try:
        order = OrderInfo()
        now = datetime.now()
        uid = request.session.get('userid')
        order.oid='%s%d'%(now.strftime('%y%m%d%H%M%S'),uid)
        order.userinfo_id = uid
        order.odate = now.strftime('%Y-%m-%d %H:%M:%S')
        order.oaddress = address
        order.ottotal = 0
        order.save()

        total = 0
        for id in carts_ids:
            detail = OrderDetailInfo()
            detail.orderinfo = order
            cart = Cartinfo.objects.get(id=id)
            goods = cart.goodsinfo
            if goods.gstock>=cart.count:
                goods.gstock = goods.gstock-cart.count
                goods.save()

                detail.goodsinfo = goods
                detail.price = goods.gprice*cart.count
                detail.count = cart.count
                detail.save()

                total = total+goods.gprice*cart.count
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/tiantian/cart')

        order.ottotal = total+10
        order.save()
        transaction.savepoint_commit(tran_id)

    except Exception as e:
        print('异常为%s'%e)
        transaction.savepoint_rollback(tran_id)
    return redirect('/tiantian/order_show/')

@login_check
def show(request,pagenum):
    userid = request.session.get('userid')
    order_lists = OrderInfo.objects.filter(userinfo_id=userid).order_by('-oid')
    paginator = Paginator(order_lists,2)

    if pagenum =='':
        pagenum=1
    page = paginator.page(int(pagenum))

    content = {
        'page_now':1,
        'paginator':paginator,
        'page':page

    }
    return render(request,'page/user_center_order.html',content)


def pay(request,oid):
    order = OrderInfo.objects.get(oid = oid)
    order.oispay = True
    order.save()
    return redirect('/tiantian/order_show')
