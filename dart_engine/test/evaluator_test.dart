// Unit-Tests des Dart-Evaluators – dieselben Fälle wie evaluator.test.ts.
// Lauf:  dart pub get && dart test
//
// Lädt dieselbe Quelle der Wahrheit (engine_model/seed_rules.json), damit
// Dart- und TS-Portierung nachweislich identisch bewerten.
import 'dart:convert';
import 'dart:io';
import 'package:test/test.dart';
import 'package:gbu_engine/gbu_engine.dart';

Ruleset loadRuleset() {
  final candidates = [
    '../seed_rules.json',      // dart test aus dem Paketverzeichnis
    'seed_rules.json',
    '../../seed_rules.json',
  ];
  for (final p in candidates) {
    final f = File(p);
    if (f.existsSync()) {
      return Ruleset.fromJson(
          jsonDecode(f.readAsStringSync()) as Map<String, dynamic>);
    }
  }
  throw StateError('seed_rules.json nicht gefunden (getestet: $candidates)');
}

void main() {
  final ruleset = loadRuleset();
  final hazardsByCode = {for (final h in ruleset.hazards) h.code: h};
  List<Rule> rulesFor(String code) =>
      ruleset.rules.where((r) => r.hazard == code).toList();

  EvaluationResult evalOne(String code, AnswerMap answers, {Set<String>? origins}) =>
      evaluateHazard(hazardsByCode[code]!, rulesFor(code), answers,
          options: EvaluateOptions(includeOrigins: origins));
  RiskStatus status(String code, AnswerMap a, {Set<String>? origins}) =>
      evalOne(code, a, origins: origins).status;

  // --- M032 ---------------------------------------------------------------
  test('M032: alles leer -> NO_RISK', () {
    expect(status('M032', {}), RiskStatus.noRisk);
  });
  test('M032: kein Notruf -> HIGH', () {
    final r = evalOne('M032', {'q_emergency_call_present': false});
    expect(r.status, RiskStatus.high);
    expect(r.matchedRule, 'M032-R001');
    expect(r.inputSnapshot, {'q_emergency_call_present': false});
  });
  test('M032: Notruf vorhanden, Rest leer -> NO_RISK', () {
    expect(status('M032', {'q_emergency_call_present': true}), RiskStatus.noRisk);
  });
  test('M032: Notruf ohne 24h -> MEDIUM (OWN_RULE)', () {
    final r = evalOne('M032',
        {'q_emergency_call_present': true, 'q_emergency_call_24h': false});
    expect(r.status, RiskStatus.medium);
    expect(r.matchedRule, 'M032-T010');
  });
  test('M032: reconstructed-only reproduziert Original (kein Notruf -> HIGH)', () {
    expect(
        status('M032', {'q_emergency_call_present': false},
            origins: {'RECONSTRUCTED_ORIGINAL'}),
        RiskStatus.high);
  });
  test('M032: reconstructed-only, Notruf ohne 24h -> NO_RISK', () {
    expect(
        status('M032',
            {'q_emergency_call_present': true, 'q_emergency_call_24h': false},
            origins: {'RECONSTRUCTED_ORIGINAL'}),
        RiskStatus.noRisk);
  });

  // --- MC4 ----------------------------------------------------------------
  test('MC4: Drahtlos=Ja, Physik=Nein -> MEDIUM', () {
    expect(
        status('MC4', {
          'q_ctrl_digital': true,
          'q_ctrl_free_access': true,
          'q_ctrl_wireless': true,
          'q_ctrl_physical': false,
        }),
        RiskStatus.medium);
  });
  test('MC4: Physik unbeantwortet -> INCOMPLETE (Bug-Fix)', () {
    expect(
        status('MC4', {
          'q_ctrl_digital': true,
          'q_ctrl_free_access': true,
          'q_ctrl_wireless': true,
        }),
        RiskStatus.incomplete);
  });
  test('MC4: beide Nein -> NO_RISK', () {
    expect(
        status('MC4', {
          'q_ctrl_digital': true,
          'q_ctrl_free_access': true,
          'q_ctrl_wireless': false,
          'q_ctrl_physical': false,
        }),
        RiskStatus.noRisk);
  });
  test('MC4: keine digitale Steuerung -> NOT_APPLICABLE', () {
    expect(status('MC4', {'q_ctrl_digital': false}), RiskStatus.notApplicable);
  });
  test('MC4: Applicability unbekannt -> INCOMPLETE', () {
    expect(status('MC4', {}), RiskStatus.incomplete);
  });

  // --- Ortsblöcke ---------------------------------------------------------
  test('M087: eine Ja-Ortsfrage, drei leer -> HIGH', () {
    final r = evalOne('M087', {'q_asbestos_machine_room': true});
    expect(r.status, RiskStatus.high);
    expect(r.matchedRule, 'M087-R001');
  });
  test('M087: alle leer -> NO_RISK', () {
    expect(status('M087', {}), RiskStatus.noRisk);
  });
  test('M090/M103: eine Ja-Ortsfrage -> MEDIUM', () {
    expect(status('M090', {'q_contamination_pit': true}), RiskStatus.medium);
    expect(status('M103', {'q_flammable_storage_other': true}), RiskStatus.medium);
  });

  // --- Einzeltrigger + Modifier -------------------------------------------
  test('M088: Ja -> MEDIUM; leer -> NO_RISK', () {
    expect(status('M088', {'q_transport_chemical': true}), RiskStatus.medium);
    expect(status('M088', {}), RiskStatus.noRisk);
  });
  test('M106: Verkehrswege + A73=Nein -> MEDIUM; A73=Ja -> NO_RISK', () {
    expect(
        status('M106', {'q_adjacent_traffic_routes': true, 'q_disabled_use': false}),
        RiskStatus.medium);
    expect(
        status('M106', {'q_adjacent_traffic_routes': true, 'q_disabled_use': true}),
        RiskStatus.noRisk);
  });

  // --- Gesamtlauf ---------------------------------------------------------
  test('evaluate(): ein Ergebnis je Gefährdung; Ausgangszustand', () {
    final results = evaluate(ruleset, {});
    expect(results.length, ruleset.hazards.length);
    final s = summarize(results);
    expect(s[RiskStatus.incomplete], 1); // MC4
    expect(s[RiskStatus.high]! + s[RiskStatus.medium]! + s[RiskStatus.low]!, 0);
    expect(s[RiskStatus.noRisk], ruleset.hazards.length - 1);
  });
  test('summarize(): mehrere Mangelbilder', () {
    final s = summarize(evaluate(ruleset, {
      'q_emergency_call_present': false,
      'q_asbestos_pit': true,
      'q_transport_radioactive': true,
      'q_ctrl_digital': true,
      'q_ctrl_free_access': true,
      'q_ctrl_wireless': true,
      'q_ctrl_physical': true,
    }));
    expect(s[RiskStatus.high], 2);
    expect(s[RiskStatus.medium], 2);
  });
}
