from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, RecentlyViewed, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent"]
    list_filter = ["parent"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["image_preview", "name", "category", "brand", "price", "stock", "is_premium_only"]
    list_filter = ["category", "brand", "is_premium_only"]
    search_fields = ["name", "brand", "description", "slug"]
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "category", "description")
        }),
        ("Product Details", {
            "fields": ("brand", "color", "size", "price", "stock", "is_premium_only")
        }),
        ("Images", {
            "fields": ("image", "external_image_url")
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        if obj.external_image_url:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.external_image_url
            )
        return "No image"

    image_preview.short_description = "Image"


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "viewed_at"]
    list_filter = ["viewed_at"]
    search_fields = ["user__username", "product__name"]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__username", "user__email"]
    filter_vertical = ["products"]