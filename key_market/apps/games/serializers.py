from functools import reduce
import operator

from django.db.models import Q

import django_filters

from rest_framework import serializers

from games.models import Game


class GameTitleFilter(django_filters.Filter):
    def filter(self, qs, value):
        bits = value.split(' ')
        title_clauses = reduce(operator.and_,
                               [Q(title__icontains=v) for v in bits])
        return qs.filter(title_clauses)[:10]


class SearchGameFilter(django_filters.FilterSet):
    title = GameTitleFilter()

    class Meta:
        fields = ['title']
        model = Game


class SearchGameSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        fields = ['title', 'url', 'image_url', 'my_coast']
        model = Game

    def get_image_url(self, obj):
        return obj.image.url
