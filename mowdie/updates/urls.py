from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^new/', views.add_update, name="add_update"),
    url(r'^(?P<update_id>\d+)$', views.show_update, name="show_update"),
    url(r'^(?P<update_id>\d+)/favorite$', views.add_favorite, name="add_favorite"),
]
