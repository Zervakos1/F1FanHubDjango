"""Application configuration for the accounts app."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Register the accounts app and load its signals when ready."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        """Import signals so post-save hooks are registered."""
        import accounts.signals