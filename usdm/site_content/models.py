from django.conf import settings
from django.db import models


class TranslationSource(models.Model):
    key = models.CharField(max_length=160, unique=True)
    source_text = models.TextField()
    context = models.CharField(max_length=160, blank=True)

    class Meta:
        db_table = "translation_sources"
        ordering = ("key",)

    def __str__(self):
        return self.key


class TranslationValue(models.Model):
    source = models.ForeignKey(
        TranslationSource,
        related_name="values",
        on_delete=models.CASCADE,
    )
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)
    translated_text = models.TextField()

    class Meta:
        db_table = "translation_values"
        constraints = [
            models.UniqueConstraint(
                fields=("source", "language"),
                name="translation_value_source_language_unique",
            ),
        ]
        ordering = ("source__key", "language")

    def __str__(self):
        return f"{self.source.key}:{self.language}"


class ContactRequest(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=80)
    message = models.TextField()
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact_requests"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.first_name} — {self.created_at:%Y-%m-%d %H:%M}"


class ContactAttachment(models.Model):
    request = models.ForeignKey(
        ContactRequest,
        related_name="attachments",
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to="contact/%Y/%m/")
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=160, blank=True)
    size = models.PositiveBigIntegerField()

    class Meta:
        db_table = "contact_attachments"
        ordering = ("id",)

    def __str__(self):
        return self.original_name
