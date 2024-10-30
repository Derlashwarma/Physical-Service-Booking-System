from django.urls import path
from .views import AdminViews

app_name = "custom_admin"
urlpatterns = [
    path('overview/',AdminViews.overview, name="overview"),
    path('users/',AdminViews.user_admin_view, name="users"),
    ]
