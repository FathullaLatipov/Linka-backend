from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, get_object_or_404, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import StudentProfile
from .serializer import StudentProfileSerializer, StudentProfileImageUpdateSerializer


class StudentProfileCurrentView(APIView):
    """GET - current user profile, PUT - update current user profile."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Student Profile'],
        operation_summary='Получить профиль студента',
        operation_description='Профиль текущего пользователя. Требует Bearer token.',
        responses={
            200: openapi.Response(description='Профиль студента'),
            401: openapi.Response(description='Не авторизован'),
            404: openapi.Response(description='Профиль не найден'),
        },
        security=[{'Bearer': []}],
    )
    def get(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        return Response({"success": True, "data": StudentProfileSerializer(profile).data})

    @swagger_auto_schema(
        tags=['Student Profile'],
        operation_summary='Обновить профиль студента',
        operation_description='PUT — обновить профиль (все поля опциональны). Требует Bearer token.',
        request_body=StudentProfileSerializer,
        responses={
            200: openapi.Response(description='Профиль обновлён'),
            401: openapi.Response(description='Не авторизован'),
            404: openapi.Response(description='Профиль не найден'),
        },
        security=[{'Bearer': []}],
    )
    def put(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Profile updated", "data": serializer.data})


class StudentProfilePictureView(APIView):
    """POST - upload profile picture for current user."""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=['Student Profile'],
        operation_summary='Загрузить фото профиля (tz.json)',
        operation_description='POST multipart/form-data. Поле: profile_image (файл JPG/PNG до 2MB). Требует Bearer token.',
        request_body=StudentProfileImageUpdateSerializer,
        responses={
            200: openapi.Response(description='Фото загружено'),
            401: openapi.Response(description='Не авторизован'),
            404: openapi.Response(description='Профиль не найден'),
        },
        security=[{'Bearer': []}],
    )
    def post(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        serializer = StudentProfileImageUpdateSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "data": {"profilePicture": serializer.data.get("profile_image")}})


@swagger_auto_schema(
    tags=['Student Profile'],
    operation_summary='Профиль студента по ID',
    operation_description='Получить профиль по pk (legacy endpoint).',
    manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID профиля')],
    responses={
        200: openapi.Response(description='Профиль'),
        404: openapi.Response(description='Не найден'),
    },
)
class StudentProfileRetrieveApiView(RetrieveAPIView):
    queryset = StudentProfile
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]

@swagger_auto_schema(
    tags=['Student Profile'],
    operation_summary='Создание профиля (setup)',
    operation_description='Первичная настройка профиля. Поля: first_name, last_name, englishLevel, profile_image (файл). Требует Bearer token.',
    request_body=StudentProfileSerializer,
    responses={
        201: openapi.Response(description='Профиль создан'),
        400: openapi.Response(description='Ошибка валидации'),
        401: openapi.Response(description='Не авторизован'),
    },
    security=[{'Bearer': []}],
)
class StudentProfileCreateApiView(CreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


@swagger_auto_schema(
    tags=['Student Profile'],
    operation_summary='Обновление аватара (legacy)',
    operation_description='Обновить фото по user_id в URL.',
    manual_parameters=[openapi.Parameter('user_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID пользователя')],
    request_body=StudentProfileImageUpdateSerializer,
    responses={
        200: openapi.Response(description='Фото обновлено'),
        400: openapi.Response(description='Ошибка валидации'),
        404: openapi.Response(description='Не найден'),
    },
)
class StudentProfileImageUpdateApiView(UpdateAPIView):
    serializer_class = StudentProfileImageUpdateSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs["user_id"]
        return StudentProfile.objects.get(user=user_id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", request.method == "PATCH")
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(StudentProfileSerializer(instance).data)



@swagger_auto_schema(
    tags=['Student Profile'],
    operation_summary='Обновление профиля (legacy)',
    operation_description='Обновить профиль по user_id в URL.',
    manual_parameters=[openapi.Parameter('user_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID пользователя')],
    request_body=StudentProfileSerializer,
    responses={
        200: openapi.Response(description='Профиль обновлён'),
        400: openapi.Response(description='Ошибка валидации'),
        404: openapi.Response(description='Не найден'),
    },
)
class StudentProfileUpdateApiView(UpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(StudentProfile,user=self.kwargs["user_id"])


@swagger_auto_schema(
    tags=['Student Profile'],
    operation_summary='Список профилей студентов',
    operation_description='Список всех профилей. Query: page, limit.',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description='Список профилей'),
    },
)
class StudentProfileListApiView(ListAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]



