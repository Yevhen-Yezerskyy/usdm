from django.db import migrations


FORM_TRANSLATIONS = {
    "contact.form.success": (
        "Дякуємо, ваш запит відправлено. Ми зв’яжемося з Вами найближчим часом.",
        "Vielen Dank, Ihre Anfrage wurde gesendet. Wir melden uns in Kürze bei Ihnen.",
    ),
    "contact.form.error": (
        "Перевірте, будь ласка, обов’язкові поля та адресу електронної пошти.",
        "Bitte prüfen Sie die Pflichtfelder und die E-Mail-Adresse.",
    ),
}


def seed_form_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for key, (ukrainian, german) in FORM_TRANSLATIONS.items():
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


def remove_form_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key__in=FORM_TRANSLATIONS).delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0007_contact_request")]
    operations = [migrations.RunPython(seed_form_translations, remove_form_translations)]
