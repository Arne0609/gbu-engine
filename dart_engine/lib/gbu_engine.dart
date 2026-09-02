/// GBU APP 4.0 – Referenz-Evaluator (Dart-Portierung).
///
/// 1:1-Übertragung von `evaluator.ts`. Reine, seiteneffektfreie Auswertung:
/// (Antworten + Regelwerk) -> Ergebnisse, in der im Datenmodell festgelegten
/// Reihenfolge: Applicability -> Pflichtfragen (required_mode) -> Regeln ->
/// Aggregation / höchste Priorität.
///
/// Bewusst ohne Flutter-Abhängigkeiten, damit die Bibliothek offline in der
/// App wie auch in reinen Dart-Tests genutzt werden kann. Ausdrücke werden –
/// wie im JSON-Regelwerk – als verschachtelte Maps ausgewertet.
library;

/// Fragen-Code -> Wert. Fehlt der Schlüssel oder ist er null => unbeantwortet.
typedef AnswerMap = Map<String, dynamic>;

/// Die sechs Bewertungszustände.
enum RiskStatus { incomplete, notApplicable, noRisk, low, medium, high }

extension RiskStatusCode on RiskStatus {
  /// Stabiler Bezeichner (identisch zu den DB-/JSON-Werten).
  String get code {
    switch (this) {
      case RiskStatus.incomplete:
        return 'INCOMPLETE';
      case RiskStatus.notApplicable:
        return 'NOT_APPLICABLE';
      case RiskStatus.noRisk:
        return 'NO_RISK';
      case RiskStatus.low:
        return 'LOW';
      case RiskStatus.medium:
        return 'MEDIUM';
      case RiskStatus.high:
        return 'HIGH';
    }
  }

  static RiskStatus fromCode(String c) {
    switch (c) {
      case 'INCOMPLETE':
        return RiskStatus.incomplete;
      case 'NOT_APPLICABLE':
        return RiskStatus.notApplicable;
      case 'NO_RISK':
        return RiskStatus.noRisk;
      case 'LOW':
        return RiskStatus.low;
      case 'MEDIUM':
        return RiskStatus.medium;
      case 'HIGH':
        return RiskStatus.high;
      default:
        throw ArgumentError('Unbekannter RiskStatus: $c');
    }
  }
}

const Map<RiskStatus, int> _severity = {
  RiskStatus.incomplete: -2,
  RiskStatus.notApplicable: -1,
  RiskStatus.noRisk: 0,
  RiskStatus.low: 1,
  RiskStatus.medium: 2,
  RiskStatus.high: 3,
};

// ---- Modell ----------------------------------------------------------------

class HazardQuestion {
  final String question;
  final String role; // APPLICABILITY/TRIGGER/COMPENSATION/MODIFIER/ACCESS_FACTOR/OPTIONAL/DOCUMENTATION
  final String requiredMode; // NEVER | ALWAYS | CONDITIONAL
  final Map<String, dynamic>? requiredWhen;

  const HazardQuestion({
    required this.question,
    required this.role,
    this.requiredMode = 'NEVER',
    this.requiredWhen,
  });

  factory HazardQuestion.fromJson(Map<String, dynamic> j) => HazardQuestion(
        question: j['question'] as String,
        role: j['role'] as String,
        requiredMode: (j['required_mode'] as String?) ?? 'NEVER',
        requiredWhen: (j['required_when'] as Map?)?.cast<String, dynamic>(),
      );
}

class Hazard {
  final String code;
  final String domain;
  final String title;
  final String? description;
  final String? category;
  final String aggregationType; // NONE/ANY/ALL/MAXIMUM/MINIMUM/DECISION_TABLE
  final String evaluationMode; // STANDARD/PARTIAL_ALLOWED/STRICT_REQUIRED
  final bool notImplemented;
  final List<HazardQuestion> questions;
  final List<SourceRef> sources; // Norm-/Quellenbezug (Anzeige)

  const Hazard({
    required this.code,
    required this.domain,
    required this.title,
    this.description,
    this.category,
    this.aggregationType = 'NONE',
    this.evaluationMode = 'STANDARD',
    this.notImplemented = false,
    this.questions = const [],
    this.sources = const [],
  });

  factory Hazard.fromJson(Map<String, dynamic> j) => Hazard(
        code: j['code'] as String,
        domain: j['domain'] as String,
        title: j['title'] as String,
        description: j['description'] as String?,
        category: j['category'] as String?,
        aggregationType: (j['aggregation_type'] as String?) ?? 'NONE',
        evaluationMode: (j['evaluation_mode'] as String?) ?? 'STANDARD',
        notImplemented: (j['not_implemented'] as bool?) ?? false,
        questions: ((j['questions'] as List?) ?? const [])
            .map((e) => HazardQuestion.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
        sources: ((j['sources'] as List?) ?? const [])
            .map((e) => SourceRef.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
      );
}

class Rule {
  final String hazard;
  final String code;
  final int priority;
  final Map<String, dynamic>? applicability;
  final Map<String, dynamic> condition;
  final RiskStatus result;
  final String? aggregation;
  final String origin; // RECONSTRUCTED_ORIGINAL/NORM_DERIVED/OWN_RULE
  final List<MeasureBinding> measures; // Maßnahmen dieser Regel (Anzeige)

  const Rule({
    required this.hazard,
    required this.code,
    required this.priority,
    this.applicability,
    required this.condition,
    required this.result,
    this.aggregation,
    this.origin = 'RECONSTRUCTED_ORIGINAL',
    this.measures = const [],
  });

  factory Rule.fromJson(Map<String, dynamic> j) => Rule(
        hazard: j['hazard'] as String,
        code: j['code'] as String,
        priority: (j['priority'] as num).toInt(),
        applicability: (j['applicability'] as Map?)?.cast<String, dynamic>(),
        condition: (j['condition'] as Map).cast<String, dynamic>(),
        result: RiskStatusCode.fromCode(j['result'] as String),
        aggregation: j['aggregation'] as String?,
        origin: (j['origin'] as String?) ?? 'RECONSTRUCTED_ORIGINAL',
        measures: ((j['measures'] as List?) ?? const [])
            .map((e) => MeasureBinding.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
      );
}

/// Eine Antwortoption einer SELECT-Frage.
class OptionDef {
  final String value;
  final String label;
  const OptionDef({required this.value, required this.label});
  factory OptionDef.fromJson(Map<String, dynamic> j) =>
      OptionDef(value: j['value'] as String, label: j['label'] as String);
}

/// Definition einer Frage inkl. Typ, Antwortoptionen und Kategorie.
class QuestionDef {
  final String code;
  final String type; // YES_NO/SELECT/…
  final String? text;
  final String? category; // Erhebungs-/Anzeigestruktur (Titel)
  final List<OptionDef> options;
  const QuestionDef(
      {required this.code, required this.type, this.text, this.category, this.options = const []});
  factory QuestionDef.fromJson(Map<String, dynamic> j) => QuestionDef(
        code: j['code'] as String,
        type: (j['type'] as String?) ?? 'YES_NO',
        text: j['text'] as String?,
        category: j['category'] as String?,
        options: ((j['options'] as List?) ?? const [])
            .map((e) => OptionDef.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
      );
}

/// Erhebungs-/Anzeigekategorie (Gruppierung der Prüfpunkte).
class CategoryDef {
  final String code;
  final String title;
  final int sortOrder;
  const CategoryDef({required this.code, required this.title, this.sortOrder = 0});
  factory CategoryDef.fromJson(Map<String, dynamic> j) => CategoryDef(
        code: (j['code'] as String?) ?? '',
        title: (j['title'] as String?) ?? '',
        sortOrder: (j['sort_order'] as num?)?.toInt() ?? 0,
      );
}

/// Maßnahme im Katalog.
class MeasureDef {
  final String code;
  final String title;
  final String type; // TECHNICAL/ORGANISATIONAL/…
  const MeasureDef({required this.code, required this.title, this.type = ''});
  factory MeasureDef.fromJson(Map<String, dynamic> j) => MeasureDef(
        code: j['code'] as String,
        title: (j['title'] as String?) ?? j['code'] as String,
        type: (j['type'] as String?) ?? '',
      );
}

/// Verknüpfung Regel -> Maßnahme.
class MeasureBinding {
  final String measure;
  final String relation;
  final bool mandatory;
  const MeasureBinding(
      {required this.measure, this.relation = 'SINGLE', this.mandatory = true});
  factory MeasureBinding.fromJson(Map<String, dynamic> j) => MeasureBinding(
        measure: j['measure'] as String,
        relation: (j['relation'] as String?) ?? 'SINGLE',
        mandatory: (j['mandatory'] as bool?) ?? true,
      );
}

/// Norm-/Quellenbezug.
class SourceRef {
  final String type; // TRBS/EN/LAW/…
  final String document;
  final String? section;
  const SourceRef({required this.type, required this.document, this.section});
  factory SourceRef.fromJson(Map<String, dynamic> j) => SourceRef(
        type: (j['type'] as String?) ?? 'OTHER',
        document: (j['document'] as String?) ?? '',
        section: j['section'] as String?,
      );
}

class Ruleset {
  final String? ruleVersion;
  final List<CategoryDef> categories;
  final List<QuestionDef> questions;
  final List<MeasureDef> measures;
  final List<Hazard> hazards;
  final List<Rule> rules;

  const Ruleset({
    this.ruleVersion,
    this.categories = const [],
    this.questions = const [],
    this.measures = const [],
    this.hazards = const [],
    this.rules = const [],
  });

  factory Ruleset.fromJson(Map<String, dynamic> j) => Ruleset(
        ruleVersion: j['rule_version'] as String?,
        categories: ((j['categories'] as List?) ?? const [])
            .map((e) => CategoryDef.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
        questions: ((j['questions'] as List?) ?? const [])
            .map((e) => QuestionDef.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
        measures: ((j['measures'] as List?) ?? const [])
            .map((e) => MeasureDef.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
        hazards: ((j['hazards'] as List?) ?? const [])
            .map((e) => Hazard.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
        rules: ((j['rules'] as List?) ?? const [])
            .map((e) => Rule.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
      );

  /// Reihenfolge-Index je Kategorietitel (für die Gruppierung in der UI).
  Map<String, int> categoryOrder() {
    final m = <String, int>{};
    for (final c in categories) {
      m[c.title] = c.sortOrder;
    }
    return m;
  }

  /// Frage nach Code (oder null).
  QuestionDef? questionByCode(String code) {
    for (final q in questions) {
      if (q.code == code) return q;
    }
    return null;
  }

  /// Maßnahme nach Code (oder null).
  MeasureDef? measureByCode(String code) {
    for (final m in measures) {
      if (m.code == code) return m;
    }
    return null;
  }
}

class EvaluationResult {
  final String hazard;
  final RiskStatus status;
  final RiskStatus automaticStatus;
  final String? matchedRule;
  final Map<String, dynamic> inputSnapshot;

  const EvaluationResult({
    required this.hazard,
    required this.status,
    required this.automaticStatus,
    required this.matchedRule,
    required this.inputSnapshot,
  });
}

class EvaluateOptions {
  /// Nur Regeln dieser Herkünfte auswerten (null = alle). Mit
  /// {'RECONSTRUCTED_ORIGINAL'} reproduziert die Engine das Original.
  final Set<String>? includeOrigins;
  const EvaluateOptions({this.includeOrigins});
}

// ---- Ausdruckssprache ------------------------------------------------------

bool _isAnswered(AnswerMap answers, String q) =>
    answers.containsKey(q) && answers[q] != null;

/// „Ausdrückliches Nein" für Applicability-Fragen.
bool _isNegative(dynamic v) {
  if (v == false || v == 0) return true;
  if (v is String) return ['nein', 'no', 'false'].contains(v.toLowerCase());
  return false;
}

bool _evalLeaf(Map<String, dynamic> leaf, AnswerMap answers) {
  final q = leaf['question'] as String;
  final op = leaf['operator'] as String;
  final answered = _isAnswered(answers, q);
  final v = answered ? answers[q] : null;
  final expected = leaf['value'];
  switch (op) {
    case 'ANSWERED':
      return answered;
    case 'NOT_ANSWERED':
      return !answered;
    // Vergleiche verlangen eine vorhandene Antwort; fehlt sie, ist das Blatt
    // FALSE (nie „unbekannt = wahr").
    case 'EQ':
      return answered && v == expected;
    case 'NEQ':
      return answered && v != expected;
    case 'GT':
      return answered && v is num && expected is num && v > expected;
    case 'GTE':
      return answered && v is num && expected is num && v >= expected;
    case 'LT':
      return answered && v is num && expected is num && v < expected;
    case 'LTE':
      return answered && v is num && expected is num && v <= expected;
    case 'IN':
      return answered && expected is List && expected.contains(v);
    case 'NOT_IN':
      return answered && expected is List && !expected.contains(v);
    default:
      return false;
  }
}

/// Wertet einen Bedingungsbaum (all/any/not oder Blatt) aus.
bool evalExpression(Map<String, dynamic> expr, AnswerMap answers) {
  if (expr.containsKey('all')) {
    return (expr['all'] as List)
        .every((e) => evalExpression((e as Map).cast<String, dynamic>(), answers));
  }
  if (expr.containsKey('any')) {
    return (expr['any'] as List)
        .any((e) => evalExpression((e as Map).cast<String, dynamic>(), answers));
  }
  if (expr.containsKey('not')) {
    return !evalExpression((expr['not'] as Map).cast<String, dynamic>(), answers);
  }
  return _evalLeaf(expr, answers);
}

void _collectQuestions(Map<String, dynamic> expr, Set<String> into) {
  if (expr.containsKey('all')) {
    for (final e in expr['all'] as List) {
      _collectQuestions((e as Map).cast<String, dynamic>(), into);
    }
    return;
  }
  if (expr.containsKey('any')) {
    for (final e in expr['any'] as List) {
      _collectQuestions((e as Map).cast<String, dynamic>(), into);
    }
    return;
  }
  if (expr.containsKey('not')) {
    _collectQuestions((expr['not'] as Map).cast<String, dynamic>(), into);
    return;
  }
  into.add(expr['question'] as String);
}

// ---- Kern ------------------------------------------------------------------

EvaluationResult evaluateHazard(
  Hazard hazard,
  List<Rule> rules,
  AnswerMap answers, {
  EvaluateOptions options = const EvaluateOptions(),
}) {
  final snapshotKeys = <String>{for (final q in hazard.questions) q.question};

  EvaluationResult build(RiskStatus status, String? matched) {
    final snap = <String, dynamic>{};
    for (final k in snapshotKeys) {
      if (_isAnswered(answers, k)) snap[k] = answers[k];
    }
    return EvaluationResult(
      hazard: hazard.code,
      status: status,
      automaticStatus: status,
      matchedRule: matched,
      inputSnapshot: snap,
    );
  }

  // Nicht implementierte Gefährdungen (z. B. MC13) nie bewerten.
  if (hazard.notImplemented) return build(RiskStatus.notApplicable, null);

  // 1) Applicability
  final appQs = hazard.questions.where((q) => q.role == 'APPLICABILITY');
  for (final q in appQs) {
    if (_isAnswered(answers, q.question) && _isNegative(answers[q.question])) {
      return build(RiskStatus.notApplicable, null);
    }
  }
  for (final q in appQs) {
    if (!_isAnswered(answers, q.question)) return build(RiskStatus.incomplete, null);
  }

  // 2) Pflichtfragen (gefährdungsspezifisch)
  for (final q in hazard.questions) {
    final required = q.requiredMode == 'ALWAYS' ||
        (q.requiredMode == 'CONDITIONAL' &&
            q.requiredWhen != null &&
            evalExpression(q.requiredWhen!, answers));
    if (required && !_isAnswered(answers, q.question)) {
      return build(RiskStatus.incomplete, null);
    }
  }

  // 3) Regeln
  final allow = options.includeOrigins;
  final applicable = rules.where((r) {
    if (allow != null && !allow.contains(r.origin)) return false;
    if (r.applicability != null && !evalExpression(r.applicability!, answers)) {
      return false;
    }
    return true;
  });
  final matching =
      applicable.where((r) => evalExpression(r.condition, answers)).toList();

  if (matching.isEmpty) return build(RiskStatus.noRisk, null);

  // 4) Aggregation / höchste Priorität
  final hazardAgg = hazard.aggregationType;
  Rule winner;
  if (hazardAgg == 'MAXIMUM' || hazardAgg == 'ANY') {
    winner = matching.reduce(
        (a, b) => _severity[b.result]! > _severity[a.result]! ? b : a);
  } else {
    winner = matching.reduce((a, b) {
      if (b.priority != a.priority) return b.priority > a.priority ? b : a;
      return _severity[b.result]! > _severity[a.result]! ? b : a;
    });
  }
  if (winner.applicability != null) {
    _collectQuestions(winner.applicability!, snapshotKeys);
  }
  _collectQuestions(winner.condition, snapshotKeys);
  return build(winner.result, winner.code);
}

/// Wertet alle Gefährdungen des Regelwerks aus.
List<EvaluationResult> evaluate(
  Ruleset ruleset,
  AnswerMap answers, {
  EvaluateOptions options = const EvaluateOptions(),
}) {
  final byHazard = <String, List<Rule>>{};
  for (final r in ruleset.rules) {
    byHazard.putIfAbsent(r.hazard, () => []).add(r);
  }
  return ruleset.hazards
      .map((h) => evaluateHazard(h, byHazard[h.code] ?? const [], answers,
          options: options))
      .toList();
}

/// Zählung der Ergebnisse je Status (für die Bewertungsübersicht).
Map<RiskStatus, int> summarize(List<EvaluationResult> results) {
  final out = {for (final s in RiskStatus.values) s: 0};
  for (final r in results) {
    out[r.status] = out[r.status]! + 1;
  }
  return out;
}
