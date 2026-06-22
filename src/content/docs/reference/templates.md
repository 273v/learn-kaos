---
title: App templates
description: The project templates kaos-ui scaffolds, and what each produces.
---

`kaos-ui new <kind> <name>` (or `scaffold(kind, name)`) generates a working project. You
ran the `web:spa` capstone in [build an app](/tutorials/build-an-app). The six kinds:

| Kind | Stack | What you get | Post-install |
|---|---|---|---|
| `web:spa` | FastAPI on kaos-agents + Vite/React + Tailwind + Caddy + Docker | Full-stack app: login → bearer → SPA calls `/v1/*` (chat, documents, search, upload) | `make install` (uv + pnpm, hardened), `make dev` |
| `web:api` | FastAPI on kaos-core | REST backend only | `make install`, `make dev` |
| `dashboard:streamlit` | Streamlit | A data dashboard app | `make install`, `make up` |
| `tui:textual` | Textual | A terminal UI app | `make install`, `make dev` |
| `module` | KAOS package skeleton | A new kaos-compatible module (tools, settings, tests) | `make install` |
| `workflow` | Single file | A one-off Python script | — |

Every template ships a `Makefile`, `.env.example`, `Dockerfile` + `docker-compose.yml`,
`CLAUDE.md`/`AGENTS.md`, a pre-commit config, and a smoke test. The frontend templates
apply pnpm supply-chain hardening (release-age cooldown, blocked exotic specifiers,
reviewed build scripts).

```bash
kaos-ui list                 # see all kinds
kaos-ui info web:spa         # details for one
kaos-ui new web:spa my-app   # scaffold
kaos-ui doctor               # health-check the environment
```

Add your own kind with `register_template()` — the CLI and MCP tools pick it up
automatically.
