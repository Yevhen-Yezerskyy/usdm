from django.db import migrations


TRANSLATIONS = {
    "site.menu": ("Меню", "Menü"),
    "site.primary_navigation": ("Основна навігація", "Hauptnavigation"),
}


def seed_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for key, (ukrainian, german) in TRANSLATIONS.items():
        source, _ = Source.objects.update_or_create(
            key=key,
            defaults={"source_text": ukrainian, "context": ""},
        )
        for language, translated_text in (("uk", ukrainian), ("de", german)):
            Value.objects.update_or_create(
                source=source,
                language=language,
                defaults={"translated_text": translated_text},
            )


def remove_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key__in=TRANSLATIONS).delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0008_contact_form_translations")]
    operations = [migrations.RunPython(seed_translations, remove_translations)]
