from news.models import Item


def last_news(request):
    return {
        'last_news': Item.objects.all(),
    }
