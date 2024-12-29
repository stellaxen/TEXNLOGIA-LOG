from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import Performance
from .serializers import PerformanceSerializer
from django.core.exceptions import ValidationError

class PerformanceListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        performances = Performance.objects.all()
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PerformanceSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

        # Check if the festival status is 'ANNOUNCED'
        if performance.festival.festival_status == 'announced':
            return Response({"error": "Cannot update a performance belonging to a festival with status 'ANNOUNCED'."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # Check user permissions
        if performance.created_by != user and user not in performance.administrators.all():
            raise PermissionDenied("You do not have permission to update this performance.")

        serializer = PerformanceSerializer(performance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, performance_id, *args, **kwargs):
        performance = self.get_object(performance_id)
        if not performance:
            return Response({"error": "Performance not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the festival status is 'ANNOUNCED'
        if performance.festival and performance.festival.festival_status == 'announced':
            return Response({"error": "Cannot delete a performance belonging to a festival with status 'ANNOUNCED'."},
                            status=status.HTTP_403_FORBIDDEN)

        user = request.user

        # Check user permissions
        if performance.created_by != user and user not in performance.administrators.all():
            raise PermissionDenied("You do not have permission to delete this performance.")

        performance.delete()
        return Response({"message": "Performance deleted successfully."}, status=status.HTTP_200_OK)
