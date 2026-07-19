# USDM

Single-site Django stack for `dev.usdm.com.ua` and, later, `usdm.com.ua`.

## Runtime model

- `usdm-dev` mounts this host checkout at `/app` and runs Django `runserver`.
- `usdm-prod` mounts the internal Docker volume `usdm-prod-code` at `/app` and runs Gunicorn.
- `postgres` is shared by the dev and production processes.
- `nginx` is the only service exposed on ports 80 and 443.
- `certbot` owns ACME certificates and renewal.

## Production release

Commit the intended code first, then copy the checkout into the production volume:

```bash
docker compose run --rm tools sh -lc 'find /app -mindepth 1 -maxdepth 1 -exec rm -rf -- {} + && cp -a /app-dev/. /app/'
docker compose run --rm usdm-prod python manage.py migrate
docker compose run --rm usdm-prod python manage.py collectstatic --noinput
docker compose up -d usdm-prod
```

Do not issue the `usdm.com.ua` certificate until its DNS points to this server.
