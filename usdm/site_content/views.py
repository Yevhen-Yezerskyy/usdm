from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from xml.sax.saxutils import escape

from .page_content import CONTACT_CONTENT, EXPERIENCE_CONTENT, HOUSES_CONTENT, LEGAL_CONTENT
from .seo import page_path, page_seo, sitemap_pages


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

PAGE_TEMPLATES = {
    "home": "pages/home.html",
    "technology": "pages/technology.html",
    "houses": "pages/houses.html",
    "experience": "pages/experience.html",
    "contact": "pages/contact.html",
    "imprint": "pages/legal.html",
    "privacy": "pages/legal.html",
    "impressum": "pages/legal.html",
    "datenschutz": "pages/legal.html",
}

PAGE_CONTENT = {
    "houses": HOUSES_CONTENT,
    "experience": EXPERIENCE_CONTENT,
    "contact": CONTACT_CONTENT,
    "imprint": LEGAL_CONTENT["impressum"],
    "privacy": LEGAL_CONTENT["datenschutz"],
    "impressum": LEGAL_CONTENT["impressum"],
    "datenschutz": LEGAL_CONTENT["datenschutz"],
}


def language_entry(request):
    # The root is the cookie/Accept-Language entry point. Explicit language
    # URLs remain independently addressable for people and search engines.
    return page(request, request.LANGUAGE_CODE, "home")


def legacy_page_redirect(request, lang, page_name):
    return HttpResponseRedirect(reverse(page_name, kwargs={"lang": lang}), status=301)


def page(request, lang, page_name):
    if lang not in settings.SITE_LANGUAGES or page_name not in PAGE_NAMES:
        raise Http404
    template_name = PAGE_TEMPLATES.get(page_name, "pages/placeholder.html")
    context = {
        "page_name": page_name,
        "page_content": PAGE_CONTENT.get(page_name),
        "page_title": page_name.title(),
        "seo": page_seo(lang, page_name),
    }

    return render(
        request,
        template_name,
        context,
    )


def robots_txt(request):
    if settings.DEBUG:
        body = "User-agent: *\nDisallow: /\n"
    else:
        body = "\n".join(
            [
                "User-agent: *",
                "Allow: /",
                "Disallow: /health/",
                "Disallow: /uk/contact/send/",
                "Disallow: /de/contact/send/",
                f"Sitemap: {settings.SITE_PUBLIC_URL.rstrip('/')}/sitemap.xml",
                "",
            ]
        )
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    site_url = settings.SITE_PUBLIC_URL.rstrip("/")
    entries = []
    for language, page_name, url in sitemap_pages():
        alternates = "".join(
            '<xhtml:link rel="alternate" hreflang="{hreflang}" href="{url}"/>'.format(
                hreflang=hreflang,
                url=escape(f"{site_url}{page_path(language_code, page_name)}"),
            )
            for hreflang, language_code in (("uk-UA", "uk"), ("de-DE", "de"))
        )
        alternates += '<xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>'.format(
            url=escape(f"{site_url}{page_path('uk', page_name)}"),
        )
        entries.append(
            "<url><loc>{url}</loc>{alternates}<changefreq>weekly</changefreq><priority>{priority}</priority></url>".format(
                url=escape(url),
                alternates=alternates,
                priority="1.0" if page_name == "home" else "0.8",
            )
        )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        f"{''.join(entries)}</urlset>"
    )
    return HttpResponse(body, content_type="application/xml; charset=utf-8")
