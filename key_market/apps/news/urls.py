from django.conf.urls import url
from news.views import NewsList, NewsDetail


urlpatterns = [
    url(r'^$', NewsList.as_view(), name='news'),
    url(r'^(?P<slug>[-\w]+)/$', NewsDetail.as_view(), name='readevent'),
]
