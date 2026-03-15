from rest_framework import serializers

class CreateRoomSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    expires_in_seconds = serializers.IntegerField(default=3600)

class RoomResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    url = serializers.CharField()
    created_at = serializers.CharField()