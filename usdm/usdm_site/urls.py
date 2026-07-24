from django.urls import path

from site_content.contact_form import submit_contact
from site_content.views import cookie_page, language_entry, legacy_page_redirect, page, robots_txt, sitemap_xml

from .views import health

urlpatterns = [
    path("", language_entry, name="language_entry"),
    path("health/", health, name="health"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
    path("sitemap_index.xml", sitemap_xml),
    path("page-sitemap.xml", sitemap_xml),
    path("timber-frame-panel-modular-technology/", legacy_page_redirect, {"lang": "uk", "page_name": "technology"}),
    path("prefab-houses/", legacy_page_redirect, {"lang": "uk", "page_name": "houses"}),
    path("experience-modular-frame-panel/", legacy_page_redirect, {"lang": "uk", "page_name": "experience"}),
    path("usdm-contacts-timber-frame-modular/", legacy_page_redirect, {"lang": "uk", "page_name": "contact"}),
    path("technology/", cookie_page, {"page_name": "technology"}),
    path("houses/", cookie_page, {"page_name": "houses"}),
    path("experience/", cookie_page, {"page_name": "experience"}),
    path("contact/", cookie_page, {"page_name": "contact"}),
    path("imprint/", cookie_page, {"page_name": "imprint"}),
    path("privacy/", cookie_page, {"page_name": "privacy"}),
    path("impressum/", legacy_page_redirect, {"lang": "uk", "page_name": "impressum"}),
    path("datenschutz/", legacy_page_redirect, {"lang": "uk", "page_name": "datenschutz"}),
    path("de/technologie/", legacy_page_redirect, {"lang": "de", "page_name": "technology"}),
    path("de/fertighaeuser/", legacy_page_redirect, {"lang": "de", "page_name": "houses"}),
    path("de/erfahrung/", legacy_page_redirect, {"lang": "de", "page_name": "experience"}),
    path("de/kontakt/", legacy_page_redirect, {"lang": "de", "page_name": "contact"}),
    path("<str:lang>/", page, {"page_name": "home"}, name="home"),
    path("<str:lang>/technology/", page, {"page_name": "technology"}, name="technology"),
    path("<str:lang>/houses/", page, {"page_name": "houses"}, name="houses"),
    path("<str:lang>/experience/", page, {"page_name": "experience"}, name="experience"),
    path("<str:lang>/contact/", page, {"page_name": "contact"}, name="contact"),
    path("<str:lang>/contact/send/", submit_contact, name="contact_submit"),
    path("<str:lang>/imprint/", page, {"page_name": "imprint"}, name="imprint"),
    path("<str:lang>/privacy/", page, {"page_name": "privacy"}, name="privacy"),
    path("<str:lang>/impressum/", page, {"page_name": "impressum"}, name="impressum"),
    path("<str:lang>/datenschutz/", page, {"page_name": "datenschutz"}, name="datenschutz"),
]
