from django.urls import path
from . import views 

app_name="job"

urlpatterns = [
    path('', views.add_job,name='add_job')
]
