from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from .models import Lessons
from .serializer import LessonSerializer


@swagger_auto_schema(
    tags=['Lessons'],
    operation_summary='Список уроков',
    operation_description='Список уроков. Для тьютора: GET /tutor/lessons/ — уроки текущего тьютора. Query: status (upcoming, completed), page, limit.',
    manual_parameters=[
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='upcoming, completed, cancelled, all'),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description='Список уроков'),
    },
)
class LessonListApiView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(
    tags=['Lessons'],
    operation_summary='Создание урока',
    operation_description='Создать урок. Тело — поля модели Lessons (см. LessonSerializer).',
    request_body=LessonSerializer,
    responses={
        201: openapi.Response(description='Урок создан'),
        400: openapi.Response(description='Ошибка валидации'),
        401: openapi.Response(description='Не авторизован'),
    },
)
class LessonCreateApiView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

