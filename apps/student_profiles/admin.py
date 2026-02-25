from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'englishLevel',
        'user__phone',
        'profile_image',
        'created_at'
    )
    search_fields = ('first_name', 'last_name',"user__phone")
    list_filter = ("englishLevel","created_at",)
    ordering = ("-created_at",)
