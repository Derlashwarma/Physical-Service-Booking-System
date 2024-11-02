from django.urls import path
from . import views

app_name = 'employee' 
urlpatterns = [
    path('feed/', views.employee_feed, name='employee_feed'),
]