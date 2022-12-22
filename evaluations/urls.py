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

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/1.0/competency/', include('competency.urls')),
    path('api/1.0/target/', include('target.urls')),
    path('target/<str:uuid>/auth', auth_passcode, name="auth-passcode"),
    path('target/<str:uuid>/exit_edit', exit_authenticated, name="exit-authenticated"),
    path('target/<str:uuid>/addaction', add_action, name="add-action"),
    path('target/<str:uuid>', target, name="show-target"),
    path('evaluation/<str:uuid>', evaluation, name="evaluation"),
    path('', index, name="index"),
    prefix_default_language=False
)
