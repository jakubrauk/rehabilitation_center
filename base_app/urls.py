from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_visit/', views.create_visit, name='create_visit'),
    path('visits/', views.visits, name='visits'),
    path('assign_visit/<str:pk>', views.assign_visit, name='assign_visit'),
    path('confirm_visit/<int:pk>', views.confirm_visit, name='confirm_visit'),
    path('visit_history/', views.show_visits_history, name='visits_history'),
    path('add_feedback/<int:pk>', views.add_feedback, name='add_feedback'),
    path('add_hospital_record/<int:pk>', views.add_hospital_record, name='add_hospital_record'),
    path('profile/', views.profile, name='profile'),
    path('rehabilitators/', views.rehabilitators, name='rehabilitator'),
    path('unconfirmed_visits/', views.show_unconfirmed_visits, name='visits_to_confirm')]


