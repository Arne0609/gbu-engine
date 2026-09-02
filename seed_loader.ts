// ============================================================================
// GBU APP 4.0 – Seed-Loader: seed_rules.json -> Datenbank
// ============================================================================
//
// Legt aus dem Seed-Regelwerk die Zeilen in rule_versions, questions, hazards,
// hazard_questions und evaluation_rules an. Fragen, die nur ueber ihren Code
// referenziert sind (in seed_rules.json gibt es keinen Fragenkatalog), werden
// als YES_NO-Fragen angelegt – ausreichend fuer Auswertung und E2E-Test.
// Idempotent ueber ON CONFLICT.
// ============================================================================

import type { Queryable } from './engine_service.ts';

type Expr = Record<string, any>;

function collectQuestionsFromExpr(expr: Expr | undefined, into: Set<string>): void {
  if (!expr) return;
  if ('all' in expr) { for (const e of expr.all) collectQuestionsFromExpr(e, into); return; }
  if ('any' in expr) { for (const e of expr.any) collectQuestionsFromExpr(e, into); return; }
  if ('not' in expr) { collectQuestionsFromExpr(expr.not, into); return; }
  if (typeof expr.question === 'string') into.add(expr.question);
}

export interface SeedResult { ruleVersionId: string; questionCount: number; }

export async function loadSeedIntoDb(db: Queryable, seed: any): Promise<SeedResult> {
  // 1) Regelversion
  const rv = (await db.query(
    `INSERT INTO rule_versions (name, version, domain, valid_from, status, description)
     VALUES ('GBU-Regelwerk', $1, 'BOTH', CURRENT_DATE, 'PUBLISHED', 'Seed aus seed_rules.json')
     ON CONFLICT (name, version) DO UPDATE SET status = 'PUBLISHED'
     RETURNING id`,
    [seed.rule_version ?? '2026.1-seed'],
  )).rows[0];
  const ruleVersionId = rv.id as string;

  const questionIdByCode = new Map<string, string>();

  // 2a) Explizit definierter Fragenkatalog (Typ + Antwortoptionen).
  for (const q of seed.questions ?? []) {
    const row = (await db.query(
      `INSERT INTO questions (code, legacy_id, domain, text, question_type)
       VALUES ($1, $2, $3, $4, $5)
       ON CONFLICT (code) DO UPDATE SET
         text = EXCLUDED.text, question_type = EXCLUDED.question_type,
         domain = EXCLUDED.domain
       RETURNING id`,
      [q.code, q.legacy_id ?? null, q.domain ?? 'BOTH', q.text ?? q.code,
       q.type ?? 'YES_NO'],
    )).rows[0];
    questionIdByCode.set(q.code, row.id);
    let sort = 0;
    for (const o of q.options ?? []) {
      await db.query(
        `INSERT INTO question_options (question_id, value, label, semantic_value, sort_order)
         VALUES ($1,$2,$3,$4,$5)
         ON CONFLICT (question_id, value) DO UPDATE SET label = EXCLUDED.label`,
        [row.id, o.value, o.label, o.semantic_value ?? null, sort++],
      );
    }
  }

  // 2b) Fragen sammeln (aus hazard_questions und Regelausdruecken); noch nicht
  //     definierte Codes als YES_NO anlegen (Rückwärtskompatibilität).
  const questionCodes = new Set<string>();
  for (const h of seed.hazards ?? []) for (const q of h.questions ?? []) questionCodes.add(q.question);
  for (const r of seed.rules ?? []) {
    collectQuestionsFromExpr(r.applicability, questionCodes);
    collectQuestionsFromExpr(r.condition, questionCodes);
  }
  for (const code of questionCodes) {
    if (questionIdByCode.has(code)) continue;
    const row = (await db.query(
      `INSERT INTO questions (code, domain, text, question_type)
       VALUES ($1, 'BOTH', $2, 'YES_NO')
       ON CONFLICT (code) DO UPDATE SET text = EXCLUDED.text
       RETURNING id`,
      [code, code],
    )).rows[0];
    questionIdByCode.set(code, row.id);
  }

  // Norm-/Quellenbezug (dedupliziert über source_references).
  const sourceIdByKey = new Map<string, string>();
  async function ensureSource(s: any): Promise<string | null> {
    if (!s || !s.document) return null;
    const type = s.type ?? 'OTHER';
    const document = String(s.document).slice(0, 80);
    const section = (s.section ?? '').slice(0, 120);
    const key = `${type}|${document}|${section}`;
    const hit = sourceIdByKey.get(key);
    if (hit) return hit;
    const row = (await db.query(
      `INSERT INTO source_references (source_type, document_code, section, title)
       VALUES ($1,$2,$3,$4)
       ON CONFLICT (source_type, document_code, section) DO UPDATE SET title = EXCLUDED.title
       RETURNING id`,
      [type, document, section, s.title ?? null],
    )).rows[0];
    sourceIdByKey.set(key, row.id);
    return row.id;
  }

  // 3) Gefaehrdungen + hazard_questions + hazard_sources
  const hazardIdByCode = new Map<string, string>();
  for (const h of seed.hazards ?? []) {
    const row = (await db.query(
      `INSERT INTO hazards (code, domain, title, description, category,
                            aggregation_type, evaluation_mode, not_implemented)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
       ON CONFLICT (code) DO UPDATE SET
         title = EXCLUDED.title, description = EXCLUDED.description,
         aggregation_type = EXCLUDED.aggregation_type,
         evaluation_mode = EXCLUDED.evaluation_mode
       RETURNING id`,
      [h.code, h.domain, h.title, h.description ?? null, h.category ?? null,
       h.aggregation_type ?? 'NONE', h.evaluation_mode ?? 'STANDARD',
       h.not_implemented ?? false],
    )).rows[0];
    hazardIdByCode.set(h.code, row.id);

    let sort = 0;
    for (const q of h.questions ?? []) {
      await db.query(
        `INSERT INTO hazard_questions (hazard_id, question_id, role, required_mode,
                                       required_expression, sort_order, notes)
         VALUES ($1,$2,$3,$4,$5::jsonb,$6,$7)
         ON CONFLICT (hazard_id, question_id, role) DO UPDATE SET
           required_mode = EXCLUDED.required_mode`,
        [row.id, questionIdByCode.get(q.question), q.role,
         q.required_mode ?? 'NEVER',
         q.required_when ? JSON.stringify(q.required_when) : null,
         sort++, q.notes ?? null],
      );
    }
    for (const s of h.sources ?? []) {
      const sid = await ensureSource(s);
      if (sid) await db.query(
        `INSERT INTO hazard_sources (hazard_id, source_reference_id) VALUES ($1,$2)
         ON CONFLICT DO NOTHING`, [row.id, sid]);
    }
  }

  // 4) Maßnahmenkatalog
  const measureIdByCode = new Map<string, string>();
  for (const m of seed.measures ?? []) {
    const row = (await db.query(
      `INSERT INTO measures (code, title, description, type, priority_class)
       VALUES ($1,$2,$3,$4,$5)
       ON CONFLICT (code) DO UPDATE SET title = EXCLUDED.title, type = EXCLUDED.type
       RETURNING id`,
      [m.code, m.title, m.description ?? null, m.type, m.priority_class ?? null],
    )).rows[0];
    measureIdByCode.set(m.code, row.id);
  }

  // 5) Bewertungsregeln (+ rule_measures)
  for (const r of seed.rules ?? []) {
    const rule = (await db.query(
      `INSERT INTO evaluation_rules
         (rule_version_id, hazard_id, code, priority, applicability_expression,
          condition_expression, result_status, aggregation_type, evidence_level,
          origin, quality_status, notes)
       VALUES ($1,$2,$3,$4,$5::jsonb,$6::jsonb,$7::risk_status,$8,$9,$10,$11,$12)
       ON CONFLICT (rule_version_id, code) DO UPDATE SET
         condition_expression = EXCLUDED.condition_expression,
         result_status = EXCLUDED.result_status
       RETURNING id`,
      [ruleVersionId, hazardIdByCode.get(r.hazard), r.code, r.priority,
       r.applicability ? JSON.stringify(r.applicability) : null,
       JSON.stringify(r.condition), r.result,
       r.aggregation ?? null, r.evidence ?? 'DIRECT',
       r.origin ?? 'RECONSTRUCTED_ORIGINAL', r.quality_status ?? 'REVIEW_REQUIRED',
       r.notes ?? null],
    )).rows[0];

    let msort = 0;
    for (const mb of r.measures ?? []) {
      const mid = measureIdByCode.get(mb.measure);
      if (!mid) continue; // Maßnahme nicht im Katalog -> überspringen
      await db.query(
        `INSERT INTO rule_measures
           (evaluation_rule_id, measure_id, group_id, relation, sort_order,
            condition_expression, mandatory)
         VALUES ($1,$2,$3,$4,$5,$6::jsonb,$7)
         ON CONFLICT (evaluation_rule_id, measure_id, group_id) DO UPDATE SET
           relation = EXCLUDED.relation, mandatory = EXCLUDED.mandatory`,
        [rule.id, mid, mb.group_id ?? '', mb.relation ?? 'SINGLE', msort++,
         mb.condition ? JSON.stringify(mb.condition) : null, mb.mandatory ?? true],
      );
    }

    for (const s of r.sources ?? []) {
      const sid = await ensureSource(s);
      if (sid) await db.query(
        `INSERT INTO rule_sources (evaluation_rule_id, source_reference_id) VALUES ($1,$2)
         ON CONFLICT DO NOTHING`, [rule.id, sid]);
    }
  }

  return { ruleVersionId, questionCount: questionIdByCode.size };
}
