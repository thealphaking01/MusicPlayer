from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all_songs/$', views.all_songs , name='all_songs'),
    url(r'^shared_playlists/$', views.shared_playlists , name='shared_playlists'),
    url(r'^create_playlist/$', views.create_playlist , name='create_playlist'),
    url(r'^my_playlists/$', views.my_playlists , name='my_playlists'),
    url(r'^playlist/(?P<id>[0-9]+)$', views.view_playlist , name='view_playlist'),
    # url(r'^edit_playlist/(?P<id>[0-9]+)$', views.edit_playlist , name='view_playlist'),
    url(r'^delete_playlist/(?P<id>[0-9]+)$', views.delete_playlist , name='view_playlist'),
    url(r'^upvote/$', views.upvote , name='upvote'),
    url(r'^logout/$', views.member_logout , name='logout'),
]