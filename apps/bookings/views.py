from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Bookings
from .serializer import BookingSerializer, BookingCancelSerializer

@swagger_auto_schema(
    tags=['Bookings'],
    operation_summary='Список бронирований',
    operation_description='Список всех бронирований. Query: page, limit.',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description='Список бронирований'),
    },
)
class BookingListApiView(ListAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(
    tags=['Bookings'],
    operation_summary='Создание бронирования',
    operation_description='Создать бронирование. Поля: tutor (TutorsTimeTable id), lesson, user, comment.',
    request_body=BookingSerializer,
    responses={
        201: openapi.Response(description='Бронирование создано'),
        400: openapi.Response(description='Ошибка валидации'),
        401: openapi.Response(description='Не авторизован'),
    },
)
class BookingCreateApiView(CreateAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(
    tags=['Bookings'],
    operation_summary='Мои бронирования',
    operation_description='Список бронирований текущего пользователя. Query: status, page, limit.',
    manual_parameters=[
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='upcoming, completed, cancelled, all'),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description='Список бронирований'),
        401: openapi.Response(description='Не авторизован'),
    },
)
class MyBookingsListApiView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookings.objects.filter(student=self.request.user)


class BookingsListCreateView(APIView):
    """GET - my bookings, POST - create booking."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Bookings'],
        operation_summary='Мои бронирования',
        operation_description='GET — мои бронирования. Query: status, page, limit.',
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='upcoming, completed, cancelled'),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(description='Список бронирований'),
        },
    )
    def get(self, request):
        qs = Bookings.objects.all()
        if request.user.is_authenticated:
            qs = qs.filter(student=request.user)
        serializer = BookingSerializer(qs, many=True)
        return Response({"success": True, "data": serializer.data})

    @swagger_auto_schema(
        tags=['Bookings'],
        operation_summary='Создать бронирование',
        operation_description='POST — создать бронирование. Поля: tutor (TutorsTimeTable id), lesson, user, comment.',
        request_body=BookingSerializer,
        responses={
            201: openapi.Response(description='Бронирование создано'),
            400: openapi.Response(description='Ошибка валидации'),
        },
    )
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    tags=['Bookings'],
    operation_summary='Отмена бронирования',
    operation_description='Отменить бронирование по bookingId. Тело (опц.): reason.',
    manual_parameters=[
        openapi.Parameter('bookingId', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID бронирования'),
        openapi.Parameter(
            'body',
            openapi.IN_BODY,
            required=False,
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'reason': openapi.Schema(type=openapi.TYPE_STRING)},
                example={'reason': 'Schedule conflict'},
            ),
        ),
    ],
    responses={
        200: openapi.Response(description='Бронирование отменено'),
        400: openapi.Response(description='Ошибка'),
        404: openapi.Response(description='Бронирование не найдено'),
    },
)
class BookingCancelUpdateApiView(UpdateAPIView):
    serializer_class = BookingCancelSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "bookingId"
    lookup_field = "pk"

    def get_queryset(self):
        return Bookings.objects.all()

    def perform_update(self, serializer):
        serializer.save(status="Canceled")


@swagger_auto_schema(
    tags=['Bookings'],
    operation_summary='Детали бронирования',
    operation_description='Получить детали бронирования по bookingId.',
    manual_parameters=[openapi.Parameter('bookingId', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True)],
    responses={
        200: openapi.Response(description='Детали бронирования'),
        404: openapi.Response(description='Не найдено'),
    },
)
class BookingDetailedInfoRetrieveApiView(RetrieveAPIView):
    queryset = Bookings.objects.select_related("lesson", "tutor")
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "bookingId"


class BookingJoinView(APIView):
    """Get join URL for video lesson. Stub for now."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Bookings'],
        operation_summary='Присоединиться к уроку',
        operation_description='Получить URL видеокомнаты. POST без тела. bookingId в path. Заглушка.',
        manual_parameters=[openapi.Parameter('bookingId', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID бронирования')],
        responses={
            200: openapi.Response(
                description='URL для подключения к уроку',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'joinUrl': openapi.Schema(type=openapi.TYPE_STRING),
                                'token': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            404: openapi.Response(description='Бронирование не найдено'),
        },
    )
    def post(self, request, bookingId):
        return Response({
            "success": True,
            "data": {
                "joinUrl": f"https://video.example.com/room/lesson_{bookingId}",
                "token": "video_session_token_xyz",
            },
        })