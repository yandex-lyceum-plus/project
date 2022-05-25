from django.urls import path
from article import views

urlpatterns = (
    path('categories/', views.categories, name='categories'),
    path('popular/', views.popular, name='popular'),
    path('new/', views.new, name='new'),
    path('r/<int:pk>', views.read_article, name='article'),
    path('a/<int:pk>', views.read_article, name='read'),
    path('', views.redirect_to_homepage, name='home_redirect'),
    path('category/<int:pk>', views.category, name='category'),
    path('result/', views.search_articles, name='search_art'),
    path('a2/<int:pk>', views.read_second_article, name='second_article'),
)
