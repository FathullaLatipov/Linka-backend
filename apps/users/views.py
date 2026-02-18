from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status

from .models import User
from .serializer import LoginSerializer, SignupSerializer, UserSerializer


@swagger_auto_schema(tags=['Authentication'], operation_summary='Регистрация')
class RegisterView(APIView):
    permission_classes = []

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


@swagger_auto_schema(tags=['Authentication'], operation_summary='Вход')
class LoginView(APIView):
    permission_classes = []

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


@swagger_auto_schema(tags=['Authentication'], operation_summary='Выход')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get["refresh"]
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

@swagger_auto_schema(tags=['Authentication'], operation_summary='Обновление токена')
class RefreshTokenView(TokenRefreshView):
    """Обёртка над TokenRefreshView для Swagger."""
    pass


@swagger_auto_schema(tags=['Authentication'], operation_summary='Список пользователей')
class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]