"""Database models for catalogue data such as categories, products, and wishlists."""

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Represent a product category or subcategory."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    def __str__(self):
        """Return the category name."""
        return self.name


class Product(models.Model):
    """Store product information shown in the catalogue."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    brand = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=20, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_premium_only = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    external_image_url = models.URLField(blank=True)

    def __str__(self):
        """Return the product name."""
        return self.name


class RecentlyViewed(models.Model):
    """Track the products each user has recently opened."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recent_views")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="viewed_by")
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-viewed_at"]
        unique_together = ("user", "product")

    def __str__(self):
        """Return a readable recently viewed entry."""
        return f"{self.user.username} viewed {self.product.name}"


class Wishlist(models.Model):
    """Store products that a user wants to save for later."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(Product, blank=True, related_name="wishlisted_by")

    def __str__(self):
        """Return a readable wishlist label."""
        return f"Wishlist - {self.user.username}"