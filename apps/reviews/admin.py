from django.contrib import admin
from .models import Reviews


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'user', 'created_at')
    search_fields = ('comment',)
