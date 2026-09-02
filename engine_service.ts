// ============================================================================
// GBU APP 4.0 – Backend-Anbindung der Bewertungsengine
// ============================================================================
//
// Verbindet den reinen Evaluator (evaluator.ts) mit der Datenbank
// (gbu_engine_schema.sql):
//   1. Regelwerk der zur Anlage gehoerenden rule_version laden,
//   2. Antworten der Beurteilung lesen,
//   3. Evaluator laufen lassen,
//   4. Ergebnisse transaktional in evaluation_results schreiben und
//      assessment_summary aktualisieren.
//
// Bewusst gegen ein minimales DB-Interface programmiert (query/…), damit es
// mit `pg` (Pool/Client) ebenso funktioniert wie mit einem Wrapper. Bestehende
// manuelle Uebersteuerungen (manual_overrides) werden NICHT ueberschrieben:
// automatic_status wird stets aktualisiert, der effektive status bleibt bei
// is_overridden = true erhalten.
// ============================================================================

import { evaluate, summarize } from './evaluator.ts';
import type { Ruleset, AnswerMap, EvaluateOptions, EvaluationResult, RiskStatus } from './evaluator.ts';

export interface Queryable {
  query(text: string, params?: unknown[]): Promise<{ rows: any[] }>;
}
export interface Pool extends Queryable {
  connect(): Promise<PoolClientLike>;
}
export interface PoolClientLike extends Queryable {
  release(): void;
}

// ---- Regelwerk aus der DB laden -------------------------------------------

export async function loadRulesetFromDb(db: Queryable, ruleVersionId: string): Promise<Ruleset> {
  const hazardRows = (await db.query(
    `SELECT DISTINCT h.id, h.code, h.domain, h.title, h.aggregation_type,
            h.evaluation_mode, h.not_implemented
       FROM hazards h
       JOIN evaluation_rules r ON r.hazard_id = h.id
      WHERE r.rule_version_id = $1`,
    [ruleVersionId],
  )).rows;

  const hazardIds = hazardRows.map((h) => h.id);
  const hqRows = hazardIds.length === 0 ? [] : (await db.query(
    `SELECT h.code AS hazard_code, q.code AS question_code, hq.role,
            hq.required_mode, hq.required_expression, hq.applicable_expression
       FROM hazard_questions hq
       JOIN questions q ON q.id = hq.question_id
       JOIN hazards   h ON h.id = hq.hazard_id
      WHERE hq.hazard_id = ANY($1)
      ORDER BY hq.sort_order`,
    [hazardIds],
  )).rows;

  const ruleRows = (await db.query(
    `SELECT r.code, h.code AS hazard_code, r.priority, r.applicability_expression,
            r.condition_expression, r.result_status, r.aggregation_type, r.origin
       FROM evaluation_rules r
       JOIN hazards h ON h.id = r.hazard_id
      WHERE r.rule_version_id = $1 AND r.active
      ORDER BY r.priority DESC`,
    [ruleVersionId],
  )).rows;

  const questionsByHazard = new Map<string, any[]>();
  for (const q of hqRows) {
    const list = questionsByHazard.get(q.hazard_code) ?? [];
    list.push({
      question: q.question_code,
      role: q.role,
      required_mode: q.required_mode,
      ...(q.required_expression ? { required_when: q.required_expression } : {}),
      ...(q.applicable_expression ? { applicable_when: q.applicable_expression } : {}),
    });
    questionsByHazard.set(q.hazard_code, list);
  }

  return {
    hazards: hazardRows.map((h) => ({
      code: h.code,
      domain: h.domain,
      title: h.title,
      aggregation_type: h.aggregation_type,
      evaluation_mode: h.evaluation_mode,
      not_implemented: h.not_implemented,
      questions: questionsByHazard.get(h.code) ?? [],
    })),
    rules: ruleRows.map((r) => ({
      hazard: r.hazard_code,
      code: r.code,
      priority: r.priority,
      ...(r.applicability_expression ? { applicability: r.applicability_expression } : {}),
      condition: r.condition_expression,
      result: r.result_status as RiskStatus,
      ...(r.aggregation_type ? { aggregation: r.aggregation_type } : {}),
      origin: r.origin,
    })),
  };
}

// ---- Antworten lesen -------------------------------------------------------

export async function readAnswers(db: Queryable, assessmentId: string): Promise<AnswerMap> {
  const rows = (await db.query(
    `SELECT q.code, a.value_boolean, a.value_number, a.value_text, a.value_date,
            a.answered, o.value AS option_value
       FROM answers a
       JOIN questions q ON q.id = a.question_id
       LEFT JOIN question_options o ON o.id = a.option_id
      WHERE a.assessment_id = $1`,
    [assessmentId],
  )).rows;

  const answers: AnswerMap = {};
  for (const r of rows) {
    if (!r.answered) continue;
    let v: boolean | number | string | null = null;
    if (r.value_boolean !== null && r.value_boolean !== undefined) v = r.value_boolean;
    else if (r.value_number !== null && r.value_number !== undefined) v = Number(r.value_number);
    else if (r.option_value !== null && r.option_value !== undefined) v = r.option_value;
    else if (r.value_text !== null && r.value_text !== undefined) v = r.value_text;
    else if (r.value_date !== null && r.value_date !== undefined) v = String(r.value_date);
    answers[r.code] = v;
  }
  return answers;
}

// ---- Bewertung + Persistenz ------------------------------------------------

export interface AssessmentEvaluation {
  results: EvaluationResult[];
  summary: Record<RiskStatus, number>;
}

export async function evaluateAssessment(
  pool: Pool,
  assessmentId: string,
  opts: EvaluateOptions = {},
): Promise<AssessmentEvaluation> {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    const asmt = (await client.query(
      'SELECT rule_version_id FROM assessments WHERE id = $1', [assessmentId],
    )).rows[0];
    if (!asmt) throw new Error(`Assessment ${assessmentId} nicht gefunden`);
    const ruleVersionId = asmt.rule_version_id;

    const ruleset = await loadRulesetFromDb(client, ruleVersionId);
    const answers = await readAnswers(client, assessmentId);
    const results = evaluate(ruleset, answers, opts);

    // Code -> id Auffloesung
    const hazardIdByCode = new Map<string, string>();
    for (const row of (await client.query(
      'SELECT id, code FROM hazards WHERE code = ANY($1)',
      [ruleset.hazards!.map((h) => h.code)],
    )).rows) hazardIdByCode.set(row.code, row.id);

    const ruleIdByCode = new Map<string, string>();
    for (const row of (await client.query(
      'SELECT id, code FROM evaluation_rules WHERE rule_version_id = $1', [ruleVersionId],
    )).rows) ruleIdByCode.set(row.code, row.id);

    for (const r of results) {
      await client.query(
        `INSERT INTO evaluation_results
           (assessment_id, hazard_id, status, automatic_status, matched_rule_id,
            rule_version_id, input_snapshot, evaluated_at)
         VALUES ($1, $2, $3::risk_status, $4::risk_status, $5, $6, $7::jsonb, now())
         ON CONFLICT (assessment_id, hazard_id) DO UPDATE SET
           automatic_status = EXCLUDED.automatic_status,
           status = CASE WHEN evaluation_results.is_overridden
                         THEN evaluation_results.status
                         ELSE EXCLUDED.automatic_status END,
           matched_rule_id = EXCLUDED.matched_rule_id,
           rule_version_id = EXCLUDED.rule_version_id,
           input_snapshot  = EXCLUDED.input_snapshot,
           evaluated_at    = now()`,
        [
          assessmentId,
          hazardIdByCode.get(r.hazard),
          r.status,
          r.automatic_status,
          r.matched_rule ? ruleIdByCode.get(r.matched_rule) ?? null : null,
          ruleVersionId,
          JSON.stringify(r.input_snapshot),
        ],
      );
    }

    const summary = summarize(results);

    // Fragenzahlen: distinkte Fragen des Regelwerks + davon beantwortet.
    const questionCodes = new Set<string>();
    for (const h of ruleset.hazards ?? []) for (const q of h.questions ?? []) questionCodes.add(q.question);
    const questionsTotal = questionCodes.size;
    let questionsAnswered = 0;
    for (const c of questionCodes) if (c in answers) questionsAnswered++;

    await client.query(
      `INSERT INTO assessment_summary
         (assessment_id, questions_total, questions_answered, hazards_total,
          hazards_high, hazards_medium, hazards_low, hazards_no_risk,
          hazards_not_applicable, hazards_incomplete, computed_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10, now())
       ON CONFLICT (assessment_id) DO UPDATE SET
         questions_total = EXCLUDED.questions_total,
         questions_answered = EXCLUDED.questions_answered,
         hazards_total = EXCLUDED.hazards_total,
         hazards_high = EXCLUDED.hazards_high,
         hazards_medium = EXCLUDED.hazards_medium,
         hazards_low = EXCLUDED.hazards_low,
         hazards_no_risk = EXCLUDED.hazards_no_risk,
         hazards_not_applicable = EXCLUDED.hazards_not_applicable,
         hazards_incomplete = EXCLUDED.hazards_incomplete,
         computed_at = now()`,
      [
        assessmentId, questionsTotal, questionsAnswered, results.length,
        summary.HIGH, summary.MEDIUM, summary.LOW, summary.NO_RISK,
        summary.NOT_APPLICABLE, summary.INCOMPLETE,
      ],
    );

    await client.query('COMMIT');
    return { results, summary };
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

// ---- Express-Anbindung (optional) -----------------------------------------
//
// Minimaler Router-Factory, framework-leicht gehalten. Erwartet einen
// pg-Pool. `app` ist ein Express-App/Router mit .post/.get.

export function registerEngineRoutes(app: any, pool: Pool): void {
  app.post('/assessments/:id/evaluate', async (req: any, res: any) => {
    try {
      const out = await evaluateAssessment(pool, req.params.id);
      res.json({ ok: true, summary: out.summary, count: out.results.length });
    } catch (err: any) {
      res.status(400).json({ ok: false, error: String(err?.message ?? err) });
    }
  });

  app.get('/assessments/:id/results', async (req: any, res: any) => {
    try {
      const { rows } = await pool.query(
        `SELECT h.code AS hazard, er.status, er.automatic_status, er.is_overridden,
                r.code AS matched_rule, er.input_snapshot, er.evaluated_at
           FROM evaluation_results er
           JOIN hazards h ON h.id = er.hazard_id
           LEFT JOIN evaluation_rules r ON r.id = er.matched_rule_id
          WHERE er.assessment_id = $1
          ORDER BY h.code`,
        [req.params.id],
      );
      res.json({ ok: true, results: rows });
    } catch (err: any) {
      res.status(400).json({ ok: false, error: String(err?.message ?? err) });
    }
  });
}
