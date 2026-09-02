// ============================================================================
// GBU APP 4.0 – DB-Pool-Fabrik
// ============================================================================
//
// Baut den pg-Pool wahlweise aus DATABASE_URL (z. B. Railway, mit SSL) oder
// aus den einzelnen PG*-Umgebungsvariablen. Optional wird ein eigenes
// Postgres-Schema gesetzt (search_path), damit die Engine bestehende Tabellen
// in einer geteilten Datenbank nicht berührt.
//
// Umgebungsvariablen:
//   DATABASE_URL   postgresql://user:pass@host:port/db  (SSL an, außer sslmode=disable)
//   PGSCHEMA       Ziel-Schema (Default: 'gbu', sobald DATABASE_URL gesetzt ist)
//   PGSSL=off      SSL trotz DATABASE_URL abschalten
// ============================================================================

import pg from 'pg';

/// Ziel-Schema der Engine (oder undefined = public, wie bei lokalem PG*-Setup).
export function engineSchema(): string | undefined {
  const explicit = process.env.PGSCHEMA;
  if (explicit && explicit.trim()) return explicit.trim();
  return process.env.DATABASE_URL ? 'gbu' : undefined;
}

export function makePool(): pg.Pool {
  const url = process.env.DATABASE_URL;
  const schema = engineSchema();
  const options = schema ? `-c search_path=${schema},public` : undefined;

  if (url) {
    // Railway-interne Verbindungen (…​.railway.internal) laufen ohne SSL;
    // der öffentliche Proxy dagegen mit SSL.
    const internal = /\.railway\.internal/i.test(url);
    const noSsl = process.env.PGSSL === 'off' || /sslmode=disable/i.test(url) || internal;
    return new pg.Pool({
      connectionString: url,
      ssl: noSsl ? false : { rejectUnauthorized: false },
      ...(options ? { options } : {}),
    });
  }
  return new pg.Pool(options ? { options } : {});
}
