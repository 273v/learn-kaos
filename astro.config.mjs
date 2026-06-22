// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Learn KAOS — Astro Starlight. Conventions match 273ventures.com:
// pnpm, Node 22, Tailwind v4 via @tailwindcss/vite, ~/@ -> src aliases.
// Sidebar grows as milestones land (M0 ships Start-here + Gallery).
// https://astro.build/config
export default defineConfig({
  site: 'https://273v.github.io',
  base: '/learn-kaos',
  trailingSlash: 'never',

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
            { label: 'Install', slug: 'get-started/install' },
            { label: 'Your first example', slug: 'get-started/first-example' },
          ],
        },
        {
          label: 'Tutorials',
          items: [{ autogenerate: { directory: 'tutorials' } }],
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
