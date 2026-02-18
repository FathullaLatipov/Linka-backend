from rest_framework import serializers

from apps.bookings.models import Bookings
from apps.tutors_profiles.models import TutorsTimeTable


class BookingSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(
        queryset=TutorsTimeTable.objects.all()
    )

    class Meta:
        model = Bookings
        fields = "__all__"

class BookingCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ("status",)