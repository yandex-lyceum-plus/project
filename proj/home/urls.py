import django.urls
import home.views

urlpatterns = [
    django.urls.path('', view=home.views.homepage, name='homepage'),
]
