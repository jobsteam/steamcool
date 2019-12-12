from django.conf.urls import url

from games import views as views_games
from games.models import StoreActivation


stories = [store for index, store in StoreActivation.CHOICES]

urlpatterns = [
    url(r'^games/$',
        views_games.GamesList.as_view(), name='list'),
    url(r'^games/(?P<slug>[-\w]+)/$',
        views_games.GamesDetail.as_view(), name='detail'),
    url(r'^games/(?P<slug>[-\w]+)/order/$',
        views_games.GamesOrder.as_view(), name='order'),
    url(r'^genre/(?P<slug>[-\w]+)/$',
        views_games.GamesList.as_view(), name='genre_list'),
    url(r'^mode/(?P<slug>[-\w]+)/$',
        views_games.GamesList.as_view(), name='mode_list'),
    url(r'^store/(?P<store>%s)/$' % '|'.join(stories),
        views_games.GamesStoreList.as_view(), name='store_list'),
    url(r'^lucky/$',
        views_games.GamesLucky.as_view(), name='lucky'),
]
