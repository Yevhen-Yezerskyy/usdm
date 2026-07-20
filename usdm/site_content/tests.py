from django.test import TestCase, override_settings

from .runtime_translation import refresh_runtime_translations


@override_settings(DEBUG=True)
class LanguageRoutingTests(TestCase):
    def setUp(self):
        refresh_runtime_translations()

    def test_default_language_is_ukrainian(self):
        response = self.client.get("/")
        self.assertRedirects(response, "/uk/", fetch_redirect_response=False)

    def test_accept_language_selects_german(self):
        response = self.client.get("/", HTTP_ACCEPT_LANGUAGE="de-DE,de;q=0.9,uk;q=0.8")
        self.assertRedirects(response, "/de/", fetch_redirect_response=False)

    def test_cookie_wins_over_accept_language(self):
        self.client.cookies["usdm_language"] = "uk"
        response = self.client.get("/", HTTP_ACCEPT_LANGUAGE="de")
        self.assertRedirects(response, "/uk/", fetch_redirect_response=False)

    def test_language_url_sets_cookie_and_translates(self):
        response = self.client.get("/de/technology/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies["usdm_language"].value, "de")
        self.assertContains(response, "Technologie")

    def test_switcher_preserves_page(self):
        response = self.client.get("/uk/houses/")
        self.assertContains(response, 'href="/de/houses/"')

        response = self.client.get("/de/houses/")
        self.assertContains(response, 'href="/uk/houses/"')
        self.assertContains(response, ">Українська</a>")

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
