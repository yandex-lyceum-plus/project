from django.urls import path
from article import views

urlpatterns = (
    path('categories/', views.categories, name='categories'),
    path('popular/', views.popular, name='popular'),
    path('new/', views.new, name='new'),
    path('', views.redirect_to_homepage),
)
