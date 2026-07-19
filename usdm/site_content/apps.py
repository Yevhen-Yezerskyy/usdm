from django.apps import AppConfig


class SiteContentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "site_content"

    def ready(self):
        from .runtime_translation import install_runtime_translation

        install_runtime_translation()
