from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.UpdateListView.as_view(), name="index"),
    url(r'^new/', views.AddUpdateView.as_view(),
        name="add_update"),
    url(r'^(?P<update_id>\d+)$', views.UpdateView.as_view(),
        name="show_update"),
    url(r'^(?P<update_id>\d+)/favorite$', views.add_favorite,
        name="add_favorite"),
    url(r'^(?P<update_id>\d+)/favorite/delete$', views.delete_favorite,
        name="delete_favorite"),
    url(r'^followed/', views.FollowedUpdatesView.as_view(),
        name="followed_updates"),
    url(r'^popular/', views.PopularUpdatesView.as_view(),
        name="popular_updates")
]
