from django.db import migrations


LABELS = {
    "site.1": ("Home", "Home", "Startseite"),
    "site.2": ("Технології", "Технології", "Technologie"),
    "site.5": ("Контакт", "Контакт", "Kontakt"),
}


def update_navigation_labels(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for key, (source_text, ukrainian, german) in LABELS.items():
        source = Source.objects.get(key=key)
        source.source_text = source_text
        source.save(update_fields=("source_text",))
        Value.objects.filter(source=source, language="uk").update(translated_text=ukrainian)
        Value.objects.filter(source=source, language="de").update(translated_text=german)


class Migration(migrations.Migration):
    dependencies = [("site_content", "0001_initial")]
    operations = [
        migrations.RunPython(update_navigation_labels, migrations.RunPython.noop),
    ]
