from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Performance
from .serializers import PerformanceSerializer


class PerformanceListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        performances = Performance.objects.all()
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PerformanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerformanceDetailAPIView(APIView):
    def get_object(self, performance_id):
        try:
            return Performance.objects.get(performance_id=performance_id)
        except Performance.DoesNotExist:
            return None

    def get(self, request, performance_id, *args, **kwargs):
        performance = self.get_object(performance_id)
        if not performance:
            return Response({"error": "Performance not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PerformanceSerializer(performance)
        return Response(serializer.data)

    def patch(self, request, performance_id, *args, **kwargs):
        performance = self.get_object(performance_id)
        if not performance:
            return Response({"error": "Performance not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PerformanceSerializer(performance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
