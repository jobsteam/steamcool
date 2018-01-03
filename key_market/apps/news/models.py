from django.db import models


class Item(models.Model):
    title = models.CharField(
        'Название новости',
        max_length=254)

    image = models.ImageField(
        'Изображение для анонса',
        blank=True, null=True,
        upload_to='uploads/')

    recom = models.ManyToManyField(
        'self',
        verbose_name='Похожая новость',
        blank=True)

    class Meta:
        default_related_name = 'Без названия'
        ordering = ['title']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
