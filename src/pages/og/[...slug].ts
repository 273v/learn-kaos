// Per-page Open Graph / social-card images, generated at build time with
// astro-og-canvas. Each docs page gets a branded card (title + description) so
// shared links render nicely on Slack, X, Discord, etc. The matching
// og:image / twitter:image meta tags are injected by src/routeData.ts.
import { getCollection } from 'astro:content';
import { OGImageRoute } from 'astro-og-canvas';

const entries = (await getCollection('docs')).filter(({ id }) => id !== '404');

const pages = Object.fromEntries(entries.map(({ data, id }) => [id, { data }]));

export const { getStaticPaths, GET } = await OGImageRoute({
  pages,
  param: 'slug',
  getImageOptions: (_id, page: (typeof pages)[string]) => ({
    title: page.data.title,
    description:
      page.data.description ??
      'Learn KAOS — open agentic infrastructure for legal & financial work.',
    bgGradient: [
      [15, 23, 42],
      [30, 27, 75],
    ],
    border: { color: [99, 102, 241], width: 24, side: 'inline-start' },
    padding: 90,
  }),
});
