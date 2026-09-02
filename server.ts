// ============================================================================
// GBU APP 4.0 – HTTP-Server (Express + pg)
// ============================================================================
//
// Bootstrap für die Bewertungsengine als REST-Dienst. Baut einen pg-Pool aus
// den üblichen PG*-Umgebungsvariablen auf und registriert die Engine-Routen
// aus engine_api.ts. Start:
//
//   PGHOST=127.0.0.1 PGPORT=5433 PGUSER=postgres PGDATABASE=gbu \
//     node --experimental-strip-types server.ts
//
// Optional: PORT (Default 8787). Vor dem ersten Start den Katalog laden:
//   node --experimental-strip-types seed_catalogs.ts
// ============================================================================

import express from 'express';
import { registerEngineApi } from './engine_api.ts';
import { makePool, engineSchema } from './db.ts';
import { bootstrapDb } from './seed_catalogs.ts';

export interface ServerOptions {
  /** Nicht-leer ⇒ Token-Pflicht (außer /health). Aus API_TOKENS/API_TOKEN. */
  apiTokens?: string[];
  /** Gesetzt ⇒ nur diese Origins per CORS erlaubt; sonst '*'. Aus CORS_ORIGINS. */
  corsOrigins?: string[];
}

function parseList(v?: string): string[] {
  return (v ?? '').split(',').map((s) => s.trim()).filter(Boolean);
}

export function createServer(pool: any, opts: ServerOptions = {}) {
  const app = express();
  app.use(express.json({ limit: '2mb' }));

  const corsOrigins = opts.corsOrigins ?? parseList(process.env.CORS_ORIGINS);
  const apiTokens = opts.apiTokens ?? parseList(process.env.API_TOKENS || process.env.API_TOKEN);

  // CORS: offen ('*') solange keine Origin-Liste gesetzt ist; sonst nur erlaubte.
  app.use((req, res, next) => {
    const origin = req.headers.origin as string | undefined;
    if (corsOrigins.length === 0) {
      res.header('Access-Control-Allow-Origin', '*');
    } else if (origin && corsOrigins.includes(origin)) {
      res.header('Access-Control-Allow-Origin', origin);
      res.header('Vary', 'Origin');
    }
    res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-API-Key');
    if (req.method === 'OPTIONS') return res.sendStatus(204);
    next();
  });

  // Auth: wenn Tokens konfiguriert sind, alles außer /health absichern.
  if (apiTokens.length > 0) {
    app.use((req, res, next) => {
      if (req.path === '/health') return next();
      const auth = req.headers.authorization as string | undefined;
      const bearer = auth && auth.startsWith('Bearer ') ? auth.slice(7) : undefined;
      const key = (req.headers['x-api-key'] as string | undefined) || bearer;
      if (key && apiTokens.includes(key)) return next();
      return res.status(401).json({ ok: false, error: 'unauthorized' });
    });
  }

  registerEngineApi(app, pool);
  return app;
}

// Direktstart nur, wenn diese Datei als Einstiegspunkt läuft (nicht im Test).
const isEntry = process.argv[1] && process.argv[1].endsWith('server.ts');
if (isEntry) {
  const pool = makePool();
  const app = createServer(pool);
  const port = Number(process.env.PORT ?? 8787);
  app.listen(port, () => {
    const src = process.env.DATABASE_URL ? `DATABASE_URL (Schema ${engineSchema()})` : 'PG*-Variablen';
    const authOn = parseList(process.env.API_TOKENS || process.env.API_TOKEN).length > 0;
    const corsOn = parseList(process.env.CORS_ORIGINS).length > 0;
    // eslint-disable-next-line no-console
    console.log(`GBU-Engine-API läuft auf Port ${port} · DB: ${src} · Auth: ${authOn ? 'Token' : 'offen'} · CORS: ${corsOn ? 'eingeschränkt' : '*'}`);
    // Idempotenter Selbst-Seed (Schema + Kataloge), abschaltbar via SEED_ON_BOOT=off.
    // SEED_ON_BOOT=force spielt die Kataloge bei jedem Start neu ein (Upsert) –
    // damit werden geänderte Regeln (z. B. Risikostufen) in einer bestehenden
    // DB aktualisiert.
    if (process.env.SEED_ON_BOOT !== 'off') {
      const force = process.env.SEED_ON_BOOT === 'force';
      bootstrapDb(pool, { force })
        .then((r) => {
          if (r.schemaCreated || r.seeded) {
            // eslint-disable-next-line no-console
            console.log(`Bootstrap: Schema ${r.schemaCreated ? 'angelegt' : 'vorhanden'}, Kataloge ${r.seeded ? 'geladen' : 'vorhanden'}.`);
          } else {
            // eslint-disable-next-line no-console
            console.log('Bootstrap: Schema und Kataloge bereits vorhanden.');
          }
        })
        .catch((e) => {
          // eslint-disable-next-line no-console
          console.error('Bootstrap fehlgeschlagen (Server läuft weiter):', e?.message ?? e);
        });
    }
  });
}
