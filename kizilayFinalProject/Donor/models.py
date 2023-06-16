from django.db import models
from django.apps import apps

class Donor(models.Model):
    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    blood_banks = models.ManyToManyField('BloodBank.BloodBank', related_name='donors')
    fullname = models.CharField(max_length=255)
    town = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=20)
    photo_url = models.URLField()  # Fotoğrafın CDN URL'sini depolar.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blood_banks = models.ManyToManyField('BloodBank.BloodBank', related_name='donors')

    def donate_to_bank(self, bank, quantity):
        # Check if this donor already donated to this bank
        if self.blood_banks.filter(id=bank.id).exists():
            # If yes, update the blood quantity in the bank
            bank.quantity += quantity
            bank.save()
        else:
            # If no, add this bank to the donor's blood banks and update the quantity
            self.blood_banks.add(bank)
            bank.quantity += quantity
            bank.save()   
