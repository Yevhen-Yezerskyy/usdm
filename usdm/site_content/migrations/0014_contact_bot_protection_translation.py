from django.db import migrations


UKRAINIAN = "Сайт використовує лише необхідні cookie-файли: usdm_language запам’ятовує обрану українську або німецьку версію, csrftoken захищає контактну форму від підроблених запитів, usdm_contact_session протягом двох годин підтверджує, що форму відкрито у браузері, а usdm_cookie_consent_v1 зберігає ваш вибір у панелі налаштувань конфіденційності. Решта цих cookie діє до одного року. Після надсилання форми cookie sessionid тимчасово, не довше 10 хвилин, зберігає результат надсилання або повідомлення про помилки. Усі cookie можна видалити в налаштуваннях браузера."
GERMAN = "Die Website verwendet nur notwendige Cookies: usdm_language speichert die gewählte ukrainische oder deutsche Sprachversion, csrftoken schützt das Kontaktformular vor gefälschten Anfragen, usdm_contact_session bestätigt zwei Stunden lang, dass das Formular in einem Browser geöffnet wurde, und usdm_cookie_consent_v1 speichert Ihre Auswahl in den Datenschutzeinstellungen. Die übrigen Cookies können bis zu einem Jahr gespeichert werden. Nach dem Absenden des Formulars speichert sessionid für höchstens zehn Minuten den Versandstatus oder Fehlermeldungen. Alle Cookies können in den Browsereinstellungen gelöscht werden."


def seed_translation(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    source, _ = Source.objects.update_or_create(
        key="contact.bot-protection.cookies",
        defaults={"source_text": UKRAINIAN, "context": ""},
    )
    for language, translated_text in (("uk", UKRAINIAN), ("de", GERMAN)):
        Value.objects.update_or_create(
            source=source,
            language=language,
            defaults={"translated_text": translated_text},
        )


def remove_translation(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key="contact.bot-protection.cookies").delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0013_contact_form_and_cookie_consent")]
    operations = [migrations.RunPython(seed_translation, remove_translation)]
