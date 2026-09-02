// Unit-Tests des Referenz-Evaluators gegen die rekonstruierten Decision Tables.
// Lauf:  node --test --experimental-strip-types evaluator.test.ts
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { evaluate, evaluateHazard, summarize } from './evaluator.ts';
import type { Ruleset, AnswerMap, Origin, EvaluationResult } from './evaluator.ts';

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
