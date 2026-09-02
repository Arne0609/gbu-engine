// Auth + CORS: der Server mit konfiguriertem Token schützt alle Endpunkte außer
// /health; CORS liefert nur für erlaubte Origins die Freigabe.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import type { AddressInfo } from 'node:net';
import pg from 'pg';
import { createServer } from './server.ts';
import { applySchema, seedCatalogs } from './seed_catalogs.ts';

const PORT = Number(process.env.PGPORT ?? 5433);
const HOST = process.env.PGHOST ?? '127.0.0.1';
const USER = process.env.PGUSER ?? 'postgres';
const DB = 'gbu_api_auth';
const TOKEN = 's3cret-token';
const ORIGIN = 'https://app.example';

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
  await seedCatalogs(pool, ['norm_cyber_minimal.json']);
  const app = createServer(pool, { apiTokens: [TOKEN], corsOrigins: [ORIGIN] });
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => {
      base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
      resolve();
    });
  });
});

after(async () => {
  if (server) await new Promise<void>((r) => server.close(() => r()));
  if (pool) await pool.end();
});

test('/health bleibt ohne Token offen', async () => {
  const r = await fetch(base + '/health');
  assert.equal(r.status, 200);
  assert.equal((await r.json()).ok, true);
});

test('geschützter Endpunkt ohne Token -> 401', async () => {
  const r = await fetch(base + '/rule-versions');
  assert.equal(r.status, 401);
  assert.equal((await r.json()).error, 'unauthorized');
});

test('mit Bearer-Token -> 200', async () => {
  const r = await fetch(base + '/rule-versions', { headers: { Authorization: `Bearer ${TOKEN}` } });
  assert.equal(r.status, 200);
  assert.ok((await r.json()).rule_versions.length >= 1);
});

test('mit X-API-Key -> 200', async () => {
  const r = await fetch(base + '/rule-versions', { headers: { 'X-API-Key': TOKEN } });
  assert.equal(r.status, 200);
});

test('falscher Token -> 401', async () => {
  const r = await fetch(base + '/rule-versions', { headers: { Authorization: 'Bearer nope' } });
  assert.equal(r.status, 401);
});

test('CORS-Preflight von erlaubtem Origin -> 204 + Freigabe', async () => {
  const r = await fetch(base + '/rule-versions', {
    method: 'OPTIONS',
    headers: { Origin: ORIGIN, 'Access-Control-Request-Method': 'GET' },
  });
  assert.equal(r.status, 204);
  assert.equal(r.headers.get('access-control-allow-origin'), ORIGIN);
});

test('CORS von fremdem Origin -> keine Freigabe', async () => {
  const r = await fetch(base + '/rule-versions', {
    method: 'OPTIONS',
    headers: { Origin: 'https://evil.example', 'Access-Control-Request-Method': 'GET' },
  });
  assert.equal(r.headers.get('access-control-allow-origin'), null);
});
