from django.db import migrations, models
import django.db.models.deletion


TRANSLATIONS = {
    "Головна": "Startseite",
    "Технологія": "Technologie",
    "Будинки": "Häuser",
    "Досвід": "Erfahrung",
    "Контакти": "Kontakt",
    "Імпресум": "Impressum",
    "Конфіденційність": "Datenschutz",
    "Сторінка готується": "Seite wird vorbereitet",
}


def seed_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for index, (ukrainian, german) in enumerate(TRANSLATIONS.items(), start=1):
        source = Source.objects.create(
            key=f"site.{index}",
            source_text=ukrainian,
        )
        Value.objects.bulk_create(
            [
                Value(source=source, language="uk", translated_text=ukrainian),
                Value(source=source, language="de", translated_text=german),
            ]
        )


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="TranslationSource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=160, unique=True)),
                ("source_text", models.TextField()),
                ("context", models.CharField(blank=True, max_length=160)),
            ],
            options={"db_table": "translation_sources", "ordering": ("key",)},
        ),
        migrations.CreateModel(
            name="TranslationValue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language", models.CharField(choices=[("uk", "Українська"), ("de", "Deutsch")], max_length=10)),
                ("translated_text", models.TextField()),
                ("source", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="values", to="site_content.translationsource")),
            ],
            options={"db_table": "translation_values", "ordering": ("source__key", "language")},
        ),
        migrations.AddConstraint(
            model_name="translationvalue",
            constraint=models.UniqueConstraint(fields=("source", "language"), name="translation_value_source_language_unique"),
        ),
        migrations.RunPython(seed_translations, migrations.RunPython.noop),
    ]
