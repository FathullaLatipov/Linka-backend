from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from apps.reviews.models import Reviews
from .models import TutorsProfile, TutorsTimeTable
from .serializer import TutorsProfileSerializer, TutorsTimeTableSerializer


@swagger_auto_schema(tags=['Tutors'], operation_summary='Список преподавателей')
class TutorProfileListAPIView(ListAPIView):
    queryset = TutorsProfile.objects.filter(is_deleted=False)
    serializer_class = TutorsProfileSerializer
    permission_classes = [IsAuthenticated]


@swagger_auto_schema(tags=['Tutors'], operation_summary='Профиль преподавателя')
class TutorProfileRetrieveApiView(RetrieveAPIView):
    serializer_class = TutorsProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TutorsProfile.objects.filter(is_deleted=False)

@swagger_auto_schema(tags=['Tutors'], operation_summary='Создание профиля преподавателя')
class TutorProfileCreateAPIView(CreateAPIView):
    queryset = TutorsProfile.objects.filter(is_deleted=False)
    serializer_class = TutorsProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

@swagger_auto_schema(tags=['Tutors'], operation_summary='Обновление профиля преподавателя')
class TutorProfileUpdateAPIView(UpdateAPIView):
    serializer_class = TutorsProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TutorsProfile.objects.filter(is_deleted=False)


@swagger_auto_schema(tags=['Tutors'], operation_summary='Удаление (soft) профиля преподавателя')
class TutorProfileDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TutorsProfile.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])


@swagger_auto_schema(tags=['Tutors'], operation_summary='Расписание преподавателя')
class TutorsTimeTableListApiView(ListAPIView):
    queryset = TutorsTimeTable.objects.all()
    serializer_class = TutorsTimeTableSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        tutor_id = self.kwargs["tutor_id"]
        return TutorsTimeTable.objects.filter(tutor=tutor_id)


@swagger_auto_schema(tags=['Tutors'], operation_summary='Отзывы о преподавателе')
class TutorsReviewListApiView(ListAPIView):
    serializer_class = TutorsTimeTableSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        tutor_id = self.kwargs["tutor_id"]
        return Reviews.objects.filter(tutor=tutor_id)

@swagger_auto_schema(tags=['Tutors'], operation_summary='Создание слота расписания')
class TutorsTimeTableCreateApiView(CreateAPIView):
    queryset = TutorsTimeTable.objects.all()
    serializer_class = TutorsTimeTableSerializer
    permission_classes = [IsAuthenticated]



