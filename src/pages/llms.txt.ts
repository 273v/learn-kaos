// Generates /llms.txt — an AI-consumable index of the whole site, following
// the llms.txt convention (https://llmstxt.org/). Built from the docs content
// collection so it can never drift from the actual pages. Fitting for an
// agentic OS: the docs are first-class context for coding agents.
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

const SITE = 'https://273v.github.io/learn-kaos';

const SECTION_ORDER = [
  ['', 'Start here'],
  ['get-started/', 'Get started'],
  ['tutorials/', 'Tutorials'],
  ['how-to/', 'How-to guides'],
  ['concepts/', 'Concepts'],
  ['reference/', 'Reference'],
] as const;

function sectionFor(id: string): string {
  for (const [prefix, label] of SECTION_ORDER) {
    if (prefix && id.startsWith(prefix)) return label;
  }
  return 'Start here';
}

export const GET: APIRoute = async () => {
  const docs = await getCollection('docs');
  const bySection = new Map<string, string[]>();

  for (const doc of docs) {
    const id = doc.id.replace(/\.(md|mdx)$/, '');
    if (id === 'index') continue;
    const label = sectionFor(id);
    const desc = doc.data.description ? `: ${doc.data.description}` : '';
    const line = `- [${doc.data.title}](${SITE}/${id})${desc}`;
    if (!bySection.has(label)) bySection.set(label, []);
    bySection.get(label)!.push(line);
  }

  const parts: string[] = [
    '# Learn KAOS',
    '',
    '> Tested, multi-learner documentation and one-command runnable examples for the',
    '> open-source KAOS (Kelvin Agentic OS) ecosystem. Every example is a self-contained',
    '> `uv run` script; every code snippet on a page is imported from a file that runs in CI.',
    '',
    'KAOS is a stack of composable kaos-* Python/Rust packages for agentic legal and',
    'financial data work: a runtime and document model, ingestion, typed LLM programming,',
    'a stateful agent runtime, a deterministic NLP/graph/citation substrate, and app',
    'scaffolding. See the package reference for the full list.',
    '',
  ];

  for (const [, label] of SECTION_ORDER) {
    const lines = bySection.get(label);
    if (!lines || lines.length === 0) continue;
    parts.push(`## ${label}`, '', ...lines.sort(), '');
  }

  return new Response(parts.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
