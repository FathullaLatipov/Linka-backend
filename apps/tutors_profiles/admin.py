from django.contrib import admin
from .models import TutorsProfile, TutorsTimeTable


@admin.register(TutorsProfile)
class TutorsProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'ielts_score', 'experience', 'is_deleted', 'created_at')
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_deleted',)


@admin.register(TutorsTimeTable)
class TutorsTimeTableAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'available_time', 'created_at')
