from django.db import migrations


TRANSLATIONS = [
    (
        "Сайт використовує необхідні cookie-файли: usdm_language запам’ятовує обрану українську або німецьку версію, csrftoken захищає контактну форму від підроблених запитів, usdm_contact_session протягом двох годин підтверджує, що форму відкрито у браузері, а usdm_cookie_consent_v2 зберігає ваш вибір для категорій «необхідні», «статистика» та «зовнішні медіа». Решта цих cookie діє до одного року. Після надсилання форми cookie sessionid тимчасово, не довше 10 хвилин, зберігає результат надсилання або повідомлення про помилки. Усі cookie можна видалити в налаштуваннях браузера.",
        "Die Website verwendet notwendige Cookies: usdm_language speichert die gewählte ukrainische oder deutsche Sprachversion, csrftoken schützt das Kontaktformular vor gefälschten Anfragen, usdm_contact_session bestätigt zwei Stunden lang, dass das Formular in einem Browser geöffnet wurde, und usdm_cookie_consent_v2 speichert Ihre Auswahl für die Kategorien „Notwendig“, „Statistik“ und „Externe Medien“. Die übrigen Cookies können bis zu einem Jahr gespeichert werden. Nach dem Absenden des Formulars speichert sessionid für höchstens zehn Minuten den Versandstatus oder Fehlermeldungen. Alle Cookies können in den Browsereinstellungen gelöscht werden.",
    ),
    (
        "На сайті немає систем вебаналітики, рекламних пікселів, профілювання, маркетингових cookie або зовнішніх медіасервісів. Панель однаково показує стандартний вибір «Статистика» та «Зовнішні медіа», але зараз ці категорії не активують жодних ресурсів і не передають дані стороннім постачальникам. Якщо ми підключимо такі сервіси, то оновимо цю політику та застосуємо збережений вами вибір.",
        "Auf dieser Website werden derzeit keine Webanalyse, Werbepixel, Profilbildung, Marketing-Cookies oder externen Mediendienste eingesetzt. Das Auswahlfenster zeigt dennoch einheitlich die Standardoptionen „Statistik“ und „Externe Medien“. Derzeit aktivieren diese Kategorien keine Ressourcen und übermitteln keine Daten an Drittanbieter. Sollten wir solche Dienste einbinden, aktualisieren wir diese Erklärung und wenden Ihre gespeicherte Auswahl an.",
    ),
]


def seed_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for index, (ukrainian, german) in enumerate(TRANSLATIONS, start=1):
        source, _ = Source.objects.update_or_create(
            key=f"cookie.standard.v2.{index}",
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
    Source.objects.filter(key__startswith="cookie.standard.v2.").delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0014_contact_bot_protection_translation")]
    operations = [migrations.RunPython(seed_translations, remove_translations)]
