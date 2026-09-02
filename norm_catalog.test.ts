// End-to-End: die aus den App-Katalogen erzeugten Engine-Seeds gegen echtes
// PostgreSQL laden, eine Auswahl beantworten, evaluieren und die Persistenz
// pruefen. Belegt die Abbildung App-Kategorie -> hazard + SELECT-Frage + Regeln
// (Ampel -> risk_status), inkl. „unbeantwortet -> INCOMPLETE".
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import pg from 'pg';
import { loadSeedIntoDb } from './seed_loader.ts';
import { evaluateAssessment } from './engine_service.ts';

const PORT = Number(process.env.PGPORT ?? 5433);
const HOST = process.env.PGHOST ?? '127.0.0.1';
const USER = process.env.PGUSER ?? 'postgres';
const DB = 'gbu_norm_e2e';
const schemaSql = readFileSync(new URL('./gbu_engine_schema.sql', import.meta.url), 'utf8');
const load = (f: string) => JSON.parse(readFileSync(new URL('./' + f, import.meta.url), 'utf8'));

let pool: pg.Pool;

before(async () => {
  const admin = new pg.Pool({ host: HOST, port: PORT, user: USER, database: 'postgres' });
  await admin.query(`DROP DATABASE IF EXISTS ${DB}`);
  await admin.query(`CREATE DATABASE ${DB}`);
  await admin.end();
  pool = new pg.Pool({ host: HOST, port: PORT, user: USER, database: DB });
  await pool.query(schemaSql);
});
after(async () => { if (pool) await pool.end(); });

// Legt Anlage + Beurteilung fuer eine rule_version an.
async function newAssessment(ruleVersionId: string): Promise<string> {
  const t = (await pool.query(`INSERT INTO tenants(name,slug) VALUES ('N','n-${Math.random().toString(36).slice(2)}') RETURNING id`)).rows[0];
  const a = (await pool.query(`INSERT INTO assets(tenant_id,asset_number) VALUES ($1,'A') RETURNING id`, [t.id])).rows[0];
  const s = (await pool.query(
    `INSERT INTO assessments(tenant_id,asset_id,type,rule_version_id) VALUES ($1,$2,'GBU',$3) RETURNING id`,
    [t.id, a.id, ruleVersionId])).rows[0];
  return s.id;
}

// Findet (hazard, question_id, option_id) dessen Auswahl das gewuenschte
// result_status ausloest.
async function pick(ruleVersionId: string, result: string, excludeQid?: string) {
  return (await pool.query(
    `SELECT h.code AS hcode, q.id AS qid, o.id AS oid
       FROM evaluation_rules r
       JOIN hazards h ON h.id = r.hazard_id
       JOIN hazard_questions hq ON hq.hazard_id = h.id
       JOIN questions q ON q.id = hq.question_id
       JOIN question_options o ON o.question_id = q.id
      WHERE r.rule_version_id = $1 AND r.result_status = $2::risk_status
        AND r.condition_expression->>'question' = q.code
        AND r.condition_expression->>'value' = o.value
        AND ($3::uuid IS NULL OR q.id <> $3::uuid)
      LIMIT 1`, [ruleVersionId, result, excludeQid ?? null])).rows[0];
}
async function answer(assessmentId: string, qid: string, oid: string) {
  await pool.query(
    `INSERT INTO answers(assessment_id,question_id,option_id,answered) VALUES ($1,$2,$3,true)`,
    [assessmentId, qid, oid]);
}
async function statusOf(assessmentId: string, hcode: string) {
  return (await pool.query(
    `SELECT er.status FROM evaluation_results er JOIN hazards h ON h.id=er.hazard_id
      WHERE er.assessment_id=$1 AND h.code=$2`, [assessmentId, hcode])).rows[0]?.status;
}

test('81-80: Auswahl -> Ampel-Risiko; unbeantwortet -> INCOMPLETE', async () => {
  const { ruleVersionId } = await loadSeedIntoDb(pool, load('norm_81_80.json'));
  const asmt = await newAssessment(ruleVersionId);

  const high = await pick(ruleVersionId, 'HIGH');
  const green = await pick(ruleVersionId, 'NO_RISK', high.qid);
  assert.ok(high && green, 'HIGH- und NO_RISK-Beispiel gefunden');
  await answer(asmt, high.qid, high.oid);
  await answer(asmt, green.qid, green.oid);

  const { summary } = await evaluateAssessment(pool, asmt);

  assert.equal(await statusOf(asmt, high.hcode), 'HIGH', 'rot -> HIGH');
  assert.equal(await statusOf(asmt, green.hcode), 'NO_RISK', 'gruen -> NO_RISK');

  const total = (await pool.query('SELECT count(DISTINCT h.id)::int n FROM hazards h JOIN evaluation_rules r ON r.hazard_id=h.id WHERE r.rule_version_id=$1', [ruleVersionId])).rows[0].n;
  // Alle nicht beantworteten Gefaehrdungen sind INCOMPLETE (SELECT required ALWAYS).
  assert.equal(summary.INCOMPLETE, total - 2, 'nicht bewertet -> INCOMPLETE, nicht NO_RISK');
  assert.equal(summary.HIGH >= 1 && summary.NO_RISK >= 1, true);

  // assessment_summary persistiert
  const s = (await pool.query('SELECT * FROM assessment_summary WHERE assessment_id=$1', [asmt])).rows[0];
  assert.equal(s.hazards_incomplete, total - 2);
  assert.equal(s.hazards_total, total);

  // Maßnahmen: Katalog geladen + rule_measures verknüpft
  const mcount = (await pool.query('SELECT count(*)::int n FROM measures')).rows[0].n;
  assert.ok(mcount > 100, 'Maßnahmenkatalog geladen');
  const rm = (await pool.query(
    `SELECT count(*)::int n FROM rule_measures rm
       JOIN evaluation_rules r ON r.id = rm.evaluation_rule_id
      WHERE r.rule_version_id = $1`, [ruleVersionId])).rows[0].n;
  assert.ok(rm > 100, 'rule_measures verknüpft');
  const rmHigh = (await pool.query(
    `SELECT m.type, m.priority_class FROM rule_measures rm
       JOIN evaluation_rules r ON r.id = rm.evaluation_rule_id
       JOIN measures m ON m.id = rm.measure_id
       JOIN hazards h ON h.id = r.hazard_id
      WHERE r.rule_version_id = $1 AND h.code = $2 AND r.result_status = 'HIGH'`,
    [ruleVersionId, high.hcode])).rows;
  assert.ok(rmHigh.length >= 1, 'HIGH-Regel trägt mindestens eine Maßnahme');
});

test('EN 81-41: SELECT mit A-D-Optionen -> INCOMPLETE/NOT_APPLICABLE/HIGH', async () => {
  const { ruleVersionId } = await loadSeedIntoDb(pool, load('norm_en8141.json'));
  const asmt = await newAssessment(ruleVersionId);

  const high = await pick(ruleVersionId, 'HIGH');
  const na = await pick(ruleVersionId, 'NOT_APPLICABLE', high.qid);
  assert.ok(high && na);
  await answer(asmt, high.qid, high.oid);
  await answer(asmt, na.qid, na.oid);

  await evaluateAssessment(pool, asmt);
  assert.equal(await statusOf(asmt, high.hcode), 'HIGH');
  assert.equal(await statusOf(asmt, na.hcode), 'NOT_APPLICABLE', 'D-Stufe -> NOT_APPLICABLE');

  // Der Katalog ist vollstaendig geladen (48 Prüfpunkte, 192 Regeln).
  const counts = (await pool.query(
    `SELECT (SELECT count(DISTINCT h.id) FROM hazards h JOIN evaluation_rules r ON r.hazard_id=h.id WHERE r.rule_version_id=$1) AS h,
            (SELECT count(*) FROM evaluation_rules WHERE rule_version_id=$1) AS r`, [ruleVersionId])).rows[0];
  assert.equal(Number(counts.h), 48);
  assert.equal(Number(counts.r), 192);

  // Norm-/Quellenbezug strukturiert abgelegt
  const src = (await pool.query('SELECT count(*)::int n FROM source_references')).rows[0].n;
  assert.ok(src > 0, 'source_references angelegt');
  const hs = (await pool.query(
    `SELECT count(*)::int n FROM hazard_sources hs
       JOIN hazards h ON h.id = hs.hazard_id
       JOIN evaluation_rules r ON r.hazard_id = h.id
      WHERE r.rule_version_id = $1`, [ruleVersionId])).rows[0].n;
  assert.ok(hs >= 48, 'jede EN-81-41-Gefährdung hat eine Quelle');
  // Beispiel: DIN-EN-Quelle existiert
  const en = (await pool.query(
    `SELECT count(*)::int n FROM source_references WHERE source_type='EN' AND document_code LIKE 'DIN EN 81-41%'`)).rows[0].n;
  assert.ok(en >= 1, 'DIN EN 81-41 als strukturierte Quelle');
});

test('Cyber (TRBS 1115-1): nicht erfüllt -> HIGH mit Maßnahme; n.a. -> NOT_APPLICABLE', async () => {
  const { ruleVersionId } = await loadSeedIntoDb(pool, load('norm_cyber_voll.json'));
  const asmt = await newAssessment(ruleVersionId);

  const high = await pick(ruleVersionId, 'HIGH');           // „Nicht erfüllt"
  const na = await pick(ruleVersionId, 'NOT_APPLICABLE', high.qid);
  await answer(asmt, high.qid, high.oid);
  await answer(asmt, na.qid, na.oid);
  const { summary } = await evaluateAssessment(pool, asmt);

  assert.equal(await statusOf(asmt, high.hcode), 'HIGH');
  assert.equal(await statusOf(asmt, na.hcode), 'NOT_APPLICABLE');
  assert.equal(summary.INCOMPLETE, 17 - 2, 'unbewertete Prüffelder -> INCOMPLETE');

  // Die HIGH-Regel (nicht erfüllt) trägt die Standardmaßnahme.
  const rm = (await pool.query(
    `SELECT m.type FROM rule_measures rm
       JOIN evaluation_rules r ON r.id = rm.evaluation_rule_id
       JOIN measures m ON m.id = rm.measure_id
       JOIN hazards h ON h.id = r.hazard_id
      WHERE r.rule_version_id = $1 AND h.code = $2 AND r.result_status = 'HIGH'`,
    [ruleVersionId, high.hcode])).rows;
  assert.ok(rm.length >= 1 && ['TECHNICAL', 'ORGANISATIONAL'].includes(rm[0].type),
    'Standardmaßnahme verknüpft');
});
