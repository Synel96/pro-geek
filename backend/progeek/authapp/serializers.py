from rest_framework import serializers
from core.models import User, RegistrationCode
import secrets

class RegistrationSerializer(serializers.ModelSerializer):
    registration_code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'registration_code']

    def validate_registration_code(self, value):
        try:
            code_obj = RegistrationCode.objects.get(code=value, is_used=False)
        except RegistrationCode.DoesNotExist:
            raise serializers.ValidationError('Invalid or already used registration code.')
        return code_obj

    def create(self, validated_data):
        # Generáljunk random aktivációs kódot
        activation_code = secrets.token_urlsafe(12)
        code_obj = RegistrationCode.objects.create(code=activation_code)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            registration_code=code_obj,
            is_active=False
        )
        user.registration_code = code_obj
        user.save()
        return user