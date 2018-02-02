from django.conf.urls import url
from django.contrib import admin
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from easy_thumbnails.files import get_thumbnailer

from games import models as game_models
from games.utils import fetch_prices, fetch_business_rival_prices


class ScreenshotInlineAdmin (admin.StackedInline):
    extra = 0
    model = game_models.Screenshot
    readonly_fields = ['field_thumbnail']

    def field_thumbnail(self, instance):
        options = {'size': (200, 0), 'quality': 80}
        thumb = get_thumbnailer(instance.image).get_thumbnail(options)
        return mark_safe(
            '<img src="{url}" title="{title}" />'.format(url=thumb.url,
                                                         title=instance.title))
    field_thumbnail.short_description = 'Превью обложки'


@admin.register(game_models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'field_sp_price',
        'field_sb_price',
        'field_zz_price',
        'field_sa_price',
        'field_my_price',
    )

    inlines = [
        ScreenshotInlineAdmin,
    ]

    fieldsets = (
        ('Основное', {
            'fields': (
                'title',
                'slug',
                'genre',
                'description',
                'language',
                'date_release',
                'publisher',
                'is_free',
                'is_slide',
                'is_soon',
                'is_special_block_1',
                'is_special_block_2',
                'is_favorite',
            )
        }),
        ('Настройка активации', {
            'fields': (
                'store_activation',
                'method_activation',
                'region',
            )
        }),
        ('Мультимедия', {
            'fields': (
                'image',
                'field_thumbnail',
                'image_slide',
                'field_slide_thumbnail',
                'id_video',
            )
        }),
        ('СЕО', {
            'fields': (
                'seo_title',
                'seo_keywords',
                'seo_description',
            )
        }),
        ('Системные требования', {
            'fields': (
                'os',
                'processor',
                'ozu',
                'video_card',
                'hdd',
            )
        }),
        ('Настройка цены', {
            'fields': (
                'my_coast',
                'store_coast',
                'in_stock',
            )
        }),
        ('Digiseller', {
            'fields': (
                'digiseller_id',
            )
        }),
        ('Анализ цен конкурентов', {
            'fields': (
                'sp_id',
                'sb_id',
                'sa_id',
                'zz_id',
            )
        }),
    )

    readonly_fields = [
        'field_thumbnail',
        'field_slide_thumbnail',
        'slug',
        'in_stock',
    ]

    def business_rival_price(self, instance, business_rival):
        price = self.business_rival_prices[instance.pk][business_rival]
        if not price:
            price = '-'
        else:
            price = int(price)
        return mark_safe(price)

    def field_sb_price(self, instance):
        return self.business_rival_price(instance, 'sb_id')
    field_sb_price.short_description = 'Steambuy'

    def field_sp_price(self, instance):
        return self.business_rival_price(instance, 'sp_id')
    field_sp_price.short_description = 'Steampay'

    def field_sa_price(self, instance):
        return self.business_rival_price(instance, 'sa_id')
    field_sa_price.short_description = 'Steam-account'

    def field_zz_price(self, instance):
        return self.business_rival_price(instance, 'zz_id')
    field_zz_price.short_description = 'Zaka-zaka'

    def field_my_price(self, instance):
        price = instance.my_coast
        br_prices = [self.business_rival_prices[instance.pk][id]
                     for id in ['sb_id', 'sp_id', 'sa_id', 'zz_id']
                     if self.business_rival_prices[instance.pk][id]]

        if br_prices:
            if price > max(br_prices):
                wrapper = '<div style="color: red;">%s</div>'
                value = int(100 - max(br_prices) * 100 / price)
                price = wrapper % ('{} ({}%)'.format(price, value))

            elif price < min(br_prices):
                wrapper = '<div style="color: green;">%s</div>'
                value = int(100 - price / min(br_prices) * 100)
                if value >= 7:
                    price = wrapper % ('{} ({}%)'.format(price, value))
        return mark_safe(price)
    field_my_price.short_description = 'Моя цена'

    def field_thumbnail(self, instance):
        options = {'size': (200, 0), 'quality': 80}
        thumb = get_thumbnailer(instance.image).get_thumbnail(options)
        return mark_safe(
            '<img src="{url}" title="{title}" />'.format(url=thumb.url,
                                                         title=instance.title))
    field_thumbnail.short_description = 'Превью обложки'

    def field_slide_thumbnail(self, instance):
        options = {'size': (200, 0), 'quality': 80}
        thumb = get_thumbnailer(instance.image_slide).get_thumbnail(options)
        return mark_safe(
            '<img src="{url}" title="{title}" />'.format(url=thumb.url,
                                                         title=instance.title))
    field_slide_thumbnail.short_description = 'Превью слайда'

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = [
            url(r'^fetch_prices/$',
                self.admin_site.admin_view(self.fetch_prices),
                name='%s_%s_fetchprices' % info),
        ]
        urls.extend(super().get_urls())
        return urls

    def fetch_prices(self, request):
        info = self.model._meta.app_label, self.model._meta.model_name
        fetch_prices()
        return redirect('admin:%s_%s_changelist' % info)

    def get_changelist(self, request, **kwargs):
        games = self.get_queryset(request)
        cache_key = 'business_rival_prices_%s' % '_'.join(
            [str(game.pk) for game in games])
        self.business_rival_prices = cache.get(cache_key, None)
        if self.business_rival_prices is None:
            self.business_rival_prices = fetch_business_rival_prices(games)
            cache.set(cache_key, self.business_rival_prices, 60 * 60 * 12)
        return super().get_changelist(request, **kwargs)


@admin.register(game_models.Genre)
class GenreAdmin(admin.ModelAdmin):
    readonly_fields = [
        'slug',
    ]


@admin.register(game_models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass
