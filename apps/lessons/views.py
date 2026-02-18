from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from .models import Lessons
from .serializer import LessonSerializer


@swagger_auto_schema(tags=['Lessons'], operation_summary='Список уроков')
class LessonListApiView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(tags=['Lessons'], operation_summary='Создание урока')
class LessonCreateApiView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

