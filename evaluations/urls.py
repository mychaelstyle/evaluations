"""evaluations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.i18n import i18n_patterns
from competency.views import index
from target.views import target, add_action, auth_passcode, exit_authenticated, evaluation
from account.views import Login, Logout, privacy, terms
from target.views.mypage import index as mypage_index
from target.views import evaluation_report

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('login', Login.as_view(),name="login"),
    path('logout',Logout.as_view(),name="logout"),
    path('privacy',privacy,name="privacy"),
    path('terms',terms,name="terms"),
    path('account/mypage',mypage_index, name="mypage"),
    path('api/1.0/competency/', include('competency.urls')),
    path('api/1.0/target/', include('target.urls')),
    path('target/<str:uuid>/auth', auth_passcode, name="auth-passcode"),
    path('target/<str:uuid>/exit_edit', exit_authenticated, name="exit-authenticated"),
    path('target/<str:uuid>/addaction', add_action, name="add-action"),
    path('target/<str:uuid>/report', evaluation_report, name="evaluation-report"),
    path('target/<str:uuid>', target, name="show-target"),
    path('evaluation/<str:uuid>', evaluation, name="evaluation"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('', index, name="index"),
    prefix_default_language=False
)
