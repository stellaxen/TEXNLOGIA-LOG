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
            if serializer.is_valid(raise_exception=True):  # Χρησιμοποιεί raise_exception για να πετάξει το σφάλμα αν είναι άκυρο
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:  # Πιάνουμε την εξαίρεση ValidationError που προκύπτει από το clean()
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

        # Έλεγχος αν το festival του performance έχει status 'ANNOUNCED'
        if performance.festival.festival_status == 'ANNOUNCED':
            return Response({"error": "Δεν επιτρέπεται η ενημέρωση της παράστασης για festival με κατάσταση 'ANNOUNCED'."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user  # Ο αυθεντικοποιημένος χρήστης

        # Έλεγχος δικαιωμάτων χρήστη για ενημέρωση
        if performance.created_by != user and user not in performance.administrators.all():
            raise PermissionDenied("Δεν έχετε δικαίωμα να επεξεργαστείτε αυτή την παράσταση.")

        # Αν περάσει τον έλεγχο, προχωράμε στην ενημέρωση
        serializer = PerformanceSerializer(performance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, performance_id, *args, **kwargs):
        performance = self.get_object(performance_id)
        if not performance:
            return Response({"error": "Performance not found"}, status=status.HTTP_404_NOT_FOUND)

        # Έλεγχος αν το festival του performance έχει status 'ANNOUNCED'
        if performance.festival.festival_status == 'ANNOUNCED':
            return Response({"error": "Δεν επιτρέπεται η διαγραφή της παράστασης για festival με κατάσταση 'ANNOUNCED'."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user  # Ο αυθεντικοποιημένος χρήστης

        # Έλεγχος δικαιωμάτων χρήστη για διαγραφή
        if performance.created_by != user and user not in performance.administrators.all():
            raise PermissionDenied("Δεν έχετε δικαίωμα να διαγράψετε αυτή την παράσταση.")

        # Αν περάσει τον έλεγχο, προχωράμε στη διαγραφή
        performance.delete()

        # Επιστρέφουμε μήνυμα επιτυχίας διαγραφής
        return Response({"message": "Η παράσταση διαγράφηκε με επιτυχία."}, status=status.HTTP_200_OK)
