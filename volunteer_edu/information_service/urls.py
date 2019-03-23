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
from django.urls import path

from information_service import views

urlpatterns = [
    path('register/', views.register),  # 注册信息
    path('register/sms/', views.register_sms),  # 注册验证码
    path('register/safe/', views.register_safe),  # 注册安全模块（暂无）

    path('login/', views.login),  # 登录
    path('logout/', views.logout),  # 登出

    path('home/', views.home),  # 个人中心

    path('update/message/', views.update_message),  # 更新信息
    path('update/image/', views.update_image),  # 更新头像
    path('update/certification/', views.update_certification),  # 更新证书

    path('test/', views.test),
]
