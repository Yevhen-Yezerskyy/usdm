# USDM

Single-site Django stack for `dev.usdm.com.ua` and, later, `usdm.com.ua`.

The Django project lives in `usdm/`; that directory contains `manage.py`, the
`usdm_site` Python package, templates, and static assets.

## Runtime model

- `usdm-dev` mounts this host checkout at `/app` and runs Django `runserver`.
- `usdm-prod` mounts the internal Docker volume `usdm-prod-code` at `/app` and runs Gunicorn.
- `postgres` is shared by the dev and production processes.
- `nginx` is the only service exposed on ports 80 and 443.
- `contact-rate-guard` provides bounded, RAM-only request limits for the
  contact form; nginx and Django use independent counters.
- `certbot` owns ACME certificates and renewal.

## Languages and translations

- Ukrainian (`uk`) is the source and default language; German (`de`) is also
  supported.
- Public pages always use a language prefix: `/uk/...` or `/de/...`.
- A visit to `/` selects the language in this order: `usdm_language` cookie,
  `Accept-Language` header, then Ukrainian fallback.
- Visiting a prefixed URL activates that language and refreshes the cookie.
- UI strings use Django `{% translate %}` and are resolved at runtime from the
  `translation_sources` and `translation_values` database tables. Missing
  translations safely fall back to the Ukrainian source text.
- The language switcher preserves the current page while replacing its URL
  prefix.

## Git repository

- GitHub repository: `https://github.com/Yevhen-Yezerskyy/usdm`
- Host checkout remote: `git@github.com:Yevhen-Yezerskyy/usdm.git`
- Default and production branch: `main`
- The host uses the dedicated deploy key at
  `/home/eee/.ssh/id_ed25519_git_usdm`; its public half is registered in
  GitHub with write access.
- The SSH host entry in `/home/eee/.ssh/config` selects that key for
  `github.com`.
- Never commit `.env`, credentials, database dumps, uploaded media, logs, or
  collected static files.

## Runtime secrets

Runtime credentials live in the ignored host file `config/secrets.env`, which
must have mode `0600`. Compose injects it into PostgreSQL and both Django
services with `env_file`; the file is not mounted into the containers. Django
settings read the values from environment variables. It currently contains
the PostgreSQL database name, user and password, plus the required Django
secret key. Never put plaintext secret values in tracked code or Compose.

Contact requests are always stored in the `contact_requests` database table.
To also send notifications by e-mail, add `EMAIL_HOST`, `EMAIL_PORT`,
`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`,
`DEFAULT_FROM_EMAIL`, and `CONTACT_RECIPIENT_EMAIL` to the ignored secrets
file. If SMTP is not configured, submitting the form still stores the request.

The public form is protected by CSRF validation, a honeypot, a signed
two-hour browser-session token bound to the host and client IP, and layered
request limits in nginx and Django. The rate guard keeps no persistent data,
bans abusive keys for 24 hours, caps its in-memory key count, and fails open if
the helper service is unavailable so that an infrastructure fault cannot take
the form offline. Its paths must stay synchronized in
`site_content/contact_rate_limit.py` and `config/contact_rate_guard/server.py`.
Valid browser tokens are reused on later page loads, and the hidden form field
is synchronized from the cookie again immediately before submission so that
multiple tabs cannot invalidate a form being filled out.

## Production release

Production code must reach the internal `usdm-prod-code` volume through Git
only. Never copy the host checkout into the volume. If the volume is empty,
initialize it from the public, read-only HTTPS remote:

```bash
docker compose run --rm tools sh -lc \
  'git clone --branch main --single-branch https://github.com/Yevhen-Yezerskyy/usdm.git /app'
```

For subsequent releases, push the reviewed commit to `origin/main`, update the
volume with a fast-forward-only pull, and run the Django release steps:

```bash
git push origin main
docker compose run --rm tools sh -lc '
  git config --global --add safe.directory /app
  git -C /app remote get-url origin >/dev/null 2>&1 ||
    git -C /app remote add origin https://github.com/Yevhen-Yezerskyy/usdm.git
  git -C /app pull --ff-only origin main
'
docker compose run --rm usdm-prod python manage.py migrate
docker compose run --rm usdm-prod python manage.py collectstatic --noinput
docker compose up -d usdm-prod
```

Do not issue the `usdm.com.ua` certificate until its DNS points to this server.
