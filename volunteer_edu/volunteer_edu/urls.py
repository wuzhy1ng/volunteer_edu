"""volunteer_edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

# from information_service.admin import admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('information_service.urls')),
    path('reserve/', include('reservation_service.urls')),
    path('recommend/', include('recommend_service.urls')),
    re_path('media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

# admin设置
admin.site.site_header = '大学生志愿家教平台运维系统'
admin.site.site_title = '大学生志愿家教平台'
