from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ..models import Target
from ..services import AUTH_TARGETS_SESSION

@login_required
def index(request):
    user = request.user
    # 現在認証済みの目標設定を確認
    authed_targets = request.session.get(AUTH_TARGETS_SESSION,[])
    # 自分の目標設定を抽出
    owned_targets = Target.objects.filter(Q(user=user)|Q(uuid__in=authed_targets)).alive().order_by('created_at').reverse().all()
    
    return render(request=request,template_name='account/mypage.html',context={'owned_targets':owned_targets})
