"""URL patterns for public, user, premium, and management dashboards."""

from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.public_dashboard, name="public-dashboard"),
    path("my-dashboard/", views.dashboard_router, name="dashboard-router"),
    path("dashboard/user/", views.user_dashboard, name="user-dashboard"),
    path("dashboard/premium/", views.premium_dashboard, name="premium-dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin-dashboard"),
]