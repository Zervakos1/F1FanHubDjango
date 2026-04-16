"""Admin configuration for cart and order models."""

from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    """Show cart items directly inside the cart admin page."""

    model = CartItem
    extra = 0


class OrderItemInline(admin.TabularInline):
    """Show order items directly inside the order admin page."""

    model = OrderItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin options for user carts."""

    list_display = ["user", "updated_at"]
    search_fields = ["user__username", "user__email"]
    inlines = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin options for simulated orders."""

    list_display = ["id", "user", "status", "total_amount", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "user__email"]
    inlines = [OrderItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin options for cart items."""

    list_display = ["cart", "product", "quantity"]
    list_filter = ["product"]
    search_fields = ["cart__user__username", "product__name"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin options for order items."""

    list_display = ["order", "product", "quantity", "price_at_purchase"]
    list_filter = ["product"]
    search_fields = ["order__user__username", "product__name"]