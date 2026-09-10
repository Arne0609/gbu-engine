// ============================================================================
// GBU APP 4.0 – Referenz-Evaluator der Bewertungsengine
// ============================================================================
//
// Reine, seiteneffektfreie Funktion: (Antworten + Regelwerk) -> Ergebnisse.
// Setzt die im Datenmodell festgelegte Auswertungsreihenfolge um (siehe
// GBU_Engine_Datenmodell.md / gbu_engine_schema.sql):
//
//   0. Annahmen (ruleset.assumptions): unbeantwortete Fragen, deren Merkmal
//        zum Baujahr abnahmepflichtig war, bekommen ihren Best-Case-Wert.
//        Erhobene Antworten bleiben unangetastet; das Ergebnis weist die
//        angenommenen Fragen in `assumed` aus.
//   1. Applicability (hazard_questions.role = APPLICABILITY)
//        unbekannt        -> INCOMPLETE
//        ausdruecklich Nein -> NOT_APPLICABLE
//   2. Pflichtfragen (hazard_questions.required_mode = ALWAYS | CONDITIONAL)
//        eine fehlt       -> INCOMPLETE
//   3. Regeln auswerten (kontrollierte Ausdruckssprache)
//        keine passt      -> INCOMPLETE + rule_gap, sobald die Gefaehrdung eine
//                            ausdrueckliche NO_RISK-Regel hat (Regelluecke =
//                            Defekt, fail-closed). Nur Regelwerke ohne jede
//                            NO_RISK-Regel (Rekonstruktion des Originals) fallen
//                            weiter auf NO_RISK + implicit_no_risk.
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
  /** Nur bei role = APPLICABILITY: Gefaehrdung anwendbar, wenn der Ausdruck
   *  wahr ist (z. B. Aufzugsart IN [seil, trommel]). Fehlt er, gilt die
   *  boolesche Regel (ausdrueckliches Nein -> NOT_APPLICABLE). */
  applicable_when?: Expression;
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
/** Begruendete Annahme fuer eine unbeantwortete Frage („Best Case").
 *
 *  Hintergrund: Merkmale, die zum Baujahr der Anlage vorgeschrieben waren,
 *  mussten vor der Inbetriebnahme nachgewiesen und durch eine ZUES abgenommen
 *  werden (z. B. UCM-Schutz nach EN 81-1/2 + A3, verbindlich seit 01.01.2012).
 *  Solche Merkmale muessen nicht erneut erhoben werden – die Frage wird
 *  optional und gilt als „vorhanden", solange niemand widerspricht.
 *
 *  Bewusste Abgrenzung: Annahmen sind NUR fuer Ausstattungsmerkmale zulaessig,
 *  nie fuer Zustandsfragen (Verschleiss, Verschmutzung, Beschaedigung) und nie
 *  fuer Organisationsfragen (Unterweisung, Notfallplan, Pruefnachweise) – eine
 *  Abnahme sagt nichts ueber den heutigen Zustand und nichts ueber die
 *  Betreiberorganisation. */
export interface Assumption {
  /** Frage, die angenommen wird. */
  question: string;
  /** Annahme greift nur, wenn dieser Ausdruck wahr ist (i. d. R. das Baujahr). */
  when: Expression;
  /** Angenommener Wert (Best Case). */
  value: AnswerValue;
  /** Begruendung – erscheint im Fragebogen, in der Bewertung und im PDF. */
  reason: string;
}

export interface Ruleset {
  rule_version?: string;
  hazards?: Hazard[];
  rules: Rule[];
  /** Begruendete Annahmen fuer unbeantwortete Fragen (siehe [Assumption]). */
  assumptions?: Assumption[];
  /** Ist dieser Ausdruck wahr, greift KEINE Annahme (widerlegbare Vermutung).
   *  Im MF-Katalog: die Abnahmeunterlagen liegen ausdruecklich nicht vor –
   *  dann ist die Abnahme nicht belegt und alles wird wieder erhoben. */
  assumptions_void_when?: Expression;
}

/** Tatsaechlich angewandte Annahme (Ergebnis von [applyAssumptions]). */
export interface AppliedAssumption {
  question: string;
  value: AnswerValue;
  reason: string;
}

export interface EvaluationResult {
  hazard: string;
  status: RiskStatus;
  automatic_status: RiskStatus;
  matched_rule: string | null;
  /** Regeln, deren Massnahmen gelten (Gewinner zuerst). Bei aggregation_type
   *  NONE nur der Gewinner – niedrigere Prioritaeten sind bewusst uebersteuert
   *  (Kompensation). Bei MAXIMUM/ANY zusaetzlich alle weiteren risikotragenden
   *  Treffer (unabhaengige Maengel derselben Gefaehrdung). */
  matched_rules: string[];
  /** Zutreffende Befundregeln (LOW/MEDIUM/HIGH), deren Massnahmen nicht gelten,
   *  weil der Gewinner sie uebersteuert – nur zur Nachvollziehbarkeit. */
  overridden_rules: string[];
  /** true: keine Regel traf zu, obwohl alle Pflichtfragen beantwortet sind –
   *  Daten-/Regeldefekt, Status ist dann INCOMPLETE (fail-closed). */
  rule_gap?: boolean;
  /** true: NO_RISK nur, weil keine Regel passt und die Gefaehrdung keine
   *  ausdrueckliche NO_RISK-Regel kennt (Altstil / Rekonstruktion). */
  implicit_no_risk?: boolean;
  /** Fragen dieser Gefaehrdung, deren Wert nicht erhoben, sondern nach
   *  [Assumption] angenommen wurde. Leer/fehlend = alles erhoben. Ein Befund
   *  mit Eintraegen hier beruht auf einer Vermutung und wird in Bewertung und
   *  PDF entsprechend gekennzeichnet. */
  assumed?: string[];
  input_snapshot: Record<string, AnswerValue>;
}

export interface EvaluateOptions {
  /** Nur Regeln dieser Herkuenfte auswerten. Fehlt die Angabe: alle. Mit
   *  {includeOrigins:['RECONSTRUCTED_ORIGINAL']} reproduziert die Engine das
   *  beobachtete Original (ohne eigene OWN_RULE-Verbesserungen). */
  includeOrigins?: Origin[];
  /** Von [applyAssumptions] gesetzte Fragen – nur zur Kennzeichnung des
   *  Ergebnisses; die Werte stehen bereits in den Antworten. */
  assumedQuestions?: ReadonlySet<string>;
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

  const build = (status: RiskStatus, matched: string | null, all: string[] = [],
                 overridden: string[] = [], gap = false, implicit = false): EvaluationResult => {
    const input_snapshot: Record<string, AnswerValue> = {};
    for (const k of snapshotKeys) if (isAnswered(answers, k)) input_snapshot[k] = answers[k];
    const r: EvaluationResult = { hazard: hazard.code, status, automatic_status: status,
      matched_rule: matched, matched_rules: all, overridden_rules: overridden, input_snapshot };
    if (gap) r.rule_gap = true;
    if (implicit) r.implicit_no_risk = true;
    // Angenommene Fragen dieser Gefaehrdung ausweisen – nur die, die hier
    // ueberhaupt eine Rolle spielen.
    if (opts.assumedQuestions && opts.assumedQuestions.size > 0) {
      const a = [...snapshotKeys].filter((k) => opts.assumedQuestions!.has(k));
      if (a.length > 0) r.assumed = a.sort();
    }
    return r;
  };

  // Nicht implementierte Gefaehrdungen (z. B. MC13) nie bewerten.
  if (hazard.not_implemented) return build('NOT_APPLICABLE', null);

  // 1) Applicability -----------------------------------------------------
  //    a) mit Ausdruck (applicable_when): Ausdruck falsch -> NOT_APPLICABLE,
  //       sofern alle referenzierten Fragen beantwortet sind, sonst INCOMPLETE.
  //    b) ohne Ausdruck: boolesche Regel (Nein -> NOT_APPLICABLE, leer -> INCOMPLETE).
  const appQs = questions.filter((q) => q.role === 'APPLICABILITY');
  for (const q of appQs) {
    if (q.applicable_when) {
      if (evalExpression(q.applicable_when, answers)) continue;
      const refs = new Set<string>();
      collectQuestions(q.applicable_when, refs);
      for (const k of refs) snapshotKeys.add(k);
      for (const k of refs) if (!isAnswered(answers, k)) return build('INCOMPLETE', null);
      return build('NOT_APPLICABLE', null);
    }
    if (isAnswered(answers, q.question) && isNegative(answers[q.question])) {
      return build('NOT_APPLICABLE', null);
    }
  }
  for (const q of appQs) {
    if (q.applicable_when) continue;
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

  // Keine Regel passt, obwohl alle Pflichtfragen beantwortet sind:
  //  - Gefaehrdung mit ausdruecklicher NO_RISK-Regel -> Regelluecke = Defekt im
  //    Regelwerk, kein Befund: INCOMPLETE + rule_gap (fail-closed).
  //  - Gefaehrdung ohne jede NO_RISK-Regel (Altstil, Rekonstruktion des
  //    Originals) -> NO_RISK + implicit_no_risk.
  if (matching.length === 0) {
    const explicitNoRisk = rules.some((r) => r.result === 'NO_RISK');
    return explicitNoRisk ? build('INCOMPLETE', null, [], [], true)
                          : build('NO_RISK', null, [], [], false, true);
  }

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
  const others = matching.filter((r) => r !== winner)
    .sort((a, b) => SEVERITY[b.result] - SEVERITY[a.result]);
  // Massnahmen: bei NONE nur der Gewinner (Prioritaet = bewusste Uebersteuerung),
  // bei MAXIMUM/ANY alle weiteren risikotragenden Treffer.
  const effective = (hazardAgg === 'MAXIMUM' || hazardAgg === 'ANY') && SEVERITY[winner.result] > 0
    ? others.filter((r) => SEVERITY[r.result] > 0) : [];
  // Uebersteuert = zutreffende Befundregeln, deren Massnahmen nicht gelten. Die
  // Kein-Risiko-Auffangregel ist kein Befund und wird nicht als uebersteuert gefuehrt.
  const overridden = others.filter((r) => !effective.includes(r) && SEVERITY[r.result] > 0);
  return build(winner.result, winner.code, [winner.code, ...effective.map((r) => r.code)],
               overridden.map((r) => r.code));
}

function collectWinnerKeys(rule: Rule): Set<string> {
  const s = new Set<string>();
  if (rule.applicability) collectQuestions(rule.applicability, s);
  collectQuestions(rule.condition, s);
  return s;
}

/**
 * Wendet die begruendeten Annahmen des Regelwerks an: Jede unbeantwortete
 * Frage, deren Bedingung zutrifft, bekommt ihren Best-Case-Wert.
 *
 * Drei Festlegungen, die den Unterschied zum Ausblenden ausmachen:
 *
 *  1. Eine bereits erhobene Antwort wird NIE ueberschrieben – der Befund vor
 *     Ort schlaegt die Vermutung immer.
 *  2. Die Bedingungen werden gegen die ERHOBENEN Antworten geprueft, nicht
 *     gegen zwischenzeitlich angenommene. So kann keine Annahme eine zweite
 *     ausloesen; das Ergebnis haengt nicht von der Reihenfolge ab.
 *  3. Ist [Ruleset.assumptions_void_when] wahr, greift keine einzige Annahme.
 *
 * Liefert eine KOPIE der Antworten; die uebergebene Map bleibt unveraendert.
 */
export function applyAssumptions(
  ruleset: Ruleset,
  answers: AnswerMap,
): { answers: AnswerMap; applied: AppliedAssumption[] } {
  const liste = ruleset.assumptions ?? [];
  if (liste.length === 0) return { answers, applied: [] };
  if (ruleset.assumptions_void_when &&
      evalExpression(ruleset.assumptions_void_when, answers)) {
    return { answers, applied: [] };
  }
  const ergaenzt: AnswerMap = { ...answers };
  const applied: AppliedAssumption[] = [];
  for (const a of liste) {
    if (isAnswered(answers, a.question)) continue;
    if (!evalExpression(a.when, answers)) continue;
    ergaenzt[a.question] = a.value;
    applied.push({ question: a.question, value: a.value, reason: a.reason });
  }
  return { answers: ergaenzt, applied };
}

/** Wertet alle Gefaehrdungen des Regelwerks aus. Annahmen werden vorher
 *  angewandt, sofern der Aufrufer sie nicht schon selbst gesetzt hat
 *  (erkennbar an opts.assumedQuestions). */
export function evaluate(
  ruleset: Ruleset,
  answers: AnswerMap,
  opts: EvaluateOptions = {},
): EvaluationResult[] {
  let wirkendeAntworten = answers;
  let optionen = opts;
  if (!opts.assumedQuestions) {
    const { answers: erg, applied } = applyAssumptions(ruleset, answers);
    wirkendeAntworten = erg;
    optionen = { ...opts, assumedQuestions: new Set(applied.map((a) => a.question)) };
  }
  const byHazard = new Map<string, Rule[]>();
  for (const r of ruleset.rules) {
    const list = byHazard.get(r.hazard) ?? [];
    list.push(r);
    byHazard.set(r.hazard, list);
  }
  const hazards = ruleset.hazards ?? [];
  return hazards.map((h) =>
    evaluateHazard(h, byHazard.get(h.code) ?? [], wirkendeAntworten, optionen));
}

/** Zaehlung der Ergebnisse je Status (fuer die Bewertungsuebersicht). */
export function summarize(results: EvaluationResult[]): Record<RiskStatus, number> {
  const out: Record<RiskStatus, number> = {
    INCOMPLETE: 0, NOT_APPLICABLE: 0, NO_RISK: 0, LOW: 0, MEDIUM: 0, HIGH: 0,
  };
  for (const r of results) out[r.status]++;
  return out;
}
