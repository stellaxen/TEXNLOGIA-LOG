from django.urls import path
from .views import PerformanceListAPIView, PerformanceDetailAPIView

urlpatterns = [
    path('', PerformanceListAPIView.as_view(), name='performance-list'),
    path('<int:performance_id>/', PerformanceDetailAPIView.as_view(), name='performance-detail'),
]