from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Festival
from .serializers import FestivalSerializer
from performance.models import Performance

class FestivalAPIView(APIView):
    def get(self, request, *args, **kwargs):
        festivals = Festival.objects.all()
        serializer = FestivalSerializer(festivals, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = FestivalSerializer(data=request.data)
        if serializer.is_valid():
            festival = serializer.save()
            # Ενημέρωση παραστάσεων αν το status είναι 'decision'
            if festival.festival_status == 'decision':
                Performance.objects.filter(festival=festival, performance_status='approved').update(performance_status='rejected')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        try:
            festival = Festival.objects.get(pk=kwargs['pk'])
        except Festival.DoesNotExist:
            return Response({'error': 'Festival not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FestivalSerializer(festival, data=request.data, partial=True)
        if serializer.is_valid():
            festival = serializer.save()
            # Ενημέρωση παραστάσεων αν το status είναι 'decision'
            if festival.festival_status == 'decision':
                Performance.objects.filter(festival=festival, performance_status='approved').update(performance_status='rejected')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
