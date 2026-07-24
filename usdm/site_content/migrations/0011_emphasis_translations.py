from django.db import migrations


EMPHASIS_TRANSLATIONS = {
    'emphasis.9fe74cd19db3fc': ('1 поверх', '1. Geschoss'),
    'emphasis.6339d44b0d183e': ('1 поверх:', '1. Geschoss:'),
    'emphasis.d6f29c78ea7fd4': ('132,7 м2', '132,7 m2'),
    'emphasis.05c4005adb6c3f': ('176, 4', '176, 4'),
    'emphasis.9ba2f5210a5098': ('2 поверх', '2. Geschoss'),
    'emphasis.7027fbe23ea39a': ('2 поверх:', '2. Geschoss:'),
    'emphasis.a9c32940e5a9a6': ('234,4', '234,4'),
    'emphasis.d0ee425f08ce6f': ('3 поверх', '3. Geschoss'),
    'emphasis.c0ae359c38dec1': ('3 поверх з мансардою:', '3. Geschoss mit Mansarde:'),
    'emphasis.416104b190dece': ('88,2', '88,2'),
    'emphasis.869f0876e4720c': ('Gluggarerðin ehf.', 'Gluggarerðin ehf.'),
    'emphasis.44b9b4c7682d58': ('Harmony Villa Sweden AB', 'Harmony Villa Sweden AB'),
    'emphasis.1216c2ec87ac11': ('Modul’art Wood.', 'Modul’art Wood.'),
    'emphasis.ab11dd7620db98': ('Nowedel GmbH', 'Nowedel GmbH'),
    'emphasis.004041fd887e35': ('Інженери та технологи', 'Ingenieure und Technologen'),
    'emphasis.b00a11b31a47e7': ('Архітектурна група', 'Unser Architektenteam'),
    'emphasis.ff2dc5b96f3124': ('Будинок дуплекс зі скатним дахом та навісом для машин 175 м2.', 'Duplexhaus mit Satteldach und Carport 175 m2.'),
    'emphasis.fb883af53b2e21': ('Будинок зі скатним дахом 142 м2', 'Haus mit Satteldach 142 m2'),
    'emphasis.ab5c2197f491e4': ('Будівельні комплекти для каркасно-панельних будинків', 'Bausätze für Holzrahmen-Panelhäuser'),
    'emphasis.add60acb62d4c4': ('Використовуємо модульну технологію будівництва.', 'Wir verwenden die modulare Bautechnologie.'),
    'emphasis.eae2eed5512b56': ('Двоповерховий будинок з плоским дахом 234 м2', 'Zweigeschossiges Haus mit Flachdach 234 m2'),
    'emphasis.a7f4c437cfc40a': ('Двоповерховий будинок з плоским дахом 393 м2', 'Zweigeschossiges Haus mit Flachdach 393 m2'),
    'emphasis.c4ece3dbe6e88c': ('Двоповерховий будинок зі скатним дахом 132 м2', 'Zweigeschossiges Haus mit Satteldach 132 m2'),
    'emphasis.9f4eddaaff7961': ('Двоповерховий будинок-дуплекс зі скатним дахом, 281 м2', 'Zweigeschossiges Duplexhaus mit Satteldach, 281 m2'),
    'emphasis.365495688bbbd7': ('Другий поверх', 'Obergeschoss'),
    'emphasis.db3f4145fd8d1e': ('Експлікація приміщеннь', 'Raumaufstellung'),
    'emphasis.cc5c3f3e1ba6a9': ('Загальна вартість 124 387', 'Gesamtkosten 124 387'),
    'emphasis.4ed2fd74132f1a': ('Загальна вартість 137 344', 'Gesamtkosten 137 344'),
    'emphasis.2bded4fbd7ae9c': ('Загальна вартість 198 817', 'Gesamtkosten 198 817'),
    'emphasis.ff8b5415ea1297': ('Загальна вартість 199 976', 'Gesamtkosten 199 976'),
    'emphasis.8246a89275a97c': ('Загальна вартість 269 541', 'Gesamtkosten 269 541'),
    'emphasis.11eacfdf77068e': ('Загальна вартість 314 952', 'Gesamtkosten 314 952'),
    'emphasis.47f8a0fd84255e': ('Загальна вартість 316 970', 'Gesamtkosten 316 970'),
    'emphasis.fae9ccd77b52e8': ('Загальна вартість 329 969', 'Gesamtkosten 329 969'),
    'emphasis.d50baa1e24da6e': ('Загальна вартість 368 422', 'Gesamtkosten 368 422'),
    'emphasis.ee54008033fffc': ('Загальна вартість 377 917', 'Gesamtkosten 377 917'),
    'emphasis.2e6344692e645e': ('Загальна вартість 380 400', 'Gesamtkosten 380 400'),
    'emphasis.cf2a3ead252401': ('Загальна вартість 459 360', 'Gesamtkosten 459 360'),
    'emphasis.362a5bae710f66': ('Загальна вартість 558 452', 'Gesamtkosten 558 452'),
    'emphasis.3a043d9cb6eaf4': ('Загальна площа будинку', 'Gesamtfläche des Hauses'),
    'emphasis.36b85c13a520c1': ('Загальна площа квартири', 'Gesamtfläche der Wohnung'),
    'emphasis.9c56e38c01c75e': ('Квартира 1', 'Wohnung 1'),
    'emphasis.9e540c3332f02e': ('Квартира 2', 'Wohnung 2'),
    'emphasis.7e33a9db9659c3': ('Квартира 3', 'Wohnung 3'),
    'emphasis.01ef49ab4464a3': ('Перший поверх', 'Erdgeschoss'),
    'emphasis.2394ea7cf7c3bb': ('Площа кожної квартири 151,3 м2', 'Fläche jeder Wohnung 151,3 m2'),
    'emphasis.176df465fd8fe9': ('Приклад розрахунку дерв’яного каркасно-панельного будівельного комплекту:', 'Beispielkalkulation für einen Holzrahmen-Panel-Bausatz:'),
    'emphasis.3b5ff7167f0f77': ('Технічні та інженерні рішення', 'Technische und ingenieurmäßige Lösungen'),
    'emphasis.a12656b2639ebd': ('Триповерховий багатоквартирний будинок 392 м2', 'Dreigeschossiges Mehrfamilienhaus 392 m2'),
    'emphasis.3699d9acf44161': ('Триповерховий багатоквартирний будинок 688 м2', 'Dreigeschossiges Mehrfamilienhaus 688 m2'),
    'emphasis.e58f55b16203af': ('Триповерховий багатоквартирний будинок зі скатним дахом 454 м2', 'Dreigeschossiges Mehrfamilienhaus mit Satteldach 454 m2'),
    'emphasis.bfc786ddb7efc4': ('Триповерховий дуплекс зі скатним дахом 354 м2', 'Dreigeschossiges Duplexhaus mit Satteldach 354 m2'),
    'emphasis.fa3012717679b2': ('Ціна за м2 1 007', 'Preis pro m2 1 007'),
    'emphasis.b6a6b1d5a25140': ('Ціна за м2 1 040', 'Preis pro m2 1 040'),
    'emphasis.6fea1b12945cab': ('Ціна за м2 1 143', 'Preis pro m2 1 143'),
    'emphasis.f4d6e7d7379f2b': ('Ціна за м2 808', 'Preis pro m2 808'),
    'emphasis.ec0cc2bc253cd8': ('Ціна за м2 811', 'Preis pro m2 811'),
    'emphasis.5037058b7fa777': ('Ціна за м2 812', 'Preis pro m2 812'),
    'emphasis.7ba8e152ef3d43': ('Ціна за м2 817', 'Preis pro m2 817'),
    'emphasis.ba64acee8e2324': ('Ціна за м2 840', 'Preis pro m2 840'),
    'emphasis.2d749b5979b0de': ('Ціна за м2 887', 'Preis pro m2 887'),
    'emphasis.51c040273537a2': ('Ціна за м2 889', 'Preis pro m2 889'),
    'emphasis.0e06de34042f6b': ('Ціна за м2 893', 'Preis pro m2 893'),
    'emphasis.436e717d3d3b0d': ('Ціна за м2 921', 'Preis pro m2 921'),
    'emphasis.dc9bf644c28939': ('Чотириповерховий багатоквартирний будинок 375 м2', 'Viergeschossiges Mehrfamilienhaus 375 m2'),
    'emphasis.9aa5377c0f39c6': ('Чотириповерховий багатоквартирний будинок 429 м2', 'Viergeschossiges Mehrfamilienhaus 429 m2'),
    'emphasis.83fc867a6ea7bf': ('€', '€'),
}


def seed_emphasis_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for key, (ukrainian, german) in EMPHASIS_TRANSLATIONS.items():
        source = Source.objects.filter(source_text=ukrainian, context="").first()
        if source is None:
            source = Source.objects.create(key=key, source_text=ukrainian, context="")
        for language, translated_text in (("uk", ukrainian), ("de", german)):
            Value.objects.update_or_create(source=source, language=language, defaults={"translated_text": translated_text})


def remove_emphasis_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key__in=EMPHASIS_TRANSLATIONS).delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0010_house_room_translations")]
    operations = [migrations.RunPython(seed_emphasis_translations, remove_emphasis_translations)]
