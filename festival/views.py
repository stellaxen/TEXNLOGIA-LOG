# festival/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Festival  # Εισάγουμε το μοντέλο που θέλουμε να εκθέσουμε μέσω API
from .serializers import FestivalSerializer

class FestivalAPIView(APIView):
    # Μέθοδος GET για επιστροφή όλων των φεστιβάλ
    def get(self, request, *args, **kwargs):
        festivals = Festival.objects.all()
        serializer = FestivalSerializer(festivals, many=True)
        return Response(serializer.data)

    # Μέθοδος POST για δημιουργία νέου φεστιβάλ
    def post(self, request, *args, **kwargs):
        serializer = FestivalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
