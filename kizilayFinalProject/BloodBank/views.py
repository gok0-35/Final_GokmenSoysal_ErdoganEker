from django.shortcuts import render
from rest_framework import viewsets
from .models import BloodBank
from .serializers import BloodBankSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Donor.serializers import DonorSerializer
from django.views import View
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from .models import BloodBank


class BloodBankViewSet(viewsets.ModelViewSet):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    

class BloodBankCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = BloodBankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BloodBankRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        hospital_id = request.data.get('hospital_id')
        quantity = request.data.get('quantity')

        if hospital_id and quantity:
            blood_bank = BloodBank.objects.filter(id=hospital_id).first()
            if blood_bank:
                if blood_bank.request_blood(quantity):
                    blood_bank.save()
                    return Response({"message": "Blood request is successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Not enough blood in the bank"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Blood bank not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)



class BloodBankList(generics.ListCreateAPIView):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    permission_classes = [AllowAny]

class BloodBankDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    permission_classes = [AllowAny]    

class BloodBankDonorsList(generics.ListAPIView):
    serializer_class = DonorSerializer

    def get_queryset(self):
        """
        This view should return a list of all the donors
        for the blood bank as determined by the blood bank ID.
        """
        blood_bank_id = self.kwargs['pk']
        return BloodBank.objects.get(id=blood_bank_id).donors.all()    
    
class AddBloodView(View):
    def post(self, request, *args, **kwargs):
        blood_type = request.POST.get('blood_type')
        quantity = request.POST.get('quantity')

        blood_bank, created = BloodBank.objects.get_or_create(
            blood_type=blood_type,
            defaults={'quantity': quantity},
        )

        if not created:
            blood_bank.quantity += int(quantity)
            blood_bank.save()

        return JsonResponse({'message': 'Blood added successfully'}, status=200)    