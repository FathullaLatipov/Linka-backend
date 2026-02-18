from django.urls import path

from .views import StudentProfileRetrieveApiView, StudentProfileCreateApiView, \
    StudentProfileImageUpdateApiView, StudentProfileUpdateApiView, StudentProfileListApiView

urlpatterns = [
    path("student/profile/setup/", StudentProfileCreateApiView.as_view(), name="student-profile-create"),
    path("student-profile/", StudentProfileListApiView.as_view(), name="student-profile-list"),
    path("student-profile/<int:pk>/", StudentProfileRetrieveApiView.as_view(), name="student-profile-get"),
    path("student-profile/<int:user_id>/update", StudentProfileUpdateApiView.as_view(), name="student-profile-update"),
    path("student-profile/image/<int:user_id>/update/", StudentProfileImageUpdateApiView.as_view(), name="student-profile-image-update"),
]
