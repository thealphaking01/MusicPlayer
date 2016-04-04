from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^playlist/$', views.playlist , name='playlist'),
    # url(r'^match/(?P<id>[0-9]+)$', views.create_team , name='create_team'),
    # url(r'^rules/$', views.rules , name='rules'),
    # url(r'^leaderboard/$', views.leaderboard , name='leaderboard'),
    # url(r'^listteams', views.listTeams , name='list_team'),
]