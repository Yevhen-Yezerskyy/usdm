from django.urls import path

from site_content.views import language_entry, page

from .views import health

urlpatterns = [
    path("", language_entry, name="language_entry"),
    path("health/", health, name="health"),
    path("<str:lang>/", page, {"page_name": "home"}, name="home"),
    path("<str:lang>/technology/", page, {"page_name": "technology"}, name="technology"),
    path("<str:lang>/houses/", page, {"page_name": "houses"}, name="houses"),
    path("<str:lang>/experience/", page, {"page_name": "experience"}, name="experience"),
    path("<str:lang>/contact/", page, {"page_name": "contact"}, name="contact"),
    path("<str:lang>/imprint/", page, {"page_name": "imprint"}, name="imprint"),
    path("<str:lang>/privacy/", page, {"page_name": "privacy"}, name="privacy"),
]
