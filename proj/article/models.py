from django.db import models
from sorl.thumbnail import get_thumbnail, ImageField
from django.utils.safestring import mark_safe
from article.validators import validate_count_words


class Article(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=150
    )
    text = models.TextField(
        verbose_name='Текст',
        validators=(validate_count_words,)
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True
    )
    categories = models.ManyToManyField(
        verbose_name='Категория',
        to='Category',
        related_name='articles'
    )
    upload = ImageField(
        upload_to='uploads/',
        null=True
    )

    def get_image_250x250(self):
        return get_thumbnail(self.upload, '250x250', crop='center', quality=51)

    def get_image_400x300(self):
        return get_thumbnail(self.upload, '400x300', crop='center', quality=51)

    def img_tmb(self):
        return mark_safe(f'<img src="{self.upload.url}" width="50">') if self.upload else 'Нет изображений'

    img_tmb.short_description = 'превью'
    img_tmb.allow_tags = True

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=150)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Gallery(models.Model):
    item_image = models.ImageField(upload_to="uploads/", null=True)
    item = models.ForeignKey(
        Article,
        on_delete=models.PROTECT,
        verbose_name="Статья",
        default=None
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def get_image_400x300(self):
        return get_thumbnail(self.item_image, '400x300', crop='center', quality=51)
