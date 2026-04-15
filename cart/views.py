from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.models import DiscountReward
from catalog.models import Product
from .models import Cart, CartItem, Order, OrderItem


def user_has_premium_access(user):
    # Premium access is granted to admins or users with an active premium subscription.
    if user.is_superuser:
        return True
    return user.premium_subscriptions.filter(is_active=True).exists()


def get_user_cart(user):
    # Ensure every authenticated user has a cart.
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    cart = get_user_cart(request.user)
    items = cart.items.select_related("product")
    return render(
        request,
        "cart/cart_detail.html",
        {
            "cart": cart,
            "items": items,
        },
    )


@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("catalog:product-list")

    product = get_object_or_404(Product, id=product_id)

    if product.is_premium_only and not user_has_premium_access(request.user):
        messages.error(
            request,
            "This item is available only for users with an active premium subscription.",
        )
        return redirect("catalog:product-detail", slug=product.slug)

    quantity = int(request.POST.get("quantity", 1))
    if quantity < 1:
        quantity = 1

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    if cart_item.quantity > product.stock:
        cart_item.quantity = product.stock

    cart_item.save()
    messages.success(request, "Item added to cart.")
    return redirect("cart:cart-detail")


@login_required
def update_cart_item(request, item_id):
    if request.method != "POST":
        return redirect("cart:cart-detail")

    cart_item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
    quantity = int(request.POST.get("quantity", 1))

    if quantity <= 0:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        if quantity > cart_item.product.stock:
            quantity = cart_item.product.stock
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated.")

    return redirect("cart:cart-detail")


@login_required
def remove_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect("cart:cart-detail")


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related("product")

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart:cart-detail")

    blocked_items = [
        item
        for item in cart_items
        if item.product.is_premium_only and not user_has_premium_access(request.user)
    ]

    if blocked_items:
        messages.error(
            request,
            "Your cart contains premium-only items. Activate premium to continue or remove those items.",
        )
        return redirect("cart:cart-detail")

    active_discount = request.user.discount_rewards.filter(is_used=False).order_by("-created_at").first()
    discount_amount = Decimal("0.00")
    reward_name = ""

    if active_discount:
        discount_amount = active_discount.discount_amount
        reward_name = active_discount.name

        if discount_amount > cart.total_price:
            discount_amount = cart.total_price

    final_total = cart.total_price - discount_amount

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            status="completed",
            total_amount=final_total,
            discount_applied=discount_amount,
            reward_name=reward_name,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price,
            )

            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
                item.product.save()

        if active_discount:
            active_discount.is_used = True
            active_discount.used_at = timezone.now()
            active_discount.save()

        if user_has_premium_access(request.user):
            earned_points = int(final_total)
            request.user.profile.premium_points += earned_points
            request.user.profile.lifetime_points += earned_points
            request.user.profile.save()
            messages.success(request, f"Purchase completed. You earned {earned_points} premium points.")
        else:
            messages.success(request, f"Purchase simulated successfully. Order #{order.id} created.")

        cart.items.all().delete()
        return redirect("cart:order-history")

    return render(
        request,
        "cart/checkout.html",
        {
            "cart": cart,
            "items": cart_items,
            "active_discount": active_discount,
            "discount_amount": discount_amount,
            "final_total": final_total,
        },
    )


@login_required
def order_history(request):
    orders = request.user.orders.prefetch_related("items__product").order_by("-created_at")
    return render(
        request,
        "cart/order_history.html",
        {
            "orders": orders,
        },
    )