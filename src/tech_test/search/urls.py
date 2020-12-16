from django.urls import path
from .views import search, get_query

appname = 'search'
urlpatterns = [
    path('', search, name = 'search'),
    path('get_query/', get_query, name ='get_query'),
]