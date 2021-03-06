from django.contrib import admin
from article.models import Article, Category, Gallery, MainArticle, Rating
from django.utils.safestring import mark_safe


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'img_tmb', )
    list_display_links = ('name', )
    list_editable = ('is_published', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name', )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('item', 'item_image', )
    list_display_links = ('item', )


@admin.register(MainArticle)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'img_tmb', )
    list_display_links = ('title', )


@admin.register(Rating)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('star', 'main_article', )
    list_display_links = ('star', )
