from django.db import migrations


ROOM_TRANSLATIONS = {
    'houses.rooms.13bb304e48da': ('1 Передпокій', '1 Diele'),
    'houses.rooms.4558e854cf34': ('1 Хол', '1 Flur'),
    'houses.rooms.b600dfd21a2a': ('1,6', '1,6'),
    'houses.rooms.1d11b0299406': ('1. Вітальня', '1. Wohnzimmer'),
    'houses.rooms.4730d8b8ac51': ('10. Гараж', '10. Garage'),
    'houses.rooms.e5bce0fa6481': ('10. Спальня', '10. Schlafzimmer'),
    'houses.rooms.508267c0ae75': ('11,1 м2', '11,1 m2'),
    'houses.rooms.cbcf26702df0': ('11,6', '11,6'),
    'houses.rooms.6a601616d8e8': ('11,7', '11,7'),
    'houses.rooms.ffe03b00be9e': ('11,7 м2', '11,7 m2'),
    'houses.rooms.ade68233c55d': ('11. Спальня', '11. Schlafzimmer'),
    'houses.rooms.69ffba8c920e': ('12,0', '12,0'),
    'houses.rooms.315af2085384': ('12,2', '12,2'),
    'houses.rooms.6d40b05d8100': ('12,8', '12,8'),
    'houses.rooms.30ec5b740165': ('12,9', '12,9'),
    'houses.rooms.5be4a1a27cc8': ('12. Спальня', '12. Schlafzimmer'),
    'houses.rooms.9210988e6896': ('13,4 м2', '13,4 m2'),
    'houses.rooms.ad582ec781dd': ('13. Спальня', '13. Schlafzimmer'),
    'houses.rooms.d6f29c78ea7f': ('132,7 м2', '132,7 m2'),
    'houses.rooms.dc6e265db0b6': ('141,6', '141,6'),
    'houses.rooms.b9a74f8f7e02': ('15,0 м2', '15,0 m2'),
    'houses.rooms.172ad11458fe': ('17,0', '17,0'),
    'houses.rooms.05c4005adb6c': ('176, 4', '176, 4'),
    'houses.rooms.775a79ee6b2b': ('18,7', '18,7'),
    'houses.rooms.c0e3a7e07213': ('2,3', '2,3'),
    'houses.rooms.cd7e53b66ca7': ('2. Гардеробна', '2. Ankleide'),
    'houses.rooms.fa8b1e8aef6d': ('2. Кухня', '2. Küche'),
    'houses.rooms.5fdddb71d93b': ('2. Спальня', '2. Schlafzimmer'),
    'houses.rooms.3691c0df5379': ('21,8', '21,8'),
    'houses.rooms.3310577160bb': ('22,9', '22,9'),
    'houses.rooms.8f9dc92c89c2': ('23,3', '23,3'),
    'houses.rooms.a9c32940e5a9': ('234,4', '234,4'),
    'houses.rooms.5f9bfc93cf35': ('24,4', '24,4'),
    'houses.rooms.779360117c5a': ('25,2', '25,2'),
    'houses.rooms.71816411c82e': ('3,1 м2', '3,1 m2'),
    'houses.rooms.831b183eaa77': ('3,3', '3,3'),
    'houses.rooms.95ac051be593': ('3,5', '3,5'),
    'houses.rooms.2c1c99030ab4': ('3,5 м2', '3,5 m2'),
    'houses.rooms.b07139e9fea4': ('3,6', '3,6'),
    'houses.rooms.a22136928555': ('3. Вітальня', '3. Wohnzimmer'),
    'houses.rooms.fe9ebde791a6': ('3. Гардеробна', '3. Ankleide'),
    'houses.rooms.4b15db745fa3': ('3. Санвузол', '3. Bad'),
    'houses.rooms.890e409d397d': ('3. Топкова', '3. Heizraum'),
    'houses.rooms.57f7f2cf7b90': ('33,5', '33,5'),
    'houses.rooms.f4ede7a64988': ('39,6', '39,6'),
    'houses.rooms.b18615a00662': ('4,4', '4,4'),
    'houses.rooms.22cf745663fc': ('4,6', '4,6'),
    'houses.rooms.407c65ab103e': ('4. Коридор', '4. Korridor'),
    'houses.rooms.e63e99dabb48': ('4. Кухня', '4. Küche'),
    'houses.rooms.3bff58f4c6bd': ('4. Санвузол', '4. Bad'),
    'houses.rooms.15abe1f24c26': ('4. Хол', '4. Flur'),
    'houses.rooms.8b3a17df7c7f': ('49,3 м2', '49,3 m2'),
    'houses.rooms.f0d86162421b': ('5,0 м2', '5,0 m2'),
    'houses.rooms.38fee875c8e3': ('5,2', '5,2'),
    'houses.rooms.409a1639a5f7': ('5,6', '5,6'),
    'houses.rooms.7e7b79cfb7fe': ('5. Вітальня – студія', '5. Wohnstudio'),
    'houses.rooms.38062162ee92': ('5. Кабінет', '5. Arbeitszimmer'),
    'houses.rooms.ba4f3024f7fb': ('5. Спальня', '5. Schlafzimmer'),
    'houses.rooms.d7429dcb8c40': ('50,1', '50,1'),
    'houses.rooms.be549cb34e29': ('6,0', '6,0'),
    'houses.rooms.0557b0de560c': ('6,2', '6,2'),
    'houses.rooms.0e9a315c9aaa': ('6,4', '6,4'),
    'houses.rooms.99ec5dedbf69': ('6,5', '6,5'),
    'houses.rooms.036633451266': ('6. Гардеробна', '6. Ankleide'),
    'houses.rooms.bd333639ae8f': ('6. Санвузол', '6. Bad'),
    'houses.rooms.19de5f1456da': ('6. Спальня', '6. Schlafzimmer'),
    'houses.rooms.4280d849a369': ('7,2', '7,2'),
    'houses.rooms.2d54973aace3': ('7. Гардеробна', '7. Ankleide'),
    'houses.rooms.109b83ca7ee1': ('7. Санвузол', '7. Bad'),
    'houses.rooms.1b059e077d30': ('7. Спальня', '7. Schlafzimmer'),
    'houses.rooms.6d0c406d5e9f': ('8,2', '8,2'),
    'houses.rooms.f49c8b2ec22d': ('8,3', '8,3'),
    'houses.rooms.859f627b5097': ('8,8', '8,8'),
    'houses.rooms.72380f30da13': ('8. Санвузол', '8. Bad'),
    'houses.rooms.65487048219f': ('8. Сходи', '8. Treppe'),
    'houses.rooms.f197da640fd4': ('8. Тераса', '8. Terrasse'),
    'houses.rooms.416104b190de': ('88,2', '88,2'),
    'houses.rooms.1f701e143948': ('9,1', '9,1'),
    'houses.rooms.03e2094a3b2e': ('9,3', '9,3'),
    'houses.rooms.a122554a8692': ('9,5', '9,5'),
    'houses.rooms.162e273d6e12': ('9,5 м2', '9,5 m2'),
    'houses.rooms.802bf5b3cabc': ('9,6', '9,6'),
    'houses.rooms.597d2e04ed63': ('9. Душова', '9. Dusche'),
    'houses.rooms.cf7062e6cd14': ('9. Санвузол', '9. Bad'),
    'houses.rooms.d4c07c28f118': ('9. Технічне приміщення', '9. Technikraum'),
    'houses.rooms.56f115e4d434': ('Вітальна студія', 'Wohnstudio'),
    'houses.rooms.365495688bbb': ('Другий поверх', 'Obergeschoss'),
    'houses.rooms.3a043d9cb6ea': ('Загальна площа будинку', 'Gesamtfläche des Hauses'),
    'houses.rooms.36b85c13a520': ('Загальна площа квартири', 'Gesamtfläche der Wohnung'),
    'houses.rooms.2659ea13cbe7': ('Навіс для машин', 'Carport'),
    'houses.rooms.6801afc40018': ('Передпокій', 'Diele'),
    'houses.rooms.01ef49ab4464': ('Перший поверх', 'Erdgeschoss'),
    'houses.rooms.b32395a97452': ('Санвузол', 'Bad'),
    'houses.rooms.784db8899c33': ('Спальня', 'Schlafzimmer'),
    'houses.rooms.c3234d4f0290': ('Технічне приміщення', 'Technikraum'),
    'houses.rooms.c3bd78228584': ('Хол', 'Flur'),
}


def seed_room_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Value = apps.get_model("site_content", "TranslationValue")
    for key, (ukrainian, german) in ROOM_TRANSLATIONS.items():
        source = Source.objects.filter(source_text=ukrainian, context="").first()
        if source is None:
            source = Source.objects.create(key=key, source_text=ukrainian, context="")
        for language, translated_text in (("uk", ukrainian), ("de", german)):
            Value.objects.update_or_create(source=source, language=language, defaults={"translated_text": translated_text})


def remove_room_translations(apps, schema_editor):
    Source = apps.get_model("site_content", "TranslationSource")
    Source.objects.filter(key__in=ROOM_TRANSLATIONS).delete()


class Migration(migrations.Migration):
    dependencies = [("site_content", "0009_accessibility_translations")]
    operations = [migrations.RunPython(seed_room_translations, remove_room_translations)]
