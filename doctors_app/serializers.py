from rest_framework import serializers
from .models import DoctorProfile, Specialization, Appointment
from user_app.models import User


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']


class DoctorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = DoctorUserSerializer()
    specialization = SpecializationSerializer()

    class Meta:
        model = DoctorProfile
        fields = ['user', 'specialization', 'phone', 'education', 'experience_years', 'bio']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = DoctorUserSerializer(read_only=True)
    doctor = DoctorUserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'reason']