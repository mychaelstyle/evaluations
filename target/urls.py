from django.urls import path
from . import views

urlpatterns = [
    path('create', views.api.create, name="api-target-create"),
    path('self_evaluation/<int:id>', views.api.self_evaluation, name="self-evaluation"),
]
