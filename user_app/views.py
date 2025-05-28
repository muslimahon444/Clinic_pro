from rest_framework import viewsets, generics
from .models import User, Appointment, SMSVerification
from .serializers import UserSerializer, AppointmentSerializer, SMSVerificationSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class SMSVerificationView(generics.CreateAPIView):
    queryset = SMSVerification.objects.all()
    serializer_class = SMSVerificationSerializer



