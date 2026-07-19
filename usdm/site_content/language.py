from django.conf import settings
from django.utils.translation.trans_real import parse_accept_lang_header


def preferred_language(request):
    cookie_language = request.COOKIES.get(settings.SITE_LANGUAGE_COOKIE_NAME)
    if cookie_language in settings.SITE_LANGUAGES:
        return cookie_language

    accepted = parse_accept_lang_header(request.headers.get("Accept-Language", ""))
    for language, _quality in accepted:
        normalized = language.split("-", 1)[0].lower()
        if normalized in settings.SITE_LANGUAGES:
            return normalized
    return settings.LANGUAGE_CODE
