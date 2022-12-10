from django.urls import path
from . import views

urlpatterns = [
    path('create', views.api.create, name="api-target-create"),
]
