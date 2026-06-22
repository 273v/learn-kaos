---
title: Deploy a KAOS app
description: Take a scaffolded web:spa app from dev to a deployed service.
---

The [capstone](/tutorials/build-an-app) scaffolds a `web:spa` app with deployment wired in —
a `Dockerfile`, `docker-compose.yml`, and a `Caddyfile` for TLS. Here's the path to a running
service.

:::caution[Manual / infrastructure step]
Deployment runs real infrastructure (and the app calls a live LLM), so it isn't exercised in
this site's CI. The generated project's `README.md` and `Makefile` are the source of truth;
this is an overview.
:::

## From scaffold to deployed

```bash
kaos-ui new web:spa my-legal-app && cd my-legal-app
make install            # uv (backend) + pnpm (frontend), supply-chain hardened
make dev                # local dev servers (FastAPI + Vite)

# containerized: build + run behind Caddy (TLS, reverse proxy)
docker compose up --build
```

## Notes

- The generated `Caddyfile` terminates TLS and reverse-proxies the API and the built SPA;
  add your domain and Caddy handles certificates.
- Set the app's auth token (`APP_AUTH_TOKEN`) and a provider API key in the environment; the
  `.env.example` lists what's needed.
- **PyPI gap:** until every `kaos-*` package the app depends on is published, you may need to
  install some from source — the project README spells this out.
- The app's architecture (auth, SSE streaming, per-session VFS, tool allowlist) is explained
  in [anatomy of a KAOS app](/concepts/anatomy-of-single-user-chat).
