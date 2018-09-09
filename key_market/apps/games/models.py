from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from pytils.translit import slugify


class GameLanguage(object):
        RU = 1
        ENG = 2
        CHOICES = (
            (RU, 'русский'),
            (ENG, 'английский'),
        )


class StoreActivation(object):
        STEAM = 1
        ORIGIN = 2
        UPLAY = 3
        ROCKSTAR = 4
        CHOICES = (
            (STEAM, 'steam'),
            (ORIGIN, 'origin'),
            (UPLAY, 'uplay'),
            (ROCKSTAR, 'rockstar'),
        )


class MethodActivation(object):
        STEAM_GIFT = 1
        STEAM_KEY = 2
        ORIGIN_KEY = 3
        UPLAY_KEY = 4
        ROCKSTAR_KEY = 5
        CHOICES = (
            (STEAM_GIFT, 'steam gift'),
            (STEAM_KEY, 'steam ключ'),
            (ORIGIN_KEY, 'origin ключ'),
            (UPLAY_KEY, 'uplay ключ'),
            (ROCKSTAR_KEY, 'rockstar ключ'),
        )


class RegionActivation(object):
        SNG_REGION = 1
        RU_REGION = 2
        RU_POL_REGION = 3
        CHOICES = (
            (SNG_REGION, 'Страны СНГ'),
            (RU_REGION, 'Россия'),
            (RU_POL_REGION, 'Россия/Польша'),
        )


class Game(models.Model):
    title = models.CharField(
        'Название игры',
        max_length=254)

    slug = models.SlugField(
        'slug',
        blank=True)

    description = models.TextField(
        'Описание игры',
        blank=True)

    date_created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True)

    date_release = models.DateField(
        'Дата выхода',
        blank=True, null=True)

    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанр',
        related_name='genres',
        blank=True)

    publisher = models.ForeignKey(
        'Publisher',
        verbose_name='Издатель',
        related_name='publishers',
        blank=True, null=True, on_delete=models.SET_NULL)

    language = models.IntegerField(
        'Язык',
        choices=GameLanguage.CHOICES,
        db_index=True, blank=True, null=True)

    store_activation = models.IntegerField(
        'активация',
        choices=StoreActivation.CHOICES,
        db_index=True, blank=True, null=True)

    method_activation = models.IntegerField(
        'способ активации',
        choices=MethodActivation.CHOICES,
        db_index=True, blank=True, null=True)

    region = models.IntegerField(
        'Региональные ограничения',
        choices=RegionActivation.CHOICES,
        db_index=True, blank=True, null=True)

    image = models.ImageField(
        'Обложка',
        blank=True, null=True,
        upload_to='gamescover/')

    image_slide = models.ImageField(
        'Изображение для слайда',
        blank=True, null=True,
        upload_to='gamescover/')

    image_banner = models.ImageField(
        'Баннер для спец. блока',
        blank=True, null=True,
        upload_to='gamescover/')

    my_coast = models.IntegerField(
        'Стоимость в рублях',
        blank=True, null=True)

    id_video = models.CharField(
        'ID youtube ролика',
        max_length=254,
        blank=True, null=True)

    in_stock = models.BooleanField(
        'Товар в наличии',
        default=False)

    store_coast = models.IntegerField(
        'Официальная стоимость',
        blank=True, null=True)

    digiseller_id = models.IntegerField(
        'Digiseller ID',
        blank=True, null=True)

    os = models.CharField(
        'ОС',
        max_length=254,
        blank=True, null=True)

    processor = models.CharField(
        'Процессор',
        max_length=1000,
        blank=True, null=True)

    ozu = models.CharField(
        'Оперативная память',
        max_length=254,
        blank=True, null=True)

    video_card = models.CharField(
        'Видеокарта',
        max_length=1000,
        blank=True, null=True)

    hdd = models.CharField(
        'Жесткий диск',
        max_length=254,
        blank=True, null=True)

    seo_title = models.CharField(
        'Заголовок страницы',
        max_length=1000,
        blank=True, null=True)

    seo_keywords = models.CharField(
        'Ключевые слова',
        max_length=1000,
        blank=True, null=True)

    seo_description = models.CharField(
        'Описание',
        max_length=1000,
        blank=True, null=True)

    is_free = models.BooleanField(
        'Игра даром',
        default=False)

    is_slide = models.BooleanField(
        'Показать в слайде',
        default=False)

    is_soon = models.BooleanField(
        'Скоро в продаже',
        default=False)

    is_case = models.BooleanField(
        'Наличие в Case',
        default=False)

    is_special_block_1 = models.BooleanField(
        'В специальный блок №1',
        default=False)

    is_special_block_2 = models.BooleanField(
        'В специальный блок №2',
        default=False)

    is_favorite = models.BooleanField(
        'В популярное',
        default=False)

    sb_id = models.IntegerField(
        'Steambuy id_d',
        blank=True, null=True)

    sp_id = models.IntegerField(
        'Steampay id_d',
        blank=True, null=True)

    sa_id = models.IntegerField(
        'Steam-Account id_d',
        blank=True, null=True)

    zz_id = models.IntegerField(
        'Zaka-Zaka id_d',
        blank=True, null=True)

    class Meta:
        default_related_name = 'Без названия'
        ordering = ['title']
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.autoslug()
        super().save(*args, **kwargs)

    def autoslug(self):
        if not self.slug:
            self.slug = slugify(self.title)

    @property
    def percent(self):
        return 100 - int(self.my_coast / self.store_coast * 100)

    @property
    def gamevideo(self):
        if self.id_video:
            return mark_safe(
                '<div class="description"><h2>Трейлер игры</h2><div class="video-content"><div class="video-container"><iframe width="560" height="315" src="https://www.youtube.com/embed/{video}?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div></div></div>'.format(video=self.id_video))
        return ''

    def get_absolute_url(self):
        return reverse('games:detail', args=[self.slug])


class Screenshot(models.Model):
    title = models.CharField(
        'Название игры',
        max_length=254)

    image = models.ImageField(
        'Скриншот',
        blank=True, null=True,
        upload_to='gallery/')

    game = models.ForeignKey(
        'Game',
        verbose_name='Скриншоты',
        related_name='screenshots',
        blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        default_related_name = 'Без названия'
        ordering = ['title']
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(
        'Название жанра',
        max_length=254)

    slug = models.SlugField(
        'slug',
        blank=True)

    class Meta:
        default_related_name = 'Без названия'
        ordering = ['title']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.autoslug()
        super().save(*args, **kwargs)

    def autoslug(self):
        self.slug = slugify(self.title)


class Publisher(models.Model):
    title = models.CharField(
        'Название издателя',
        max_length=254)

    class Meta:
        default_related_name = 'Без названия'
        ordering = ['title']
        verbose_name = 'Издатель'
        verbose_name_plural = 'Издатели'

    def __str__(self):
        return self.title
