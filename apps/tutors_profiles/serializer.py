import os
from decimal import Decimal

from rest_framework import serializers
from .models import TutorsProfile, TutorsTimeTable

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_CERT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

class TutorsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorsProfile
        fields = "__all__"
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "ielts_score": {"required": True},
            "experience": {"required": True},
        }

    def validate_first_name(self, value):
        value = value.strip()
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value

    def validate_last_name(self, value):
        value = value.strip()
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")
        return value

    def validate_experience(self, value):
        if value < 0 or value > 60:
            raise serializers.ValidationError("Experience must be between 0 and 60 years.")
        return value

    def validate_profile_image(self, file):
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise serializers.ValidationError("Profile image must be a JPG or PNG file.")

        if file.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Profile image must not exceed 2MB.")

        return file

    def validate_certificate_image(self, file):
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in ALLOWED_CERT_EXTENSIONS:
            raise serializers.ValidationError("Certificate file must be JPG, PNG, or PDF.")

        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Certificate file must not exceed 5MB.")

        return file


    def validate_ielts_score(self, value):
        v = Decimal(str(value))

        if v < Decimal("0") or v > Decimal("9"):
            raise serializers.ValidationError("IELTS score must be between 0 and 9.")

        if (v * 2) % 1 != 0:
            raise serializers.ValidationError("IELTS score must be in 0.5 increments (e.g., 6.5, 7.0).")

        return value

class TutorsTimeTableSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(
    #     queryset=TutorsProfile.objects.filter(is_tutor = True)
    # )
#     Temporary query bro
    class Meta:
        model = TutorsTimeTable
        fields = "__all__"
