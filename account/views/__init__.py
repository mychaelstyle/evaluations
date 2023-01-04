from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import LoginForm

@login_required
def mypage(request):
    return render(request=request,template_name='account/mypage.html')

def privacy(request):
    return render(request=request, template_name='privacy.html')

def terms(request):
    return render(request=request, template_name='terms.html')

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'account/login.html'
    def post(self,request):
        return super().post(request)

class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'account/login.html'

