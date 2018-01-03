from django.views.generic import ListView, DetailView
from news.models import Item


class NewsList(ListView):
    model = Item
    template_name = "news_list.html"


class NewsDetail(DetailView):
    model = Item
    template_name = "news_detail.html"
