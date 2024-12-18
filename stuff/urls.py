from django.urls import path
from .views import StuffList

urlpatterns = [
    path('', StuffList.as_view(), name='stuff-list'),
]
