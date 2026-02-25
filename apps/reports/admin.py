from django.contrib import admin
from .models import Reports


@admin.register(Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student__first_name','student__last_name', "comment",'created_at')
    search_fields = ("student__first_name","student__last_name",)
    ordering = ("-created_at",)
