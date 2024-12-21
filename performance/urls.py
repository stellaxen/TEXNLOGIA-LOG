from django.urls import path
from .views import PerformanceListAPIView, PerformanceDetailAPIView

urlpatterns = [
    path('performances/', PerformanceListAPIView.as_view(), name='performance-list'),
    path('performances/<int:performance_id>/', PerformanceDetailAPIView.as_view(), name='performance-detail'),
]