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

    def test_ukrainian_navigation_matches_source_site(self):
        response = self.client.get("/uk/")
        self.assertContains(response, ">Home</a>")
        self.assertContains(response, ">Технології</a>")
        self.assertContains(response, ">Контакт</a>")

    def test_unknown_language_is_not_a_page(self):
        self.assertEqual(self.client.get("/fr/").status_code, 404)
