from django.urls import path
from .views import *

app_name="rate"

urlpatterns = [
    path('<str:username>/<int:job_id>',rate_user, name="rate_user")
]
