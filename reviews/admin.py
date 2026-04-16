"""Admin configuration for review management."""

from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Customize how reviews appear in the Django admin."""

    list_display = ["product", "user", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["product__name", "user__username", "comment"]