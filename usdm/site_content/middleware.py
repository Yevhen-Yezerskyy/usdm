from django.conf import settings
from django.http import Http404
from django.utils import translation


class SiteLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        first_segment = request.path_info.strip("/").split("/", 1)[0].lower()
        if first_segment in settings.SITE_LANGUAGES:
            language = first_segment
        elif first_segment in {"health", "static", "media"} or not first_segment:
            language = settings.LANGUAGE_CODE
        else:
            raise Http404

        translation.activate(language)
        request.LANGUAGE_CODE = language
        try:
            response = self.get_response(request)
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
