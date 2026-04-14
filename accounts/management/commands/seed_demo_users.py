from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from cart.models import Cart


class Command(BaseCommand):
    help = "Create or refresh demo users for testing"

    def handle(self, *args, **kwargs):
        self.create_regular_user()
        self.create_premium_user()
        self.create_admin_user()
        self.create_extra_user()
        self.stdout.write(self.style.SUCCESS("Demo users created or updated successfully."))

    def create_regular_user(self):
        user, _ = User.objects.get_or_create(
            username="regularuser",
            defaults={"email": "regular@example.com"}
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

        Cart.objects.get_or_create(user=user)

    def create_premium_user(self):
        user, _ = User.objects.get_or_create(
            username="premiumuser",
            defaults={"email": "premium@example.com"}
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

        Cart.objects.get_or_create(user=user)

    def create_admin_user(self):
        user, _ = User.objects.get_or_create(
            username="adminuser",
            defaults={"email": "admin@example.com"}
        )
        user.email = "admin@example.com"
        user.set_password("Admin123!")
        user.is_staff = True
        user.is_superuser = True
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = "premium"
        profile.phone = "3333333333"
        profile.country = "Cyprus"
        profile.save()

        Cart.objects.get_or_create(user=user)

    def create_extra_user(self):
        user, _ = User.objects.get_or_create(
            username="testuser",
            defaults={"email": "test@example.com"}
        )
        user.email = "test@example.com"
        user.set_password("Test123!")
        user.is_staff = False
        user.is_superuser = False
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = "user"
        profile.phone = "4444444444"
        profile.country = "Greece"
        profile.save()

        Cart.objects.get_or_create(user=user)