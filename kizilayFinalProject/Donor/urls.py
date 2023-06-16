from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonorViewSet
from .views import DonorCreateView
from .views import DonorDetail

router = DefaultRouter()
router.register(r'', DonorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/', DonorDetail.as_view()),
]
