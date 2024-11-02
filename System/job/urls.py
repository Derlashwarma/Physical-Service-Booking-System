from django.urls import path
from .views import JobViews 

app_name="job"

urlpatterns = [
    path('', JobViews.add_job,name='add_job'),
    path('apply/<int:job_id>', JobViews.apply_job,name='apply_job'),
    path('jobs/<int:job_id>', JobViews.show_applications,name='my_jobs'),
    path('edit/<int:job_id>', JobViews.edit_job,name='edit_job'),
    path('accept/<int:application_id>', JobViews.accept_application,name='accept'),
    path('reject/<int:application_id>/', JobViews.reject_application, name='reject')
]
