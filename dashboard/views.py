"""Views for public, user, premium, and management dashboards."""

from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.utils import timezone
from accounts.models import PremiumSubscription
from cart.models import Cart, Order
from catalog.models import Category, Product, Wishlist
from reviews.models import Review

PRODUCT_NAME_MAX = 30
PRODUCT_SLUG_MAX = 35
PRODUCT_BRAND_MAX = 20
PRODUCT_COLOR_MAX = 25
PRODUCT_SIZE_MAX = 20
PRODUCT_DESCRIPTION_MAX = 1000

def sync_user_premium_role(user):
    """Keep role data aligned with subscriptions without overwriting manager users."""
    if user.is_superuser:
        return

    if user.profile.role == "manager":
        return

    has_active_subscription = user.premium_subscriptions.filter(is_active=True).exists()
    user.profile.role = "premium" if has_active_subscription else "user"
    user.profile.save()


def user_has_premium_access(user):
    """Return True for admins, managers, or users with an active premium subscription."""
    if user.is_superuser:
        return True

    if getattr(user.profile, "role", "") == "manager":
        return True

    return user.premium_subscriptions.filter(is_active=True).exists()


def user_has_management_access(user):
    """Return True for users allowed to access the in-site management dashboard."""
    return user.is_superuser or getattr(user.profile, "role", "") == "manager"


def build_unique_product_slug(value, exclude_product_id=None):
    """Create a unique slug for a product, optionally excluding the current product."""
    base_slug = slugify(value).strip("-") or "product"
    slug = base_slug
    counter = 2

    existing_products = Product.objects.all()
    if exclude_product_id is not None:
        existing_products = existing_products.exclude(id=exclude_product_id)

    while existing_products.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


def public_dashboard(request):
    """Render the public homepage with featured content and placeholder media."""
    featured_products = Product.objects.order_by("?")[:6]
    premium_highlights = Product.objects.filter(is_premium_only=True).order_by("name")[:3]

    def make_card_image(text, bg, fg="ffffff"):
        safe_text = text.replace(" ", "+")
        return f"https://placehold.co/900x900/{bg}/{fg}?text={safe_text}"

    driver_cards = [
        {"name": "George Russell", "team": "Mercedes", "image_url": make_card_image("George Russell", "111827")},
        {"name": "Kimi Antonelli", "team": "Mercedes", "image_url": make_card_image("Kimi Antonelli", "374151")},
        {"name": "Charles Leclerc", "team": "Ferrari", "image_url": make_card_image("Charles Leclerc", "b91c1c")},
        {"name": "Lewis Hamilton", "team": "Ferrari", "image_url": make_card_image("Lewis Hamilton", "dc2626")},
        {"name": "Lando Norris", "team": "McLaren", "image_url": make_card_image("Lando Norris", "ea580c")},
        {"name": "Oscar Piastri", "team": "McLaren", "image_url": make_card_image("Oscar Piastri", "f97316")},
        {"name": "Esteban Ocon", "team": "Haas F1 Team", "image_url": make_card_image("Esteban Ocon", "6b7280")},
        {"name": "Oliver Bearman", "team": "Haas F1 Team", "image_url": make_card_image("Oliver Bearman", "4b5563")},
        {"name": "Pierre Gasly", "team": "Alpine", "image_url": make_card_image("Pierre Gasly", "1d4ed8")},
        {"name": "Franco Colapinto", "team": "Alpine", "image_url": make_card_image("Franco Colapinto", "2563eb")},
        {"name": "Max Verstappen", "team": "Red Bull Racing", "image_url": make_card_image("Max Verstappen", "1e40af")},
        {"name": "Isack Hadjar", "team": "Red Bull Racing", "image_url": make_card_image("Isack Hadjar", "1d4ed8")},
        {"name": "Liam Lawson", "team": "Racing Bulls", "image_url": make_card_image("Liam Lawson", "0f172a")},
        {"name": "Arvid Lindblad", "team": "Racing Bulls", "image_url": make_card_image("Arvid Lindblad", "1e293b")},
        {"name": "Nico Hulkenberg", "team": "Audi", "image_url": make_card_image("Nico Hulkenberg", "166534")},
        {"name": "Gabriel Bortoleto", "team": "Audi", "image_url": make_card_image("Gabriel Bortoleto", "14532d")},
        {"name": "Carlos Sainz", "team": "Williams", "image_url": make_card_image("Carlos Sainz", "2563eb")},
        {"name": "Alexander Albon", "team": "Williams", "image_url": make_card_image("Alexander Albon", "1d4ed8")},
        {"name": "Fernando Alonso", "team": "Aston Martin", "image_url": make_card_image("Fernando Alonso", "065f46")},
        {"name": "Lance Stroll", "team": "Aston Martin", "image_url": make_card_image("Lance Stroll", "047857")},
        {"name": "Sergio Perez", "team": "Cadillac", "image_url": make_card_image("Sergio Perez", "7f1d1d")},
        {"name": "Valtteri Bottas", "team": "Cadillac", "image_url": make_card_image("Valtteri Bottas", "991b1b")},
    ]

    team_cards = [
        {"name": "Mercedes", "image_url": make_card_image("Mercedes", "111827")},
        {"name": "Ferrari", "image_url": make_card_image("Ferrari", "b91c1c")},
        {"name": "McLaren", "image_url": make_card_image("McLaren", "ea580c")},
        {"name": "Haas F1 Team", "image_url": make_card_image("Haas F1 Team", "4b5563")},
        {"name": "Alpine", "image_url": make_card_image("Alpine", "1d4ed8")},
        {"name": "Red Bull Racing", "image_url": make_card_image("Red Bull Racing", "1e40af")},
        {"name": "Racing Bulls", "image_url": make_card_image("Racing Bulls", "0f172a")},
        {"name": "Audi", "image_url": make_card_image("Audi", "166534")},
        {"name": "Williams", "image_url": make_card_image("Williams", "2563eb")},
        {"name": "Cadillac", "image_url": make_card_image("Cadillac", "7f1d1d")},
        {"name": "Aston Martin", "image_url": make_card_image("Aston Martin", "065f46")},
    ]

    context = {
        "featured_products": featured_products,
        "premium_highlights": premium_highlights,
        "driver_cards": driver_cards,
        "team_cards": team_cards,
    }
    return render(request, "dashboard/public_dashboard.html", context)


@login_required
def dashboard_router(request):
    """Send users to the correct dashboard based on access level."""
    if user_has_management_access(request.user):
        return redirect("dashboard:admin-dashboard")

    sync_user_premium_role(request.user)

    if user_has_premium_access(request.user):
        return redirect("dashboard:premium-dashboard")

    return redirect("dashboard:user-dashboard")


@login_required
def user_dashboard(request):
    """Render the normal user dashboard."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    recent_orders = request.user.orders.prefetch_related("items__product").order_by("-created_at")[:3]
    recent_order_count = request.user.orders.count()
    recently_viewed = request.user.recent_views.select_related("product", "product__category")[:6]

    context = {
        "cart": cart,
        "cart_items": cart.items.select_related("product"),
        "cart_items_count": cart.items.count(),
        "recent_orders": recent_orders,
        "recent_order_count": recent_order_count,
        "recently_viewed": recently_viewed,
        "wishlist_count": wishlist.products.count(),
    }
    return render(request, "dashboard/user_dashboard.html", context)


@login_required
def premium_dashboard(request):
    """Render the premium member dashboard."""
    if user_has_management_access(request.user):
        return redirect("dashboard:admin-dashboard")

    sync_user_premium_role(request.user)

    if not user_has_premium_access(request.user):
        return redirect("dashboard:user-dashboard")

    cart, _ = Cart.objects.get_or_create(user=request.user)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    active_subscription = request.user.premium_subscriptions.filter(is_active=True).order_by("-started_at").first()
    premium_products = Product.objects.filter(is_premium_only=True).order_by("name")[:6]
    recent_orders = request.user.orders.prefetch_related("items__product").order_by("-created_at")[:3]
    recently_viewed = request.user.recent_views.select_related("product", "product__category")[:6]
    discount_rewards = request.user.discount_rewards.filter(is_used=False).order_by("-created_at")[:5]
    raffle_entries = request.user.raffle_entries.order_by("-created_at")[:5]
    raffle_entries_count = request.user.raffle_entries.count()
    joined_raffles_count = request.user.raffle_entries.filter(status="joined").count()
    won_raffles_count = request.user.raffle_entries.filter(status="won").count()

    context = {
        "cart": cart,
        "cart_items_count": cart.items.count(),
        "wishlist_count": wishlist.products.count(),
        "active_subscription": active_subscription,
        "premium_products": premium_products,
        "recent_orders": recent_orders,
        "recently_viewed": recently_viewed,
        "discount_rewards": discount_rewards,
        "raffle_entries": raffle_entries,
        "raffle_entries_count": raffle_entries_count,
        "joined_raffles_count": joined_raffles_count,
        "won_raffles_count": won_raffles_count,
    }
    return render(request, "dashboard/premium_dashboard.html", context)


def validate_product_text_lengths(name, slug_value, description, brand, color, size, external_image_url):
    if len(name) > PRODUCT_NAME_MAX:
        raise ValueError(f"Product name must be at most {PRODUCT_NAME_MAX} characters.")

    if len(slug_value) > PRODUCT_SLUG_MAX:
        raise ValueError(f"Slug must be at most {PRODUCT_SLUG_MAX} characters.")

    if len(description) > PRODUCT_DESCRIPTION_MAX:
        raise ValueError(f"Description must be at most {PRODUCT_DESCRIPTION_MAX} characters.")

    if len(brand) > PRODUCT_BRAND_MAX:
        raise ValueError(f"Brand must be at most {PRODUCT_BRAND_MAX} characters.")

    if len(color) > PRODUCT_COLOR_MAX:
        raise ValueError(f"Color must be at most {PRODUCT_COLOR_MAX} characters.")

    if len(size) > PRODUCT_SIZE_MAX:
        raise ValueError(f"Size must be at most {PRODUCT_SIZE_MAX} characters.")

@login_required
def admin_dashboard(request):
    """Render the in-site management dashboard for superusers and managers."""
    if not user_has_management_access(request.user):
        return redirect("dashboard:dashboard-router")

    if request.method == "POST":
        action = request.POST.get("action", "").strip()

        if action == "add_product":
            try:
                name = request.POST.get("name", "").strip()
                slug_input = request.POST.get("slug", "").strip()
                description = request.POST.get("description", "").strip()
                category = get_object_or_404(Category, id=request.POST.get("category_id"))
                brand = request.POST.get("brand", "").strip()
                color = request.POST.get("color", "").strip()
                size = request.POST.get("size", "").strip()
                price = Decimal(request.POST.get("price", "0"))
                stock = max(0, int(request.POST.get("stock", "0")))
                external_image_url = request.POST.get("external_image_url", "").strip()
                is_premium_only = request.POST.get("is_premium_only") == "on"

                if not name or not description:
                    messages.error(request, "Name and description are required.")
                    return redirect("dashboard:admin-dashboard")

                slug_value = build_unique_product_slug(slug_input or name, exclude_product_id=None)

                validate_product_text_lengths(
                    name=name,
                    slug_value=slug_value,
                    description=description,
                    brand=brand,
                    color=color,
                    size=size,
                )

                product = Product.objects.create(
                    category=category,
                    name=name,
                    slug=slug_value,
                    description=description,
                    brand=brand,
                    color=color,
                    size=size,
                    price=price,
                    stock=stock,
                    is_premium_only=is_premium_only,
                    external_image_url=external_image_url,
                )

                uploaded_image = request.FILES.get("image")
                if uploaded_image:
                    product.image = uploaded_image
                    product.save()

                messages.success(request, f"Product '{product.name}' added successfully.")
            except (InvalidOperation, ValueError):
                messages.error(request, "Invalid product values provided.")

            return redirect("dashboard:admin-dashboard")

        if action == "update_product":
            product = get_object_or_404(Product, id=request.POST.get("product_id"))

            try:
                name = request.POST.get("name", "").strip()
                slug_input = request.POST.get("slug", "").strip()
                description = request.POST.get("description", "").strip()
                category = get_object_or_404(Category, id=request.POST.get("category_id"))
                brand = request.POST.get("brand", "").strip()
                color = request.POST.get("color", "").strip()
                size = request.POST.get("size", "").strip()
                price = Decimal(request.POST.get("price", "0"))
                stock = max(0, int(request.POST.get("stock", "0")))
                external_image_url = request.POST.get("external_image_url", "").strip()

                is_premium_only = request.POST.get("is_premium_only", "0") == "1"
                clear_image = request.POST.get("clear_image", "0") == "1"
                uploaded_image = request.FILES.get("image")

                if not name or not description:
                    messages.error(request, "Name and description are required.")
                    return redirect("dashboard:admin-dashboard")

                slug_value = build_unique_product_slug(slug_input or name, exclude_product_id=product.id)

                validate_product_text_lengths(
                    name=name,
                    slug_value=slug_value,
                    description=description,
                    brand=brand,
                    color=color,
                    size=size,
                )

                product.name = name
                product.slug = build_unique_product_slug(slug_input or name, exclude_product_id=product.id)
                product.category = category
                product.description = description
                product.brand = brand
                product.color = color
                product.size = size
                product.price = price
                product.stock = stock
                product.external_image_url = external_image_url
                product.is_premium_only = is_premium_only

                if clear_image and product.image:
                    product.image.delete(save=False)
                    product.image = None

                if uploaded_image:
                    if product.image:
                        product.image.delete(save=False)
                    product.image = uploaded_image

                product.save()
                messages.success(request, f"Product '{product.name}' updated successfully.")
            except (InvalidOperation, ValueError) as error:
                messages.error(request, str(error) or "Invalid product values provided.")

            return redirect("dashboard:admin-dashboard")

        if action == "delete_product":
            product = get_object_or_404(Product, id=request.POST.get("product_id"))
            product_name = product.name
            product.delete()
            messages.success(request, f"Product '{product_name}' deleted successfully.")
            return redirect("dashboard:admin-dashboard")

        if action == "change_user_role":
            managed_user = get_object_or_404(
                User.objects.select_related("profile"),
                id=request.POST.get("user_id"),
            )
            new_role = request.POST.get("role", "").strip()

            valid_roles = {choice[0] for choice in managed_user.profile.ROLE_CHOICES}

            if managed_user == request.user:
                messages.error(request, "You cannot change your own role from the management dashboard.")
                return redirect("dashboard:admin-dashboard")

            if managed_user.is_superuser:
                messages.error(request, "Superuser roles cannot be changed from this page.")
                return redirect("dashboard:admin-dashboard")

            if new_role not in valid_roles:
                messages.error(request, "Invalid role selected.")
                return redirect("dashboard:admin-dashboard")

            if new_role == "premium":
                has_active_subscription = managed_user.premium_subscriptions.filter(is_active=True).exists()
                if not has_active_subscription:
                    PremiumSubscription.objects.create(
                        user=managed_user,
                        plan_name="Premium Membership",
                        price=15.00,
                        is_active=True,
                    )
                managed_user.profile.role = "premium"

            elif new_role == "user":
                managed_user.premium_subscriptions.filter(is_active=True).update(
                    is_active=False,
                    ended_at=timezone.now(),
                )
                managed_user.profile.role = "user"

            elif new_role == "manager":
                managed_user.premium_subscriptions.filter(is_active=True).update(
                    is_active=False,
                    ended_at=timezone.now(),
                )
                managed_user.profile.role = "manager"

            managed_user.profile.save()
            messages.success(request, f"Role for '{managed_user.username}' updated to {new_role}.")
            return redirect("dashboard:admin-dashboard")

        if action == "delete_user":
            managed_user = get_object_or_404(User.objects.select_related("profile"), id=request.POST.get("user_id"))

            if managed_user == request.user:
                messages.error(request, "You cannot delete your own account from the management dashboard.")
                return redirect("dashboard:admin-dashboard")

            if managed_user.is_superuser:
                messages.error(request, "Superuser accounts cannot be deleted from this page.")
                return redirect("dashboard:admin-dashboard")

            username = managed_user.username
            managed_user.delete()
            messages.success(request, f"User '{username}' deleted successfully.")
            return redirect("dashboard:admin-dashboard")

        if action == "delete_order":
            order = get_object_or_404(Order, id=request.POST.get("order_id"))
            order_id = order.id
            order.delete()
            messages.success(request, f"Order #{order_id} deleted successfully.")
            return redirect("dashboard:admin-dashboard")

    premium_user_count = (
        PremiumSubscription.objects.filter(is_active=True)
        .values("user")
        .distinct()
        .count()
    )

    managed_users = (
        User.objects.select_related("profile")
        .filter(is_superuser=False)
        .order_by("username")
    )

    managed_products = Product.objects.select_related("category", "category__parent").order_by("name")
    all_orders = Order.objects.select_related("user").prefetch_related("items__product").order_by("-created_at")
    categories = Category.objects.select_related("parent").order_by("name")

    context = {
        "total_users": User.objects.filter(is_superuser=False).count(),
        "premium_users": premium_user_count,
        "total_products": Product.objects.count(),
        "premium_products": Product.objects.filter(is_premium_only=True).count(),
        "total_orders": Order.objects.count(),
        "total_reviews": Review.objects.count(),
        "latest_orders": all_orders[:5],
        "all_orders": all_orders,
        "managed_users": managed_users,
        "managed_products": managed_products,
        "categories": categories,
        "can_open_django_admin": request.user.is_superuser,
    }
    return render(request, "dashboard/admin_dashboard.html", context)