from django.contrib import admin
from .models import Reviews


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('tutor__first_name',
                    'tutor__last_name',
                    'student__first_name',
                    'student__last_name',
                    'created_at')
    search_fields = ('comment',)
