from django.db import migrations


OLD_UKRAINIAN = (
    "Відповідальним за обробку персональних даних на цьому сайті є Товариство з "
    "обмеженою відповідальністю «ЮСДМ». Контактні дані наведені поруч. З питань "
    "приватності напишіть нам на sb@usdm.com.ua."
)
NEW_UKRAINIAN = OLD_UKRAINIAN.replace("sb@usdm.com.ua", "info@usdm.com.ua")
OLD_GERMAN = (
    "Verantwortlicher für die Verarbeitung personenbezogener Daten auf dieser Website "
    "ist TOV „USDM“. Die Kontaktdaten finden Sie nebenstehend. Datenschutzanfragen "
    "richten Sie bitte an sb@usdm.com.ua."
)
NEW_GERMAN = OLD_GERMAN.replace("sb@usdm.com.ua", "info@usdm.com.ua")


def set_public_contact_email(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    source = Source.objects.filter(source_text=OLD_UKRAINIAN, context="").first()
    if source is None:
        source = Source.objects.filter(key="legal.v2.038").first()
    if source is None:
        source = Source.objects.create(
            key="legal.v2.038",
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


def restore_previous_contact_email(apps, schema_editor):
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
    dependencies = [("site_content", "0015_standard_cookie_consent_translation")]

    operations = [migrations.RunPython(set_public_contact_email, restore_previous_contact_email)]
