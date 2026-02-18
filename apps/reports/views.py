from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from .models import Reports
from .serializer import ReportsSerializer


@swagger_auto_schema(tags=['Reports'], operation_summary='Список отчётов')
class ReportsListApiView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(tags=['Reports'], operation_summary='Создание отчёта')
class ReportsCreateApiView(CreateAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [AllowAny]

