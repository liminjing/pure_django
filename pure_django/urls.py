"""pure_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from my_blog.views import blog,new_blog
from blash.views import blash,new_blash,new_website

from django.conf.urls import url,include
from login.views import index,register,login,logout,user_confirm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',blog),
    path('blash/',blash),

    url(r'^new_blash',new_blash),
    url(r'^new_website',new_website),
    url(r'new_blog',new_blog),

    path('index/',index),
    path('login/',login),
    path('register/',register),
    path('logout/',logout),
    path('captcha',include('captcha.urls')), #验证码
    path('confirm/',user_confirm),
]
