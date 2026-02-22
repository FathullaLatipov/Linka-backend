from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.reviews.models import Reviews
from .models import TutorsProfile, TutorsTimeTable
from .serializer import TutorsProfileSerializer, TutorsTimeTableSerializer


@swagger_auto_schema(
    tags=['Tutors'],
    operation_summary='Список преподавателей',
    operation_description='Список всех преподавателей. Требует Bearer token.',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Страница'),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Лимит на страницу'),
        openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Поиск по имени'),
    ],
    responses={200: openapi.Response(description='Список преподавателей')},
    security=[{'Bearer': []}],
)
class TutorProfileListAPIView(ListAPIView):
    queryset = TutorsProfile.objects.filter(is_deleted=False)
    serializer_class = TutorsProfileSerializer
    permission_classes = [IsAuthenticated]


@swagger_auto_schema(
    tags=['Tutors'],
    operation_summary='Профиль преподавателя',
    operation_description='Детали преподавателя по tutorId (pk).',
    manual_parameters=[openapi.Parameter('tutorId', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID преподавателя')],
    responses={
        200: openapi.Response(description='Профиль преподавателя'),
        404: openapi.Response(description='Не найден'),
    },
    security=[{'Bearer': []}],
)
class TutorProfileRetrieveApiView(RetrieveAPIView):
    serializer_class = TutorsProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "tutorId"
    lookup_field = "pk"

    def get_queryset(self):
        return TutorsProfile.objects.filter(is_deleted=False)

@swagger_auto_schema(
    tags=['Tutor App'],
    operation_summary='Создание профиля тьютора (setup)',
    operation_description='Первичная настройка. Поля: fullName/displayName, profilePhoto, ieltsScore, ieltsCertificate. multipart/form-data.',
    request_body=TutorsProfileSerializer,
    responses={
        200: openapi.Response(description='Профиль создан'),
        201: openapi.Response(description='Создан'),
        400: openapi.Response(description='Ошибка валидации'),
    },
    security=[{'Bearer': []}],
)
class TutorProfileCreateAPIView(CreateAPIView):
    queryset = TutorsProfile.objects.filter(is_deleted=False)
    serializer_class = TutorsProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class TutorProfileCurrentView(APIView):
    """PUT /tutor/profile/ - update current user's tutor profile."""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=['Tutor App'],
        operation_summary='Обновить профиль тьютора',
        operation_description='PUT — обновить профиль текущего пользователя-тьютора. displayName, bio, introVideoUrl, ieltsBreakdown.',
        request_body=TutorsProfileSerializer,
        responses={
            200: openapi.Response(description='Профиль обновлён'),
            400: openapi.Response(description='Ошибка валидации'),
            404: openapi.Response(description='Не найден'),
        },
        security=[{'Bearer': []}],
    )
    def put(self, request):
        profile = get_object_or_404(TutorsProfile, user=request.user.id)
        serializer = TutorsProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Profile updated", "data": serializer.data})


@swagger_auto_schema(
    tags=['Tutors'],
    operation_summary='Обновление профиля (legacy)',
    operation_description='Обновить по pk в URL.',
    manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID профиля')],
    request_body=TutorsProfileSerializer,
    responses={
        200: openapi.Response(description='Профиль обновлён'),
        400: openapi.Response(description='Ошибка валидации'),
        404: openapi.Response(description='Не найден'),
    },
    security=[{'Bearer': []}],
)
class TutorProfileUpdateAPIView(UpdateAPIView):
    serializer_class = TutorsProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TutorsProfile.objects.filter(is_deleted=False)


@swagger_auto_schema(
    tags=['Tutors'],
    operation_summary='Удаление (soft) профиля',
    operation_description='Мягкое удаление — is_deleted=true. pk в URL.',
    manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID профиля')],
    responses={
        200: openapi.Response(description='Удалено'),
        204: openapi.Response(description='Удалено'),
        401: openapi.Response(description='Не авторизован'),
        404: openapi.Response(description='Не найден'),
    },
    security=[{'Bearer': []}],
)
class TutorProfileDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TutorsProfile.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])


@swagger_auto_schema(
    tags=['Tutors'],
    operation_summary='Расписание преподавателя',
    operation_description='Свободные слоты по tutorId. Query: date (YYYY-MM-DD), duration (20,30,40,60).',
    manual_parameters=[
        openapi.Parameter('tutorId', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter('date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='YYYY-MM-DD'),
        openapi.Parameter('duration', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='20, 30, 40 или 60 мин'),
    ],
    responses={200: openapi.Response(description='Список слотов')},
    security=[{'Bearer': []}],
)
class TutorsTimeTableListApiView(ListAPIView):
    queryset = TutorsTimeTable.objects.all()
    serializer_class = TutorsTimeTableSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tutor_id = self.kwargs.get("tutorId") or self.kwargs.get("tutor_id")
        return TutorsTimeTable.objects.filter(tutor=tutor_id)


@swagger_auto_schema(
    tags=['Tutors'],
    operation_summary='Отзывы о преподавателе',
    operation_description='Список отзывов по tutorId. Query: page, limit.',
    manual_parameters=[
        openapi.Parameter('tutorId', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={200: openapi.Response(description='Список отзывов')},
    security=[{'Bearer': []}],
)
class TutorsReviewListApiView(ListAPIView):
    serializer_class = TutorsTimeTableSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tutor_id = self.kwargs.get("tutorId") or self.kwargs.get("tutor_id")
        return Reviews.objects.filter(tutor=tutor_id)

@swagger_auto_schema(
    tags=['Tutor App'],
    operation_summary='Добавить слот расписания',
    operation_description='Создать слот доступности. Тело: available_time (HH:MM), tutor (id).',
    request_body=TutorsTimeTableSerializer,
    responses={
        201: openapi.Response(description='Слот создан'),
        400: openapi.Response(description='Ошибка валидации'),
    },
    security=[{'Bearer': []}],
)
class TutorsTimeTableCreateApiView(CreateAPIView):
    queryset = TutorsTimeTable.objects.all()
    serializer_class = TutorsTimeTableSerializer
    permission_classes = [IsAuthenticated]



