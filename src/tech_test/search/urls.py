from django.urls import path
from .views import home, search_bar


urlpatterns = [
    path('', home),
    path('search_bar/', search_bar),
]