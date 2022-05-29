from django.db import models
from sorl.thumbnail import get_thumbnail, ImageField
from django.utils.safestring import mark_safe
from article.validators import validate_count_words
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model
import django


User = get_user_model()


class MainArticle(models.Model):
    title = models.CharField(default=None, verbose_name='Заголовок', max_length=150)
    text = models.TextField(default=None, verbose_name='Текст', validators=(validate_count_words,))
    articles = models.ManyToManyField(default=None, verbose_name='Статьи', to='Article', related_name='main_articles')
    upload = ImageField(default=None, upload_to='uploads/', null=True)
    category = models.ForeignKey(verbose_name='Категория', to='Category', related_name='articles',
                                 on_delete=models.RESTRICT)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    def get_image_250x250(self):
        return get_thumbnail(self.upload, '250x250', crop='center', quality=51)

    def get_image_400x300(self):
        return get_thumbnail(self.upload, '400x300', crop='center', quality=51)

    def img_tmb(self):
        return mark_safe(f'<img src="{self.upload.url}" width="50">') if self.upload else 'Нет изображений'

    img_tmb.short_description = 'превью'
    img_tmb.allow_tags = True

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'вики'
        verbose_name_plural = 'вики'


class Article(models.Model):
    name = models.CharField(default=None, verbose_name='Название', max_length=150)
    author = models.ForeignKey(default=None, verbose_name='Автор', to=User, related_name='author',
                               on_delete=models.RESTRICT)
    text = models.TextField(default=None, verbose_name='Текст', validators=(validate_count_words,))
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    upload = ImageField(default=None, upload_to='uploads/', null=True)
    published_date = models.DateTimeField(verbose_name="Дата публикации", default=django.utils.timezone.now)

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
    upload = ImageField(default=None, upload_to='uploads/', null=True)

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
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Gallery(models.Model):
    item_image = models.ImageField(upload_to="uploads/", null=True)
    item = models.ForeignKey(Article, on_delete=models.PROTECT, verbose_name="Статья", default=None)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def get_image_400x300(self):
        return get_thumbnail(self.item_image, '400x300', crop='center', quality=51)



class Rating(models.Model):
    CHOICES = [(str(i), i) for i in range(11)]
    star = models.CharField(verbose_name='Оценка', max_length=2, choices=CHOICES, default='0')
    main_article = models.ForeignKey(verbose_name='Статья', to=MainArticle, on_delete=models.CASCADE,
                                     related_name='ratings')
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE, related_name='ratings')
    review = models.TextField(verbose_name='Отзыв', max_length=250, default=None, null=True)
    published_date = models.DateTimeField(verbose_name="Дата отзыва", default=django.utils.timezone.now)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = (UniqueConstraint(name='rating_unique', fields=('main_article', 'user')), )
    
        def __str__(self):
            return f'{self.star} to {self.article} by {self.user}'
