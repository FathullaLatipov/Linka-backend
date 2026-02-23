from django.contrib import admin
from .models import Bookings


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'user', 'status', 'created_at')
    list_filter = ('status',)
