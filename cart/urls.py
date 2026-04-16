"""URL patterns for cart, checkout, and order history pages."""

from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart-detail"),
    path("add/<int:product_id>/", views.add_to_cart, name="add-to-cart"),
    path("update/<int:item_id>/", views.update_cart_item, name="update-cart-item"),
    path("remove/<int:item_id>/", views.remove_cart_item, name="remove-cart-item"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_history, name="order-history"),
]