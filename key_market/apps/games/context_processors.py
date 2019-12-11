import string

from django.core.cache import cache

from games.models import Game, Genre, Mode, StoreActivation
from games.utils import fetch_last_pay


def sitewide(request):
    return {
        'alphabet': string.ascii_lowercase,
        'genre_list': Genre.objects.all(),
        'mode_list': Mode.objects.all(),
        'store_list': [store[1] for store in StoreActivation.CHOICES],
        'soon': Game.objects.filter(is_soon=True)[:3],
        'soon_block': Game.objects.filter(is_soon=True)[:3]
    }


def last_pay(request):
    cache_key = 'last_pay'
    ids = cache.get(cache_key, None)
    if ids is None:
        ids = fetch_last_pay()[:9]
        cache.set(cache_key, ids, 60 * 10)

    games = {'%s' % game.digiseller_id: game
             for game in Game.objects.filter(digiseller_id__in=ids)}
    return {'last_pay': [games[id] for id in ids if id in games.keys()]}
