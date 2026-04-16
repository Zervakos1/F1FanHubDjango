"""Admin configuration for account-related models."""

from django.contrib import admin

from .models import Profile, PremiumSubscription, DiscountReward, RaffleEntry


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin options for user profiles."""

    list_display = ["user", "role", "premium_points", "lifetime_points", "phone", "country"]
    list_filter = ["role", "country"]
    search_fields = ["user__username", "user__email", "phone", "country"]


@admin.register(PremiumSubscription)
class PremiumSubscriptionAdmin(admin.ModelAdmin):
    """Admin options for premium subscriptions."""

    list_display = ["user", "plan_name", "price", "is_active", "started_at", "ended_at"]
    list_filter = ["is_active", "started_at", "ended_at"]
    search_fields = ["user__username", "user__email", "plan_name"]


@admin.register(DiscountReward)
class DiscountRewardAdmin(admin.ModelAdmin):
    """Admin options for discount rewards."""

    list_display = ["user", "name", "discount_amount", "points_cost", "is_used", "created_at"]
    list_filter = ["is_used", "created_at"]
    search_fields = ["user__username", "name"]


@admin.register(RaffleEntry)
class RaffleEntryAdmin(admin.ModelAdmin):
    """Admin options for raffle entries."""

    list_display = ["user", "prize_name", "points_cost", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "prize_name"]