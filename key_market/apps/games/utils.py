import requests

from django.conf import settings

from dicttoxml import dicttoxml

from xml.etree import cElementTree as ET

from games.models import Game


def fetch_prices():
    url = '%s%s' % (settings.DIGISELLER_API, 'seller-goods')
    data = {
        'id_seller': settings.DIGISELLER_ID,
        'currency': 'RUR',
        'rows': '2000',
    }

    r = requests.post(url, json=data)
    response = r.json()
    if response['retval'] == 0:
        for game in response['rows']:
            (Game.objects.filter(digiseller_id=game['id_goods'])
                         .update(my_coast=game['price_rur'],
                                 in_stock=game['in_stock']))


def fetch_business_rival_prices(games):
    """
    Возвращает цены конкурентов.
    """
    url = '%s%s' % (settings.DIGISELLER_API, 'seller-goods')

    games_dict = {}
    for game in games:
        games_dict.update({
            game.pk: {
                'sb_id': game.sb_id,
                'sp_id': game.sp_id,
                'sa_id': game.sa_id,
                'zz_id': game.zz_id,
            },
        })

    stories_id = {
        'sb_id': 182844,
        'sp_id': 165393,
        'sa_id': 162527,
        'zz_id': 237841,
    }

    stories_games = {}
    for story_name, story_id in stories_id.items():
        page = 1
        pages = 1
        stories_games.update({story_name: []})
        while page <= pages:
            data = {
                'id_seller': story_id,
                'currency': 'RUR',
                'rows': '2000',
                'page': page,
            }
            r = requests.post(url, json=data)
            response = r.json()
            pages = response['pages']
            page += 1
            stories_games[story_name] += response['rows']

    prices = {}
    for game_id, stories in games_dict.items():
        prices.update({
            game_id: {
                story: next(
                    (story_game['price_rur']
                     for story_game in stories_games[story]
                     if story_game['id_goods'] == story_game_id and
                     story_game['in_stock']),
                    None
                )
                for story, story_game_id in stories.items()
            }
        })
    return prices


def fetch_last_pay():
    """
    Возвращает список ID (digiseller) товаров в порядке убывания даты.
    """
    url = '%s%s' % (settings.DIGISELLER_OLD_API, 'shop_last_sales.asp')
    data = {
        'seller': {
            'id': settings.DIGISELLER_ID,
            'uid': settings.DIGISELLER_UID,
        },
    }
    xml_data = dicttoxml(data, custom_root='digiseller.request')
    headers = {'Content-Type': 'application/xml'}
    r = requests.post(url, data=xml_data, headers=headers)

    xml_doc = ET.fromstring(r.text)
    return [id.text for id in xml_doc.findall('sales/sale/product/id')]


def fetch_reviews():
    """
    Возвращает список всех отзывов магазина.
    """
    url = '%s%s' % (settings.DIGISELLER_OLD_API, 'shop_reviews.asp')
    data = {
        'seller': {
            'id': settings.DIGISELLER_ID,
        },
        'reviews': {
            'type': 'good',
        },
        'pages': {
            'rows': 9999,
        },
    }
    xml_data = dicttoxml(data, custom_root='digiseller.request')
    headers = {'Content-Type': 'application/xml'}
    r = requests.post(url, data=xml_data, headers=headers)

    xml_doc = ET.fromstring(r.text)
    xml_reviews = [review for review in xml_doc.findall('reviews/review')]
    return [{
        'date': r.find('date').text[:10],
        'info': r.find('info').text,
    } for r in xml_reviews]
