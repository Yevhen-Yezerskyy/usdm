from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from .language import preferred_language


PAGE_NAMES = {
    "home",
    "technology",
    "houses",
    "experience",
    "contact",
    "imprint",
    "privacy",
    "impressum",
    "datenschutz",
}


def language_entry(request):
    language = preferred_language(request)
    response = HttpResponseRedirect(f"/{language}/")
    response.set_cookie(
        settings.SITE_LANGUAGE_COOKIE_NAME,
        language,
        max_age=settings.SITE_LANGUAGE_COOKIE_MAX_AGE,
        samesite="Lax",
        secure=not settings.DEBUG,
    )
    return response


def page(request, lang, page_name):
    if lang not in settings.SITE_LANGUAGES or page_name not in PAGE_NAMES:
        raise Http404
    template_name = "pages/home.html" if page_name == "home" else "pages/placeholder.html"
    return render(request, template_name, {"page_name": page_name})
