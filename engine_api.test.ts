// End-to-End über HTTP: Express-App aus server.ts gegen echtes PostgreSQL,
// Katalog laden, Beurteilung anlegen, Antworten per PUT speichern + evaluieren,
// Ergebnisse und Zusammenfassung lesen. Belegt die komplette REST-Anbindung.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import type { AddressInfo } from 'node:net';
import pg from 'pg';
import { createServer } from './server.ts';
import { applySchema, seedCatalogs } from './seed_catalogs.ts';

const PORT = Number(process.env.PGPORT ?? 5433);
const HOST = process.env.PGHOST ?? '127.0.0.1';
const USER = process.env.PGUSER ?? 'postgres';
const DB = 'gbu_api_e2e';

let pool: pg.Pool;
let server: any;
let base = '';

before(async () => {
  const admin = new pg.Pool({ host: HOST, port: PORT, user: USER, database: 'postgres' });
  await admin.query(`DROP DATABASE IF EXISTS ${DB}`);
  await admin.query(`CREATE DATABASE ${DB}`);
  await admin.end();
  pool = new pg.Pool({ host: HOST, port: PORT, user: USER, database: DB });
  await applySchema(pool);
  // Zwei Kataloge: ein kleiner (Cyber-Minimal) und einer mit Normquellen (EN 81-41).
  await seedCatalogs(pool, ['norm_cyber_minimal.json', 'norm_en8141.json']);
  const app = createServer(pool);
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => {
      const a = server.address() as AddressInfo;
      base = `http://127.0.0.1:${a.port}`;
      resolve();
    });
  });
});

after(async () => {
  if (server) await new Promise<void>((r) => server.close(() => r()));
  if (pool) await pool.end();
});

const get = async (p: string) => (await fetch(base + p)).json();
const send = async (p: string, method: string, body?: unknown) =>
  (await fetch(base + p, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  })).json();

test('GET /health meldet ok', async () => {
  const j = await get('/health');
  assert.equal(j.ok, true);
});

test('GET /rule-versions listet beide geladenen Kataloge', async () => {
  const j = await get('/rule-versions');
  assert.equal(j.ok, true);
  assert.ok(j.rule_versions.length >= 2, 'mindestens 2 Regelversionen');
  for (const rv of j.rule_versions) assert.ok(rv.hazards > 0, `${rv.version} hat Gefährdungen`);
});

test('Katalog + Bewertungsdurchlauf: PUT löst HIGH aus, Ergebnisse + Summary stimmen', async () => {
  const rvs = (await get('/rule-versions')).rule_versions;
  const rv = rvs.find((r: any) => r.version === 'en8141-2026.1') ?? rvs[0];

  // Katalog über HTTP beziehen und Grundform prüfen.
  const cat = (await get(`/rule-versions/${rv.id}/catalog`)).catalog;
  assert.ok(cat.hazards.length > 0 && cat.rules.length > 0 && cat.questions.length > 0);

  // Eine (Frage, Option) finden, deren Auswahl HIGH auslöst.
  const hit = (await pool.query(
    `SELECT q.code AS qcode, o.value AS oval, h.code AS hcode
       FROM evaluation_rules r
       JOIN hazards h ON h.id = r.hazard_id
       JOIN questions q ON q.code = r.condition_expression->>'question'
       JOIN question_options o ON o.question_id = q.id
        AND o.value = r.condition_expression->>'value'
      WHERE r.rule_version_id = $1 AND r.result_status = 'HIGH'::risk_status
      LIMIT 1`, [rv.id])).rows[0];
  assert.ok(hit, 'HIGH-auslösende Regel gefunden');

  // Beurteilung anlegen.
  const created = await send('/assessments', 'POST', { rule_version_id: rv.id });
  assert.equal(created.ok, true);
  const id = created.assessment_id;
  assert.ok(id);

  // Antwort speichern + evaluieren.
  const put = await send(`/assessments/${id}/answers`, 'PUT', { answers: { [hit.qcode]: hit.oval } });
  assert.equal(put.ok, true);
  assert.ok(put.summary.HIGH >= 1, `Summary HIGH>=1, war ${JSON.stringify(put.summary)}`);
  // Der Rest ist unbeantwortet -> INCOMPLETE (nicht NO_RISK).
  assert.ok(put.summary.INCOMPLETE >= 1, 'unbeantwortete Gefährdungen sind INCOMPLETE');

  // Ergebnisse: die getroffene Gefährdung ist HIGH.
  const results = (await get(`/assessments/${id}/results`)).results;
  const target = results.find((r: any) => r.hazard === hit.hcode);
  assert.ok(target, 'Zielgefährdung in Ergebnissen');
  assert.equal(target.status, 'HIGH');

  // Gesamtabruf: Antwort ist gespeichert, Summary vorhanden.
  const full = await get(`/assessments/${id}`);
  assert.equal(full.ok, true);
  assert.equal(full.answers[hit.qcode], hit.oval);
  assert.ok(full.summary && full.summary.hazards_high >= 1, 'persistierte Summary zählt HIGH');
});

test('unbekannte rule_version -> 404', async () => {
  const res = await fetch(base + '/rule-versions/00000000-0000-0000-0000-000000000000/catalog');
  assert.equal(res.status, 404);
});
