# Contact-form spam protection

The public form is protected by independent nginx and Django rate-limit
namespaces, a signed browser-session token, Django CSRF validation and a
server-side honeypot. The guard keeps only recent timestamps and bans in RAM;
it deliberately fails open if the guard service itself is unavailable.

For `/uk/contact/send/` and `/de/contact/send/`, nginx checks the guard before
Django receives a request. Django then requires the exact signed
`usdm_contact_session` value from both the browser cookie and the hidden form
field, before making a second guard request in its own namespace. The form
script populates that field; a simple HTTP client cannot submit successfully.

Keep the route lists in `server.py` and `usdm/site_content/contact_rate_limit.py`
in sync. Do not log submitted form contents, attachments or session tokens.

Check the protection with:

```sh
docker compose exec -T usdm-dev python manage.py test site_content.tests --noinput
docker compose run --rm --no-deps contact-rate-guard python /app/test_server.py
docker compose config --quiet
docker compose exec -T nginx nginx -t
```
