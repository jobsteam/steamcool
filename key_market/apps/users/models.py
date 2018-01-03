from django.db import models


class User(models.Model):
    mail = models.EmailField(
        'E-mail пользователя',
        max_length=254)

    date_created = models.DateTimeField(
        'Дата создания записи',
        auto_now_add=True)

    class Meta:
        default_related_name = 'Без названия'
        ordering = ['date_created']
        verbose_name = 'Электронный адрес'
        verbose_name_plural = 'Электронные адреса'

    def __str__(self):
        return self.mail
