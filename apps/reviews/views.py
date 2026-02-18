from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from .models import Reviews
from .serializer import ReviewSerializer


@swagger_auto_schema(tags=['Reviews'], operation_summary='Создание отзыва')
class ReviewCreateApiView(CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(tags=['Reviews'], operation_summary='Отзывы (по user_id)')
class ReviewListApiView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Reviews.objects.filter(user=user_id)