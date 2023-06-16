from django.shortcuts import render
from rest_framework import viewsets
from .models import Donor
from .serializers import DonorSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .filters import DonorFilter

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

class DonorCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DonorList(generics.ListCreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = DonorFilter
    search_fields = ['name', 'city']

class DonorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated]    