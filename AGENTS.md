# Project rules

- This repository hosts one Django site on one VPS.
- Development runs from the host checkout mounted at `/app`.
- Production runs from the internal `usdm-prod-code` volume mounted at `/app`.
- Update and deploy the code in the internal `usdm-prod-code` production volume only through Git. Do not copy code into that volume directly from the host checkout or by any other out-of-band method.
- Never mount the host checkout into `usdm-prod`.
- Keep site configuration in Django settings, not in Compose.
- Runtime secrets live only in the ignored `config/secrets.env` file. Keep application code reading them from environment variables.
- Do not commit `.env`, `config/secrets.env`, plaintext secrets, runtime media, logs, or collected static files.
- Issue a certificate for `usdm.com.ua` only after its DNS points to this server.
