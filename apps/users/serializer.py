from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
User = get_user_model()

class SignupSerializer(serializers.Serializer):
    phone = serializers.CharField(allow_null=False, allow_blank=False, max_length=13)
    password = serializers.CharField(allow_null=False, allow_blank=False)
    password2 = serializers.CharField(allow_null=False, allow_blank=False)

    def validate_phone(self, value):
        if len(value)!=9:
            raise serializers.ValidationError("Enter the phone number correctly")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("User with this phone number already exists")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("The passwords does nor match")

        validate_password(data["password"])
        return data

    def create(self, validated_data):
        phone = validated_data["phone"]
        password = validated_data["password"]
        user = User.objects.create_user(phone=phone, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, allow_blank=False, allow_null=False)
    password = serializers.CharField(allow_blank=False, allow_null=False)

    def validate(self, attrs):
        phone = attrs["phone"]
        password = attrs["password"]

        user = authenticate(phone=phone, password=password)

        if not user:
            raise serializers.ValidationError("Phone number or password are invalid")

        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        attrs["user"] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, help_text='JWT refresh token для инвалидации')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, help_text='JWT refresh token')


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=20, help_text='+998901234567')


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=20)
    code = serializers.CharField(required=True, help_text='SMS-код (в dev: пароль)')


# --- OTP Flow (2025–2026 mobile app standard) ---

import re


def validate_e164(value):
    """E.164: + и цифры, для Узбекистана +998XXXXXXXXX."""
    if not value or not value.startswith('+'):
        raise serializers.ValidationError('Номер должен быть в формате E.164, например +998901234567')
    digits = re.sub(r'\D', '', value)
    if len(digits) < 10 or len(digits) > 15:
        raise serializers.ValidationError('Неверная длина номера')
    return value


class SendOTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        max_length=20,
        validators=[validate_e164],
        help_text='Номер в формате E.164, например +998901234567',
    )


class VerifyOTPRequestSerializer(serializers.Serializer):
    verifyID = serializers.CharField(required=True, help_text='ID из ответа send-otp')
    otp_code = serializers.CharField(required=True, min_length=4, max_length=10, help_text='Код подтверждения')







