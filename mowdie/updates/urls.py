from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^new/', login_required(views.AddUpdateView.as_view()), name="add_update"),
    url(r'^(?P<update_id>\d+)$', views.UpdateView.as_view(), name="show_update"),
    url(r'^(?P<update_id>\d+)/favorite$', views.add_favorite, name="add_favorite"),
    url(r'^(?P<update_id>\d+)/favorite/delete$', views.delete_favorite, name="delete_favorite"),
    url(r'^followed/', views.followed_updates, name="followed_updates"),
    url(r'^favorite/', views.most_favorited_updates, name="most_favorited_updates")
]
