from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPCode


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'is_active', 'is_staff', 'is_teacher', 'is_student')
    search_fields = ('phone',)
    ordering = ('phone',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_teacher', 'is_student')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_teacher', 'is_student')}),
    )


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('verify_id', 'phone', 'otp_code', 'expires_at', 'created_at')
    search_fields = ('phone', 'verify_id')
    list_filter = ('created_at',)
