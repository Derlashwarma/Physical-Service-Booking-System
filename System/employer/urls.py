from django.urls import path
from . import views

app_name = 'employer' 
urlpatterns = [
    path('feed/', views.employer_feed, name='employer_feed'),
]