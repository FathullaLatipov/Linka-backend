from django.urls import path

from .views import (
    BookingCreateApiView,
    BookingsListCreateView,
    MyBookingsListApiView,
    BookingCancelUpdateApiView,
    BookingDetailedInfoRetrieveApiView,
    BookingJoinView,
)

urlpatterns = [
    # Bookings (tz.json)
    path("bookings/", BookingsListCreateView.as_view(), name="bookings-list-create"),
    path("bookings/<int:bookingId>/", BookingDetailedInfoRetrieveApiView.as_view(), name="bookings-detail"),
    path("bookings/<int:bookingId>/cancel/", BookingCancelUpdateApiView.as_view(), name="bookings-cancel"),
    path("bookings/<int:bookingId>/join/", BookingJoinView.as_view(), name="bookings-join"),
    # Legacy
    path("bookings/book/", BookingCreateApiView.as_view(), name="booking-create"),
    path("bookings/<int:user_id>/my/", MyBookingsListApiView.as_view(), name="my-booking-list"),
]