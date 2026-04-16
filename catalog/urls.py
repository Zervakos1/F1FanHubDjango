"""URL patterns for catalogue pages and wishlist actions."""

from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.product_list, name="product-list"),
    path("wishlist/", views.wishlist_detail, name="wishlist-detail"),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add-to-wishlist"),
    path("wishlist/remove/<int:product_id>/", views.remove_from_wishlist, name="remove-from-wishlist"),
    path("<slug:slug>/", views.product_detail, name="product-detail"),
]