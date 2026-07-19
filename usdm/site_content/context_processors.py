from django.conf import settings


def language_navigation(request):
    current = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
    segments = request.path_info.strip("/").split("/")
    remainder = segments[1:] if segments and segments[0] in settings.SITE_LANGUAGES else segments
    suffix = "/".join(segment for segment in remainder if segment)

    languages = []
    labels = dict(settings.LANGUAGES)
    for code in settings.SITE_LANGUAGES:
        url = f"/{code}/"
        if suffix:
            url += f"{suffix}/"
        languages.append(
            {"code": code, "name": labels[code], "url": url, "active": code == current}
        )
    return {"site_languages": languages, "current_language": current}
