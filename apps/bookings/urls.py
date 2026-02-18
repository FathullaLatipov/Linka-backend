from django.urls import path

from .views import BookingCreateApiView, BookingListApiView, MyBookingsListApiView, BookingCancelUpdateApiView, \
    BookingDetailedInfoRetrieveApiView

urlpatterns = [
    path("bookings/book",BookingCreateApiView.as_view(), name="booking-create"),
    path("bookings/",BookingListApiView.as_view(), name="booking-list"),
    path("bookings/<int:user_id>",MyBookingsListApiView.as_view(), name="my-booking-list"),
    path("bookings/<int:booking_id>/cancel/",BookingCancelUpdateApiView.as_view(), name="booking-cancel"),
    path("bookings/<int:user_id>",MyBookingsListApiView.as_view(), name="my-booking-list"),
    path("bookings/<int:pk>",BookingDetailedInfoRetrieveApiView.as_view(), name="detailed-info"),
]