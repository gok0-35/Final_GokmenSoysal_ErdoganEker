from django.db import models
from django.core.mail import send_mail
from django.apps import apps

class BloodBank(models.Model):
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
    quantity = models.PositiveIntegerField(default=0)
    hospital_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # If it's a new object
        if not self.pk:
            super().save(*args, **kwargs)  # Call the "real" save() method.

            # Get the Donor model
            Donor = apps.get_model('Donor', 'Donor')
            
            # Get donors with the same blood type
            donors = Donor.objects.filter(blood_type=self.blood_type)
            
            # Send an email to each donor
            for donor in donors:
                send_mail(
                    'Blood is available',
                    f'Hello {donor.fullname}, blood of your type is available at {self.hospital_name}.',
                    'from@example.com',
                    [donor.email],
                    fail_silently=False,
                )
        else:
            super().save(*args, **kwargs)  # Call the "real" save() method.

    def request_blood(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            self.save()
            return True
        else:
            return False

class BloodRequest(models.Model):
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3, choices=BloodBank.BLOOD_TYPE_CHOICES)
    units = models.PositiveIntegerField()
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hospital_name

