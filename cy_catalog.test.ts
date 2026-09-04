// End-to-End fuer den Cyber-Typ „Cyber-GBU komponentenbasiert" (norm_cyber_mf.json):
// Seed gegen echtes PostgreSQL laden (domain CYBER, Sichtbarkeitsregeln,
// applicable_expression, Dokumentationsfragen), Anlagen beantworten und die
// Bewertung ueber engine_service pruefen. Belegt:
//   * Relaissteuerung / nicht vernetzt -> NOT_APPLICABLE statt INCOMPLETE
//   * Vorscreening (keine Schnittstelle) -> NO_RISK, Massnahmenfrage nicht Pflicht
//   * Fernzugriff ohne Massnahmen -> HIGH; unabhaengige Sicherheitseinrichtung -> MEDIUM
//   * Fehlende ZUES-Dokumentationsfrage -> INCOMPLETE (K-C20)
//   * Katalog-Export traegt domain CYBER und die fuenf Erhebungsbereiche.
//   node --test --experimental-strip-types cy_catalog.test.ts   (PGPORT=5433)
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import pg from 'pg';
import { loadSeedIntoDb } from './seed_loader.ts';
import { evaluateAssessment } from './engine_service.ts';
import { loadCatalogForClient } from './engine_api.ts';

const PORT = Number(process.env.PGPORT ?? 5433);
const HOST = process.env.PGHOST ?? '127.0.0.1';
const USER = process.env.PGUSER ?? 'postgres';
const DB = 'gbu_cy_e2e';
const schemaSql = readFileSync(new URL('./gbu_engine_schema.sql', import.meta.url), 'utf8');
const seed = JSON.parse(readFileSync(new URL('./norm_cyber_mf.json', import.meta.url).pathname, 'utf8'));

let pool: pg.Pool;
let rv: string;

before(async () => {
  const admin = new pg.Pool({ host: HOST, port: PORT, user: USER, database: 'postgres' });
  await admin.query(`DROP DATABASE IF EXISTS ${DB}`);
  await admin.query(`CREATE DATABASE ${DB}`);
  await admin.end();
  pool = new pg.Pool({ host: HOST, port: PORT, user: USER, database: DB });
  await pool.query(schemaSql);
  rv = (await loadSeedIntoDb(pool, seed)).ruleVersionId;
});
after(async () => { if (pool) await pool.end(); });

async function newAssessment(): Promise<string> {
  const t = (await pool.query(`INSERT INTO tenants(name,slug) VALUES ('CY','cy-${Math.random().toString(36).slice(2)}') RETURNING id`)).rows[0];
  const a = (await pool.query(`INSERT INTO assets(tenant_id,asset_number) VALUES ($1,'A') RETURNING id`, [t.id])).rows[0];
  return (await pool.query(
    `INSERT INTO assessments(tenant_id,asset_id,type,rule_version_id) VALUES ($1,$2,'CYBER',$3) RETURNING id`,
    [t.id, a.id, rv])).rows[0].id;
}
async function answer(asmt: string, code: string, value: boolean | number | string) {
  const q = (await pool.query('SELECT id, question_type FROM questions WHERE code=$1', [code])).rows[0];
  assert.ok(q, 'Frage ' + code);
  let cols: any = { b: null, n: null, o: null };
  if (q.question_type === 'YES_NO') cols.b = value;
  else if (q.question_type === 'NUMBER') cols.n = value;
  else cols.o = (await pool.query('SELECT id FROM question_options WHERE question_id=$1 AND value=$2', [q.id, value])).rows[0]?.id;
  if (q.question_type === 'SELECT') assert.ok(cols.o, `Option ${value} von ${code}`);
  await pool.query(
    `INSERT INTO answers(assessment_id,question_id,value_boolean,value_number,option_id,answered)
     VALUES ($1,$2,$3,$4,$5,true)
     ON CONFLICT (assessment_id,question_id) DO UPDATE SET value_boolean=EXCLUDED.value_boolean,
       value_number=EXCLUDED.value_number, option_id=EXCLUDED.option_id`,
    [asmt, q.id, cols.b, cols.n, cols.o]);
}
async function statusOf(asmt: string, hcode: string) {
  const r = (await pool.query(
    `SELECT er.status, ru.code AS rule FROM evaluation_results er JOIN hazards h ON h.id=er.hazard_id
       LEFT JOIN evaluation_rules ru ON ru.id = er.matched_rule_id
      WHERE er.assessment_id=$1 AND h.code=$2`, [asmt, hcode])).rows[0];
  return r ? { status: r.status, rule: r.rule } : undefined;
}

test('Seed geladen: domain CYBER, Sichtbarkeitsregeln, applicable_expression, Faktor/Personengruppen', async () => {
  const d = (await pool.query(`SELECT count(*)::int n FROM questions WHERE code LIKE 'q%_%' AND domain='CYBER'`)).rows[0].n;
  assert.equal(d, seed.questions.length, 'alle Fragen domain CYBER: ' + d);
  const hd = (await pool.query(`SELECT count(*)::int n FROM hazards WHERE code LIKE 'CY-%' AND domain='CYBER'`)).rows[0].n;
  assert.equal(hd, seed.hazards.length, 'alle Gefaehrdungen domain CYBER');
  const vis = (await pool.query(`SELECT count(*)::int n FROM question_visibility_rules`)).rows[0].n;
  assert.ok(vis >= 40, 'Sichtbarkeitsregeln: ' + vis);
  const ap = (await pool.query(`SELECT count(*)::int n FROM hazard_questions WHERE applicable_expression IS NOT NULL`)).rows[0].n;
  assert.ok(ap >= 2, 'applicable_expression (Steuerungsart, Aufzugsart): ' + ap);
  const hf = (await pool.query(`SELECT count(*)::int n FROM hazards WHERE code LIKE 'CY-%' AND hazard_factor IS NOT NULL AND person_groups IS NOT NULL`)).rows[0].n;
  assert.equal(hf, seed.hazards.length, 'Gefaehrdungsfaktor + Personengruppen an jeder Gefaehrdung');
  const withNoRisk = new Set(seed.rules.filter((r: any) => r.result === 'NO_RISK').map((r: any) => r.hazard));
  assert.deepEqual(seed.hazards.filter((h: any) => !withNoRisk.has(h.code)).map((h: any) => h.code), [], 'ohne NO_RISK-Regel');
  const noMeasure = seed.rules.filter((r: any) => ['LOW', 'MEDIUM', 'HIGH'].includes(r.result) && !(r.measures?.length));
  assert.deepEqual(noMeasure.map((r: any) => r.code), [], 'Risikoregeln ohne Massnahme');
});

test('Relaissteuerung ohne Vernetzung: Steuerung und Kanaele NOT_APPLICABLE, Rest bewertet', async () => {
  const asmt = await newAssessment();
  await answer(asmt, 'qa_aufzugsart', 'seil');
  await answer(asmt, 'qa_steuerungsart', 'relais');
  await answer(asmt, 'qa_vernetzt', false);
  await answer(asmt, 'qa_gebaeude_anbindung', false);
  await answer(asmt, 'qa_maschinenraum', false);
  await evaluateAssessment(pool, asmt);
  for (const h of ['CY-C01', 'CY-C10', 'CY-C11', 'CY-C12', 'CY-C13', 'CY-C14'])
    assert.equal((await statusOf(asmt, h))?.status, 'NOT_APPLICABLE', h);
  assert.equal((await statusOf(asmt, 'CY-C04'))?.status, 'INCOMPLETE', 'Notruf offen -> INCOMPLETE, nie NO_RISK');
});

test('Komponente: Vorscreening, Fernzugriff ohne Massnahmen HIGH, Kompensation MEDIUM, Zugangsmodifier', async () => {
  const asmt = await newAssessment();
  await answer(asmt, 'qa_aufzugsart', 'seil');
  await answer(asmt, 'qa_steuerungsart', 'vernetzt');
  await answer(asmt, 'qa_maschinenraum', true);
  await answer(asmt, 'qz_steuerung_frei', false);
  await answer(asmt, 'qz_triebwerksraum_frei', false);
  await answer(asmt, 'qz_schacht_frei', false);
  // PESSRAL ohne Schnittstelle -> NO_RISK ueber Vorscreening, Massnahmenfrage nicht Pflicht
  await answer(asmt, 'qc_pessral_vorhanden', true);
  await answer(asmt, 'qc_pessral_schnittstelle', 'keine');
  // UCM mit Fernzugriff ohne Massnahmen
  await answer(asmt, 'qc_ucm_vorhanden', true);
  await answer(asmt, 'qc_ucm_schnittstelle', 'fernzugriff');
  await answer(asmt, 'qc_ucm_massnahmen', 'keine');
  await evaluateAssessment(pool, asmt);
  const p = await statusOf(asmt, 'CY-C02');
  assert.equal(p?.status, 'NO_RISK'); assert.equal(p?.rule, 'CY-C02-R1');
  assert.equal((await statusOf(asmt, 'CY-C07'))?.status, 'INCOMPLETE', 'Kompensationsfrage ist Pflicht');
  await answer(asmt, 'qc_ucm_unabhaengig', false);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'CY-C07'))?.status, 'HIGH', 'Fernzugriff ohne Massnahmen -> HIGH (K-C01)');
  await answer(asmt, 'qc_ucm_unabhaengig', true);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'CY-C07'))?.status, 'MEDIUM', 'unabhaengige Ausloesung -> MEDIUM (K-C08)');
  // lokal ohne Massnahmen: Zugang gesichert MEDIUM, Zugang frei HIGH
  await answer(asmt, 'qc_ucm_schnittstelle', 'kabelgebunden');
  await answer(asmt, 'qc_ucm_unabhaengig', false);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'CY-C07'))?.status, 'MEDIUM');
  await answer(asmt, 'qz_steuerung_frei', true);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'CY-C07'))?.status, 'HIGH', 'lokal, keine Massnahmen, Zugang frei -> HIGH (K-C05)');
  // Fernzugriff mit umgesetzten Massnahmen -> NO_RISK (K-C06)
  await answer(asmt, 'qz_steuerung_frei', false);
  await answer(asmt, 'qc_ucm_schnittstelle', 'fernzugriff');
  await answer(asmt, 'qc_ucm_massnahmen', 'umgesetzt');
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'CY-C07'))?.status, 'NO_RISK', 'K-C06');
});

test('Organisation: ZUES-Dokumentationsfragen sind Pflicht (K-C20), Aenderung ohne Pruefung HIGH', async () => {
  const asmt = await newAssessment();
  await answer(asmt, 'qa_ueberwachungsbeduerftig', true);
  await answer(asmt, 'qo_pruefung_fristen', true);
  await answer(asmt, 'qo_wirksamkeit', true);
  await answer(asmt, 'qo_funktion', true);
  await answer(asmt, 'qo_zues_beruecksichtigt', true);
  await answer(asmt, 'qo_zues_erfasst', true);
  await answer(asmt, 'qo_zues_stand_technik', true);
  await answer(asmt, 'qo_aenderungen', true);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'CY-O05'))?.status, 'INCOMPLETE', 'Nr. 3 fehlt (ueberwachungsbeduerftig)');
  assert.equal((await statusOf(asmt, 'CY-O06'))?.status, 'INCOMPLETE', 'Folgefrage geprueft? fehlt');
  await answer(asmt, 'qo_zues_erhebliches_risiko', true);
  await answer(asmt, 'qo_aenderungen_geprueft', false);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'CY-O05'))?.status, 'NO_RISK');
  assert.equal((await statusOf(asmt, 'CY-O06'))?.status, 'HIGH', 'K-C18');
});

test('Katalog-Export fuer den Client: domain CYBER, fuenf Erhebungsbereiche, Kompensationsfrage sichtbar bedingt', async () => {
  const cat = await loadCatalogForClient(pool, rv);
  assert.equal(cat.questions.length, seed.questions.length);
  const q = cat.questions.find((x: any) => x.code === 'qc_ucm_unabhaengig');
  assert.ok(q?.visible_when && q.ui_number === '3.7.4', 'visible_when + ui_number');
  const h = cat.hazards.find((x: any) => x.code === 'CY-C01');
  assert.ok(h.hazard_factor && h.person_groups.length > 0, 'Faktor + Personengruppen');
  assert.ok(h.questions.find((x: any) => x.role === 'APPLICABILITY')?.applicable_when, 'applicable_when (Steuerungsart)');
  assert.equal(cat.categories.length, 5, 'Erhebungsbereiche: ' + cat.categories.length);
});
