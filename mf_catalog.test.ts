// End-to-End fuer den mehrfragigen Typ „EN 81-20 mehrfragig" (norm_81_20_mf.json):
// Seed gegen echtes PostgreSQL laden (inkl. ui_number, Sichtbarkeitsregeln,
// applicable_expression, hazard_factor/person_groups), zwei Anlagen beantworten
// und die Bewertung ueber engine_service pruefen. Belegt:
//   * Anlagenmerkmal als Ausdruck -> NOT_APPLICABLE (Hydraulik: keine Bremse/Fang)
//   * Zahlenschwelle + Kompensation ueber Prioritaet (Schuerze, Haltegenauigkeit)
//   * Pflichtfrage fehlt -> INCOMPLETE, nie NO_RISK
//   * Katalog-Export fuer den Client enthaelt die neuen Felder.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import pg from 'pg';
import { loadSeedIntoDb } from './seed_loader.ts';
import { evaluateAssessment } from './engine_service.ts';
import { loadCatalogForClient } from './engine_api.ts';
import { evaluate } from './evaluator.ts';

const PORT = Number(process.env.PGPORT ?? 5433);
const HOST = process.env.PGHOST ?? '127.0.0.1';
const USER = process.env.PGUSER ?? 'postgres';
const DB = 'gbu_mf_e2e';
const schemaSql = readFileSync(new URL('./gbu_engine_schema.sql', import.meta.url), 'utf8');
const seed = JSON.parse(readFileSync(new URL('./norm_81_20_mf.json', import.meta.url).pathname, 'utf8'));

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
  const t = (await pool.query(`INSERT INTO tenants(name,slug) VALUES ('MF','mf-${Math.random().toString(36).slice(2)}') RETURNING id`)).rows[0];
  const a = (await pool.query(`INSERT INTO assets(tenant_id,asset_number) VALUES ($1,'A') RETURNING id`, [t.id])).rows[0];
  return (await pool.query(
    `INSERT INTO assessments(tenant_id,asset_id,type,rule_version_id) VALUES ($1,$2,'GBU',$3) RETURNING id`,
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

test('Seed geladen: Fragen mit ui_number/Sichtbarkeit, hazard_questions mit applicable_expression', async () => {
  const q = (await pool.query(`SELECT count(*)::int n FROM questions WHERE code LIKE 'q%_%' AND ui_number IS NOT NULL`)).rows[0].n;
  assert.ok(q >= 250, 'ui_number gesetzt: ' + q);
  const vis = (await pool.query(`SELECT count(*)::int n FROM question_visibility_rules`)).rows[0].n;
  assert.ok(vis >= 80, 'Sichtbarkeitsregeln: ' + vis);
  const ap = (await pool.query(`SELECT count(*)::int n FROM hazard_questions WHERE applicable_expression IS NOT NULL`)).rows[0].n;
  assert.ok(ap >= 8, 'applicable_expression: ' + ap);
  const hf = (await pool.query(`SELECT count(*)::int n FROM hazards WHERE code LIKE 'MF-%' AND hazard_factor IS NOT NULL AND person_groups IS NOT NULL`)).rows[0].n;
  assert.equal(hf, seed.hazards.length, 'Gefaehrdungsfaktor + Personengruppen an jeder Gefaehrdung');
});

test('Hydraulikaufzug: Seil-Gefaehrdungen NOT_APPLICABLE, Hydraulik-Gefaehrdung bewertet', async () => {
  const asmt = await newAssessment();
  await answer(asmt, 'qa_aufzugsart', 'hydraulik');
  await answer(asmt, 'qa_antrieb', 'hydraulisch');
  await answer(asmt, 'qm_absperrventil', true);
  await answer(asmt, 'qm_absperrventil_gekennz', true);
  await answer(asmt, 'qm_rohrbruch', false);
  await answer(asmt, 'qm_kav', true);
  await answer(asmt, 'qm_absinkt', false);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'MF-M08'))?.status, 'NOT_APPLICABLE', 'Bremse nur bei Seil');
  assert.equal((await statusOf(asmt, 'MF-S05'))?.status, 'NOT_APPLICABLE', 'Fangvorrichtung nur bei Seil');
  assert.equal((await statusOf(asmt, 'MF-M03'))?.status, 'NOT_APPLICABLE', 'Einzug nur bei Seil');
  assert.equal((await statusOf(asmt, 'MF-M10'))?.status, 'NOT_APPLICABLE', 'Fahrschuetze nicht bei hydraulischem Antrieb');
  const h = await statusOf(asmt, 'MF-M13');
  assert.equal(h?.status, 'HIGH', 'Rohrbruchsicherung fehlt -> HIGH');
  assert.equal((await statusOf(asmt, 'MF-K01'))?.status, 'INCOMPLETE', 'Notruf unbeantwortet -> INCOMPLETE, nie NO_RISK');
});

test('Seilaufzug: Schuerze 200 mm mit/ohne Kompensation, Stufenbildung mit PmeM-Modifier', async () => {
  const asmt = await newAssessment();
  await answer(asmt, 'qa_aufzugsart', 'seil');
  await answer(asmt, 'qa_nutzung_pmem', true);
  await answer(asmt, 'qk_schuerze_mm', 200);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'MF-K04'))?.status, 'INCOMPLETE', 'Kompensationsfrage wird unter 300 mm Pflicht');
  await answer(asmt, 'qk_befreiung_nur_fachkundig', true);
  await evaluateAssessment(pool, asmt);
  let k04 = await statusOf(asmt, 'MF-K04');
  assert.equal(k04?.status, 'MEDIUM');
  assert.equal(k04?.rule, 'MF-K04-R1');
  await answer(asmt, 'qk_befreiung_nur_fachkundig', false);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'MF-K04'))?.status, 'HIGH');

  await answer(asmt, 'qk_stufe_mm', 15);
  await evaluateAssessment(pool, asmt);
  const k03 = await statusOf(asmt, 'MF-K03');
  assert.equal(k03?.status, 'HIGH', '10-20 mm + PmeM-Nutzung -> HIGH (Modifier)');
  assert.equal(k03?.rule, 'MF-K03-R2');
  await answer(asmt, 'qa_nutzung_pmem', false);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'MF-K03'))?.status, 'MEDIUM', 'ohne Modifier MEDIUM');
});

test('Ortsmatrix: Asbest an einem Ort -> HIGH, aber erst wenn alle Ortsfragen beantwortet sind', async () => {
  const asmt = await newAssessment();
  await answer(asmt, 'qa_maschinenraum', true);
  await answer(asmt, 'qz_asbest', false);
  await answer(asmt, 'qm_asbest', true);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'MF-U01'))?.status, 'INCOMPLETE', 'Schacht/Grube/unbekannt noch offen');
  await answer(asmt, 'qs_asbest', false);
  await answer(asmt, 'qg_asbest', false);
  await answer(asmt, 'qu_asbest_unbekannt', false);
  await evaluateAssessment(pool, asmt);
  assert.equal((await statusOf(asmt, 'MF-U01'))?.status, 'HIGH');
});

test('Katalog-Export fuer den Client traegt die neuen Felder', async () => {
  const cat = await loadCatalogForClient(pool, rv);
  const q = cat.questions.find((x: any) => x.code === 'qz_bel_ausreichend');
  assert.ok(q?.visible_when && q.ui_number === '5.2', 'visible_when + ui_number');
  const h = cat.hazards.find((x: any) => x.code === 'MF-M08');
  assert.ok(h.hazard_factor && h.person_groups.length > 0, 'Faktor + Personengruppen');
  const ap = h.questions.find((x: any) => x.role === 'APPLICABILITY');
  assert.ok(ap?.applicable_when, 'applicable_when im Export');
  assert.ok(cat.categories.length >= 10, 'Erhebungsbereiche: ' + cat.categories.length);
});

test('Review 02.09.2026: jede Gefaehrdung hat eine ausdrueckliche Kein-Risiko-Regel, Massnahmen aller Treffer', async () => {
  const seed = JSON.parse(readFileSync(new URL('./norm_81_20_mf.json', import.meta.url).pathname, 'utf8'));
  const withNoRisk = new Set(seed.rules.filter((r: any) => r.result === 'NO_RISK').map((r: any) => r.hazard));
  const missing = seed.hazards.filter((h: any) => !withNoRisk.has(h.code)).map((h: any) => h.code);
  assert.deepEqual(missing, [], 'ohne NO_RISK-Regel: ' + missing.join(','));
  const noMeasure = seed.rules.filter((r: any) => ['LOW', 'MEDIUM', 'HIGH'].includes(r.result) && !(r.measures?.length));
  assert.deepEqual(noMeasure.map((r: any) => r.code), [], 'Risikoregeln ohne Massnahme');
  // Stufenbildung 15 mm mit PmeM: R2 (HIGH) gewinnt, R3 (MEDIUM) trifft ebenfalls zu -> beide in matched_rules
  const res = evaluate(seed, { qk_stufe_mm: 15, qk_nachregulierung: true, qa_nutzung_pmem: true });
  const k03 = res.find((r) => r.hazard === 'MF-K03')!;
  assert.equal(k03.status, 'HIGH');
  assert.deepEqual(k03.matched_rules, ['MF-K03-R2'], 'NONE: nur der Gewinner traegt Massnahmen');
  assert.ok(k03.overridden_rules.includes('MF-K03-R3'), 'R3 trifft zu, ist aber uebersteuert: ' + k03.overridden_rules.join(','));
  // MAXIMUM: unabhaengige Maengel derselben Gefaehrdung fuehren Massnahmen zusammen
  const m03 = evaluate(seed, { qa_aufzugsart: 'seil', qa_maschinenraum: true, qm_hauptschalter: true,
    qm_hauptschalter_abschliessbar: false, qm_hauptschalter_gekennz: false, qm_kennz_elektrisch: true }).find((r) => r.hazard === 'MF-M03')!;
  if (m03.status !== 'INCOMPLETE') assert.ok(m03.matched_rules.length >= 1, 'M03 bewertet');
  // Regelluecke ist fail-closed: keine Regel -> INCOMPLETE + rule_gap
  const gapSeed = { hazards: [{ code: 'X', questions: [{ question: 'qx', role: 'TRIGGER', required_mode: 'ALWAYS' }] }],
    rules: [{ hazard: 'X', code: 'X-R1', priority: 100, condition: { question: 'qx', operator: 'EQ', value: false }, result: 'HIGH' },
            { hazard: 'X', code: 'X-R2', priority: 1, condition: { question: 'qy', operator: 'EQ', value: true }, result: 'NO_RISK' }] } as any;
  const gap = evaluate(gapSeed, { qx: true })[0];
  assert.equal(gap.status, 'INCOMPLETE'); assert.equal(gap.rule_gap, true);
  // Altstil ohne jede NO_RISK-Regel (Rekonstruktion): weiterhin NO_RISK, aber gekennzeichnet
  const legacy = evaluate({ ...gapSeed, rules: [gapSeed.rules[0]] }, { qx: true })[0];
  assert.equal(legacy.status, 'NO_RISK'); assert.equal(legacy.implicit_no_risk, true);
  // Im MF-Seed kann es keinen impliziten Kein-Risiko-Zustand geben
  for (const h of seed.hazards) assert.ok(seed.rules.some((r: any) => r.hazard === h.code && r.result === 'NO_RISK'), h.code);
  // Alles in Ordnung -> ausdrueckliche NO_RISK-Regel statt stillem Fallback
  const ok = evaluate(seed, { qk_stufe_mm: 3, qk_nachregulierung: true, qa_nutzung_pmem: false }).find((r) => r.hazard === 'MF-K03')!;
  assert.equal(ok.status, 'NO_RISK');
  assert.ok(ok.matched_rule, 'NO_RISK durch Regel, nicht durch Fallback');
});

test('K-K12: Hydraulikaufzug hat immer Tueruebrueckung -> ohne UCM HIGH, Frage 8.27 nicht noetig', async () => {
  const seed = JSON.parse(readFileSync(new URL('./norm_81_20_mf.json', import.meta.url).pathname, 'utf8'));
  const st = (a: Record<string, any>) => evaluate(seed, a).find((r) => r.hazard === 'MF-K12')!;
  assert.equal(st({ qa_aufzugsart: 'hydraulik', qa_ucm_a3: false }).status, 'HIGH');
  assert.equal(st({ qa_aufzugsart: 'hydraulik', qa_ucm_a3: false }).matched_rule, 'MF-K12-R1');
  assert.equal(st({ qa_aufzugsart: 'hydraulik', qa_ucm_a3: true }).status, 'NO_RISK');
  assert.equal(st({ qa_aufzugsart: 'seil', qa_ucm_a3: false }).status, 'INCOMPLETE', 'Seil: 8.27 ist Pflicht');
  assert.equal(st({ qa_aufzugsart: 'seil', qa_ucm_a3: false, qk_ucm_sr_modul: true, qm_zweikreisbremse: true,
    qm_bremse_ueberwacht: true, qa_lagerung_statisch_bestimmt: true }).status, 'HIGH', 'Seil mit SR-Modul: HIGH trotz Bremse');
  const q = seed.questions.find((x: any) => x.code === 'qk_ucm_sr_modul');
  assert.ok(q.visible_when, '8.27 bei Hydraulik ausgeblendet');
});
