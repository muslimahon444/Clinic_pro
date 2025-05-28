from rest_framework import serializers
from .models import DoctorProfile, Specialization, Appointment
from user_app.models import User


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'



class DoctorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = DoctorUserSerializer()
    specialization = SpecializationSerializer()

    class Meta:
        model = DoctorProfile
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        if not user.is_active:
            raise serializers.ValidationError("Вы должны подтвердить email, прежде чем записаться.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)