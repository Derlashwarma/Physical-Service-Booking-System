from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('',views.login_user,name='login'),
]
