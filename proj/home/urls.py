from django.urls import path
from django.http import HttpResponse
from home.views import homepage

urlpatterns = [
    path('', view=homepage, name='homepage'),
]
