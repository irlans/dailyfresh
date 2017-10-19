from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
def login_check(func):
    def check(request,*args,**kwargs):
        if request.session.get('username',''):
            return func(request,*args,**kwargs)
        else:
            current_url = request.path
            redirect = HttpResponseRedirect(reverse('login'))
            redirect.set_cookie('url',current_url,)
            return redirect
    return check