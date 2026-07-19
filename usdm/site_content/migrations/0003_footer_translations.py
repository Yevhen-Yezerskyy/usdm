from django.db import migrations


FOOTER_TRANSLATIONS = {
    "footer.tagline": (
        "КАРКАСНО-ПАНЕЛЬНІ БУДИНКИ",
        "КАРКАСНО-ПАНЕЛЬНІ БУДИНКИ",
        "HOLZRAHMEN-PANELHÄUSER",
    ),
    "footer.representative.germany": (
        "Представник у Німеччині",
        "Представник у Німеччині",
        "Vertretung in Deutschland",
    ),
    "footer.representative.sweden": (
        "Представник у Швеції",
        "Представник у Швеції",
        "Vertretung in Schweden",
    ),
    "footer.representative.iceland": (
        "Представник в Ісландії",
        "Представник в Ісландії",
        "Vertretung in Island",
    ),
    "footer.representative.france": (
        "Представник у Франції",
        "Представник у Франції",
        "Vertretung in Frankreich",
    ),
    "footer.copyright": (
        "© 2012 – 2025 ТОВ “ЮСДМ”",
        "© 2012 – 2025 ТОВ “ЮСДМ”",
        "© 2012 – 2025 TOV “USDM”",
    ),
    "footer.description": (
        "Модульні каркасно-панельні будинкі за модульною технологією, власне виробнитство дерев’яних будівельних конструкцій",
        "Модульні каркасно-панельні будинкі за модульною технологією, власне виробнитство дерев’яних будівельних конструкцій",
        "Modulare Holzrahmen-Panelhäuser in modularer Bauweise, eigene Herstellung von Holzbaukonstruktionen",
    ),
}


def seed_footer_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for key, (source_text, ukrainian, german) in FOOTER_TRANSLATIONS.items():
        source, _ = Source.objects.update_or_create(
            key=key,
            defaults={"source_text": source_text},
        )
        Value.objects.update_or_create(
            source=source,
            language="uk",
            defaults={"translated_text": ukrainian},
        )
        Value.objects.update_or_create(
            source=source,
            language="de",
            defaults={"translated_text": german},
        )


def remove_footer_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key__in=FOOTER_TRANSLATIONS).delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0002_match_original_navigation_labels")]
    operations = [
        migrations.RunPython(seed_footer_translations, remove_footer_translations),
    ]
