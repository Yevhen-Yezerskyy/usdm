from django.db import migrations


OLD_UKRAINIAN = "Бут Сергій Петрович"
NEW_UKRAINIAN = "Антон Трупак"
OLD_GERMAN = "Serhii Petrovych But"
NEW_GERMAN = "Anton Trupak"


def set_legal_manager(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    source = Source.objects.filter(source_text=OLD_UKRAINIAN, context="").first()
    if source is None:
        source = Source.objects.filter(key="legal.v2.011").first()
    if source is None:
        source = Source.objects.create(
            key="legal.v2.011",
            source_text=NEW_UKRAINIAN,
            context="",
        )
    else:
        source.source_text = NEW_UKRAINIAN
        source.save(update_fields=("source_text",))
    for language, text in (("uk", NEW_UKRAINIAN), ("de", NEW_GERMAN)):
        Value.objects.update_or_create(
            source=source,
            language=language,
            defaults={"translated_text": text},
        )


def restore_previous_legal_manager(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    source = Source.objects.filter(source_text=NEW_UKRAINIAN, context="").first()
    if source is None:
        return
    source.source_text = OLD_UKRAINIAN
    source.save(update_fields=("source_text",))
    for language, text in (("uk", OLD_UKRAINIAN), ("de", OLD_GERMAN)):
        Value.objects.update_or_create(
            source=source,
            language=language,
            defaults={"translated_text": text},
        )


class Migration(migrations.Migration):
    dependencies = [("site_content", "0016_public_contact_email")]

    operations = [migrations.RunPython(set_legal_manager, restore_previous_legal_manager)]
