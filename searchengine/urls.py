from django.urls import path
from searchengine import views

urlpatterns = [
    path('', views.search, name='search'),
]
