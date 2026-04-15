from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import render, get_object_or_404, redirect

from reviews.models import Review
from .models import Product, Category, RecentlyViewed, Wishlist


def product_list(request):
    # Product catalogue with search and filter support.
    products = Product.objects.select_related("category", "category__parent").all().order_by("name")
    parent_categories = Category.objects.filter(parent__isnull=True).prefetch_related("subcategories").order_by("name")

    q = request.GET.get("q", "").strip()
    brand = request.GET.get("brand", "").strip()
    color = request.GET.get("color", "").strip()
    size = request.GET.get("size", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    category_slug = request.GET.get("category", "").strip()

    selected_category = None

    if q:
        products = products.filter(name__icontains=q)

    if brand:
        products = products.filter(brand__icontains=brand)

    if color:
        products = products.filter(color__icontains=color)

    if size:
        products = products.filter(size__icontains=size)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()

        if selected_category:
            if selected_category.parent is None:
                child_ids = selected_category.subcategories.values_list("id", flat=True)
                products = products.filter(Q(category=selected_category) | Q(category_id__in=child_ids))
            else:
                products = products.filter(category=selected_category)

    context = {
        "products": products,
        "parent_categories": parent_categories,
        "selected_category": selected_category,
    }
    return render(request, "catalog/product_list.html", context)


def product_detail(request, slug):
    # Detailed product page with recommendations, reviews, and wishlist state.
    product = get_object_or_404(
        Product.objects.select_related("category", "category__parent"),
        slug=slug,
    )

    has_premium_access = False
    is_in_wishlist = False

    if request.user.is_authenticated:
        has_premium_access = (
            request.user.is_superuser
            or request.user.premium_subscriptions.filter(is_active=True).exists()
        )

        RecentlyViewed.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={},
        )

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        is_in_wishlist = wishlist.products.filter(id=product.id).exists()

    reviews = product.reviews.select_related("user").order_by("-created_at")
    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    same_brand_same_category = Product.objects.filter(
        brand=product.brand,
        category=product.category,
    ).exclude(id=product.id)

    same_brand = Product.objects.filter(
        brand=product.brand
    ).exclude(id=product.id)

    if product.category.parent:
        same_group = Product.objects.filter(
            category__parent=product.category.parent
        ).exclude(id=product.id)
    else:
        same_group = Product.objects.filter(
            Q(category=product.category) | Q(category__parent=product.category)
        ).exclude(id=product.id)

    recommendations = []
    added_ids = set()

    for queryset in [same_brand_same_category, same_brand, same_group]:
        for item in queryset:
            if item.id not in added_ids:
                recommendations.append(item)
                added_ids.add(item.id)
            if len(recommendations) == 4:
                break
        if len(recommendations) == 4:
            break

    context = {
        "product": product,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1),
        "review_count": reviews.count(),
        "recommendations": recommendations,
        "is_in_wishlist": is_in_wishlist,
        "has_premium_access": has_premium_access,
    }
    return render(request, "catalog/product_detail.html", context)


@login_required
def wishlist_detail(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.select_related("category", "category__parent").order_by("name")
    return render(request, "catalog/wishlist.html", {"wishlist_products": products})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect("catalog:wishlist-detail")


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product)
    return redirect("catalog:wishlist-detail")