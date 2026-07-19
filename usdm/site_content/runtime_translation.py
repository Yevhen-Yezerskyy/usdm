from threading import RLock

from django.conf import settings
from django.db import connection
from django.utils.translation import trans_real


_lock = RLock()
_catalogs = {}
_loaded = False
_installed = False


def _normalize_language(language):
    return str(language or "").split("-", 1)[0].lower()


def refresh_runtime_translations():
    catalogs = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT v.language, s.context, s.source_text, v.translated_text
                FROM translation_values v
                JOIN translation_sources s ON s.id = v.source_id
                WHERE v.translated_text <> ''
                """
            )
            rows = cursor.fetchall()
    except Exception:
        rows = []

    for language, context, source_text, translated_text in rows:
        key = (
            f"{context}{trans_real.CONTEXT_SEPARATOR}{source_text}"
            if context
            else source_text
        )
        catalogs.setdefault(_normalize_language(language), {})[key] = translated_text

    global _catalogs, _loaded
    with _lock:
        _catalogs = catalogs
        _loaded = True
    return sum(len(catalog) for catalog in catalogs.values())


def _translation_for(language, message):
    global _loaded
    if not _loaded:
        refresh_runtime_translations()
    with _lock:
        return _catalogs.get(_normalize_language(language), {}).get(message)


def install_runtime_translation():
    global _installed
    if _installed:
        return

    original_gettext = trans_real.DjangoTranslation.gettext
    original_ngettext = trans_real.DjangoTranslation.ngettext

    def gettext(translation, message):
        language = getattr(
            translation,
            "_DjangoTranslation__language",
            settings.LANGUAGE_CODE,
        )
        translated = _translation_for(language, str(message))
        if translated is not None:
            return translated
        if _normalize_language(language) == settings.LANGUAGE_CODE:
            return str(message)
        return original_gettext(translation, message)

    trans_real.DjangoTranslation.gettext = gettext

    def ngettext(translation, singular, plural, number):
        message = singular if number == 1 else plural
        language = getattr(
            translation,
            "_DjangoTranslation__language",
            settings.LANGUAGE_CODE,
        )
        translated = _translation_for(language, str(message))
        if translated is not None:
            return translated
        if _normalize_language(language) == settings.LANGUAGE_CODE:
            return str(message)
        return original_ngettext(translation, singular, plural, number)

    trans_real.DjangoTranslation.ngettext = ngettext
    _installed = True
