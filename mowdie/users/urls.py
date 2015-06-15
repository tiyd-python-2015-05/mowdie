"""mowdie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from users import views as users_views

urlpatterns = [
    url(r'^(?P<user_id>\d+)$', users_views.show_user, name="show_user"),
    url(r'^register/$', users_views.user_register, name="user_register"),
    url(r'^edit/', users_views.edit_profile, name="edit_profile"),
    url(r'^(?P<user_id>\d+)/follow/$', users_views.follow_user,
        name="follow_user"),
]
