import os

from rest_framework import serializers
from .models import StudentProfile

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_CERT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["first_name","last_name","englishLevel","profile_image"]

        extra_kwargs = {
            "first_name":{"required":True, "allow_blank":False},
            "last_name":{"required":True,"allow_blank":False}
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

    def validate_profile_image(self, file):
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise serializers.ValidationError("Profile image must be a JPG or PNG file.")

        if file.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Profile image must not exceed 2MB.")

        return file


class StudentProfileImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ("profile_image",)
