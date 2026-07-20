from django.db import migrations


HOME_TRANSLATIONS = {
    "home.hero.title": (
        "ВИРОБНИЦТВО КАРКАСНО-ПАНЕЛЬНИХ БУДИНКІВ",
        "ВИРОБНИЦТВО КАРКАСНО-ПАНЕЛЬНИХ БУДИНКІВ",
        "HERSTELLUNG VON HOLZRAHMEN-PANELHÄUSERN",
    ),
    "home.hero.export": (
        "ЕКСПОРТ БУДІВЕЛЬНИХ КОМПЛЕКТІВ",
        "ЕКСПОРТ БУДІВЕЛЬНИХ КОМПЛЕКТІВ",
        "EXPORT VON BAUSÄTZEN",
    ),
    "home.hero.experience": (
        "10 РОКІВ ДОСВІДУ",
        "10 РОКІВ ДОСВІДУ",
        "10 JAHRE ERFAHRUNG",
    ),
    "home.production.heading": (
        "ВИРОБНИЦТВО ТА ЕКСПОРТ",
        "ВИРОБНИЦТВО ТА ЕКСПОРТ",
        "PRODUKTION UND EXPORT",
    ),
    "home.production.title": (
        "Префабриковані каркасно-панельні дерев’яні будівельні комплекти",
        "Префабриковані каркасно-панельні дерев’яні будівельні комплекти",
        "Vorgefertigte Holzrahmen-Panel-Bausätze",
    ),
    "home.production.body": (
        "Виробництво будівельних комплектів для каркасно-панельних будинків. Дерев’яний несучий каркас, багатошарові панелі зовнішніх та внутрішніх стін, перегородок, покрівлі, перекриття, підлоги, ферми або покриття. Виробництво здійснюється на автоматизованій лінії WEINMANN.",
        "Виробництво будівельних комплектів для каркасно-панельних будинків. Дерев’яний несучий каркас, багатошарові панелі зовнішніх та внутрішніх стін, перегородок, покрівлі, перекриття, підлоги, ферми або покриття. Виробництво здійснюється на автоматизованій лінії WEINMANN.",
        "Herstellung von Bausätzen für Holzrahmen-Panelhäuser. Tragender Holzrahmen, mehrschichtige Paneele für Außen- und Innenwände, Trennwände, Dach, Geschossdecken, Boden, Binder oder Dachtragwerk. Die Produktion erfolgt auf einer automatisierten WEINMANN-Linie.",
    ),
    "home.houses.title": (
        "Каркасно-панельні будинки та споруди",
        "Каркасно-панельні будинки та споруди",
        "Holzrahmen-Panelhäuser und Bauwerke",
    ),
    "home.houses.body": (
        "Будівництво за модульною технологією. Виробництво готових модульних будинків в цеху, доставка та монтаж. Будинки виробляються з різним ступенем готовності та комплектації – від зовнішнього оздоблення до повністю готового будинку.",
        "Будівництво за модульною технологією. Виробництво готових модульних будинків в цеху, доставка та монтаж. Будинки виробляються з різним ступенем готовності та комплектації – від зовнішнього оздоблення до повністю готового будинку.",
        "Bauen in modularer Bauweise. Herstellung fertiger modularer Häuser in der Werkhalle, Lieferung und Montage. Die Häuser werden in unterschiedlichen Ausbau- und Ausstattungsgraden gefertigt – von der Außenverkleidung bis zum schlüsselfertigen Haus.",
    ),
    "home.download": (
        "ЗАВАНТАЖИТИ ПРЕЗЕНТАЦІЮ",
        "ЗАВАНТАЖИТИ ПРЕЗЕНТАЦІЮ",
        "PRÄSENTATION HERUNTERLADEN",
    ),
    "home.details": (
        "ДОКЛАДНІШЕ",
        "ДОКЛАДНІШЕ",
        "MEHR ERFAHREN",
    ),
}


def seed_home_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for key, (source_text, ukrainian, german) in HOME_TRANSLATIONS.items():
        source, _ = Source.objects.update_or_create(
            key=key,
            defaults={"source_text": source_text},
        )
        for language, translated_text in (("uk", ukrainian), ("de", german)):
            Value.objects.update_or_create(
                source=source,
                language=language,
                defaults={"translated_text": translated_text},
            )


def remove_home_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key__in=HOME_TRANSLATIONS).delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0003_footer_translations")]
    operations = [migrations.RunPython(seed_home_translations, remove_home_translations)]
