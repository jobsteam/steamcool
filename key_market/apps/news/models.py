from django.db import models
from django.urls import reverse

from pytils.translit import slugify


class Item(models.Model):
    title = models.CharField(
        'Название новости',
        max_length=254)

    slug = models.SlugField(
        'slug',
        blank=True,
        max_length=254)

    image = models.ImageField(
        'Изображение для анонса',
        blank=True, null=True,
        upload_to='uploads/')

    short_text = models.TextField(
        'Анонс новости',
        blank=True)

    full_text = models.TextField(
        'Текст новости',
        blank=True)

    date_created = models.DateTimeField(
        'Дата новости',
        auto_now_add=True)

    class Meta:
        default_related_name = 'Без названия'
        ordering = ['title']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.autoslug()
        super().save(*args, **kwargs)

    def autoslug(self):
        self.slug = slugify(self.title)

    def get_absolute_url(self):
        return reverse('news:readevent', args=[self.slug])
