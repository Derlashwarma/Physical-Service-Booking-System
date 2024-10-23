from django.urls import path
from .views import JobViews 

app_name="job"

urlpatterns = [
    path('', JobViews.add_job,name='add_job'),
    path('apply/<int:job_id>', JobViews.apply_job,name='apply_job')
]
