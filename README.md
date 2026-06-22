# Learn KAOS

Tested, multi-learner documentation and **one-command runnable examples** for the
open-source [KAOS](https://github.com/273v) (Kelvin Agentic OS) ecosystem.

The site is built with **Astro Starlight**. Its defining property: **every code
sample is tested**. Examples are self-contained
[PEP 723](https://peps.python.org/pep-0723/) scripts; docs pages import those exact
files byte-for-byte (via Vite `?raw`), so what you read is what CI runs.

> Built in public, milestone by milestone. This is **M0**: the scaffold, the
> offline-tested pipeline, and the first golden-path pages.

## Repository layout

```
src/                Astro Starlight site (content under src/content/docs/)
examples/           PEP 723 one-command examples + index.toml (gallery manifest)
snippets/           tested doc fragments (imported into MDX) — grows in M1
tests/              pytest harness (snippets-test) over the examples
scripts/            embed_check.py, gen_reference.py, kaos_learn.py launcher
.github/workflows/  ci.yml (6 jobs) + deploy.yml (GitHub Pages)
```

Python tooling lives at the repo root (`examples/`, `snippets/`, `tests/`,
`scripts/`) — deliberately *outside* Astro's `src/` so the site build never
processes Python files.

## Develop the site

```bash
pnpm install          # Node 22, pnpm 10 (see .nvmrc / .npmrc)
pnpm dev              # local dev server
pnpm build            # static build into dist/
```

Conventions match [273ventures.com](https://273ventures.com): pnpm, Node 22,
Tailwind v4 via `@tailwindcss/vite`, `~`/`@` → `src` aliases.

## Run the examples

```bash
uv run examples/citations-extract.py        # local
python3 scripts/kaos_learn.py list          # discover examples
python3 scripts/kaos_learn.py run graph-pagerank
```

Or run any example with **zero clone**:

```bash
uv run https://raw.githubusercontent.com/273v/learn-kaos/main/examples/citations-extract.py
```

## Test like CI does

```bash
for f in examples/*.py; do uv run "$f"; done   # examples-smoke
uv run --with pytest pytest tests/ -q          # snippets-test
python3 scripts/embed_check.py                 # embed-check
python3 scripts/gen_reference.py               # reference-gen
pnpm build                                     # site-build
```

All offline — no API keys, no network models. LLM examples (landing in M1) use a
deterministic in-process fake model and only call a real provider when
`KAOS_LEARN_LIVE=1` is set.

## License

[Apache-2.0](LICENSE) — matching the rest of the KAOS ecosystem.
