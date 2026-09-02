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

export function createServer(pool: any) {
  const app = express();
  app.use(express.json({ limit: '2mb' }));
  // CORS offen für die App-Anbindung (in Produktion einschränken).
  app.use((_req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    if (_req.method === 'OPTIONS') return res.sendStatus(204);
    next();
  });
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
    // eslint-disable-next-line no-console
    console.log(`GBU-Engine-API läuft auf Port ${port} · DB: ${src}`);
    // Idempotenter Selbst-Seed (Schema + Kataloge), abschaltbar via SEED_ON_BOOT=off.
    if (process.env.SEED_ON_BOOT !== 'off') {
      bootstrapDb(pool)
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
