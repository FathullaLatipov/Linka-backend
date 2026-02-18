from rest_framework import serializers

from .models import Lessons


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = "__all__"