from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "profile"

urlpatterns = [
    path('<str:username>/',views.profile, name='profile'),
    path('edit/<str:username>/',views.edit_profile, name="edit_profile")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
