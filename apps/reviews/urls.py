from django.urls import path

from .views import ReviewCreateApiView, ReviewListApiView, MyReviewsListApiView

urlpatterns = [
    # Reviews (tz.json)
    path("reviews/", ReviewCreateApiView.as_view(), name="reviews-create"),
    path("reviews/my/", MyReviewsListApiView.as_view(), name="reviews-my"),
    # Legacy
    path("review/create/", ReviewCreateApiView.as_view(), name="review-create"),
    path("review/<int:user_id>/", ReviewListApiView.as_view(), name="review-get"),
]
