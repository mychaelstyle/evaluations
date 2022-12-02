from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.api_task.search, name="tasks"),
    path('task/<int:id>',views.api_task.task, name="task"),
    path('', views.api.competencies, name="competencies"),
    path('<int:id>',views.api.competency, name="competency"),
]
