import django
import django.conf.urls.static


urlpatterns = [
    django.urls.path('admin/', django.contrib.admin.site.urls),
    django.urls.path('auth/', django.urls.include('users.urls')),
    django.urls.path('edit/', django.urls.include('edit.urls')),
    django.urls.path('read/', django.urls.include('article.urls')),
    django.urls.path('', django.urls.include('home.urls')),
]

if django.conf.settings.DEBUG:
    urlpatterns += django.conf.urls.static.static(django.conf.settings.STATIC_URL, document_root=django.conf.settings.STATIC_ROOT)
