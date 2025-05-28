from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorProfileViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorProfileViewSet, basename='doctor')



urlpatterns = [
    path('doctors_app/', include(router.urls)),
]
