# serializers.py
from rest_framework import serializers
from .models import Stuff

class StuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stuff
        fields = '__all__'  # Επέλεξε ποια πεδία θέλεις να εμφανίζονται, μπορείς να το προσαρμόσεις όπως χρειάζεσαι
