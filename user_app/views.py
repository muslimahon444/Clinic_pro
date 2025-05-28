from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Appointment, SMSVerification
from .serializers import (
    UserSerializer,
    AppointmentSerializer,
    SMSVerificationSerializer,
    EmailVerificationRequestSerializer,
    EmailVerificationConfirmSerializer,
)

class RequestVerificationCodeView(APIView):
    def post(self, request):
        serializer = EmailVerificationRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Код отправлен на email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmVerificationCodeView(APIView):
    def post(self, request):
        serializer = EmailVerificationConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'detail': 'Email подтвержден'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class SMSVerificationView(generics.CreateAPIView):
    queryset = SMSVerification.objects.all()
    serializer_class = SMSVerificationSerializer




