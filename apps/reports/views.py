from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from .models import Reports
from .serializer import ReportsSerializer


@swagger_auto_schema(
    tags=['Admin'],
    operation_summary='Список отчётов',
    operation_description='GET /admin/reports/ — список всех отчётов (admin). Query: status, page, limit.',
    manual_parameters=[
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='pending, reviewed, resolved'),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description='Список отчётов'),
    },
)
class ReportsListApiView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(
    tags=['Tutor App'],
    operation_summary='Создать отчёт (жалоба)',
    operation_description='POST /tutor/reports/ — тьютор жалуется на студента. tz.json: lessonId, reason (abuse, inappropriate_behavior, other), description. Наш: comment, user.',
    request_body=ReportsSerializer,
    responses={
        201: openapi.Response(description='Отчёт создан'),
        400: openapi.Response(description='Ошибка валидации'),
        401: openapi.Response(description='Не авторизован'),
    },
)
class ReportsCreateApiView(CreateAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [AllowAny]

