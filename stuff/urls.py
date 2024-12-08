from django.urls import path
from .views import StuffList

urlpatterns = [
    path('stuff/', StuffList.as_view(), name='stuff-list'),
]
