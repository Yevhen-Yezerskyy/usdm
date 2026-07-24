from django.db import migrations, models
import django.db.models.deletion


TRANSLATIONS = [
    ("Ваше ім’я *", "Ihr Vorname *"),
    ("Ваше прізвище", "Ihr Nachname"),
    ("Ваш email *", "Ihre E-Mail-Adresse *"),
    ("Ваш телефон *", "Ihre Telefonnummer *"),
    ("Ваше повідомлення або запит *", "Ihre Nachricht oder Anfrage *"),
    ("Вибрати файли проєкту", "Projektdateien auswählen"),
    ("Будь ласка, вкажіть ваше ім’я.", "Bitte geben Sie Ihren Vornamen ein."),
    ("Вказане ім’я надто довге.", "Der eingegebene Vorname ist zu lang."),
    ("Вказане прізвище надто довге.", "Der eingegebene Nachname ist zu lang."),
    ("Будь ласка, вкажіть адресу електронної пошти.", "Bitte geben Sie Ihre E-Mail-Adresse ein."),
    ("Будь ласка, вкажіть дійсну адресу електронної пошти.", "Bitte geben Sie eine gültige E-Mail-Adresse ein."),
    ("Вказана адреса електронної пошти надто довга.", "Die eingegebene E-Mail-Adresse ist zu lang."),
    ("Будь ласка, вкажіть номер телефону.", "Bitte geben Sie Ihre Telefonnummer ein."),
    ("Вказаний номер телефону надто довгий.", "Die eingegebene Telefonnummer ist zu lang."),
    ("Будь ласка, напишіть повідомлення або запит.", "Bitte geben Sie Ihre Nachricht oder Anfrage ein."),
    ("Повідомлення надто довге.", "Die Nachricht ist zu lang."),
    ("Один із вибраних файлів порожній.", "Eine der ausgewählten Dateien ist leer."),
    ("Один із вибраних файлів не вдалося прочитати.", "Eine der ausgewählten Dateien konnte nicht gelesen werden."),
    ("Назва одного з вибраних файлів надто довга.", "Der Name einer ausgewählten Datei ist zu lang."),
    ("Підтвердьте згоду на обробку персональних даних.", "Bitte stimmen Sie der Verarbeitung Ihrer personenbezogenen Daten zu."),
    ("Будь ласка, вкажіть дійсний номер телефону.", "Bitte geben Sie eine gültige Telefonnummer ein."),
    ("Можна додати щонайбільше 10 файлів.", "Sie können maximal 10 Dateien hinzufügen."),
    ("Загальний розмір файлів не повинен перевищувати 25 МБ.", "Die Dateien dürfen zusammen maximal 25 MB groß sein."),
    ("Формат файлу «%(name)s» не підтримується.", "Das Dateiformat von „%(name)s“ wird nicht unterstützt."),
    ("Можна додати щонайбільше {maximum} файлів.", "Sie können maximal {maximum} Dateien hinzufügen."),
    ("Загальний розмір файлів не повинен перевищувати {maximum} МБ.", "Die Dateien dürfen zusammen maximal {maximum} MB groß sein."),
    ("Формат файлу «{name}» не підтримується.", "Das Dateiformat von „{name}“ wird nicht unterstützt."),
    ("Видалити файл {name}", "Datei {name} entfernen"),
    ("Ваш запит прийнято. Ми зв’яжемося з вами найближчим часом.", "Ihre Anfrage wurde angenommen. Wir melden uns in Kürze bei Ihnen."),
    ("Не вдалося прийняти запит. Будь ласка, напишіть нам на вказану електронну адресу.", "Ihre Anfrage konnte nicht angenommen werden. Bitte verwenden Sie die auf dieser Website angegebene E-Mail-Adresse."),
    ("Ваше ім’я", "Ihr Vorname"),
    ("Повідомлення", "Nachricht"),
    ("Перетягніть файли сюди або виберіть їх", "Dateien hierher ziehen oder auswählen"),
    ("Можна додати кілька файлів, загалом не більше 25 МБ.", "Mehrere Dateien möglich, insgesamt maximal 25 MB."),
    ("Я ознайомився(-лася) з", "Ich habe die"),
    ("політикою конфіденційності", "Datenschutzerklärung gelesen"),
    ("та погоджуюся на обробку моїх персональних даних. *", "und akzeptiere die Verarbeitung meiner personenbezogenen Daten. *"),
    ("Відкрити налаштування cookie", "Cookie-Einstellungen öffnen"),
    ("Налаштування cookie", "Cookie-Einstellungen"),
    ("Налаштування конфіденційності", "Datenschutz-Einstellungen"),
    ("Ми використовуємо лише необхідні cookie для вибору мови, захисту контактної форми та збереження ваших налаштувань. Аналітики й реклами немає.", "Wir verwenden nur notwendige Cookies für die Sprachwahl, den Schutz des Kontaktformulars und die Speicherung Ihrer Einstellungen. Analyse und Werbung setzen wir nicht ein."),
    ("Докладніше", "Details"),
    ("Прийняти всі", "Alle akzeptieren"),
    ("Зрозуміло", "Verstanden"),
    ("Закрити", "Schließen"),
    ("Зберегти вибір", "Auswahl speichern"),
    ("Конфіденційність", "Datenschutz"),
    ("Необхідні cookie", "Notwendige Cookies"),
    ("Потрібні для збереження вибраної мови, налаштувань конфіденційності, захисту форми та показу результату її надсилання.", "Erforderlich für die gewählte Sprache, Ihre Datenschutzeinstellungen, den Schutz des Formulars und die Anzeige des Versandstatus."),
    ("Статистика", "Statistik"),
    ("Допомагає зрозуміти використання сайту. Зараз ця категорія не використовується.", "Hilft uns, die Nutzung der Website zu verstehen. Diese Kategorie wird derzeit nicht verwendet."),
    ("Зовнішні медіа", "Externe Medien"),
    ("Дозволяє завантажувати вміст сторонніх сервісів. Зараз ця категорія не використовується.", "Erlaubt das Laden externer Inhalte. Diese Kategorie wird derzeit nicht verwendet."),
    ("Сайт використовує лише необхідні cookie-файли: usdm_language запам’ятовує обрану українську або німецьку версію, csrftoken захищає контактну форму від підроблених запитів, а usdm_cookie_consent_v1 зберігає ваш вибір у панелі налаштувань конфіденційності. Вони діють до одного року. Після надсилання форми cookie sessionid тимчасово, не довше 10 хвилин, зберігає результат надсилання або повідомлення про помилки. Усі cookie можна видалити в налаштуваннях браузера.", "Die Website verwendet nur notwendige Cookies: usdm_language speichert die gewählte ukrainische oder deutsche Sprachversion, csrftoken schützt das Kontaktformular vor gefälschten Anfragen und usdm_cookie_consent_v1 speichert Ihre Auswahl in den Datenschutzeinstellungen. Diese Cookies können bis zu einem Jahr gespeichert werden. Nach dem Absenden des Formulars speichert sessionid für höchstens zehn Minuten den Versandstatus oder Fehlermeldungen. Alle Cookies können in den Browsereinstellungen gelöscht werden."),
    ("На сайті немає систем вебаналітики, рекламних пікселів, профілювання чи маркетингових cookie. Тому панель повідомляє лише про необхідні cookie й не пропонує фіктивних категорій згоди. Якщо склад cookie зміниться, ми оновимо цю політику та, коли це потрібно, запросимо згоду.", "Wir setzen keine Webanalyse, Werbepixel, Profilbildung oder Marketing-Cookies ein. Das Banner informiert daher ausschließlich über notwendige Cookies und zeigt keine fiktiven Einwilligungskategorien. Ändert sich der Einsatz von Cookies, aktualisieren wir diese Erklärung und holen, soweit erforderlich, Ihre Einwilligung ein."),
    ("Якщо ви звертаєтеся через форму, ми отримуємо ім’я, прізвище (якщо вказане), електронну адресу, номер телефону, текст повідомлення, обрану мову, час надсилання та додані вами файли. Дані зберігаються в базі сайту, а файли — у захищеному сховищі сайту; повідомлення також може бути надіслане відповідальному працівнику електронною поштою.", "Wenn Sie das Kontaktformular nutzen, verarbeiten wir Ihren Vornamen, gegebenenfalls Nachnamen, Ihre E-Mail-Adresse, Telefonnummer, Nachricht, gewählte Sprache, den Zeitpunkt des Versands und die von Ihnen beigefügten Dateien. Die Angaben werden in der Datenbank und die Dateien im geschützten Speicher der Website abgelegt; die Nachricht kann außerdem per E-Mail an den zuständigen Mitarbeiter übermittelt werden."),
]


def seed_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for index, (ukrainian, german) in enumerate(TRANSLATIONS, start=1):
        source = Source.objects.filter(source_text=ukrainian, context="").first()
        if source is None:
            source = Source.objects.create(
                key=f"contact.v2.{index:03d}", source_text=ukrainian, context=""
            )
        for language, translated_text in (("uk", ukrainian), ("de", german)):
            Value.objects.update_or_create(
                source=source,
                language=language,
                defaults={"translated_text": translated_text},
            )


def remove_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key__startswith="contact.v2.").delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0012_legal_pages_rewrite")]
    operations = [
        migrations.CreateModel(
            name="ContactAttachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="contact/%Y/%m/")),
                ("original_name", models.CharField(max_length=255)),
                ("content_type", models.CharField(blank=True, max_length=160)),
                ("size", models.PositiveBigIntegerField()),
                ("request", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attachments", to="site_content.contactrequest")),
            ],
            options={
                "db_table": "contact_attachments",
                "ordering": ("id",),
            },
        ),
        migrations.RunPython(seed_translations, remove_translations),
    ]
