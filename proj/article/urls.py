from django.urls import path
from article import views

urlpatterns = (
    path('categories/', views.categories, name='categories'),
    path('popular/', views.popular, name='popular'),
    path('new/', views.new, name='new'),
    path('r/<int:pk>', views.read_article, name='article'),
    path('a/<int:pk>', views.read, name='read'),
    path('', views.redirect_to_homepage, name='home_redirect'),
)
