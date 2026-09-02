// ============================================================================
// GBU APP 4.0 – REST-API der Bewertungsengine (Express)
// ============================================================================
//
// Baut auf engine_service.ts auf und stellt die Endpunkte bereit, die eine
// App (Flutter/Web) braucht: Katalog aus der DB laden, Beurteilung anlegen,
// Antworten speichern, evaluieren und Ergebnisse lesen. Der ausgelieferte
// Katalog hat dieselbe Form wie die Seed-Dateien (questions/measures/hazards/
// rules) – die App kann ihn statt gebündelter Assets auch über HTTP beziehen.
// ============================================================================

import { evaluateAssessment } from './engine_service.ts';
import type { Pool } from './engine_service.ts';

// ---- Katalog für den Client (Anzeige-Form) aus der DB rekonstruieren -------

export async function loadCatalogForClient(db: Pool, ruleVersionId: string): Promise<any> {
  const rv = (await db.query(
    'SELECT id, name, version, domain FROM rule_versions WHERE id = $1', [ruleVersionId])).rows[0];
  if (!rv) return null;

  const hazardRows = (await db.query(
    `SELECT DISTINCT h.id, h.code, h.domain, h.title, h.description, h.category,
            h.aggregation_type, h.evaluation_mode, h.not_implemented
       FROM hazards h JOIN evaluation_rules r ON r.hazard_id = h.id
      WHERE r.rule_version_id = $1
      ORDER BY h.code`, [ruleVersionId])).rows;
  const hazardIds = hazardRows.map((h) => h.id);

  const hqRows = hazardIds.length ? (await db.query(
    `SELECT h.code AS hazard_code, q.code AS question_code, hq.role, hq.required_mode
       FROM hazard_questions hq JOIN questions q ON q.id = hq.question_id
       JOIN hazards h ON h.id = hq.hazard_id
      WHERE hq.hazard_id = ANY($1) ORDER BY hq.sort_order`, [hazardIds])).rows : [];

  const srcRows = hazardIds.length ? (await db.query(
    `SELECT h.code AS hazard_code, s.source_type AS type, s.document_code AS document, s.section
       FROM hazard_sources hs JOIN source_references s ON s.id = hs.source_reference_id
       JOIN hazards h ON h.id = hs.hazard_id
      WHERE hs.hazard_id = ANY($1)`, [hazardIds])).rows : [];

  const qCodes = [...new Set(hqRows.map((r) => r.question_code))];
  const qRows = qCodes.length ? (await db.query(
    `SELECT code, question_type, text FROM questions WHERE code = ANY($1)`, [qCodes])).rows : [];
  const optRows = qCodes.length ? (await db.query(
    `SELECT q.code AS qcode, o.value, o.label FROM question_options o
       JOIN questions q ON q.id = o.question_id
      WHERE q.code = ANY($1) ORDER BY o.sort_order`, [qCodes])).rows : [];

  const ruleRows = (await db.query(
    `SELECT r.id, r.code, h.code AS hazard_code, r.priority, r.applicability_expression,
            r.condition_expression, r.result_status, r.aggregation_type, r.origin
       FROM evaluation_rules r JOIN hazards h ON h.id = r.hazard_id
      WHERE r.rule_version_id = $1 AND r.active`, [ruleVersionId])).rows;
  const ruleIds = ruleRows.map((r) => r.id);
  const rmRows = ruleIds.length ? (await db.query(
    `SELECT r.code AS rule_code, m.code AS measure_code, rm.relation, rm.mandatory, rm.group_id
       FROM rule_measures rm JOIN evaluation_rules r ON r.id = rm.evaluation_rule_id
       JOIN measures m ON m.id = rm.measure_id
      WHERE rm.evaluation_rule_id = ANY($1) ORDER BY rm.sort_order`, [ruleIds])).rows : [];
  const measRows = (await db.query(
    `SELECT DISTINCT m.code, m.title, m.type FROM measures m
       JOIN rule_measures rm ON rm.measure_id = m.id
       JOIN evaluation_rules r ON r.id = rm.evaluation_rule_id
      WHERE r.rule_version_id = $1`, [ruleVersionId])).rows;

  const optByQ = new Map<string, any[]>();
  for (const o of optRows) (optByQ.get(o.qcode) ?? optByQ.set(o.qcode, []).get(o.qcode))!
    .push({ value: o.value, label: o.label });
  const questions = qRows.map((q) => ({
    code: q.code, type: q.question_type, text: q.text, options: optByQ.get(q.code) ?? [],
  }));

  const hqByHaz = new Map<string, any[]>();
  for (const r of hqRows) (hqByHaz.get(r.hazard_code) ?? hqByHaz.set(r.hazard_code, []).get(r.hazard_code))!
    .push({ question: r.question_code, role: r.role, required_mode: r.required_mode });
  const srcByHaz = new Map<string, any[]>();
  for (const s of srcRows) (srcByHaz.get(s.hazard_code) ?? srcByHaz.set(s.hazard_code, []).get(s.hazard_code))!
    .push({ type: s.type, document: s.document, ...(s.section ? { section: s.section } : {}) });
  const hazards = hazardRows.map((h) => ({
    code: h.code, domain: h.domain, title: h.title, description: h.description ?? undefined,
    category: h.category ?? undefined, aggregation_type: h.aggregation_type,
    evaluation_mode: h.evaluation_mode, not_implemented: h.not_implemented,
    questions: hqByHaz.get(h.code) ?? [], sources: srcByHaz.get(h.code) ?? [],
  }));

  const mbByRule = new Map<string, any[]>();
  for (const m of rmRows) (mbByRule.get(m.rule_code) ?? mbByRule.set(m.rule_code, []).get(m.rule_code))!
    .push({ measure: m.measure_code, relation: m.relation, mandatory: m.mandatory });
  const rules = ruleRows.map((r) => ({
    hazard: r.hazard_code, code: r.code, priority: r.priority,
    ...(r.applicability_expression ? { applicability: r.applicability_expression } : {}),
    condition: r.condition_expression, result: r.result_status,
    ...(r.aggregation_type ? { aggregation: r.aggregation_type } : {}),
    origin: r.origin, measures: mbByRule.get(r.code) ?? [],
  }));

  return {
    rule_version_id: rv.id, rule_version: `${rv.name} ${rv.version}`, domain: rv.domain,
    questions, measures: measRows, hazards, rules,
  };
}

// ---- Antworten speichern (Code -> passende Spalte) -------------------------

async function saveAnswers(db: Pool, assessmentId: string, answers: Record<string, unknown>): Promise<void> {
  for (const [code, value] of Object.entries(answers)) {
    const q = (await db.query('SELECT id, question_type FROM questions WHERE code = $1', [code])).rows[0];
    if (!q) continue;
    const cols: any = { value_boolean: null, value_number: null, value_text: null, option_id: null };
    if (value === null || value === undefined || value === '') {
      await db.query('DELETE FROM answers WHERE assessment_id = $1 AND question_id = $2', [assessmentId, q.id]);
      continue;
    }
    if (q.question_type === 'YES_NO' || q.question_type === 'YES_NO_NA') {
      cols.value_boolean = value === true || value === 'true' || value === 'ja';
    } else if (q.question_type === 'NUMBER') {
      cols.value_number = Number(value);
    } else if (q.question_type === 'SELECT' || q.question_type === 'MULTI_SELECT' || q.question_type === 'SELECT_PHOTO') {
      const o = (await db.query('SELECT id FROM question_options WHERE question_id = $1 AND value = $2', [q.id, value])).rows[0];
      if (o) cols.option_id = o.id; else cols.value_text = String(value);
    } else {
      cols.value_text = String(value);
    }
    await db.query(
      `INSERT INTO answers (assessment_id, question_id, value_boolean, value_number, value_text, option_id, answered)
       VALUES ($1,$2,$3,$4,$5,$6,true)
       ON CONFLICT (assessment_id, question_id) DO UPDATE SET
         value_boolean = EXCLUDED.value_boolean, value_number = EXCLUDED.value_number,
         value_text = EXCLUDED.value_text, option_id = EXCLUDED.option_id, answered = true`,
      [assessmentId, q.id, cols.value_boolean, cols.value_number, cols.value_text, cols.option_id]);
  }
}

// ---- Routen ----------------------------------------------------------------

export function registerEngineApi(app: any, pool: Pool): void {
  const wrap = (fn: any) => (req: any, res: any) =>
    fn(req, res).catch((e: any) => res.status(400).json({ ok: false, error: String(e?.message ?? e) }));

  app.get('/health', wrap(async (_req: any, res: any) => {
    await pool.query('SELECT 1');
    res.json({ ok: true });
  }));

  app.get('/rule-versions', wrap(async (_req: any, res: any) => {
    const rows = (await pool.query(
      `SELECT rv.id, rv.name, rv.version, rv.domain,
              count(DISTINCT r.hazard_id)::int AS hazards
         FROM rule_versions rv LEFT JOIN evaluation_rules r ON r.rule_version_id = rv.id
        GROUP BY rv.id ORDER BY rv.name`)).rows;
    res.json({ ok: true, rule_versions: rows });
  }));

  app.get('/rule-versions/:id/catalog', wrap(async (req: any, res: any) => {
    const cat = await loadCatalogForClient(pool, req.params.id);
    if (!cat) return res.status(404).json({ ok: false, error: 'rule_version nicht gefunden' });
    res.json({ ok: true, catalog: cat });
  }));

  app.post('/assessments', wrap(async (req: any, res: any) => {
    const { rule_version_id, type = 'GBU', asset_number = 'API' } = req.body ?? {};
    if (!rule_version_id) throw new Error('rule_version_id fehlt');
    const tenant = (await pool.query(
      `INSERT INTO tenants (name, slug) VALUES ('API-Demo','api-demo')
       ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name RETURNING id`)).rows[0];
    const asset = (await pool.query(
      `INSERT INTO assets (tenant_id, asset_number) VALUES ($1,$2) RETURNING id`,
      [tenant.id, asset_number])).rows[0];
    const a = (await pool.query(
      `INSERT INTO assessments (tenant_id, asset_id, type, rule_version_id)
       VALUES ($1,$2,$3,$4) RETURNING id`,
      [tenant.id, asset.id, type, rule_version_id])).rows[0];
    res.json({ ok: true, assessment_id: a.id });
  }));

  app.put('/assessments/:id/answers', wrap(async (req: any, res: any) => {
    const answers = (req.body && req.body.answers) || {};
    await saveAnswers(pool, req.params.id, answers);
    const out = await evaluateAssessment(pool, req.params.id);
    res.json({ ok: true, summary: out.summary });
  }));

  app.post('/assessments/:id/evaluate', wrap(async (req: any, res: any) => {
    const out = await evaluateAssessment(pool, req.params.id);
    res.json({ ok: true, summary: out.summary, count: out.results.length });
  }));

  app.get('/assessments/:id/results', wrap(async (req: any, res: any) => {
    const rows = (await pool.query(
      `SELECT h.code AS hazard, er.status, er.automatic_status, er.is_overridden,
              r.code AS matched_rule, er.input_snapshot
         FROM evaluation_results er JOIN hazards h ON h.id = er.hazard_id
         LEFT JOIN evaluation_rules r ON r.id = er.matched_rule_id
        WHERE er.assessment_id = $1 ORDER BY h.code`, [req.params.id])).rows;
    res.json({ ok: true, results: rows });
  }));

  app.get('/assessments/:id', wrap(async (req: any, res: any) => {
    const a = (await pool.query(
      `SELECT id, type, status, rule_version_id FROM assessments WHERE id = $1`, [req.params.id])).rows[0];
    if (!a) return res.status(404).json({ ok: false, error: 'assessment nicht gefunden' });
    const answers = (await pool.query(
      `SELECT q.code, a.value_boolean, a.value_number, a.value_text, o.value AS option_value
         FROM answers a JOIN questions q ON q.id = a.question_id
         LEFT JOIN question_options o ON o.id = a.option_id
        WHERE a.assessment_id = $1 AND a.answered`, [req.params.id])).rows;
    const ansMap: Record<string, unknown> = {};
    for (const r of answers) ansMap[r.code] =
      r.option_value ?? r.value_boolean ?? (r.value_number != null ? Number(r.value_number) : r.value_text);
    const summary = (await pool.query(
      `SELECT * FROM assessment_summary WHERE assessment_id = $1`, [req.params.id])).rows[0] ?? null;
    res.json({ ok: true, assessment: a, answers: ansMap, summary });
  }));
}
