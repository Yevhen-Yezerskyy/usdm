from django.conf import settings
from django.http import Http404
from django.utils import translation

from .language import preferred_language


class SiteLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        first_segment = request.path_info.strip("/").split("/", 1)[0].lower()
        if first_segment in settings.SITE_LANGUAGES:
            language = first_segment
        elif not first_segment:
            language = preferred_language(request)
        elif first_segment in {
            "health",
            "robots.txt",
            "sitemap.xml",
            "sitemap_index.xml",
            "page-sitemap.xml",
            "static",
            "media",
            "timber-frame-panel-modular-technology",
            "prefab-houses",
            "experience-modular-frame-panel",
            "usdm-contacts-timber-frame-modular",
            "impressum",
            "datenschutz",
        }:
            language = settings.LANGUAGE_CODE
        else:
            raise Http404

        translation.activate(language)
        request.LANGUAGE_CODE = language
        try:
            response = self.get_response(request)
            if first_segment in settings.SITE_LANGUAGES or not first_segment:
                response["Content-Language"] = "de-DE" if language == "de" else "uk-UA"
            if first_segment in settings.SITE_LANGUAGES:
                response.set_cookie(
                    settings.SITE_LANGUAGE_COOKIE_NAME,
                    language,
                    max_age=settings.SITE_LANGUAGE_COOKIE_MAX_AGE,
                    samesite="Lax",
                    secure=not settings.DEBUG,
                )
            return response
        finally:
            translation.deactivate()
