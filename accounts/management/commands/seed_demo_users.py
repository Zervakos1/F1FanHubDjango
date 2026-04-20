"""Management command for creating reusable demo accounts for the project."""

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import PremiumSubscription, Profile
from cart.models import Cart


class Command(BaseCommand):
    """Create or refresh the demo users used for presentation and testing."""

    help = "Create or refresh demo users for testing"

    def handle(self, *args, **kwargs):
        """Run all demo-user creation helpers in sequence."""
        self.create_regular_user()
        self.create_premium_user()
        self.create_manager_user()
        self.create_admin_user()
        self.remove_old_test_user()
        self.stdout.write(self.style.SUCCESS("Demo users created or updated successfully."))

    def ensure_cart(self, user):
        Cart.objects.get_or_create(user=user)

    def deactivate_all_premium_subscriptions(self, user):
        user.premium_subscriptions.update(
            is_active=False,
            ended_at=None,
        )

    def ensure_active_premium_subscription(self, user):
        subscription = user.premium_subscriptions.filter(is_active=True).first()

        if subscription:
            subscription.plan_name = "Premium Membership"
            subscription.price = Decimal("15.00")
            subscription.ended_at = None
            subscription.save()
            return

        user.premium_subscriptions.filter(is_active=False).update(
            plan_name="Premium Membership",
            price=Decimal("15.00"),
            is_active=True,
            ended_at=None,
        )

        if not user.premium_subscriptions.filter(is_active=True).exists():
            PremiumSubscription.objects.create(
                user=user,
                plan_name="Premium Membership",
                price=Decimal("15.00"),
                is_active=True,
            )

    def create_regular_user(self):
        """Create the normal user account."""
        user, _ = User.objects.get_or_create(
            username="regularuser",
            defaults={"email": "regular@example.com"},
        )
        user.email = "regular@example.com"
        user.set_password("Regular123!")
        user.is_staff = False
        user.is_superuser = False
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = "user"
        profile.phone = "1111111111"
        profile.country = "Cyprus"
        profile.save()

        self.deactivate_all_premium_subscriptions(user)
        self.ensure_cart(user)

    def create_premium_user(self):
        """Create the premium user account."""
        user, _ = User.objects.get_or_create(
            username="premiumuser",
            defaults={"email": "premium@example.com"},
        )
        user.email = "premium@example.com"
        user.set_password("Premium123!")
        user.is_staff = False
        user.is_superuser = False
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = "premium"
        profile.phone = "2222222222"
        profile.country = "Cyprus"
        profile.save()

        self.ensure_active_premium_subscription(user)
        self.ensure_cart(user)

    def create_manager_user(self):
        """Create the manager account with in-site management access only."""
        user, _ = User.objects.get_or_create(
            username="manageruser",
            defaults={"email": "manager@example.com"},
        )
        user.email = "manager@example.com"
        user.set_password("Manager123!")
        user.is_staff = False
        user.is_superuser = False
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = "manager"
        profile.phone = "4444444444"
        profile.country = "Greece"
        profile.save()

        self.deactivate_all_premium_subscriptions(user)
        self.ensure_cart(user)

    def create_admin_user(self):
        """Create the real Django superuser account."""
        user, _ = User.objects.get_or_create(
            username="adminuser",
            defaults={"email": "admin@example.com"},
        )
        user.email = "admin@example.com"
        user.set_password("Admin123!")
        user.is_staff = True
        user.is_superuser = True
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = "manager"
        profile.phone = "3333333333"
        profile.country = "Cyprus"
        profile.save()

        self.deactivate_all_premium_subscriptions(user)
        self.ensure_cart(user)

    def remove_old_test_user(self):
        """Delete the old test user if it still exists."""
        User.objects.filter(username="testuser").delete()