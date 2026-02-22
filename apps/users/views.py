from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status

import random
import uuid
from django.utils import timezone
from datetime import timedelta

from .models import User, OTPCode
from .serializer import (
    LoginSerializer,
    SignupSerializer,
    UserSerializer,
    LogoutSerializer,
    RefreshTokenSerializer,
    SendCodeSerializer,
    VerifyCodeSerializer,
    SendOTPRequestSerializer,
    VerifyOTPRequestSerializer,
)

class RegisterView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Регистрация',
        operation_description='Регистрация нового пользователя. Телефон 9 цифр (без +998).',
        request_body=SignupSerializer,
        responses={
            201: openapi.Response(
                description='Пользователь создан',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(description='Неверные данные'),
        },
    )
    def post(self, request):
        s = SignupSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        user = s.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "user":{
                    "id":user.id,
                    "phone": user.phone
                },
                "access":str(refresh.access_token),
                "refresh":str(refresh)
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Вход',
        operation_description='Вход по телефону и паролю. Телефон 9 цифр (без +998).',
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description='Успешный вход',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                    },
                ),
            ),
            400: openapi.Response(description='Неверные данные'),
            401: openapi.Response(description='Неверный телефон или пароль'),
        },
    )
    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        user = s.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Выход',
        operation_description='Выход из системы. Требует Bearer token. Передайте refresh token в теле для инвалидации.',
        request_body=LogoutSerializer,
        responses={
            200: openapi.Response(
                description='Успешный выход',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            400: openapi.Response(description='Отсутствует refresh token'),
            401: openapi.Response(description='Не авторизован'),
        },
        security=[{'Bearer': []}],
    )
    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response(
                {
                    "error":"Refresh token is required"
                },
                status=400
            )

        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(
                {
                    "detail": "Logged out successfully"
                },
                status=200
            )
        except Exception:
            return Response(
                {
                    "error": "Invalid token"
                },
                status=400
            )

@swagger_auto_schema(
    tags=['Authentication'],
    operation_summary='Обновление токена',
    operation_description='Обновить access token. Принимает refresh token (поле "refresh" в теле).',
    request_body=RefreshTokenSerializer,
    responses={
        200: openapi.Response(
            description='Новые токены',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        401: openapi.Response(description='Невалидный refresh token'),
    },
)
class RefreshTokenView(TokenRefreshView):
    """Обёртка над TokenRefreshView для Swagger."""
    pass


class SendCodeView(APIView):
    """Send SMS verification code. Stub for dev."""
    permission_classes = []

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Отправить SMS-код (tz.json)',
        operation_description='Отправка SMS с кодом верификации. Заглушка для dev.',
        request_body=SendCodeSerializer,
        responses={
            200: openapi.Response(
                description='Код отправлен',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'expiresIn': openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                ),
            ),
            400: openapi.Response(description='Номер не указан'),
        },
    )
    def post(self, request):
        phone = request.data.get("phone", "")
        if not phone:
            return Response({"success": False, "message": "Phone required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"success": True, "message": "Verification code sent", "expiresIn": 120},
            status=status.HTTP_200_OK,
        )


class VerifyCodeView(APIView):
    """Verify SMS code and login. Uses code as password for dev (no SMS)."""
    permission_classes = []

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Верификация кода и вход (tz.json)',
        operation_description='Подтверждение SMS-кода и авторизация. В dev: code = пароль.',
        request_body=VerifyCodeSerializer,
        responses={
            200: openapi.Response(
                description='Успешная авторизация',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'accessToken': openapi.Schema(type=openapi.TYPE_STRING),
                        'refreshToken': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                                'role': openapi.Schema(type=openapi.TYPE_STRING),
                                'isProfileComplete': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            },
                        ),
                    },
                ),
            ),
            400: openapi.Response(description='Не указаны phone или code'),
            401: openapi.Response(description='Неверный телефон или код'),
        },
    )
    def post(self, request):
        phone = request.data.get("phone", "")
        code = request.data.get("code", "")
        if not phone or not code:
            return Response(
                {"success": False, "message": "Phone and code required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        from django.contrib.auth import authenticate
        user = authenticate(request, phone=phone, password=code)
        if not user:
            return Response(
                {"success": False, "message": "Invalid phone or code"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "success": True,
                "accessToken": str(refresh.access_token),
                "refreshToken": str(refresh),
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "role": getattr(user, "role", "student"),
                    "isProfileComplete": hasattr(user, "student_profile") and user.student_profile is not None,
                },
            },
            status=status.HTTP_200_OK,
        )


# --- OTP Flow (классический flow как в мобильных приложениях Узбекистана 2025–2026) ---
# Rate limiting: рекомендуется добавить ThrottleAnonRate (например 5/min на send-otp, 10/min на verify-otp)


class SendOTPView(APIView):
    """POST /auth/send-otp/ — отправка OTP. В production: интеграция с SMS-провайдером."""
    permission_classes = []
    # TODO: throttle_classes = [AnonRateThrottle]  # rate limiting

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Отправить OTP-код',
        operation_description='Отправляет код подтверждения на телефон. Формат E.164: +998901234567. В dev: код сохраняется в БД, SMS не отправляется.',
        request_body=SendOTPRequestSerializer,
        responses={
            200: openapi.Response(
                description='Код отправлен',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        'verifyID': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='550e8400-e29b-41d4-a716-446655440000',
                            description='UUID для верификации',
                        ),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Код отправлен'),
                        'expiresIn': openapi.Schema(type=openapi.TYPE_INTEGER, example=120, description='Секунд до истечения'),
                    },
                ),
            ),
            400: openapi.Response(
                description='Неверный формат номера',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        serializer = SendOTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']

        otp = ''.join(random.choices('0123456789', k=6))
        verify_id = str(uuid.uuid4())
        expires_at = timezone.now() + timedelta(seconds=120)

        OTPCode.objects.create(
            verify_id=verify_id,
            phone=phone,
            otp_code=otp,
            expires_at=expires_at,
        )

        # В production: отправить SMS через провайдера (Eskiz, Nexmo и т.д.)
        # send_sms(phone, f'Ваш код: {otp}')

        return Response(
            {
                'success': True,
                'verifyID': verify_id,
                'message': 'Код отправлен',
                'expiresIn': 120,
            },
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(APIView):
    """POST /auth/verify-otp/ — верификация OTP и выдача JWT."""
    permission_classes = []
    # TODO: throttle_classes = [AnonRateThrottle]

    def _get_or_create_user(self, phone):
        user = User.objects.filter(phone=phone).first()
        if not user:
            # Нормализация для lookup: +998901234567 -> 901234567 (legacy)
            legacy = phone.replace('+998', '') if phone.startswith('+998') else phone
            user = User.objects.filter(phone=legacy).first()
        if not user:
            user = User.objects.create_user(phone=phone)
            user.set_unusable_password()
            user.save()
        return user

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Подтвердить OTP и войти',
        operation_description='Проверяет код, при успехе возвращает JWT и данные пользователя. При первом входе создаёт пользователя.',
        request_body=VerifyOTPRequestSerializer,
        responses={
            200: openapi.Response(
                description='Успешная авторизация',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        'accessToken': openapi.Schema(type=openapi.TYPE_STRING),
                        'refreshToken': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'phone': openapi.Schema(type=openapi.TYPE_STRING, example='+998901234567'),
                                'role': openapi.Schema(type=openapi.TYPE_STRING, example='student'),
                                'isProfileComplete': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            },
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description='Неверный или истёкший код',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        serializer = VerifyOTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify_id = serializer.validated_data['verifyID']
        otp_code = serializer.validated_data['otp_code']

        try:
            record = OTPCode.objects.get(verify_id=verify_id)
        except OTPCode.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Неверный verifyID или код истёк'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if record.is_expired():
            return Response(
                {'success': False, 'message': 'Код истёк. Запросите новый.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if record.otp_code != otp_code:
            return Response(
                {'success': False, 'message': 'Неверный код подтверждения'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = self._get_or_create_user(record.phone)
        refresh = RefreshToken.for_user(user)

        # Опционально: удалить использованный OTP (одноразовый)
        record.delete()

        role = 'tutor' if user.is_teacher else 'student'
        has_profile = hasattr(user, 'student_profile') and user.student_profile is not None

        return Response(
            {
                'success': True,
                'accessToken': str(refresh.access_token),
                'refreshToken': str(refresh),
                'user': {
                    'id': user.id,
                    'phone': user.phone,
                    'role': role,
                    'isProfileComplete': has_profile,
                },
            },
            status=status.HTTP_200_OK,
        )


@swagger_auto_schema(
    tags=['Authentication'],
    operation_summary='Список пользователей',
    operation_description='Получить список всех пользователей. Query: page, limit.',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description='Список пользователей'),
    },
)
class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]