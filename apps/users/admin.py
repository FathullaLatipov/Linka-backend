from django.contrib import admin
from .models import OTPCode


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('verify_id', 'phone', 'otp_code', 'expires_at', 'created_at')
    search_fields = ('phone', 'verify_id')
