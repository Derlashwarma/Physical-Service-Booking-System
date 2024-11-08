"""
URL configuration for System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('employee/', include('employee.urls', namespace="employee")),   # Employee app URLs
    path('employer/', include('employer.urls', namespace="employer")),
    path('job/', include('job.urls', namespace='job')),
    path('chat/', include('chat.urls', namespace="chat"))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
