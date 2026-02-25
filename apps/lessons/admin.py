from django.contrib import admin
from .models import Lessons


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','created_at')
    search_fields = ('name',)
    ordering = ("-created_at",)
