// Starlight route middleware: inject per-page og:image / twitter:image meta
// pointing at the build-time cards from src/pages/og/[...slug].ts.
// The OG URLs must carry the project base (/learn-kaos) AND be absolute.
import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

const BASE = '/learn-kaos'; // keep in sync with astro.config.mjs `base`

export const onRequest = defineRouteMiddleware((context) => {
  const route = context.locals.starlightRoute;
  const id = route.id || 'index';
  if (id === '404') return; // no card generated for the 404 page
  const ogImageUrl = new URL(`${BASE}/og/${id}.png`, context.site);

  const { head } = route;
  head.push({ tag: 'meta', attrs: { property: 'og:image', content: ogImageUrl.href } });
  head.push({ tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } });
  head.push({ tag: 'meta', attrs: { property: 'og:image:height', content: '630' } });
  head.push({ tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } });
  head.push({ tag: 'meta', attrs: { name: 'twitter:image', content: ogImageUrl.href } });
});
