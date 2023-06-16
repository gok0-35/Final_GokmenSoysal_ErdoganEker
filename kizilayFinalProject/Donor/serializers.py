from rest_framework import serializers
from BloodBank.models import BloodBank
from .models import Donor

class BloodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBank
        fields = ['id', 'name', 'location']


class DonorSerializer(serializers.ModelSerializer):
    blood_banks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Donor
        fields = '__all__'  

    def update(self, instance, validated_data):
        from BloodBank.serializers import BloodBankSerializer  # Avoid circular import issue
        blood_banks = self.context['request'].data.getlist('blood_banks')
        instance.blood_banks.set(blood_banks)
        instance.save()
        return instance     

