from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^new/', views.add_update, name="add_update"),
    url(r'^(?P<update_id>\d+)$', views.show_update, name="show_update"),
    url(r'^(?P<update_id>\d+)/favorite$', views.add_favorite, name="add_favorite"),
    url(r'^(?P<update_id>\d+)/favorite/delete$', views.delete_favorite, name="delete_favorite"),
    url(r'^followed/', views.followed_updates, name="followed_updates"),
    url(r'^favorite/', views.most_favorited_updates, name="most_favorited_updates")
]
