from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.api_task.search, name="api-tasks"),
    path('task/<int:id>',views.api_task.task, name="api-task"),
    path('', views.api.competencies, name="api-competencies"),
    path('<int:id>',views.api.competency, name="api-competency"),
]
