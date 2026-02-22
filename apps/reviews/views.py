from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Reviews
from .serializer import ReviewSerializer


@swagger_auto_schema(
    tags=['Reviews'],
    operation_summary='Создать отзыв',
    operation_description='Создать отзыв на преподавателя. tz.json: lessonId (bookingId), rating (1-5), comment. Наш API: tutor (id), comment, user.',
    request_body=ReviewSerializer,
    responses={
        201: openapi.Response(description='Отзыв создан'),
        400: openapi.Response(description='Ошибка валидации'),
        401: openapi.Response(description='Не авторизован'),
    },
)
class ReviewCreateApiView(CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(
    tags=['Reviews'],
    operation_summary='Мои отзывы',
    operation_description='Список отзывов текущего пользователя. Query: page, limit.',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description='Список моих отзывов'),
        401: openapi.Response(description='Не авторизован'),
    },
)
class MyReviewsListApiView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Reviews.objects.filter(user=self.request.user.id)
        return Reviews.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"success": True, "data": serializer.data})


@swagger_auto_schema(
    tags=['Reviews'],
    operation_summary='Отзывы по user_id (legacy)',
    operation_description='Список отзывов пользователя по user_id в URL.',
    manual_parameters=[openapi.Parameter('user_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True)],
    responses={
        200: openapi.Response(description='Список отзывов'),
        404: openapi.Response(description='Пользователь не найден'),
    },
)
class ReviewListApiView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Reviews.objects.filter(user=user_id)