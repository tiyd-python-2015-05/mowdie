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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from updates import views as update_views

from home.views import AboutView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', RedirectView.as_view(url='/updates/')),
    url(r'^(?P<update_id>\d+)$', update_views.UpdateRedirectView.as_view()),
    url(r'^updates/', include('updates.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^about/', AboutView.as_view(), name="about")
]
