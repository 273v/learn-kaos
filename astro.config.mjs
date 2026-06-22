// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { visit } from 'unist-util-visit';

const BASE = '/learn-kaos';

// Starlight base-prefixes sidebar/nav links but NOT links written in page
// *content* (`[text](/path)` in md/mdx). This rehype plugin prepends the base
// to root-relative internal links so content links don't 404 on the project
// Pages site. (Hero `actions` are frontmatter, not content — they hardcode the
// base on the home page.)
function rehypeBaseLinks() {
  return (tree) => {
    visit(tree, 'element', (node) => {
      if (node.tagName !== 'a') return;
      const href = node.properties?.href;
      if (typeof href !== 'string') return;
      // root-relative, not external, not already based, not an anchor
      if (
        href.startsWith('/') &&
        !href.startsWith('//') &&
        href !== BASE &&
        !href.startsWith(BASE + '/')
      ) {
        node.properties.href = BASE + href;
      }
    });
  };
}

// Learn KAOS — Astro Starlight. Conventions match 273ventures.com:
// pnpm, Node 22, Tailwind v4 via @tailwindcss/vite, ~/@ -> src aliases.
// Sidebar grows as milestones land (M0 ships Start-here + Gallery).
// https://astro.build/config
export default defineConfig({
  site: 'https://273v.github.io',
  base: BASE,
  trailingSlash: 'never',

  markdown: {
    rehypePlugins: [rehypeBaseLinks],
  },

  integrations: [
    starlight({
      title: 'Learn KAOS',
      description:
        'Tested, multi-learner docs and one-command runnable examples for the open-source KAOS (Kelvin Agentic OS) ecosystem.',
      customCss: ['./src/styles/global.css'],
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/273v/learn-kaos' },
      ],
      sidebar: [
        {
          label: 'Start here',
          items: [
            { label: 'What is KAOS?', slug: 'what-is-kaos' },
            { label: 'How KAOS fits together', slug: 'architecture' },
            { label: 'Pick your path', slug: 'learning-paths' },
            { label: 'Install', slug: 'get-started/install' },
            { label: 'Your first example', slug: 'get-started/first-example' },
          ],
        },
        {
          label: 'Tutorials',
          items: [{ autogenerate: { directory: 'tutorials' } }],
        },
        {
          label: 'How-to',
          items: [{ autogenerate: { directory: 'how-to' } }],
        },
        {
          label: 'Concepts',
          items: [{ autogenerate: { directory: 'concepts' } }],
        },
        {
          label: 'Reference',
          items: [{ autogenerate: { directory: 'reference' } }],
        },
        {
          label: 'Examples gallery',
          items: [{ label: 'Gallery', slug: 'gallery' }],
        },
      ],
    }),
    sitemap(),
  ],

  vite: {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        '~': new URL('./src', import.meta.url).pathname,
        '@': new URL('./src', import.meta.url).pathname,
        // depth-independent imports of the tested source-of-truth files
        // (rendered into MDX via `?raw` so shown == tested).
        '#examples': new URL('./examples', import.meta.url).pathname,
        '#snippets': new URL('./snippets', import.meta.url).pathname,
      },
    },
  },
});
