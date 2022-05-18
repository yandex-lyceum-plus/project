from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('edit/', include('edit.urls')),
    path('read/', include('article.urls')),
    path('', include('home.urls')),
]
