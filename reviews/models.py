"""Database models for product reviews."""

from django.contrib.auth.models import User
from django.db import models

from catalog.models import Product


class Review(models.Model):
    """Store one review per user for a specific product."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"],
                name="unique_review_per_user_product",
            )
        ]

    def __str__(self):
        """Return a readable review label for admin and debugging."""
        return f"{self.user.username} - {self.product.name}"