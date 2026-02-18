from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import Bookings
from .serializer import BookingSerializer, BookingCancelSerializer


@swagger_auto_schema(tags=['Bookings'], operation_summary='Список бронирований')
class BookingListApiView(ListAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(tags=['Bookings'], operation_summary='Создание бронирования')
class BookingCreateApiView(CreateAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     pass


@swagger_auto_schema(tags=['Bookings'], operation_summary='Мои бронирования')
class MyBookingsListApiView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Bookings.objects.filter(user=user_id)

@swagger_auto_schema(tags=['Bookings'], operation_summary='Отмена бронирования')
class BookingCancelUpdateApiView(UpdateAPIView):
    serializer_class = BookingCancelSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "booking_id"

    def get_queryset(self):
        return Bookings.objects.all()

    def perform_update(self, serializer):
        serializer.status = "Canceled"
        serializer.save(update_fields=["status"])


@swagger_auto_schema(tags=['Bookings'], operation_summary='Детали бронирования')
class BookingDetailedInfoRetrieveApiView(RetrieveAPIView):
    queryset = Bookings.objects.select_related("lesson", "tutor")
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]