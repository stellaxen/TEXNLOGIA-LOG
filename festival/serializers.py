# festival/serializers.py

from rest_framework import serializers
from .models import Festival  # Το μοντέλο που θέλεις να χρησιμοποιήσεις

class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival  # Αντικατέστησε το με το μοντέλο που έχεις στο app Festival
        fields = '__all__'  # Ή μπορείς να καθορίσεις συγκεκριμένα πεδία π.χ. ['name', 'location']
