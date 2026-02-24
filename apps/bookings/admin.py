from django.contrib import admin
from .models import Bookings


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'student__first_name','student__last_name', 'tutor__tutor__first_name','status', 'created_at')
    list_filter = ('status',)
