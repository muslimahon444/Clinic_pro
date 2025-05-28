from rest_framework import serializers
from django.core.mail import send_mail
from .models import User, Appointment, SMSVerification
import random

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_staff', 'role']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class SMSVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSVerification
        fields = ['email', 'code']

class EmailVerificationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data['name']
        code = f"{random.randint(1000, 9999)}"

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.is_active = False
            user.save()

        SMSVerification.objects.create(email=email, code=code)

        send_mail(
            subject='Код подтверждения',
            message=f'Здравствуйте, {name}. Ваш код подтверждения: {code}',
            from_email='noreply@yourclinic.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return validated_data

class EmailVerificationConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, data):
        email = data['email']
        code = data['code']

        try:
            verification = SMSVerification.objects.filter(
                email=email, code=code, is_used=False
            ).latest('created_at')
        except SMSVerification.DoesNotExist:
            raise serializers.ValidationError('Неверный код')

        if not verification.is_code_valid():
            raise serializers.ValidationError('Код устарел')

        verification.is_used = True
        verification.save()

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        return data

