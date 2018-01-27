from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from easy_thumbnails.files import get_thumbnailer

from news import models as news_models


class ItemAdminForm(forms.ModelForm):
    pass


@admin.register(news_models.Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm

    list_display = (
        'title',
        'date_created',
    )

    readonly_fields = [
        'slug',
        'field_thumbnail',
    ]

    fieldsets = (
            ('Основное', {
                'fields': (
                    'title',
                    'slug',
                    'image',
                    'field_thumbnail',
                    'short_text',
                    'full_text',
                )
            }),
        )

    def field_thumbnail(self, instance):
        options = {'size': (200, 0), 'quality': 80}
        thumb = get_thumbnailer(instance.image).get_thumbnail(options)
        return mark_safe(
            '<img src="{url}" title="{title}" />'.format(url=thumb.url,
                                                         title=instance.title))
    field_thumbnail.short_description = 'Превью обложки'
