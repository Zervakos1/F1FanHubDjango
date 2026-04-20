"""Database models for user profiles, premium subscriptions, and rewards."""

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Extend the default Django user with extra profile and reward data.

    Roles:
    - user: regular registered user
    - premium: user with active premium features
    - manager: business operator with in-site management access
    """

    ROLE_CHOICES = [
        ("user", "User"),
        ("premium", "Premium"),
        ("manager", "Manager"),
    ]

    premium_points = models.PositiveIntegerField(default=0)
    lifetime_points = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        """Return the username for the related profile."""
        return self.user.username


class PremiumSubscription(models.Model):
    """Store simulated premium membership subscriptions for users."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="premium_subscriptions")
    plan_name = models.CharField(max_length=100, default="Premium Membership")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=15.00)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Return a readable premium subscription label."""
        return f"{self.user.username} - {self.plan_name}"


class DiscountReward(models.Model):
    """Store redeemable discount rewards created from premium points."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discount_rewards")
    name = models.CharField(max_length=100, default="€10 Discount Voucher")
    points_cost = models.PositiveIntegerField(default=200)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Return a readable discount reward label."""
        return f"{self.user.username} - {self.name}"


class RaffleEntry(models.Model):
    """Store raffle entries created when users redeem premium points."""

    STATUS_CHOICES = [
        ("joined", "Joined"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="raffle_entries")
    prize_name = models.CharField(max_length=150, default="Free Ticket Raffle")
    points_cost = models.PositiveIntegerField(default=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="joined")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable raffle entry label."""
        return f"{self.user.username} - {self.prize_name}"