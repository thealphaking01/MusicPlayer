from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^playlist/$', views.playlist , name='playlist'),
    url(r'^upvote/$', views.upvote , name='upvote'),
    url(r'^logout/$', views.member_logout , name='logout'),
]