from django.conf import settings


COOKIE_PAGE_ALIASES = {
    "impressum/": "imprint/",
    "datenschutz/": "privacy/",
}


def language_navigation(request):
    current = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
    path_parts = request.path_info.lstrip("/").split("/", 1)
    has_language_prefix = path_parts[0] in settings.SITE_LANGUAGES
    page_path = path_parts[1] if has_language_prefix and len(path_parts) > 1 else ""
    if not has_language_prefix:
        page_path = request.path_info.lstrip("/")
    page_path = COOKIE_PAGE_ALIASES.get(page_path, page_path)

    languages = []
    labels = dict(settings.LANGUAGES)
    for code in settings.SITE_LANGUAGES:
        url = f"/{page_path}" if page_path else "/"
        languages.append(
            {
                "code": code,
                "name": labels[code],
                "url": url,
                "active": code == current,
            }
        )
    return {"site_languages": languages, "current_language": current}
