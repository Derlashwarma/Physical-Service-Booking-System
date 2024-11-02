from django.urls import path
from .views import AdminViews

app_name = "custom_admin"
urlpatterns = [
    path('overview/',AdminViews.overview, name="overview"),
    path('users/',AdminViews.user_admin_view, name="users"),
    path('users/edit/<int:user_id>',AdminViews.edit_user_admin_view, name="edit_users"),
    path('jobapplications/',AdminViews.job_application_admin, name="job_applications"),
    path('jobapplications/edit/<int:application_id>',AdminViews.edit_application, name="edit_application"),
    path('jobs/',AdminViews.job_admin, name="job_admin")
]
