from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from adminsortable2.admin import SortableAdminMixin

from easy_thumbnails.files import get_thumbnailer

from games import models as game_models
from games.utils import fetch_prices


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


class PartnerInlineAdmin (admin.StackedInline):
    extra = 0
    model = game_models.Partner


@admin.register(game_models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'field_my_price'
    )

    inlines = [
        PartnerInlineAdmin,
        ScreenshotInlineAdmin,
    ]

    fieldsets = (
        ('Основное', {
            'fields': (
                'title',
                'slug',
                'genre',
                'mode',
                'description',
                'language',
                'date_release',
                'publisher'
            )
        }),
        ('Обложка игры', {
            'classes': ('wide',),
            'fields': (
                'image',
                'field_thumbnail',
            )
        }),
        ('Настройки активации', {
            'classes': ('wide',),
            'fields': (
                'store_activation',
                'method_activation',
                'region',
            )
        }),
        ('Системные требования', {
            'classes': ('wide',),
            'fields': (
                'os',
                'processor',
                'ozu',
                'video_card',
                'hdd',
            )
        }),
        ('СЕО', {
            'classes': ('wide',),
            'fields': (
                'seo_title',
                'seo_keywords',
                'seo_description',
            )
        }),
        ('Настрока отображения', {
            'classes': ('wide',),
            'fields': (
                'is_soon',
                'on_main_page'
            )
        }),
        ('Настройка слайда', {
            'classes': ('wide',),
            'fields': (
                'is_slide',
                'image_slide',
                'field_slide_thumbnail',
                'slide_text'
            )
        }),
        ('Трейлер игры', {
            'classes': ('wide',),
            'fields': (
                'id_video',
            )
        }),
        ('Цена / Digiseller', {
            'classes': ('wide',),
            'fields': (
                'digiseller_id',
                'my_coast',
                'store_coast',
                'in_stock',
            )
        }),
    )

    readonly_fields = [
        'field_thumbnail',
        'field_slide_thumbnail',
        'in_stock',
    ]

    prepopulated_fields = {
        'slug': (
            'title',
        )
    }

    def field_my_price(self, instance):
        price = instance.my_coast
        return mark_safe('{my_coast} руб.'.format(my_coast=price))
    field_my_price.short_description = 'Цена'

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


@admin.register(game_models.Genre)
class GenreAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = [
        'slug',
    ]


@admin.register(game_models.Mode)
class ModeAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = [
        'slug',
    ]


@admin.register(game_models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass
