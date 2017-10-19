from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from page.models import *
from hashlib import sha1
from page.login_check import *
from goods.models import *
from django.template import loader
# Create your views here.


def login(request):
    cookie_username = request.COOKIES.get('username')
    if cookie_username:
        return render(request,'page/login.html',{'username':cookie_username})
    else:
        return render(request,'page/login.html')


def register(request):

    return render(request,'page/register.html')


def register_handle(request):
    uname = request.POST.get('user_name')
    upwd = request.POST.get('pwd')
    uemail = request.POST.get('email')
    s = sha1()
    s.update(upwd.encode('utf-8'))
    upwd = s.hexdigest()
    user_info = userinfo()
    ret = userinfo.objects.filter(uname=uname)
    if len(ret)==1:
        return HttpResponseRedirect('/tiantian/register')
    else:
        user_info.uname = uname
        user_info.upwd = upwd
        user_info.uemail = uemail
        user_info.save()
        return HttpResponseRedirect('page/login.html')


def login_handle(request):
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    s = sha1()
    s.update(upwd.encode('utf-8'))
    upwd = s.hexdigest()
    ret = userinfo.objects.filter(uname=uname, upwd=upwd)
    if len(ret) == 1:
        #登录成功
        request.session['username'] = uname
        request.session['userid'] = ret[0].id
        redirect = HttpResponseRedirect('/tiantian/user_center_info')
        redirect.set_cookie('username', uname)
        return redirect
    else:
        #账号有误
        if request.POST.get('rememberName') == '1':
            response = HttpResponseRedirect('/tiantian/login')
            response.set_cookie('username', uname)
        return response

@login_check
def user_center_info(request):
    print(request.session.get('username'))
    userid = request.session.get('userid')
    username = userinfo.objects.filter(id=userid)[0].uname
    uphone = userinfo.objects.filter(id=userid)[0].uphone
    uadress = userinfo.objects.filter(id=userid)[0].uaddress

    goodslist = []
    recent = request.COOKIES.get('Recent')
    if recent != None:
        recent1 = recent.split(',')
        for goods_id in recent1:
            goodslist.append(Goods_info.objects.get(id=int(goods_id)))
    content = {
        'username':username,
        'uphone':uphone,
        'uadress':uadress,
        'recentgoods':goodslist,
    }
    return render(request,'page/user_center_info.html',content)

def quite_login(request):
    request.session.flush()
    return HttpResponseRedirect('login')

@login_check
def user_center_order(request):
    return redirect('/tiantian/order_show')

@login_check
def user_center_site(request):
    userid = request.session['userid']
    user_info = userinfo.objects.filter(id=userid)[0]
    if request.method == 'GET':
        ureceive = user_info.ureceive
        uaddress = user_info.uaddress
        content = {
            'ureceive':ureceive,
            'uaddress':uaddress,
        }
    else:
        ureceive = request.POST.get('ureceive')
        uaddress = request.POST.get('uaddress')
        uzipcode = request.POST.get('uzipcode')
        uphone = request.POST.get('uphone')
        user_info.ureceive = ureceive
        user_info.uaddress = uaddress
        user_info.uzipcode = uzipcode
        user_info.uphone = uphone
        user_info.save()
        content = {
            'ureceive': ureceive,
            'uaddress': uaddress,
        }
    return render(request, 'page/user_center_site.html', content)


def index(request):
    return render(request,'page/index.html')