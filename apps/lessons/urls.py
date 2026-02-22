from django.urls import path

from .views import LessonListApiView, LessonCreateApiView

urlpatterns = [
    # Lessons / Tutor app (tz.json)
    path("tutor/lessons/", LessonListApiView.as_view(), name="tutor-lessons"),
    path("lessons/", LessonListApiView.as_view(), name="lessons-list"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons-create"),
]