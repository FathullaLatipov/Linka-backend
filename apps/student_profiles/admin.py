from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'englishLevel', 'user', 'created_at')
    search_fields = ('first_name', 'last_name')
