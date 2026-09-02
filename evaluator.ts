// ============================================================================
// GBU APP 4.0 – Referenz-Evaluator der Bewertungsengine
// ============================================================================
//
// Reine, seiteneffektfreie Funktion: (Antworten + Regelwerk) -> Ergebnisse.
// Setzt die im Datenmodell festgelegte Auswertungsreihenfolge um (siehe
// GBU_Engine_Datenmodell.md / gbu_engine_schema.sql):
//
//   1. Applicability (hazard_questions.role = APPLICABILITY)
//        unbekannt        -> INCOMPLETE
//        ausdruecklich Nein -> NOT_APPLICABLE
//   2. Pflichtfragen (hazard_questions.required_mode = ALWAYS | CONDITIONAL)
//        eine fehlt       -> INCOMPLETE
//   3. Regeln auswerten (kontrollierte Ausdruckssprache)
//        keine passt      -> NO_RISK
//   4. Aggregation / hoechste Prioritaet -> result_status
//
// Bewusst ohne Fremdabhaengigkeiten, damit der Code 1:1 nach Dart (Flutter,
// Offline-Bewertung) und ins Node-Backend portierbar ist.
// ============================================================================

// ---- Werte & Antworten -----------------------------------------------------

export type AnswerValue = boolean | number | string | null;
/** Fragen-Code -> Wert. Fehlt der Schluessel oder ist er null => unbeantwortet. */
export type AnswerMap = Record<string, AnswerValue>;

export type RiskStatus =
  | 'INCOMPLETE' | 'NOT_APPLICABLE' | 'NO_RISK' | 'LOW' | 'MEDIUM' | 'HIGH';

export type Operator =
  | 'EQ' | 'NEQ' | 'GT' | 'GTE' | 'LT' | 'LTE'
  | 'IN' | 'NOT_IN' | 'ANSWERED' | 'NOT_ANSWERED';

export type Leaf = { question: string; operator: Operator; value?: AnswerValue | AnswerValue[] };
export type Expression =
  | { all: Expression[] }
  | { any: Expression[] }
  | { not: Expression }
  | Leaf;

export type Role =
  | 'APPLICABILITY' | 'TRIGGER' | 'COMPENSATION' | 'MODIFIER'
  | 'ACCESS_FACTOR' | 'OPTIONAL' | 'DOCUMENTATION';
export type RequiredMode = 'NEVER' | 'ALWAYS' | 'CONDITIONAL';
export type AggregationType = 'NONE' | 'ANY' | 'ALL' | 'MAXIMUM' | 'MINIMUM' | 'DECISION_TABLE';
export type Origin = 'RECONSTRUCTED_ORIGINAL' | 'NORM_DERIVED' | 'OWN_RULE';

export interface HazardQuestion {
  question: string;
  role: Role;
  required_mode?: RequiredMode;
  required_when?: Expression;
}
export interface Hazard {
  code: string;
  domain: string;
  title: string;
  aggregation_type?: AggregationType;
  evaluation_mode?: 'STANDARD' | 'PARTIAL_ALLOWED' | 'STRICT_REQUIRED';
  not_implemented?: boolean;
  questions?: HazardQuestion[];
}
export interface Rule {
  hazard: string;
  code: string;
  priority: number;
  applicability?: Expression;
  condition: Expression;
  result: RiskStatus;
  aggregation?: AggregationType;
  origin?: Origin;
}
export interface Ruleset {
  rule_version?: string;
  hazards?: Hazard[];
  rules: Rule[];
}

export interface EvaluationResult {
  hazard: string;
  status: RiskStatus;
  automatic_status: RiskStatus;
  matched_rule: string | null;
  input_snapshot: Record<string, AnswerValue>;
}

export interface EvaluateOptions {
  /** Nur Regeln dieser Herkuenfte auswerten. Fehlt die Angabe: alle. Mit
   *  {includeOrigins:['RECONSTRUCTED_ORIGINAL']} reproduziert die Engine das
   *  beobachtete Original (ohne eigene OWN_RULE-Verbesserungen). */
  includeOrigins?: Origin[];
}

// ---- Hilfen ----------------------------------------------------------------

const SEVERITY: Record<RiskStatus, number> = {
  INCOMPLETE: -2, NOT_APPLICABLE: -1, NO_RISK: 0, LOW: 1, MEDIUM: 2, HIGH: 3,
};

function isAnswered(answers: AnswerMap, q: string): boolean {
  return Object.prototype.hasOwnProperty.call(answers, q) && answers[q] !== null;
}

/** „Ausdrueckliches Nein" fuer Applicability-Fragen. */
function isNegative(v: AnswerValue): boolean {
  if (v === false || v === 0) return true;
  if (typeof v === 'string') return ['nein', 'no', 'false'].includes(v.toLowerCase());
  return false;
}

function evalLeaf(leaf: Leaf, answers: AnswerMap): boolean {
  const answered = isAnswered(answers, leaf.question);
  const v = answered ? answers[leaf.question] : null;
  switch (leaf.operator) {
    case 'ANSWERED':     return answered;
    case 'NOT_ANSWERED': return !answered;
    // Alle Vergleiche verlangen eine vorhandene Antwort. Fehlt sie, ist das
    // Blatt FALSE (nie „unbekannt = wahr") – so faellt ein Ortsblock mit lauter
    // leeren Fragen korrekt auf NO_RISK statt zu triggern.
    case 'EQ':  return answered && v === leaf.value;
    case 'NEQ': return answered && v !== leaf.value;
    case 'GT':  return answered && typeof v === 'number' && v >  (leaf.value as number);
    case 'GTE': return answered && typeof v === 'number' && v >= (leaf.value as number);
    case 'LT':  return answered && typeof v === 'number' && v <  (leaf.value as number);
    case 'LTE': return answered && typeof v === 'number' && v <= (leaf.value as number);
    case 'IN':  return answered && Array.isArray(leaf.value) && leaf.value.includes(v as AnswerValue);
    case 'NOT_IN': return answered && Array.isArray(leaf.value) && !leaf.value.includes(v as AnswerValue);
    default: return false;
  }
}

export function evalExpression(expr: Expression, answers: AnswerMap): boolean {
  if ('all' in expr) return expr.all.every((e) => evalExpression(e, answers));
  if ('any' in expr) return expr.any.some((e) => evalExpression(e, answers));
  if ('not' in expr) return !evalExpression(expr.not, answers);
  return evalLeaf(expr as Leaf, answers);
}

// Alle Fragen-Codes, die ein Ausdruck referenziert (fuer den input_snapshot).
function collectQuestions(expr: Expression, into: Set<string>): void {
  if ('all' in expr) { expr.all.forEach((e) => collectQuestions(e, into)); return; }
  if ('any' in expr) { expr.any.forEach((e) => collectQuestions(e, into)); return; }
  if ('not' in expr) { collectQuestions(expr.not, into); return; }
  into.add((expr as Leaf).question);
}

// ---- Kern ------------------------------------------------------------------

export function evaluateHazard(
  hazard: Hazard,
  rules: Rule[],
  answers: AnswerMap,
  opts: EvaluateOptions = {},
): EvaluationResult {
  const questions = hazard.questions ?? [];
  const snapshotKeys = new Set<string>();
  for (const hq of questions) snapshotKeys.add(hq.question);

  const build = (status: RiskStatus, matched: string | null): EvaluationResult => {
    const input_snapshot: Record<string, AnswerValue> = {};
    for (const k of snapshotKeys) if (isAnswered(answers, k)) input_snapshot[k] = answers[k];
    return { hazard: hazard.code, status, automatic_status: status, matched_rule: matched, input_snapshot };
  };

  // Nicht implementierte Gefaehrdungen (z. B. MC13) nie bewerten.
  if (hazard.not_implemented) return build('NOT_APPLICABLE', null);

  // 1) Applicability -----------------------------------------------------
  const appQs = questions.filter((q) => q.role === 'APPLICABILITY');
  for (const q of appQs) {
    if (isAnswered(answers, q.question) && isNegative(answers[q.question])) {
      return build('NOT_APPLICABLE', null);
    }
  }
  for (const q of appQs) {
    if (!isAnswered(answers, q.question)) return build('INCOMPLETE', null);
  }

  // 2) Pflichtfragen (gefaehrdungsspezifisch) ----------------------------
  for (const q of questions) {
    const mode = q.required_mode ?? 'NEVER';
    const required =
      mode === 'ALWAYS' ||
      (mode === 'CONDITIONAL' && q.required_when != null &&
        evalExpression(q.required_when, answers));
    if (required && !isAnswered(answers, q.question)) return build('INCOMPLETE', null);
  }

  // 3) Regeln ------------------------------------------------------------
  const allow = opts.includeOrigins ? new Set(opts.includeOrigins) : null;
  const applicable = rules.filter((r) => {
    if (allow && !allow.has((r.origin ?? 'RECONSTRUCTED_ORIGINAL') as Origin)) return false;
    if (r.applicability && !evalExpression(r.applicability, answers)) return false;
    return true;
  });
  const matching = applicable.filter((r) => evalExpression(r.condition, answers));

  if (matching.length === 0) return build('NO_RISK', null);

  // 4) Aggregation / hoechste Prioritaet ---------------------------------
  const hazardAgg = hazard.aggregation_type ?? 'NONE';
  let winner: Rule;
  if (hazardAgg === 'MAXIMUM' || hazardAgg === 'ANY') {
    // Hoechste Schwere unter den zutreffenden Regeln.
    winner = matching.reduce((a, b) =>
      SEVERITY[b.result] > SEVERITY[a.result] ? b : a);
  } else {
    // Hoechste Prioritaet, bei Gleichstand hoechste Schwere.
    winner = matching.reduce((a, b) => {
      if (b.priority !== a.priority) return b.priority > a.priority ? b : a;
      return SEVERITY[b.result] > SEVERITY[a.result] ? b : a;
    });
  }
  for (const k of collectWinnerKeys(winner)) snapshotKeys.add(k);
  return build(winner.result, winner.code);
}

function collectWinnerKeys(rule: Rule): Set<string> {
  const s = new Set<string>();
  if (rule.applicability) collectQuestions(rule.applicability, s);
  collectQuestions(rule.condition, s);
  return s;
}

/** Wertet alle Gefaehrdungen des Regelwerks aus. */
export function evaluate(
  ruleset: Ruleset,
  answers: AnswerMap,
  opts: EvaluateOptions = {},
): EvaluationResult[] {
  const byHazard = new Map<string, Rule[]>();
  for (const r of ruleset.rules) {
    const list = byHazard.get(r.hazard) ?? [];
    list.push(r);
    byHazard.set(r.hazard, list);
  }
  const hazards = ruleset.hazards ?? [];
  return hazards.map((h) => evaluateHazard(h, byHazard.get(h.code) ?? [], answers, opts));
}

/** Zaehlung der Ergebnisse je Status (fuer die Bewertungsuebersicht). */
export function summarize(results: EvaluationResult[]): Record<RiskStatus, number> {
  const out: Record<RiskStatus, number> = {
    INCOMPLETE: 0, NOT_APPLICABLE: 0, NO_RISK: 0, LOW: 0, MEDIUM: 0, HIGH: 0,
  };
  for (const r of results) out[r.status]++;
  return out;
}
