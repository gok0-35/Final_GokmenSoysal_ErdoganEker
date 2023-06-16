import django_filters
from .models import Donor

class DonorFilter(django_filters.FilterSet):
    blood_type = django_filters.CharFilter(field_name='blood_type')

    class Meta:
        model = Donor
        fields = ['blood_type']