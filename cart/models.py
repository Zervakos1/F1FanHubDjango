"""Database models for cart, cart items, orders, and order items."""

from django.contrib.auth.models import User
from django.db import models

from catalog.models import Product


class Cart(models.Model):
    """Store the current active shopping cart for a user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable cart label."""
        return f"Cart - {self.user.username}"

    @property
    def total_price(self):
        """Calculate the current total price of all cart items."""
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    """Store one product entry inside a cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        """Return a readable cart item label."""
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        """Calculate the subtotal for this cart line."""
        return self.product.price * self.quantity


class Order(models.Model):
    """Store a simulated order created during checkout."""

    STATUS_CHOICES = [
        ("placed", "Placed"),
        ("completed", "Completed"),
    ]

    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reward_name = models.CharField(max_length=100, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        """Return a readable order label."""
        return f"Order #{self.id} - {self.user.username}"

    @property
    def total_items(self):
        """Count the total quantity of all items in the order."""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """Store one purchased product line inside an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Return a readable order item label."""
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        """Calculate the subtotal for this order line."""
        return self.quantity * self.price_at_purchase