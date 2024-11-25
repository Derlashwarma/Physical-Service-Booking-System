from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customadmin/', include('custom_admin.urls', namespace="custom_admin")),
    path('register/',include('register.urls', namespace="register")),
    path('login/',include('login.urls', namespace="login")),
    path('', include('landing.urls', namespace="landing")),
    path('profile/', include('profile.urls', namespace='profile')),
    path('employee/', include('employee.urls', namespace="employee")),
    path('employer/', include('employer.urls', namespace="employer")),
    path('job/', include('job.urls', namespace='job')),
    path('chat/', include('chat.urls', namespace="chat")),
    path('rate/', include('rate.urls', namespace='rate'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
