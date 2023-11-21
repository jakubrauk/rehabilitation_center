from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_visit/', views.create_visit, name='create_visit'),
    path('visits/', views.visits, name='visits'),
    path('assign_visit/<str:pk>', views.assign_visit, name='assign_visit')
]
