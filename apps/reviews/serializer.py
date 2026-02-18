from rest_framework import serializers

from .models import Reviews
from apps.tutors_profiles.models import TutorsProfile


class ReviewSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(
        queryset=TutorsProfile.objects.filter(is_deleted=False)
    )
    class Meta:
        model = Reviews
        fields = "__all__"