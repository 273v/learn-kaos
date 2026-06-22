// Loads the examples gallery manifest (examples/index.toml) at build time.
// The manifest is the single source of truth shared by the gallery page,
// the `kaos-learn` launcher, and CI.
import { parse } from 'smol-toml';
// `?raw` keeps this depth-independent and avoids a Node fs read at build.
import rawToml from '#examples/index.toml?raw';

export interface Example {
  id: string;
  title: string;
  summary: string;
  packages: string[];
  persona: string;
  level: string;
  offline_ok: boolean;
  needs_key: boolean;
  est_cost_usd: number;
  tutorial?: string;
}

const parsed = parse(rawToml) as { example?: Example[] };

export const examples: Example[] = parsed.example ?? [];
