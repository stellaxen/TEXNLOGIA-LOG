from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stuff
from .serializers import StuffSerializer

class StuffList(APIView):
    def get(self, request):
        users = Stuff.objects.all()
        serializer = StuffSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StuffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
