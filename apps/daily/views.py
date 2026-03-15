from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.daily import create_room, get_room, delete_room, create_meeting_token
from .serializers import CreateRoomSerializer
import requests


class CreateRoomView(APIView):
    def post(self, request):
        serializer = CreateRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            room = create_room(
                name=serializer.validated_data.get("name"),
                expires_in_seconds=serializer.validated_data.get("expires_in_seconds", 3600),
            )

            # Сразу генерируем токен для создателя (owner)
            token = create_meeting_token(
                room_name=room["name"],
                user_name=request.user.username if request.user.is_authenticated else None,
                is_owner=True,
            )

            return Response({
                "room": {
                    "id": room["id"],
                    "name": room["name"],
                    "url": room["url"],
                },
                "token": token["token"],  # передаёшь на фронтенд
            }, status=status.HTTP_201_CREATED)

        except requests.HTTPError as e:
            return Response(
                {"error": f"Daily.co error: {e.response.text}"},
                status=e.response.status_code,
            )


class RoomDetailView(APIView):
    def get(self, request, room_name):
        """Получить информацию о комнате"""
        try:
            room = get_room(room_name)
            return Response(room)
        except requests.HTTPError as e:
            return Response({"error": e.response.text}, status=e.response.status_code)

    def delete(self, request, room_name):
        """Удалить комнату"""
        try:
            result = delete_room(room_name)
            return Response(result)
        except requests.HTTPError as e:
            return Response({"error": e.response.text}, status=e.response.status_code)


class JoinRoomView(APIView):
    def post(self, request, room_name):
        """Получить токен для входа в существующую комнату"""
        try:
            token = create_meeting_token(
                room_name=room_name,
                user_name=request.user.username if request.user.is_authenticated else None,
                is_owner=False,
            )
            room = get_room(room_name)

            return Response({
                "url": room["url"],
                "token": token["token"],
            })
        except requests.HTTPError as e:
            return Response({"error": e.response.text}, status=e.response.status_code)