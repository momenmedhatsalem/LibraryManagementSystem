from django.apps import AppConfig


class BorrowConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrow"

    def ready(self):
        import borrow.signals  # Import signals when the app is ready
