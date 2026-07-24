from django.conf import settings


def language_navigation(request):
    current = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
    languages = []
    labels = dict(settings.LANGUAGES)
    for code in settings.SITE_LANGUAGES:
        languages.append(
            {
                "code": code,
                "name": labels[code],
                "url": "/",
                "active": code == current,
            }
        )
    return {"site_languages": languages, "current_language": current}
