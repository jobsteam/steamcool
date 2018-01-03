from django.contrib import admin

from users import models as users_models


@admin.register(users_models.User)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('mail', 'date_created')
