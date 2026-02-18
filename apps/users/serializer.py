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







