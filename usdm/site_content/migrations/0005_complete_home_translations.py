from django.db import migrations


HOME_TRANSLATIONS = {
    "home.request": ("ВІДПРАВИТИ ЗАПИТ", "Anfrage senden"),
    "home.technology.heading": ("ТЕХНОЛОГІЇ ТА РОЗТАШУВАННЯ", "Technologien und Standorte"),
    "home.technology.body": (
        "Модульна технологія будівництва. Технологія каркасно-панельного будівництва. Застосування сертифікованої технології WEINMANN для виробництва каркасів та панелей. Енергозберігаючі технології. Технології проектування. Технологія швидкого монтажу будинків. Використання сучасних технологій будівництва та виробництва формує високотехнологічне підприємство, що здатне забезпечити високу якість виробництва та будівництва.",
        "Modulare Bautechnologie. Technologie des Holzrahmen-Panelbaus. Einsatz zertifizierter WEINMANN-Technologie zur Herstellung von Rahmen und Paneelen. Energieeffiziente Technologien. Planungstechnologien. Technologie für die schnelle Hausmontage. Der Einsatz moderner Bau- und Produktionstechnologien bildet ein Hightech-Unternehmen, das eine hohe Qualität in Produktion und Bauausführung sicherstellen kann.",
    ),
    "home.location.body": (
        "Виробничі потужності ТОВ «ЮСДМ» розташовані у Закарпатській області, м. Іршава, та в Київській області. Розташоване в Закарпатті виробництво обслуговує захід України. Це полегшує та здешевлює логістику, покращує сервіс клієнтам. Розташування на відстані до 100 км до кордонів із Словаччиною, Угорщиною та Румунією сприяє експорту до Європи. Розташоване в Київський області виробництво спрямоване на відбудову руйнувань, які зазнала Київська область весною цього року.",
        "Die Produktionskapazitäten von TOV «USDM» befinden sich in der Oblast Transkarpatien, Stadt Irschawa, sowie in der Oblast Kyjiw. Der Standort in Transkarpatien bedient den Westen der Ukraine. Das vereinfacht und vergünstigt die Logistik und verbessert den Service für Kunden. Die Lage bis zu 100 km von den Grenzen zur Slowakei, zu Ungarn und Rumänien entfernt unterstützt den Export nach Europa. Der Produktionsstandort in der Oblast Kyjiw ist auf den Wiederaufbau der Schäden ausgerichtet, die die Region Kyjiw im Frühjahr dieses Jahres erlitten hat.",
    ),
    "home.products.heading": ("ПРОДУКЦІЯ ТА РОБОТИ", "Produkte und Leistungen"),
    "home.products.item1": (
        "Повні комплекти для будівництва каркасно-панельних будинків – дерев’яний несучий каркас, багатошарові панелі зовнішніх та внутрішніх стін, перегородок, покрівлі, перекриття, підлоги, ферми або покриття, з встановленими вікнами та дверима.",
        "Komplette Bausätze für Holzrahmen-Panelhäuser – tragender Holzrahmen, mehrschichtige Paneele für Außen- und Innenwände, Trennwände, Dach, Geschossdecken, Boden, Binder oder Dachtragwerk, mit eingebauten Fenstern und Türen.",
    ),
    "home.products.item2": (
        "Модульні каркасно-панельні будинки різного ступеню готовності від зовнішнього оздоблення, вікон та покрівлі до повністю готового будинку з внутрішнім оздобленням, внутрішніми комунікаціями, освітленням, сантехнікою, меблями.",
        "Modulare Holzrahmen-Panelhäuser in unterschiedlichen Fertigstellungsgraden – von Außenverkleidung, Fenstern und Dach bis zum vollständig fertigen Haus mit Innenausbau, inneren technischen Anlagen, Beleuchtung, Sanitär und Möbeln.",
    ),
    "home.products.item3": (
        "Доставка комплектів каркасно-панельних будинків та модульних будинків територією України та до ЄС. Роботи по монтажу каркасно-панельних будинків, монтажу модульних будинків, влаштуванню (будівництву) фундаментів, зовнішніх комунікацій та благоустрою ділянки на території Україні, та всебічну проектну та технологічну підтримку по виконанню цих робіт на території ЄС.",
        "Lieferung von Bausätzen für Holzrahmen-Panelhäuser und modularen Häusern innerhalb der Ukraine und in die EU. Montagearbeiten für Holzrahmen-Panelhäuser, Montage modularer Häuser, Herstellung bzw. Bau von Fundamenten, Außenanschlüssen und Außenanlagen in der Ukraine sowie umfassende planerische und technologische Unterstützung für die Ausführung dieser Arbeiten in der EU.",
    ),
    "home.houses.banner": ("КАРКАСНО-ПАНЕЛЬНІ БУДИНКИ", "Holzrahmen-Panelhäuser"),
    "home.houses.banner_second": ("МОДУЛЬНА ТЕХНОЛОГІЯ БУДІВНИЦТВА", "Modulare Bautechnologie"),
    "home.houses.projects": ("ПРОЕКТИ ТА ЦІНИ", "Projekte und Preise"),
    "home.houses.142.title": ("Будинок зі скатним дахом 142 м2", "Haus mit Satteldach 142 m2"),
    "home.houses.142.body": (
        "Одноповерховий будинок з 5 спальнями, 3 санвузлами, вітальнею – студією 50,1 м2. Комфортний для проживання для сім’ї на 5-6 чоловік.",
        "Einstöckiges Haus mit 5 Schlafzimmern, 3 Bädern und einem Wohnstudio von 50,1 m2. Komfortabel für eine Familie mit 5-6 Personen.",
    ),
    "home.houses.393.title": ("Двоповерховий будинок з плоским дахом 393 м2", "Zweigeschossiges Haus mit Flachdach 393 m2"),
    "home.houses.393.body": (
        "Просторий будинок з 3 спальнями, 6 санвузлами, вітальнею, кухнею столовою та вітальнею – студією, з 2 терасами: 21 м2 та 20,7 м2. Великий гараж на 3 автомобіля.",
        "Geräumiges Haus mit 3 Schlafzimmern, 6 Bädern, Wohnzimmer, Wohnküche und Wohnstudio, mit 2 Terrassen: 21 m2 und 20,7 m2. Große Garage für 3 Autos.",
    ),
    "home.houses.354.title": ("Двоповерховий дуплекс 354 м2", "Zweigeschossiges Duplexhaus 354 m2"),
    "home.houses.354.body": (
        "Будинок розрахований на 2 сім’ї. У будинку 2 двоповерхові апартаменти з 3 спальнями, вітальнею, кухнею-їдальнею, ванними кімнатами та гаражем.",
        "Das Haus ist für 2 Familien ausgelegt. Es umfasst 2 zweigeschossige Apartments mit 3 Schlafzimmern, Wohnzimmer, Wohnküche, Badezimmern und Garage.",
    ),
    "home.company.banner": ("ТОВ “ЮСДМ”", "TOV “USDM”"),
    "home.company.banner_subtitle": ("ВИРОБНИЦТВО ТА БУДІВНИЦТВО", "Produktion und Bau"),
    "home.company.heading": ("ПРО КОМПАНІЮ", "Über das Unternehmen"),
    "home.company.body1": (
        "ТОВ «ЮСДМ» є будівельною та виробничою компанією. За 10 років ми збудували декілька сотень будинків та споруд, загальною площею більш ніж 35 000 м2, з яких 10 000 м2 використовуючи модульну технологію будівництва. Більшість збудованого є каркасно-панельні будинки з дерев’яним каркасом. Здобуто величезний досвід в промисловому виробництві дерев’яних каркасно-панельних елементів будинків та споруд.",
        "TOV «USDM» ist ein Bau- und Produktionsunternehmen. In 10 Jahren haben wir mehrere hundert Häuser und Bauwerke mit einer Gesamtfläche von mehr als 35.000 m2 errichtet, davon 10.000 m2 in modularer Bauweise. Der größte Teil davon sind Holzrahmen-Panelhäuser mit Holztragwerk. Wir haben umfangreiche Erfahrung in der industriellen Produktion von Holzrahmen-Panel-Elementen für Häuser und Bauwerke gesammelt.",
    ),
    "home.company.body2": (
        "ТОВ «ЮСДМ» є членом Німецько-Української промислово-торговельної палати (AHK Ukraine).",
        "TOV «USDM» ist Mitglied der Deutsch-Ukrainischen Industrie- und Handelskammer (AHK Ukraine).",
    ),
    "home.company.body3": (
        "ТОВ «ЮСДМ» має досвідчений та освідчений персонал, який здатен виконувати проектні та технологічні роботи, керувати виробничим процесом, забезпечувати необхідну якість менеджменту від узгодження економічних та інженерних умов замовлення до передачі готової продукції, або здачі готового будинку.",
        "TOV «USDM» verfügt über erfahrenes und qualifiziertes Personal, das Planungs- und Technologiearbeiten ausführen, den Produktionsprozess steuern und die erforderliche Managementqualität sicherstellen kann – von der Abstimmung wirtschaftlicher und technischer Auftragsbedingungen bis zur Übergabe der fertigen Produkte oder des fertigen Hauses.",
    ),
    "home.construction.banner": ("КАРКАСНО-ПАНЕЛЬНЕ БУДІВНИЦТВО", "Holzrahmen-Panelbau"),
    "home.construction.subtitle": ("КРАЩІ ВЛАСТИВОСТІ ДЕРЕВА", "die besten Eigenschaften von Holz"),
    "home.construction.second": ("ВИСОКОТЕХНОЛОГІЧНЕ ВИРОБНИЦТВО", "Hightech-Produktion"),
    "home.experience.heading": ("ДОСВІД ТОВ “ЮСДМ”", "ERFAHRUNG VON TOV “USDM”"),
    "home.experience.body1": (
        "За 10 років ми збудували різноманітні будинки та споруди. Від ресторану до дачного будинку, від готелю до гаражу, від рекреаційного комплексу до житлового будинку на березі Дніпра. Збудовані нами будинки розташовані по всій Україні – від Дніпра до Тернополя, від Київський області до Закарпаття.",
        "In 10 Jahren haben wir unterschiedliche Häuser und Bauwerke errichtet: vom Restaurant bis zum Ferienhaus, vom Hotel bis zur Garage, vom Erholungskomplex bis zum Wohnhaus am Ufer des Dnipro. Die von uns gebauten Häuser befinden sich in der ganzen Ukraine – von Dnipro bis Ternopil, von der Oblast Kyjiw bis Transkarpatien.",
    ),
    "home.experience.body2": (
        "Будинки та споруди одно та багатоповерхові, житлові та комерційні, різного рівня складності, різної площі та призначення. Цей величезний досвід ми використовуємо задля досягнення високої якості будівництва та виробництва, та постійно оновлюємся й здобуваємо новий досвід.",
        "Ein- und mehrgeschossige Häuser und Bauwerke, Wohn- und Gewerbebauten, mit unterschiedlicher Komplexität, Fläche und Nutzung. Diese umfangreiche Erfahrung nutzen wir, um eine hohe Qualität in Bauausführung und Produktion zu erreichen; zugleich erneuern wir uns ständig und sammeln neue Erfahrung.",
    ),
    "home.experience.body3": (
        "Засновники та керівники ТОВ «ЮСДМ» створили та вивели на український ринок будинки SKANDI – будинки у стилі Barnhouse. Десятки таких будинків збудовано по всій Україні.",
        "Die Gründer und Geschäftsführer von TOV «USDM» haben die SKANDI-Häuser auf den ukrainischen Markt gebracht – Häuser im Barnhouse-Stil. Dutzende solcher Häuser wurden in der ganzen Ukraine errichtet.",
    ),
    "home.experience.button": ("ПЕРЕДИВИТИСЬ ЗБУДОВАНЕ НАМИ", "Unsere realisierten Projekte ansehen"),
    "home.panels.banner": ("ДЕРЕВ’ЯНИЙ КАРКАС ТА ТЕХНОЛОГІЧНІ ПАНЕЛІ", "Holzrahmen und technische Paneele"),
    "home.panels.subtitle": ("КОМПЛЕКТИ ДЛЯ КАРКАСНО-ПАНЕЛЬНОГО БУДІВНИЦТВА", "Bausätze für den Holzrahmen-Panelbau"),
}


def seed_home_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for key, (ukrainian, german) in HOME_TRANSLATIONS.items():
        source, _ = Source.objects.update_or_create(
            key=key,
            defaults={"source_text": ukrainian},
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
    dependencies = [("site_content", "0004_home_intro_translations")]
    operations = [migrations.RunPython(seed_home_translations, remove_home_translations)]
