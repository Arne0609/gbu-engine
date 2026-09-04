// ============================================================================
// GBU APP 4.0 – Katalog-Seeding (CLI)
// ============================================================================
//
// Legt das Schema an (idempotent, falls nötig) und lädt die sechs Norm-Kataloge
// als Regelversionen in die DB. Aufruf:
//
//   PGHOST=127.0.0.1 PGPORT=5433 PGUSER=postgres PGDATABASE=gbu \
//     node --experimental-strip-types seed_catalogs.ts [--schema]
//
// --schema  vorher gbu_engine_schema.sql einspielen (Tabellen anlegen).
// ============================================================================

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { loadSeedIntoDb } from './seed_loader.ts';
import { makePool, engineSchema } from './db.ts';

const HERE = path.dirname(fileURLToPath(import.meta.url));

export const CATALOG_FILES = [
  'norm_81_20.json',
  'norm_81_80.json',
  'norm_2026.json',
  'norm_en8141.json',
  'norm_cyber_voll.json',
  'norm_cyber_minimal.json',
  'norm_81_20_mf.json',
  'norm_cyber_mf.json',
  'norm_81_80_mf.json',
];

export async function applySchema(db: any): Promise<void> {
  let sql = readFileSync(path.join(HERE, 'gbu_engine_schema.sql'), 'utf8');
  const schema = engineSchema();
  if (schema) {
    // Engine in ein eigenes Schema legen (bestehende Tabellen bleiben unberührt).
    sql = `CREATE SCHEMA IF NOT EXISTS ${schema};\nSET search_path TO ${schema}, public;\n${sql}`;
  }
  await db.query(sql);
}

/// Idempotente Spalten-Erweiterungen für bereits angelegte Datenbanken
/// (entspricht dem Migrationsblock am Ende von gbu_engine_schema.sql).
export const MIGRATIONS = [
  'ALTER TABLE hazards          ADD COLUMN IF NOT EXISTS hazard_factor text',
  'ALTER TABLE hazards          ADD COLUMN IF NOT EXISTS person_groups text[]',
  'ALTER TABLE hazard_questions ADD COLUMN IF NOT EXISTS applicable_expression jsonb',
  'ALTER TABLE questions        ADD COLUMN IF NOT EXISTS min_value numeric',
  'ALTER TABLE questions        ADD COLUMN IF NOT EXISTS max_value numeric',
];

export async function applyMigrations(db: any): Promise<void> {
  const schema = engineSchema();
  if (schema) await db.query(`SET search_path TO ${schema}, public`);
  for (const sql of MIGRATIONS) await db.query(sql);
}

export async function seedCatalogs(db: any, files: string[] = CATALOG_FILES) {
  const out: { file: string; ruleVersionId: string; questionCount: number }[] = [];
  for (const file of files) {
    const seed = JSON.parse(readFileSync(path.join(HERE, file), 'utf8'));
    const r = await loadSeedIntoDb(db, seed);
    out.push({ file, ...r });
  }
  return out;
}

/// Idempotenter Start-Bootstrap: Schema anlegen, falls es fehlt; Kataloge
/// laden, falls noch keine Regelversion existiert. Sicher bei jedem Deploy
/// aufrufbar – berührt nur das Engine-Schema.
export async function bootstrapDb(
  db: any,
  opts: { force?: boolean } = {},
): Promise<{ schemaCreated: boolean; seeded: boolean }> {
  const schema = engineSchema() ?? 'public';
  const reg = await db.query('SELECT to_regclass($1) AS t', [`${schema}.rule_versions`]);
  let schemaCreated = false;
  if (!reg.rows[0].t) {
    await applySchema(db);
    schemaCreated = true;
  } else {
    await applyMigrations(db);
  }
  // Seeden, solange nicht alle Kataloge vorhanden sind (fängt einen zuvor
  // abgebrochenen Seed-Lauf ab) – oder erzwungen bei force. loadSeedIntoDb ist
  // per Upsert idempotent, aktualisiert also bestehende Regeln (z. B. neue
  // Risikostufen) ohne Datenverlust.
  const cnt = await db.query(`SELECT count(*)::int AS n FROM ${schema}.rule_versions`);
  let seeded = false;
  if (opts.force || cnt.rows[0].n < CATALOG_FILES.length) {
    await seedCatalogs(db);
    seeded = true;
  }
  return { schemaCreated, seeded };
}

const isEntry = process.argv[1] && process.argv[1].endsWith('seed_catalogs.ts');
if (isEntry) {
  const withSchema = process.argv.includes('--schema');
  const pool = makePool();
  const client = await pool.connect();
  try {
    if (withSchema) {
      // eslint-disable-next-line no-console
      console.log('Schema wird eingespielt …');
      await applySchema(client);
    } else {
      await applyMigrations(client);
    }
    const res = await seedCatalogs(client);
    for (const r of res) {
      // eslint-disable-next-line no-console
      console.log(`  ${r.file.padEnd(24)} rule_version=${r.ruleVersionId}  Fragen=${r.questionCount}`);
    }
    // eslint-disable-next-line no-console
    console.log(`Fertig: ${res.length} Kataloge geladen.`);
  } finally {
    client.release();
    await pool.end();
  }
}
