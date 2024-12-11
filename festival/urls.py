# festival/urls.py

from django.urls import path
from .views import FestivalAPIView

urlpatterns = [
    path('', FestivalAPIView.as_view(), name='festival-list-create'),
]
