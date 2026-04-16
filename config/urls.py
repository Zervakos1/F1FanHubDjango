"""
Main URL configuration for the project.

This file connects:
- the Django admin site
- each feature app through namespaced includes
- simple static pages like About, Contact, and FAQ

Using namespaces allows templates and redirects to use the pattern:
'appname:viewname'
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # Django admin panel.
    path("admin/", admin.site.urls),

    # Dashboard routes, including the empty root path for the homepage.
    path("", include(("dashboard.urls", "dashboard"), namespace="dashboard")),

    # Feature app routes.
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("catalog/", include(("catalog.urls", "catalog"), namespace="catalog")),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("reviews/", include(("reviews.urls", "reviews"), namespace="reviews")),

    # Simple template-based informational pages.
    path("about/", TemplateView.as_view(template_name="about/about.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="contact/contact.html"), name="contact"),
    path("faq/", TemplateView.as_view(template_name="faq/faq.html"), name="faq"),
]

# Serve uploaded media files locally only when DEBUG is enabled.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)