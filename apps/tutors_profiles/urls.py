from django.urls import path
from .views import TutorProfileListAPIView, TutorProfileCreateAPIView, TutorProfileUpdateAPIView, \
    TutorProfileDeleteAPIView, TutorProfileRetrieveApiView, TutorsTimeTableCreateApiView, TutorsTimeTableListApiView, \
    TutorsReviewListApiView

urlpatterns = [
    path("tutor-profile/", TutorProfileListAPIView.as_view(), name="tutor-profile-list"),
    path("tutor-profile/create/", TutorProfileCreateAPIView.as_view(), name="tutor-profile-create"),
    path("tutor-profile/<int:pk>/", TutorProfileRetrieveApiView.as_view(), name="tutor-profile-get"),
    path("tutor-profile/<int:pk>/update/", TutorProfileUpdateAPIView.as_view(), name="tutor-profile-update"),
    path("tutor-profile/<int:pk>/delete/", TutorProfileDeleteAPIView.as_view(), name="tutor-profile-delete"),
    path("tutor-time-table/create", TutorsTimeTableCreateApiView.as_view(), name="tutor-time-table-create"),
    path("tutor-time-table/<int:tutor_id>", TutorsTimeTableListApiView.as_view(), name="tutor-time-table-list"),
    path("tutor-reviews/<int:tutor_id>", TutorsReviewListApiView.as_view(), name="tutor-reviews"),
]
