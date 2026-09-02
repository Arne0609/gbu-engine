// Unit-Tests des Referenz-Evaluators gegen die rekonstruierten Decision Tables.
// Lauf:  node --test --experimental-strip-types evaluator.test.ts
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { evaluate, evaluateHazard, summarize } from './evaluator.ts';
import type { Ruleset, AnswerMap, Origin, EvaluationResult, Hazard, Rule } from './evaluator.ts';

const ruleset: Ruleset = JSON.parse(
  readFileSync(new URL('./seed_rules.json', import.meta.url), 'utf8'),
);
const hazardsByCode = new Map(ruleset.hazards!.map((h) => [h.code, h]));
const rulesByHazard = (code: string) => ruleset.rules.filter((r) => r.hazard === code);

/** Bewertet genau eine Gefaehrdung. */
function evalOne(code: string, answers: AnswerMap, includeOrigins?: Origin[]): EvaluationResult {
  return evaluateHazard(hazardsByCode.get(code)!, rulesByHazard(code), answers,
    includeOrigins ? { includeOrigins } : {});
}
const status = (code: string, answers: AnswerMap, inc?: Origin[]) => evalOne(code, answers, inc).status;

// ---------------------------------------------------------------------------
// M032 – Notrufeinrichtung (Decision Table + zwei Regelwelten)
// ---------------------------------------------------------------------------
test('M032: alles leer -> NO_RISK (fehlende Antwort ist nicht HOCH und nicht INCOMPLETE)', () => {
  assert.equal(status('M032', {}), 'NO_RISK');
});
test('M032: kein Notruf -> HIGH', () => {
  const r = evalOne('M032', { q_emergency_call_present: false });
  assert.equal(r.status, 'HIGH');
  assert.equal(r.matched_rule, 'M032-R001');
  assert.deepEqual(r.input_snapshot, { q_emergency_call_present: false });
});
test('M032: Notruf vorhanden, Rest leer -> NO_RISK', () => {
  assert.equal(status('M032', { q_emergency_call_present: true }), 'NO_RISK');
});
test('M032: Notruf ohne 24h-Aufschaltung -> MITTEL (unsere OWN_RULE-Zielregel)', () => {
  const r = evalOne('M032', { q_emergency_call_present: true, q_emergency_call_24h: false });
  assert.equal(r.status, 'MEDIUM');
  assert.equal(r.matched_rule, 'M032-T010');
});
test('M032: Reconstructed-only reproduziert das Original (kein Notruf -> HOCH)', () => {
  assert.equal(status('M032', { q_emergency_call_present: false }, ['RECONSTRUCTED_ORIGINAL']), 'HIGH');
});
test('M032: Reconstructed-only – Notruf ohne 24h -> KEIN RISIKO (Original, ohne OWN_RULE)', () => {
  assert.equal(
    status('M032', { q_emergency_call_present: true, q_emergency_call_24h: false }, ['RECONSTRUCTED_ORIGINAL']),
    'NO_RISK',
  );
});

// ---------------------------------------------------------------------------
// MC4 – Cyber-Bauplan: ODER-Schnittstelle + Pflicht beider Fragen
// ---------------------------------------------------------------------------
test('MC4: Drahtlos=Ja, Physik ausdruecklich Nein -> MITTEL', () => {
  assert.equal(status('MC4', {
    q_ctrl_digital: true, q_ctrl_free_access: true, q_ctrl_wireless: true, q_ctrl_physical: false,
  }), 'MEDIUM');
});
test('MC4: Physik-Frage UNBEANTWORTET -> INCOMPLETE (Bug-Fix, nicht NO_RISK)', () => {
  assert.equal(status('MC4', {
    q_ctrl_digital: true, q_ctrl_free_access: true, q_ctrl_wireless: true, // physical fehlt
  }), 'INCOMPLETE');
});
test('MC4: beide Schnittstellen Nein -> NO_RISK', () => {
  assert.equal(status('MC4', {
    q_ctrl_digital: true, q_ctrl_free_access: true, q_ctrl_wireless: false, q_ctrl_physical: false,
  }), 'NO_RISK');
});
test('MC4: keine digitale Steuerung -> NOT_APPLICABLE', () => {
  assert.equal(status('MC4', { q_ctrl_digital: false }), 'NOT_APPLICABLE');
});
test('MC4: Applicability unbekannt -> INCOMPLETE', () => {
  assert.equal(status('MC4', {}), 'INCOMPLETE');
});

// ---------------------------------------------------------------------------
// Ortsblock M087 – ANY / PARTIAL_ALLOWED (der Gegenpol zu MC4)
// ---------------------------------------------------------------------------
test('M087: eine Ja-Ortsfrage, drei leer -> HIGH (Teilantwort genuegt)', () => {
  const r = evalOne('M087', { q_asbestos_machine_room: true });
  assert.equal(r.status, 'HIGH');
  assert.equal(r.matched_rule, 'M087-R001');
});
test('M087: alle Ortsfragen leer -> NO_RISK', () => {
  assert.equal(status('M087', {}), 'NO_RISK');
});
test('M090/M103: eine Ja-Ortsfrage -> MITTEL', () => {
  assert.equal(status('M090', { q_contamination_pit: true }), 'MEDIUM');
  assert.equal(status('M103', { q_flammable_storage_other: true }), 'MEDIUM');
});

// ---------------------------------------------------------------------------
// Einzeltrigger-Kundenbefragung + Modifier
// ---------------------------------------------------------------------------
test('M088: Transport chemischer Gefahrstoffe = Ja -> MITTEL; leer -> NO_RISK', () => {
  assert.equal(status('M088', { q_transport_chemical: true }), 'MEDIUM');
  assert.equal(status('M088', {}), 'NO_RISK');
});
test('M106: angrenzende Verkehrswege + A73=Nein -> MITTEL; A73=Ja -> NO_RISK', () => {
  assert.equal(status('M106', { q_adjacent_traffic_routes: true, q_disabled_use: false }), 'MEDIUM');
  assert.equal(status('M106', { q_adjacent_traffic_routes: true, q_disabled_use: true }), 'NO_RISK');
});

// ---------------------------------------------------------------------------
// Gesamtlauf + Uebersicht
// ---------------------------------------------------------------------------
test('evaluate(): liefert je Gefaehrdung genau ein Ergebnis', () => {
  const results = evaluate(ruleset, {});
  assert.equal(results.length, ruleset.hazards!.length);
  // Ausgangszustand: keine Applicability-Gefaehrdung bewertbar (MC4 INCOMPLETE),
  // alle uebrigen ohne Trigger -> NO_RISK.
  const s = summarize(results);
  assert.equal(s.INCOMPLETE, 1);           // MC4 (Applicability unbekannt)
  assert.equal(s.HIGH + s.MEDIUM + s.LOW, 0);
  assert.equal(s.NO_RISK, ruleset.hazards!.length - 1);
});
test('summarize(): mehrere Mangelbilder gleichzeitig', () => {
  const answers: AnswerMap = {
    q_emergency_call_present: false,        // M032 HIGH
    q_asbestos_pit: true,                   // M087 HIGH
    q_transport_radioactive: true,          // M093 MEDIUM
    q_ctrl_digital: true, q_ctrl_free_access: true,
    q_ctrl_wireless: true, q_ctrl_physical: true, // MC4 MEDIUM
  };
  const s = summarize(evaluate(ruleset, answers));
  assert.equal(s.HIGH, 2);
  assert.equal(s.MEDIUM, 2);
});

// ---- applicable_when (Anlagenmerkmal als Ausdruck) -------------------------
// Blaupause: Schindler f019 Aufzugsart schaltet Seil-Gefaehrdungen (M002/M004/...)
// – im Eigenbau explizit als NOT_APPLICABLE statt stummem „Kein Risiko".
const HAZ_SEIL: Hazard = {
  code: 'MF-TEST-SEIL', domain: 'GBU', title: 'Seil-Gefaehrdung', aggregation_type: 'NONE',
  questions: [
    { question: 'qa_aufzugsart', role: 'APPLICABILITY', required_mode: 'NEVER',
      applicable_when: { question: 'qa_aufzugsart', operator: 'IN', value: ['seil', 'trommel'] } },
    { question: 'q_fang', role: 'TRIGGER', required_mode: 'ALWAYS' },
  ],
};
const RULES_SEIL: Rule[] = [
  { hazard: 'MF-TEST-SEIL', code: 'S-R1', priority: 100,
    condition: { question: 'q_fang', operator: 'EQ', value: false }, result: 'HIGH', origin: 'OWN_RULE' },
];

test('applicable_when: Hydraulik -> NOT_APPLICABLE (auch bei fehlender Fangfrage)', () => {
  const r = evaluateHazard(HAZ_SEIL, RULES_SEIL, { qa_aufzugsart: 'hydraulik' });
  assert.equal(r.status, 'NOT_APPLICABLE');
});
test('applicable_when: Aufzugsart unbeantwortet -> INCOMPLETE', () => {
  const r = evaluateHazard(HAZ_SEIL, RULES_SEIL, { q_fang: false });
  assert.equal(r.status, 'INCOMPLETE');
});
test('applicable_when: Seil + Fang fehlt -> HIGH; Seil ohne Fangantwort -> INCOMPLETE', () => {
  assert.equal(evaluateHazard(HAZ_SEIL, RULES_SEIL, { qa_aufzugsart: 'seil', q_fang: false }).status, 'HIGH');
  assert.equal(evaluateHazard(HAZ_SEIL, RULES_SEIL, { qa_aufzugsart: 'seil' }).status, 'INCOMPLETE');
});

// ---- Zahlenschwellen + Kompensation ueber Prioritaet (Fahrkorbtuerschuerze) --
const HAZ_SCHUERZE: Hazard = {
  code: 'MF-TEST-K04', domain: 'GBU', title: 'Schuerze', aggregation_type: 'NONE',
  questions: [
    { question: 'qk_schuerze_mm', role: 'TRIGGER', required_mode: 'ALWAYS' },
    { question: 'qk_fachkundig', role: 'COMPENSATION', required_mode: 'CONDITIONAL',
      required_when: { question: 'qk_schuerze_mm', operator: 'LT', value: 300 } },
  ],
};
const RULES_SCHUERZE: Rule[] = [
  { hazard: 'MF-TEST-K04', code: 'K-R1', priority: 300, result: 'MEDIUM', origin: 'OWN_RULE',
    condition: { all: [{ question: 'qk_schuerze_mm', operator: 'LT', value: 300 },
                       { question: 'qk_fachkundig', operator: 'EQ', value: true }] } },
  { hazard: 'MF-TEST-K04', code: 'K-R2', priority: 200, result: 'HIGH', origin: 'OWN_RULE',
    condition: { question: 'qk_schuerze_mm', operator: 'LT', value: 300 } },
  { hazard: 'MF-TEST-K04', code: 'K-R3', priority: 100, result: 'MEDIUM', origin: 'OWN_RULE',
    condition: { question: 'qk_schuerze_mm', operator: 'LT', value: 750 } },
];
test('Zahlenschwelle: 750 mm -> NO_RISK, 500 -> MEDIUM, 200 -> HIGH, 200 + fachkundig -> MEDIUM', () => {
  assert.equal(evaluateHazard(HAZ_SCHUERZE, RULES_SCHUERZE, { qk_schuerze_mm: 750 }).status, 'NO_RISK');
  assert.equal(evaluateHazard(HAZ_SCHUERZE, RULES_SCHUERZE, { qk_schuerze_mm: 500 }).status, 'MEDIUM');
  const r200 = evaluateHazard(HAZ_SCHUERZE, RULES_SCHUERZE, { qk_schuerze_mm: 200 });
  assert.equal(r200.status, 'INCOMPLETE', 'unter 300 mm wird die Kompensationsfrage Pflicht');
  assert.equal(evaluateHazard(HAZ_SCHUERZE, RULES_SCHUERZE, { qk_schuerze_mm: 200, qk_fachkundig: false }).status, 'HIGH');
  const comp = evaluateHazard(HAZ_SCHUERZE, RULES_SCHUERZE, { qk_schuerze_mm: 200, qk_fachkundig: true });
  assert.equal(comp.status, 'MEDIUM');
  assert.equal(comp.matched_rule, 'K-R1', 'spezifischere Regel (hoehere Prioritaet) gewinnt');
});
