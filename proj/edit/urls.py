from django.urls import path
from article.views import redirect_to_homepage
from edit.views import edit_article

urlpatterns = [
    path('', redirect_to_homepage),
    path('<int:pk>/', edit_article, name='edit_article')
]
