from django.db import migrations


LEGAL_TRANSLATIONS = [
    ("Юридична інформація", "Rechtliche Informationen"),
    ("Impressum", "Impressum"),
    ("Відомості про власника та оператора вебсайту usdm.com.ua", "Angaben zum Eigentümer und Betreiber der Website usdm.com.ua"),
    ("На цій сторінці", "Auf dieser Seite"),
    ("ТОВ «ЮСДМ»", "TOV „USDM“"),
    ("Повне найменування", "Vollständiger Name"),
    ("Товариство з обмеженою відповідальністю «ЮСДМ»", "TOV „USDM“ (ukrainische Gesellschaft mit beschränkter Haftung)"),
    ("Код ЄДРПОУ", "Unternehmensnummer (EDRPOU)"),
    ("38464817", "38464817"),
    ("Керівник", "Geschäftsführer"),
    ("Бут Сергій Петрович", "Serhii Petrovych But"),
    ("Юридична адреса", "Geschäftsanschrift"),
    ("Україна, 04655, м. Київ, вул. Глибочицька, буд. 72, офіс 320/1", "Hlybochytska-Straße 72, Büro 320/1, 04655 Kyjiw, Ukraine"),
    ("Телефон", "Telefon"),
    ("+380 67 543 59 10", "+380 67 543 59 10"),
    ("Електронна пошта", "E-Mail"),
    ("sb@usdm.com.ua", "sb@usdm.com.ua"),
    ("Власник вебсайту", "Diensteanbieter"),
    ("Власником і оператором цього вебсайту є Товариство з обмеженою відповідальністю «ЮСДМ» (ТОВ «ЮСДМ»), зареєстроване відповідно до законодавства України.", "Eigentümer und Betreiber dieser Website ist TOV „USDM“, eine nach ukrainischem Recht eingetragene Gesellschaft mit beschränkter Haftung."),
    ("Відомості на цій сторінці також надаються для виконання вимог § 5 німецького Закону про цифрові послуги (DDG), оскільки вебсайт доступний німецькою мовою.", "Die Angaben auf dieser Seite erfolgen zugleich gemäß § 5 des deutschen Digitale-Dienste-Gesetzes (DDG), da die Website auch in deutscher Sprache angeboten wird."),
    ("Інформація та пропозиції", "Informationen und Angebote"),
    ("Ми уважно готуємо матеріали сайту, однак описи, візуалізації, технічні рішення, ціни та строки мають інформаційний характер. Остаточний обсяг робіт, характеристики, вартість і строки визначаються індивідуально в комерційній пропозиції та договорі.", "Wir erstellen die Inhalte dieser Website mit Sorgfalt. Beschreibungen, Visualisierungen, technische Lösungen, Preise und Termine dienen jedoch der ersten Information. Der endgültige Leistungsumfang, die Eigenschaften, Kosten und Termine werden individuell im Angebot und im Vertrag festgelegt."),
    ("Обмеження на цій сторінці не виключають відповідальності ТОВ «ЮСДМ» у випадках, коли така відповідальність прямо встановлена законом.", "Die Hinweise auf dieser Seite beschränken die Haftung von TOV „USDM“ nicht, soweit eine Haftung gesetzlich zwingend vorgeschrieben ist."),
    ("Зовнішні посилання", "Externe Links"),
    ("Сайт містить посилання на соціальні мережі та сторонні сервіси зв’язку. Їхній вміст і правила обробки даних контролюють відповідні оператори. Якщо ми дізнаємося про незаконний вміст за посиланням, то перевіримо повідомлення та, за наявності підстав, видалимо таке посилання.", "Diese Website enthält Links zu sozialen Netzwerken und Kommunikationsdiensten Dritter. Für deren Inhalte und Datenverarbeitung sind die jeweiligen Betreiber verantwortlich. Erhalten wir einen konkreten Hinweis auf rechtswidrige Inhalte, prüfen wir ihn und entfernen den betreffenden Link, sofern dies geboten ist."),
    ("Авторські права", "Urheberrecht"),
    ("Тексти, фотографії, візуалізації, креслення, дизайн та інші матеріали сайту належать ТОВ «ЮСДМ» або використовуються на законних підставах. Копіювання, публікація чи інше використання матеріалів поза межами, дозволеними законом, потребує попередньої письмової згоди правовласника.", "Texte, Fotografien, Visualisierungen, Zeichnungen, Gestaltung und sonstige Inhalte dieser Website stehen im Eigentum von TOV „USDM“ oder werden rechtmäßig genutzt. Jede Vervielfältigung, Veröffentlichung oder sonstige Nutzung außerhalb der gesetzlich erlaubten Grenzen bedarf der vorherigen schriftlichen Zustimmung des jeweiligen Rechteinhabers."),
    ("Захист персональних даних", "Datenschutz"),
    ("Політика конфіденційності", "Datenschutzerklärung"),
    ("Зрозуміло про те, які дані обробляє usdm.com.ua і навіщо", "Welche Daten usdm.com.ua verarbeitet, zu welchem Zweck und welche Rechte Sie haben"),
    ("Редакція від 21 липня 2026 року", "Stand: 21. Juli 2026"),
    ("Розділи політики", "Inhalt"),
    ("Відповідальний за дані", "Verantwortlicher"),
    ("Компанія", "Unternehmen"),
    ("Адреса", "Anschrift"),
    ("Запити щодо даних", "Datenschutzanfragen"),
    ("1. Хто відповідає за дані", "1. Verantwortlicher"),
    ("Відповідальним за обробку персональних даних на цьому сайті є Товариство з обмеженою відповідальністю «ЮСДМ». Контактні дані наведені поруч. З питань приватності напишіть нам на sb@usdm.com.ua.", "Verantwortlicher für die Verarbeitung personenbezogener Daten auf dieser Website ist TOV „USDM“. Die Kontaktdaten finden Sie nebenstehend. Datenschutzanfragen richten Sie bitte an sb@usdm.com.ua."),
    ("2. Які дані ми обробляємо", "2. Welche Daten wir verarbeiten"),
    ("Під час відкриття сторінок сервер технічно отримує IP-адресу, дату й час запиту, адресу запитаної сторінки, адресу попередньої сторінки (referrer), відомості про браузер і операційну систему, статус відповіді та обсяг переданих даних. Ці відомості записуються до журналів сервера.", "Beim Aufruf einer Seite erhält der Server technisch bedingt Ihre IP-Adresse, Datum und Uhrzeit der Anfrage, die aufgerufene Adresse, die zuvor besuchte Seite (Referrer), Angaben zu Browser und Betriebssystem, den Antwortstatus sowie die übertragene Datenmenge. Diese Angaben werden in Serverprotokollen gespeichert."),
    ("Якщо ви звертаєтеся через форму, ми отримуємо ім’я, прізвище (якщо вказане), електронну адресу, номер телефону, текст повідомлення, обрану мову та час надсилання. Дані зберігаються в базі сайту; повідомлення також може бути надіслане відповідальному працівнику електронною поштою.", "Wenn Sie das Kontaktformular nutzen, verarbeiten wir Ihren Vornamen, gegebenenfalls Nachnamen, Ihre E-Mail-Adresse, Telefonnummer, Nachricht, gewählte Sprache und den Zeitpunkt des Versands. Die Daten werden in der Datenbank der Website gespeichert; die Nachricht kann außerdem per E-Mail an den zuständigen Mitarbeiter übermittelt werden."),
    ("Якщо ви телефонуєте, пишете електронною поштою або в месенджері, ми обробляємо дані, які ви повідомили в такому зверненні.", "Bei einer Kontaktaufnahme per Telefon, E-Mail oder Messenger verarbeiten wir die Angaben, die Sie uns dabei mitteilen."),
    ("3. Мета та правові підстави", "3. Zwecke und Rechtsgrundlagen"),
    ("Контактні дані потрібні, щоб відповісти на запит, уточнити вимоги до проєкту, підготувати пропозицію та, за потреби, укласти або виконати договір. Технічні дані потрібні для стабільної й безпечної роботи сайту, діагностики помилок і захисту від зловживань.", "Kontaktdaten verarbeiten wir, um Ihre Anfrage zu beantworten, Projektanforderungen zu klären, ein Angebot zu erstellen und gegebenenfalls einen Vertrag anzubahnen oder zu erfüllen. Technische Daten benötigen wir für den stabilen und sicheren Betrieb der Website, zur Fehlerdiagnose und zur Abwehr von Missbrauch."),
    ("Обробка здійснюється відповідно до Закону України «Про захист персональних даних». Якщо застосовується Загальний регламент ЄС про захист даних (GDPR), підставами є дії на запит особи до укладення договору або виконання договору, виконання юридичних обов’язків та наш законний інтерес у безпечній роботі сайту (стаття 6(1)(b), (c) і (f) GDPR). Згода використовується лише тоді, коли закон вимагає саме її.", "Die Verarbeitung erfolgt nach dem ukrainischen Gesetz über den Schutz personenbezogener Daten. Soweit die Datenschutz-Grundverordnung (DSGVO) anwendbar ist, stützen wir die Verarbeitung auf vorvertragliche Maßnahmen oder die Vertragserfüllung, die Erfüllung rechtlicher Pflichten sowie unser berechtigtes Interesse am sicheren Betrieb der Website (Art. 6 Abs. 1 Buchst. b, c und f DSGVO). Eine Einwilligung holen wir nur ein, wenn sie gesetzlich erforderlich ist."),
    ("4. Cookie-файли", "4. Cookies"),
    ("Сайт використовує лише необхідні cookie-файли: usdm_language запам’ятовує обрану українську або німецьку версію, а csrftoken захищає контактну форму від підроблених запитів. Строк дії кожного з них — до одного року; cookie можна видалити в налаштуваннях браузера.", "Die Website verwendet nur erforderliche Cookies: usdm_language merkt sich die gewählte ukrainische oder deutsche Sprachversion; csrftoken schützt das Kontaktformular vor gefälschten Anfragen. Beide Cookies können bis zu einem Jahr gespeichert und jederzeit in den Browsereinstellungen gelöscht werden."),
    ("На сайті немає систем вебаналітики, рекламних пікселів, профілювання чи маркетингових cookie. Тому окремий банер згоди зараз не показується. Якщо склад cookie зміниться, ми оновимо цю політику та, коли це потрібно, запросимо згоду.", "Wir setzen derzeit keine Webanalyse, Werbepixel, Profilbildung oder Marketing-Cookies ein. Daher erscheint kein gesondertes Einwilligungsbanner. Ändert sich der Einsatz von Cookies, aktualisieren wir diese Erklärung und holen, soweit erforderlich, Ihre Einwilligung ein."),
    ("5. Хто може отримати дані", "5. Empfänger der Daten"),
    ("Доступ до даних мають лише уповноважені працівники ТОВ «ЮСДМ» та постачальники, які забезпечують хостинг, технічне обслуговування й електронну пошту, — лише в обсязі, потрібному для їхніх завдань. Дані також можуть бути надані державному органу, якщо цього вимагає закон.", "Zugriff auf personenbezogene Daten erhalten nur befugte Mitarbeiter von TOV „USDM“ sowie Dienstleister für Hosting, technische Betreuung und E-Mail – jeweils nur, soweit dies für ihre Aufgabe erforderlich ist. Daten können außerdem an Behörden übermittelt werden, wenn wir gesetzlich dazu verpflichtet sind."),
    ("Ми не продаємо персональні дані та не передаємо їх рекламним мережам.", "Wir verkaufen keine personenbezogenen Daten und übermitteln sie nicht an Werbenetzwerke."),
    ("6. Обробка даних в Україні", "6. Datenverarbeitung in der Ukraine"),
    ("ТОВ «ЮСДМ» зареєстроване в Україні. Надсилаючи звернення, ви безпосередньо контактуєте з українською компанією, тому надані вами дані обробляються в Україні. Це не передача окремому сторонньому одержувачу: дані надходять безпосередньо відповідальному за їх обробку. Якщо до конкретної обробки застосовується GDPR, ТОВ «ЮСДМ» дотримується його вимог незалежно від місця обробки.", "TOV „USDM“ hat seinen Sitz in der Ukraine. Wenn Sie uns eine Anfrage senden, nehmen Sie unmittelbar Kontakt zu einem ukrainischen Unternehmen auf; Ihre Angaben werden daher in der Ukraine verarbeitet. Es handelt sich nicht um eine Weitergabe an einen eigenständigen Dritten: Die Daten gelangen unmittelbar zum Verantwortlichen. Soweit die DSGVO auf die konkrete Verarbeitung anwendbar ist, beachtet TOV „USDM“ ihre Anforderungen unabhängig vom Ort der Verarbeitung."),
    ("7. Як довго зберігаються дані", "7. Speicherdauer"),
    ("Звернення зберігаються до завершення комунікації, а далі — лише поки це потрібно для виконання домовленостей, дотримання строків зберігання документів або захисту правових вимог. Серверні журнали зберігаються стільки, скільки потрібно для безпеки та діагностики, після чого видаляються або перезаписуються. Конкретний строк може бути продовжений, якщо цього вимагає закон або розслідування інциденту.", "Anfragen speichern wir bis zum Abschluss der Kommunikation und danach nur so lange, wie dies zur Erfüllung von Vereinbarungen, zur Einhaltung gesetzlicher Aufbewahrungsfristen oder zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen erforderlich ist. Serverprotokolle werden nur so lange vorgehalten, wie sie für Sicherheit und Fehlerdiagnose benötigt werden, und anschließend gelöscht oder überschrieben. Eine längere Speicherung erfolgt nur, wenn das Gesetz oder die Untersuchung eines Sicherheitsvorfalls dies verlangt."),
    ("8. Ваші права", "8. Ihre Rechte"),
    ("У випадках, передбачених законом, ви можете дізнатися, чи обробляємо ми ваші дані, отримати до них доступ і копію, вимагати виправлення, видалення або обмеження обробки, заперечити проти обробки, відкликати згоду та отримати дані у переносному форматі.", "Im gesetzlich vorgesehenen Umfang haben Sie das Recht auf Auskunft und eine Kopie Ihrer Daten, Berichtigung, Löschung, Einschränkung der Verarbeitung, Widerspruch, Widerruf einer Einwilligung sowie Datenübertragbarkeit. Der Widerruf berührt nicht die Rechtmäßigkeit der bis dahin erfolgten Verarbeitung."),
    ("Ви також можете подати скаргу Уповноваженому Верховної Ради України з прав людини. Якщо застосовується GDPR, ви маєте право звернутися до наглядового органу за місцем проживання, роботи або ймовірного порушення.", "Sie können sich außerdem beim Menschenrechtsbeauftragten des ukrainischen Parlaments beschweren. Soweit die DSGVO anwendbar ist, können Sie eine Beschwerde bei einer Aufsichtsbehörde einreichen, insbesondere an Ihrem Aufenthaltsort, Arbeitsplatz oder am Ort des mutmaßlichen Verstoßes."),
    ("9. Добровільність і автоматизовані рішення", "9. Freiwilligkeit und automatisierte Entscheidungen"),
    ("Надання даних через контактну форму є добровільним. Без обов’язкових полів ми не зможемо опрацювати звернення та відповісти. Сайт не приймає щодо відвідувачів автоматизованих рішень і не створює профілів.", "Die Angabe von Daten im Kontaktformular ist freiwillig. Ohne die Pflichtfelder können wir Ihre Anfrage jedoch nicht bearbeiten und beantworten. Die Website trifft keine automatisierten Entscheidungen über Besucher und erstellt keine Profile."),
    ("10. Безпека та оновлення політики", "10. Sicherheit und Aktualisierung"),
    ("Ми застосовуємо належні технічні й організаційні заходи для захисту даних від втрати, зміни, розголошення та несанкціонованого доступу. Абсолютно безпечного способу передавання даних через інтернет не існує, тому заходи захисту регулярно переглядаються.", "Wir setzen angemessene technische und organisatorische Maßnahmen ein, um Daten vor Verlust, Veränderung, Offenlegung und unbefugtem Zugriff zu schützen. Eine absolut sichere Datenübertragung über das Internet gibt es nicht; deshalb überprüfen wir unsere Schutzmaßnahmen regelmäßig."),
    ("Актуальна редакція політики завжди опублікована на цій сторінці. Ми оновимо її, якщо зміниться робота сайту, порядок обробки даних або вимоги законодавства.", "Die jeweils aktuelle Fassung dieser Erklärung ist auf dieser Seite veröffentlicht. Wir aktualisieren sie, wenn sich die Funktionsweise der Website, unsere Datenverarbeitung oder die gesetzlichen Anforderungen ändern."),
]


def seed_legal_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for index, (ukrainian, german) in enumerate(LEGAL_TRANSLATIONS, start=1):
        source = Source.objects.filter(source_text=ukrainian, context="").first()
        if source is None:
            source = Source.objects.create(
                key=f"legal.v2.{index:03d}", source_text=ukrainian, context=""
            )
        for language, translated_text in (("uk", ukrainian), ("de", german)):
            Value.objects.update_or_create(
                source=source,
                language=language,
                defaults={"translated_text": translated_text},
            )


def remove_legal_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key__startswith="legal.v2.").delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0011_emphasis_translations")]
    operations = [migrations.RunPython(seed_legal_translations, remove_legal_translations)]
