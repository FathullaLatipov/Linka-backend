from django.urls import path

from .views import LessonListApiView, LessonCreateApiView

urlpatterns = [
    path("lessons/",LessonListApiView.as_view(),name="lessons-list"),
    path("lessons/create",LessonCreateApiView.as_view(),name="lessons-create"),
]