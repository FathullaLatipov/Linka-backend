from django.contrib import admin
from .models import Reports


@admin.register(Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
