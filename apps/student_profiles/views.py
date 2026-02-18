from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, get_object_or_404, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import StudentProfile
from .serializer import StudentProfileSerializer, StudentProfileImageUpdateSerializer


@swagger_auto_schema(tags=['Student Profile'], operation_summary='Профиль студента (по ID)')
class StudentProfileRetrieveApiView(RetrieveAPIView):
    queryset = StudentProfile
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]

@swagger_auto_schema(tags=['Student Profile'], operation_summary='Создание профиля студента')
class StudentProfileCreateApiView(CreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


@swagger_auto_schema(tags=['Student Profile'], operation_summary='Обновление аватара')
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



@swagger_auto_schema(tags=['Student Profile'], operation_summary='Обновление профиля')
class StudentProfileUpdateApiView(UpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(StudentProfile,user=self.kwargs["user_id"])


@swagger_auto_schema(tags=['Student Profile'], operation_summary='Список профилей студентов')
class StudentProfileListApiView(ListAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]



