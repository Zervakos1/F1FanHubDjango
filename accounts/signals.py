"""Signals that create related user data when a new account is created."""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Cart
from catalog.models import Wishlist
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    """Create the related profile, cart, and wishlist for each new user."""
    if created:
        Profile.objects.create(user=instance)
        Cart.objects.create(user=instance)
        Wishlist.objects.create(user=instance)