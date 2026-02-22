from django.urls import path
from .views import (
    TutorProfileListAPIView,
    TutorProfileCreateAPIView,
    TutorProfileUpdateAPIView,
    TutorProfileDeleteAPIView,
    TutorProfileRetrieveApiView,
    TutorProfileCurrentView,
    TutorsTimeTableCreateApiView,
    TutorsTimeTableListApiView,
    TutorsReviewListApiView,
)

urlpatterns = [
    # Tutors (tz.json)
    path("tutors/", TutorProfileListAPIView.as_view(), name="tutors-list"),
    path("tutors/<int:tutorId>/", TutorProfileRetrieveApiView.as_view(), name="tutors-detail"),
    path("tutors/<int:tutorId>/availability/", TutorsTimeTableListApiView.as_view(), name="tutors-availability"),
    path("tutors/<int:tutorId>/reviews/", TutorsReviewListApiView.as_view(), name="tutors-reviews"),
    # Tutor App (tz.json)
    path("tutor/profile/setup/", TutorProfileCreateAPIView.as_view(), name="tutor-profile-setup"),
    path("tutor/profile/", TutorProfileCurrentView.as_view(), name="tutor-profile-current"),
    path("tutor/availability/", TutorsTimeTableCreateApiView.as_view(), name="tutor-availability"),
    # Legacy
    path("tutor-profile/", TutorProfileListAPIView.as_view(), name="tutor-profile-list"),
    path("tutor-profile/create/", TutorProfileCreateAPIView.as_view(), name="tutor-profile-create"),
    path("tutor-profile/<int:pk>/", TutorProfileRetrieveApiView.as_view(), name="tutor-profile-get"),
    path("tutor-profile/<int:pk>/update/", TutorProfileUpdateAPIView.as_view(), name="tutor-profile-update"),
    path("tutor-profile/<int:pk>/delete/", TutorProfileDeleteAPIView.as_view(), name="tutor-profile-delete"),
    path("tutor-time-table/<int:tutor_id>/", TutorsTimeTableListApiView.as_view(), name="tutor-time-table-list"),
]
