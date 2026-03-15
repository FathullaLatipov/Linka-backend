from django.urls import path
from .views import CreateRoomView, RoomDetailView, JoinRoomView

urlpatterns = [
    path("rooms/", CreateRoomView.as_view(), name="create-room"),
    path("rooms/<str:room_name>/", RoomDetailView.as_view(), name="room-detail"),
    path("rooms/<str:room_name>/join/", JoinRoomView.as_view(), name="join-room"),
]