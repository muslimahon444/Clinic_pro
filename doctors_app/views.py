from rest_framework import viewsets
from .models import DoctorProfile, Specialization, Appointment
from .serializers import DoctorProfileSerializer, SpecializationSerializer, AppointmentSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'doctorprofile'):
            return self.queryset.filter(doctor__user=user)
        return self.queryset.none()  # Return an empty queryset if the user is not authenticated or not a doctor



