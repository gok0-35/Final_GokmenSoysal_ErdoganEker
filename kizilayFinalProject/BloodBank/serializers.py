from rest_framework import serializers
from .models import BloodBank

class BloodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBank
        fields = '__all__'  # Tüm alanları serileştirir
