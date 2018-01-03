from django import forms
from django.contrib import admin

from news import models as news_models


class ItemAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recom'].queryset = news_models.Item.objects.exclude(
            pk__exact=self.instance.pk)


@admin.register(news_models.Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
