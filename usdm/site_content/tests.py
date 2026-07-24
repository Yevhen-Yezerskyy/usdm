import tempfile
import sys
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase, override_settings

from .contact_form import ContactForm, MAX_TOTAL_UPLOAD_BYTES
from .contact_rate_limit import ContactRateLimitMiddleware, SESSION_COOKIE
from .runtime_translation import refresh_runtime_translations
from .models import ContactAttachment, ContactRequest
from .seo import PUBLIC_PAGE_NAMES, page_seo


@override_settings(DEBUG=True)
class LanguageRoutingTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_media = tempfile.TemporaryDirectory(prefix="usdm-test-media-")
        cls.media_override = override_settings(MEDIA_ROOT=cls.test_media.name)
        cls.media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.media_override.disable()
        cls.test_media.cleanup()

    def setUp(self):
        refresh_runtime_translations()

    def test_default_language_is_ukrainian(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Language"], "uk-UA")
        self.assertContains(response, "ВИРОБНИЦТВО КАРКАСНО-ПАНЕЛЬНИХ БУДИНКІВ")

    def test_accept_language_selects_german(self):
        response = self.client.get("/", HTTP_ACCEPT_LANGUAGE="de-DE,de;q=0.9,uk;q=0.8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Language"], "de-DE")
        self.assertContains(response, "HERSTELLUNG VON HOLZRAHMEN-PANELHÄUSERN")

    def test_cookie_wins_over_accept_language(self):
        self.client.cookies["usdm_language"] = "uk"
        response = self.client.get("/", HTTP_ACCEPT_LANGUAGE="de")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Language"], "uk-UA")

    def test_cookie_switcher_uses_a_clean_root_url(self):
        response = self.client.get("/")
        self.assertContains(response, 'href="/" data-language-switch="de"')

        self.client.cookies["usdm_language"] = "de"
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Language"], "de-DE")

    def test_language_url_sets_cookie_and_translates(self):
        response = self.client.get("/de/technology/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies["usdm_language"].value, "de")
        self.assertContains(response, "Technologie")

    def test_switcher_keeps_the_current_page_url(self):
        response = self.client.get("/uk/houses/")
        self.assertContains(response, 'href="/houses/" data-language-switch="de"')

        response = self.client.get("/de/houses/")
        self.assertContains(response, 'href="/houses/" data-language-switch="uk"')
        self.assertContains(response, ">Українська</a>")

    def test_cookie_page_uses_selected_language_without_redirect(self):
        self.client.cookies["usdm_language"] = "de"
        response = self.client.get("/houses/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Language"], "de-DE")
        self.assertContains(response, "Vorgefertigte Häuser")

    def test_ukrainian_navigation_matches_source_site(self):
        response = self.client.get("/uk/")
        self.assertContains(response, ">Home</a>")
        self.assertContains(response, ">Технології</a>")
        self.assertContains(response, ">Контакт</a>")

    def test_footer_contains_all_representatives(self):
        response = self.client.get("/uk/")
        self.assertContains(response, "Представник у Німеччині")
        self.assertContains(response, "Представник у Швеції")
        self.assertContains(response, "Представник в Ісландії")
        self.assertContains(response, "Представник у Франції")
        self.assertContains(response, 'href="/uk/impressum/"')

    def test_footer_is_translated_to_german(self):
        response = self.client.get("/de/")
        self.assertContains(response, "HOLZRAHMEN-PANELHÄUSER")
        self.assertContains(response, "Vertretung in Deutschland")
        self.assertContains(response, "Modulare Holzrahmen-Panelhäuser")

    def test_home_contains_reusable_intro_sections(self):
        response = self.client.get("/uk/")
        self.assertTemplateUsed(response, "pages/home.html")
        self.assertContains(response, 'class="hero hero--parallax hero--home"')
        self.assertContains(response, "data-parallax")
        self.assertContains(response, 'class="feature-grid layout-row"')
        self.assertContains(response, "ВИРОБНИЦТВО ТА ЕКСПОРТ")
        self.assertContains(response, "/static/img/home-production.jpg")
        self.assertContains(response, 'href="/uk/technology/"')
        self.assertContains(response, 'href="/uk/houses/"')

    def test_home_intro_is_translated_to_german(self):
        response = self.client.get("/de/")
        self.assertContains(response, "HERSTELLUNG VON HOLZRAHMEN-PANELHÄUSERN")
        self.assertContains(response, "PRODUKTION UND EXPORT")
        self.assertContains(response, "PRÄSENTATION HERUNTERLADEN")
        self.assertContains(response, 'href="/de/technology/"')

    def test_home_contains_all_source_sections(self):
        response = self.client.get("/uk/")
        self.assertContains(response, "ТЕХНОЛОГІЇ ТА РОЗТАШУВАННЯ")
        self.assertContains(response, "ПРОДУКЦІЯ ТА РОБОТИ")
        self.assertContains(response, "ПРО КОМПАНІЮ")
        self.assertContains(response, "ДОСВІД ТОВ “ЮСДМ”")
        self.assertContains(response, "/static/img/home-house-393.jpg")
        self.assertContains(response, 'class="feature-grid feature-grid--three layout-row"')
        self.assertContains(response, 'class="hero hero--parallax hero--panels"')

    def test_complete_home_is_translated_to_german(self):
        response = self.client.get("/de/")
        self.assertContains(response, "Technologien und Standorte")
        self.assertContains(response, "Produkte und Leistungen")
        self.assertContains(response, "Über das Unternehmen")
        self.assertContains(response, "Unsere realisierten Projekte ansehen")
        self.assertContains(response, "Bausätze für den Holzrahmen-Panelbau")

    def test_unknown_language_is_not_a_page(self):
        self.assertEqual(self.client.get("/fr/").status_code, 404)

    def test_internal_pages_use_their_real_templates_and_heading_style(self):
        expected = {
            "technology": "pages/technology.html",
            "houses": "pages/houses.html",
            "experience": "pages/experience.html",
            "contact": "pages/contact.html",
            "impressum": "pages/legal.html",
            "datenschutz": "pages/legal.html",
        }
        for page_name, template_name in expected.items():
            with self.subTest(page=page_name):
                response = self.client.get(f"/uk/{page_name}/")
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)

        self.assertContains(self.client.get("/uk/technology/"), "section-heading--inner")
        self.assertNotContains(self.client.get("/uk/"), "section-heading--inner")

    def test_houses_contains_all_projects_carousels_lightboxes_and_documents(self):
        response = self.client.get("/uk/houses/")
        self.assertEqual(response.content.count(b"data-carousel "), 13)
        self.assertEqual(response.content.count(b"data-lightbox-gallery"), 13)
        self.assertContains(response, "/static/docs/132m2-Price-USDM.pdf")
        self.assertContains(response, "/static/docs/429m2-Presentation-USDM.pdf")
        self.assertContains(response, "Передпокій")
        self.assertContains(response, "Загальна площа будинку")
        self.assertContains(
            response,
            '<p class="project-price"><strong><span>Загальна вартість</span><span>137 344 €</span></strong></p>',
            html=True,
        )
        self.assertContains(response, "<em>У вартість будинку входить: каркас, вікна, зовнішні двері, жалюзі, монтаж, зовнішнє оздоблення, покрівля.</em>", html=True)
        self.assertContains(response, "<strong>Перший поверх</strong>", html=True)
        self.assertContains(response, "<strong>132,7 м2</strong>", html=True)
        self.assertContains(
            response,
            "<p class=\"hero__subtitle\">приклади префабрикованних будинків<br>зовнішний вигляд, планування та ціни</p>",
            html=True,
        )

    def test_technology_preserves_source_emphasis(self):
        response = self.client.get("/uk/technology/")
        self.assertContains(
            response,
            "<strong>Використовуємо модульну технологію будівництва.</strong>",
            html=True,
        )
        self.assertContains(response, "<strong>Архітектурна група</strong>", html=True)
        self.assertContains(response, "<strong>Інженери та технологи</strong>", html=True)

    def test_experience_galleries_are_complete_and_open_in_lightbox(self):
        response = self.client.get("/uk/experience/")
        self.assertEqual(response.content.count(b"data-lightbox-gallery"), 3)
        self.assertEqual(response.content.count(b"data-lightbox-item"), 76)
        self.assertContains(response, "Технологія, доставка, монтаж")

    def test_internal_pages_are_translated_to_german(self):
        technology = self.client.get("/de/technology/")
        self.assertContains(technology, "Rahmen und Paneele für Häuser")
        houses = self.client.get("/de/houses/")
        self.assertContains(houses, "Zweigeschossiges Haus mit Satteldach 132 m2")
        self.assertContains(houses, "Gesamtfläche des Hauses")
        experience = self.client.get("/de/experience/")
        self.assertContains(experience, "Beispiele realisierter Projekte")
        contact = self.client.get("/de/contact/")
        self.assertContains(contact, "Ihr Vorname *")
        legal = self.client.get("/de/datenschutz/")
        self.assertContains(legal, "Datenschutzerklärung")
        self.assertContains(legal, "keine Webanalyse")
        imprint = self.client.get("/de/impressum/")
        self.assertContains(imprint, "Angaben zum Eigentümer und Betreiber")

    def test_contact_form_validates_and_stores_requests_with_attachments(self):
        invalid = self.client.post(
            "/uk/contact/send/",
            {
                "first_name": "Test",
                "email": "bad",
                "phone": "text",
                "message": "",
                "next": "/uk/contact/",
            },
        )
        self.assertRedirects(
            invalid,
            "/uk/contact/#contact-form",
            fetch_redirect_response=False,
        )
        page = self.client.get("/uk/contact/")
        self.assertEqual(
            set(page.context["contact_errors"]),
            {"email", "phone", "message", "privacy"},
        )
        self.assertEqual(ContactRequest.objects.count(), 0)

        valid = self.client.post(
            "/uk/contact/send/",
            {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "phone": "+380000000000",
                "message": "Test request",
                "privacy": "on",
                "next": "/uk/contact/",
                "files": SimpleUploadedFile(
                    "plan.pdf",
                    b"test plan",
                    content_type="application/pdf",
                ),
            },
        )
        self.assertRedirects(
            valid,
            "/uk/contact/#contact-form",
            fetch_redirect_response=False,
        )
        request = ContactRequest.objects.get()
        self.assertEqual(request.language, "uk")
        self.assertEqual(request.email, "test@example.com")
        attachment = ContactAttachment.objects.get(request=request)
        self.assertEqual(attachment.original_name, "plan.pdf")
        self.assertEqual(attachment.size, 9)
        status_page = self.client.get("/uk/contact/")
        self.assertEqual(status_page.context["contact_status"]["name"], "success")
        self.assertEqual(self.client.get("/uk/contact/").context["contact_status"]["name"], "")

    def test_contact_form_security_and_limits(self):
        self.assertEqual(self.client.get("/uk/contact/send/").status_code, 405)
        csrf_response = Client(enforce_csrf_checks=True).post(
            "/uk/contact/send/",
            {
                "first_name": "Test",
                "email": "test@example.com",
                "phone": "+380000000000",
                "message": "Test request",
                "privacy": "on",
            },
        )
        self.assertEqual(csrf_response.status_code, 403)

        honeypot = self.client.post(
            "/uk/contact/send/",
            {"website": "https://spam.example", "next": "/uk/contact/"},
        )
        self.assertEqual(honeypot.status_code, 302)
        self.assertEqual(ContactRequest.objects.count(), 0)

        self.assertEqual(MAX_TOTAL_UPLOAD_BYTES, 25 * 1024 * 1024)
        form = ContactForm(
            {
                "first_name": "Test",
                "email": "test@example.com",
                "phone": "+380000000000",
                "message": "Test request",
                "privacy": True,
            },
            {"files": [SimpleUploadedFile("malware.exe", b"bad")]},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("files", form.errors)

    def test_contact_form_requires_a_signed_browser_session(self):
        middleware = ContactRateLimitMiddleware(
            lambda request: HttpResponse("page", content_type="text/html")
        )
        factory = RequestFactory()
        browser_argv = ["manage.py", "runserver"]

        page_request = factory.get(
            "/uk/contact/", HTTP_HOST="localhost:8000", REMOTE_ADDR="192.0.2.10"
        )
        with patch.object(sys, "argv", browser_argv):
            page_response = middleware(page_request)
        token = page_response.cookies[SESSION_COOKIE].value
        self.assertEqual(page_response.cookies[SESSION_COOKIE]["max-age"], 7200)

        later_page_request = factory.get(
            "/de/technology/", HTTP_HOST="localhost:8000", REMOTE_ADDR="192.0.2.10"
        )
        later_page_request.COOKIES[SESSION_COOKIE] = token
        with patch.object(sys, "argv", browser_argv):
            later_page_response = middleware(later_page_request)
        self.assertNotIn(SESSION_COOKIE, later_page_response.cookies)

        post_request = factory.post(
            "/uk/contact/send/",
            {"contact_session": token},
            HTTP_HOST="localhost:8000",
            REMOTE_ADDR="192.0.2.10",
        )
        post_request.COOKIES[SESSION_COOKIE] = token
        with (
            patch.object(sys, "argv", browser_argv),
            patch.object(middleware, "_guard_allows", return_value=(True, 0)),
        ):
            self.assertEqual(middleware(post_request).status_code, 200)

        bad_request = factory.post(
            "/de/contact/send/",
            {"contact_session": token},
            HTTP_HOST="localhost:8000",
            REMOTE_ADDR="192.0.2.11",
        )
        bad_request.COOKIES[SESSION_COOKIE] = token
        with patch.object(sys, "argv", browser_argv):
            blocked = middleware(bad_request)
        self.assertEqual(blocked.status_code, 429)
        self.assertEqual(blocked["Retry-After"], "60")

    def test_cookie_notice_uses_standard_serenity_categories_and_text(self):
        response = self.client.get("/uk/")
        self.assertContains(response, 'data-consent-cookie="usdm_cookie_consent_v2"')
        self.assertContains(
            response,
            'data-consent-categories="statistics external_media"',
        )
        self.assertContains(response, "Datenschutz-Einstellungen")
        self.assertContains(response, "Nur notwendige")
        self.assertContains(response, "Externe Medien")

        german = self.client.get("/de/")
        self.assertContains(
            german,
            "Wir verwenden notwendige Cookies sowie optionale Dienste",
        )
        self.assertContains(german, "Cookie-Einstellungen")

        contact = self.client.get("/uk/contact/")
        self.assertContains(contact, 'name="contact_session"')
        self.assertContains(contact, "usdm_contact_session=")
        self.assertContains(contact, 'field.form.addEventListener("submit", syncSession)')
        self.assertContains(contact, 'class="contact-honeypot"')

    def test_original_wordpress_urls_redirect_to_language_routes(self):
        redirects = {
            "/timber-frame-panel-modular-technology/": "/uk/technology/",
            "/prefab-houses/": "/uk/houses/",
            "/experience-modular-frame-panel/": "/uk/experience/",
            "/usdm-contacts-timber-frame-modular/": "/uk/contact/",
            "/impressum/": "/uk/impressum/",
            "/datenschutz/": "/uk/datenschutz/",
            "/de/technologie/": "/de/technology/",
            "/de/fertighaeuser/": "/de/houses/",
            "/de/erfahrung/": "/de/experience/",
            "/de/kontakt/": "/de/contact/",
        }
        for source, target in redirects.items():
            with self.subTest(source=source):
                response = self.client.get(source)
                self.assertEqual(response.status_code, 301)
                self.assertEqual(response["Location"], target)

    def test_seo_metadata_and_gtm_are_rendered_independently_of_cookie_consent(self):
        response = self.client.get("/de/technology/")
        self.assertContains(
            response,
            "Technologie für Holzrahmen-Panelhäuser | USDM",
        )
        self.assertContains(response, 'rel="canonical" href="https://usdm.com.ua/de/technology/"')
        self.assertContains(response, 'hreflang="uk-UA" href="https://usdm.com.ua/uk/technology/"')
        self.assertContains(response, 'property="og:image" content="https://usdm.com.ua/static/img/og-technology.jpg"')
        self.assertEqual(response["Content-Language"], "de-DE")
        self.assertContains(response, 'type="application/ld+json"')
        self.assertContains(response, '"@type":"ImageObject"')
        self.assertContains(response, '"@type":"BreadcrumbList"')
        self.assertContains(response, "GTM-K95Z727")
        self.assertNotContains(response, "data-consent-gtm")

    def test_public_pages_have_one_h1_and_complete_seo_metadata(self):
        for language in ("uk", "de"):
            for page_name in PUBLIC_PAGE_NAMES:
                with self.subTest(language=language, page=page_name):
                    path = "/{}/{}".format(language, "" if page_name == "home" else f"{page_name}/")
                    response = self.client.get(path)
                    seo = page_seo(language, page_name)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.content.count(b"<h1"), 1)
                    self.assertContains(response, f"<title>{seo['title']}</title>", html=True)
                    self.assertContains(response, f'name="description" content="{seo["description"]}"')
                    self.assertContains(response, 'property="og:image:alt"')
                    self.assertContains(response, f'<html lang="{seo["language_tag"]}">')
                    self.assertEqual(response["Content-Language"], seo["language_tag"])

    def test_content_images_have_contextual_alternatives(self):
        houses = self.client.get("/uk/houses/")
        self.assertContains(houses, 'alt="Префабриковані будинки"')
        self.assertContains(houses, 'alt="Двоповерховий будинок зі скатним дахом 132 м2. — 1"')
        self.assertContains(houses, 'aria-label="Двоповерховий будинок зі скатним дахом 132 м2. — 1"')

        experience = self.client.get("/uk/experience/")
        self.assertContains(experience, 'alt="Досвід збудованого"')
        self.assertContains(experience, 'alt="Приклади збудованого — 1"')

    @override_settings(DEBUG=False)
    def test_production_robots_and_sitemap_expose_only_canonical_pages(self):
        robots = self.client.get("/robots.txt")
        self.assertEqual(robots.status_code, 200)
        self.assertContains(robots, "Allow: /")
        self.assertContains(robots, "Sitemap: https://usdm.com.ua/sitemap.xml")

        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap.status_code, 200)
        self.assertEqual(sitemap["Content-Type"], "application/xml; charset=utf-8")
        self.assertEqual(sitemap.content.count(b"<url>"), 14)
        self.assertEqual(sitemap.content.count(b"<xhtml:link"), 42)
        self.assertContains(sitemap, 'hreflang="uk-UA"')
        self.assertContains(sitemap, 'hreflang="x-default"')
        self.assertNotContains(sitemap, "<lastmod>")
        self.assertContains(sitemap, "https://usdm.com.ua/de/technology/")
        self.assertNotContains(sitemap, "/de/technologie/")
