// End-to-End-Test der Backend-Anbindung gegen ein echtes PostgreSQL.
// Lauf (Container):  PGPORT=5433 node --test --experimental-strip-types engine_service.test.ts
//
// Baut eine frische DB aus gbu_engine_schema.sql, laedt seed_rules.json,
// legt Anlage + Beurteilung + Antworten an, ruft evaluateAssessment() und
// prueft die persistierten evaluation_results und assessment_summary.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import pg from 'pg';
import { loadSeedIntoDb } from './seed_loader.ts';
import { evaluateAssessment } from './engine_service.ts';

const PORT = Number(process.env.PGPORT ?? 5433);
const HOST = process.env.PGHOST ?? 'localhost';
const USER = process.env.PGUSER ?? 'postgres';
const DB = 'gbu_e2e';

const schemaSql = readFileSync(new URL('./gbu_engine_schema.sql', import.meta.url), 'utf8');
const seed = JSON.parse(readFileSync(new URL('./seed_rules.json', import.meta.url), 'utf8'));

let pool: pg.Pool;
const ctx: Record<string, string> = {};

before(async () => {
  // frische Datenbank
  const admin = new pg.Pool({ host: HOST, port: PORT, user: USER, database: 'postgres' });
  await admin.query(`DROP DATABASE IF EXISTS ${DB}`);
  await admin.query(`CREATE DATABASE ${DB}`);
  await admin.end();

  pool = new pg.Pool({ host: HOST, port: PORT, user: USER, database: DB });
  await pool.query(schemaSql);
  const seedRes = await loadSeedIntoDb(pool, seed);
  assert.ok(seedRes.questionCount > 0);

  // Mandant / Anlage / Beurteilung
  const tenant = (await pool.query(
    `INSERT INTO tenants (name, slug) VALUES ('E2E','e2e') RETURNING id`)).rows[0];
  const asset = (await pool.query(
    `INSERT INTO assets (tenant_id, asset_number) VALUES ($1,'A-1') RETURNING id`,
    [tenant.id])).rows[0];
  const assessment = (await pool.query(
    `INSERT INTO assessments (tenant_id, asset_id, type, rule_version_id)
     VALUES ($1,$2,'GBU_CYBER',$3) RETURNING id`,
    [tenant.id, asset.id, seedRes.ruleVersionId])).rows[0];
  ctx.assessmentId = assessment.id;

  // Antworten setzen (boolean YES_NO)
  const setBool = async (code: string, val: boolean) => {
    const q = (await pool.query('SELECT id FROM questions WHERE code=$1', [code])).rows[0];
    await pool.query(
      `INSERT INTO answers (assessment_id, question_id, value_boolean, answered)
       VALUES ($1,$2,$3,true)`, [assessment.id, q.id, val]);
  };
  await setBool('q_emergency_call_present', false); // M032 -> HIGH
  await setBool('q_asbestos_pit', true);            // M087 -> HIGH (ANY, drei leer)
  await setBool('q_transport_chemical', true);      // M088 -> MEDIUM
  await setBool('q_ctrl_digital', true);            // MC4 anwendbar
  await setBool('q_ctrl_free_access', true);
  await setBool('q_ctrl_wireless', true);
  // q_ctrl_physical BEWUSST unbeantwortet -> MC4 INCOMPLETE
});

after(async () => { if (pool) await pool.end(); });

test('evaluateAssessment schreibt evaluation_results + assessment_summary', async () => {
  const { summary } = await evaluateAssessment(pool, ctx.assessmentId);

  // In-Memory-Zusammenfassung
  assert.equal(summary.HIGH, 2, 'M032 + M087');
  assert.equal(summary.MEDIUM, 1, 'M088');
  assert.equal(summary.INCOMPLETE, 1, 'MC4 (Physik-Frage fehlt)');
  assert.equal(summary.NO_RISK, seed.hazards.length - 4);

  // Persistierte Ergebnisse
  const rows = (await pool.query(
    `SELECT h.code, er.status, r.code AS rule
       FROM evaluation_results er
       JOIN hazards h ON h.id = er.hazard_id
       LEFT JOIN evaluation_rules r ON r.id = er.matched_rule_id
      WHERE er.assessment_id = $1`, [ctx.assessmentId])).rows;
  const byCode = Object.fromEntries(rows.map((r) => [r.code, r]));
  assert.equal(rows.length, seed.hazards.length, 'ein Ergebnis je Gefaehrdung');
  assert.equal(byCode['M032'].status, 'HIGH');
  assert.equal(byCode['M032'].rule, 'M032-R001', 'matched_rule_id aufgeloest');
  assert.equal(byCode['M087'].status, 'HIGH');
  assert.equal(byCode['M088'].status, 'MEDIUM');
  assert.equal(byCode['MC4'].status, 'INCOMPLETE');
  assert.equal(byCode['MC4'].rule, null, 'INCOMPLETE hat keine matched_rule');
  assert.equal(byCode['M090'].status, 'NO_RISK');

  // input_snapshot ist revisionssicher gespeichert
  const snap = (await pool.query(
    `SELECT input_snapshot FROM evaluation_results er JOIN hazards h ON h.id=er.hazard_id
      WHERE er.assessment_id=$1 AND h.code='M032'`, [ctx.assessmentId])).rows[0];
  assert.deepEqual(snap.input_snapshot, { q_emergency_call_present: false });

  // assessment_summary persistiert
  const s = (await pool.query(
    'SELECT * FROM assessment_summary WHERE assessment_id=$1', [ctx.assessmentId])).rows[0];
  assert.equal(s.hazards_high, 2);
  assert.equal(s.hazards_incomplete, 1);
  assert.equal(s.hazards_total, seed.hazards.length);
  assert.ok(s.questions_answered >= 6 && s.questions_answered <= s.questions_total);
});

test('Reconstructed-only reproduziert das Original (idempotenter Re-Run)', async () => {
  // Notruf vorhanden, aber keine 24h-Aufschaltung: Original -> KEIN RISIKO.
  const q = async (code: string) =>
    (await pool.query('SELECT id FROM questions WHERE code=$1', [code])).rows[0].id;
  await pool.query(
    `INSERT INTO answers (assessment_id, question_id, value_boolean, answered)
     VALUES ($1,$2,true,true)
     ON CONFLICT (assessment_id, question_id) DO UPDATE SET value_boolean=EXCLUDED.value_boolean, answered=true`,
    [ctx.assessmentId, await q('q_emergency_call_present')]);
  await pool.query(
    `INSERT INTO answers (assessment_id, question_id, value_boolean, answered)
     VALUES ($1,$2,false,true)
     ON CONFLICT (assessment_id, question_id) DO UPDATE SET value_boolean=EXCLUDED.value_boolean, answered=true`,
    [ctx.assessmentId, await q('q_emergency_call_24h')]);

  const full = await evaluateAssessment(pool, ctx.assessmentId);
  const rowFull = (await pool.query(
    `SELECT er.status FROM evaluation_results er JOIN hazards h ON h.id=er.hazard_id
      WHERE er.assessment_id=$1 AND h.code='M032'`, [ctx.assessmentId])).rows[0];
  assert.equal(rowFull.status, 'MEDIUM', 'volles Regelwerk: unsere OWN_RULE');
  void full;

  const recon = await evaluateAssessment(pool, ctx.assessmentId, { includeOrigins: ['RECONSTRUCTED_ORIGINAL'] });
  const rowRecon = (await pool.query(
    `SELECT er.status FROM evaluation_results er JOIN hazards h ON h.id=er.hazard_id
      WHERE er.assessment_id=$1 AND h.code='M032'`, [ctx.assessmentId])).rows[0];
  assert.equal(rowRecon.status, 'NO_RISK', 'reconstructed-only: Original');
  void recon;
});
