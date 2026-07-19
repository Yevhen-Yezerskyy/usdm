# Project rules

- This repository hosts one Django site on one VPS.
- Development runs from the host checkout mounted at `/app`.
- Production runs from the internal `usdm-prod-code` volume mounted at `/app`.
- Never mount the host checkout into `usdm-prod`.
- Keep site configuration in Django settings, not in Compose.
- Do not commit `.env`, plaintext secrets, runtime media, logs, or collected static files.
- Issue a certificate for `usdm.com.ua` only after its DNS points to this server.

