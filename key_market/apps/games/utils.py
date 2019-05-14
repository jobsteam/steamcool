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
    req = requests.post(url, data=xml_data, headers=headers)

    # На случай, если digiseller ничего не вернул.
    if req.status_code != 200:
        return []

    xml_doc = ET.fromstring(req.text)
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
