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
