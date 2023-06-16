from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BloodBankViewSet
from .views import BloodBankCreateView
from .views import BloodBankRequestView
from .views import BloodBankDonorsList
from .views import AddBloodView
from .models import BloodBank

router = DefaultRouter()
router.register(r'', BloodBankViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('request/', BloodBankRequestView.as_view(), name='request_blood'),
    path('<int:pk>/donors/', BloodBankDonorsList.as_view()),
    path('add-blood/', AddBloodView.as_view(), name='add_blood'),
]
