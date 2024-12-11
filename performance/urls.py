# your_app/urls.py

from django.urls import path
from .views import PerformanceAPIView

urlpatterns = [
    path('', PerformanceAPIView.as_view(), name='performance-list-create'),
]
