from django.urls import path

from .views import ReviewCreateApiView, ReviewListApiView

urlpatterns = [
    path("review/create/", ReviewCreateApiView.as_view(), name="review-create"),
    path("review/<int:user_id>/", ReviewListApiView.as_view(), name="review-get"),
]
