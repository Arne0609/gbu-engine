import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:gbu_engine/gbu_engine.dart';
import 'api_client.dart';
import 'catalog_source.dart';

/// Hält die geladenen Kataloge und die Antworten je Katalog und stellt die
/// Auswertung (Evaluator aus gbu_engine) für die Oberfläche bereit.
///
/// Die Kataloge kommen aus einer [CatalogSource]: entweder aus gebündelten
/// Assets (offline) oder über die Engine-API ([HttpCatalogSource]). Im
/// HTTP-Modus werden Antworten zusätzlich serverseitig persistiert und die
/// dortige Zusammenfassung als Gegenprobe geführt; die angezeigten Ergebnisse
/// rechnet weiterhin die lokale Engine (sofort, offlinefähig, gleicher Port).
class AssessmentController extends ChangeNotifier {
  final CatalogSource source;
  final GbuApiClient? api;

  AssessmentController({CatalogSource? source, this.api})
      : source = source ?? AssetCatalogSource();

  final Map<String, CatalogRef> _refs = {}; // label -> ref
  final Map<String, Ruleset> _catalogs = {}; // label -> geladenes Regelwerk
  final Map<String, Map<String, dynamic>> _answers = {}; // label -> Antworten
  final Map<String, String> _assessmentIds = {}; // label -> assessment_id (remote)
  final Map<String, Map<String, int>> _serverSummary = {}; // label -> Zählung (remote)

  List<String> _labels = const [];
  String? current;
  String? selectedHazard;
  bool loading = true;
  String? error;

  // Serverabgleich (nur HTTP-Modus).
  bool syncing = false;
  String? syncError;
  Timer? _debounce;

  bool get isRemote => source.isRemote;
  List<String> get catalogLabels => _labels;
  Ruleset get catalog => _catalogs[current]!;
  Map<String, dynamic> get answers {
    final c = current;
    if (c == null) return <String, dynamic>{};
    return _answers[c] ??= <String, dynamic>{};
  }

  /// Serverseitige Zählung je RiskStatus für den aktuellen Katalog (oder null).
  Map<String, int>? get serverSummary => current == null ? null : _serverSummary[current];

  Future<void> load() async {
    try {
      final refs = await source.list();
      if (refs.isEmpty) throw StateError('Keine Kataloge verfügbar');
      for (final r in refs) {
        _refs[r.label] = r;
      }
      _labels = refs.map((r) => r.label).toList(growable: false);
      current = _labels.firstWhere((l) => l.contains('81-41'), orElse: () => _labels.first);
      await _ensureLoaded(current!);
      _prefill(current!);
      await _syncNow(current!); // erste Persistenz/Gegenprobe im HTTP-Modus
    } catch (e) {
      error = '$e';
    }
    loading = false;
    notifyListeners();
  }

  List<EvaluationResult> get results => evaluate(catalog, answers);
  Map<RiskStatus, int> get summary => summarize(results);

  EvaluationResult? resultFor(String hazardCode) {
    for (final r in results) {
      if (r.hazard == hazardCode) return r;
    }
    return null;
  }

  void selectCatalog(String label) {
    if (label == current) return;
    // Asynchron laden; bei noch nicht geladenem Remote-Katalog Spinner zeigen.
    unawaited(_switchTo(label));
  }

  Future<void> _switchTo(String label) async {
    selectedHazard = null;
    syncError = null;
    if (!_catalogs.containsKey(label)) {
      loading = true;
      current = label;
      notifyListeners();
      try {
        await _ensureLoaded(label);
      } catch (e) {
        error = '$e';
        loading = false;
        notifyListeners();
        return;
      }
      loading = false;
    } else {
      current = label;
    }
    if ((_answers[label] ?? const <String, dynamic>{}).isEmpty) _prefill(label);
    notifyListeners();
    await _syncNow(label);
  }

  Future<void> _ensureLoaded(String label) async {
    if (_catalogs.containsKey(label)) return;
    final ref = _refs[label]!;
    _catalogs[label] = await source.load(ref);
    _answers[label] ??= {};
  }

  void setAnswer(String questionCode, String? value) {
    if (value == null || value.isEmpty) {
      answers.remove(questionCode);
    } else {
      answers[questionCode] = value;
    }
    notifyListeners();
    _scheduleSync(current!);
  }

  void selectHazard(String? code) {
    selectedHazard = code;
    notifyListeners();
  }

  // ---- Serverabgleich (HTTP-Modus) -----------------------------------------

  void _scheduleSync(String label) {
    if (!isRemote || api == null) return;
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 500), () => unawaited(_syncNow(label)));
  }

  /// Antworten des Katalogs speichern und Server-Zusammenfassung übernehmen.
  /// Fehler blockieren die Oberfläche nicht (Offline-Fähigkeit bleibt).
  Future<void> _syncNow(String label) async {
    if (!isRemote || api == null) return;
    final ref = _refs[label];
    if (ref?.ruleVersionId == null) return;
    syncing = true;
    syncError = null;
    notifyListeners();
    try {
      var id = _assessmentIds[label];
      id ??= _assessmentIds[label] = await api!.createAssessment(ref!.ruleVersionId!);
      final sum = await api!.saveAnswers(id, _answers[label] ?? const <String, dynamic>{});
      _serverSummary[label] = {
        for (final e in sum.entries) e.key: (e.value as num).toInt(),
      };
    } catch (e) {
      syncError = '$e';
    }
    syncing = false;
    notifyListeners();
  }

  @override
  void dispose() {
    _debounce?.cancel();
    api?.close();
    super.dispose();
  }

  /// Beispiel-Vorbelegung, damit die Oberfläche in einem realistischen
  /// Arbeitszustand öffnet (erste Prüfpunkte mit gemischten Stufen).
  void _prefill(String label) {
    final c = _catalogs[label]!;
    final a = _answers[label] ??= {};
    final byHaz = <String, List<Rule>>{};
    for (final r in c.rules) {
      byHaz.putIfAbsent(r.hazard, () => []).add(r);
    }
    const wanted = [
      RiskStatus.high, RiskStatus.noRisk, RiskStatus.medium,
      RiskStatus.notApplicable, RiskStatus.noRisk,
    ];
    var wi = 0;
    for (final h in c.hazards) {
      if (wi >= wanted.length) break;
      if (h.questions.isEmpty) continue;
      final q = h.questions.first.question;
      final want = wanted[wi];
      for (final r in byHaz[h.code] ?? const <Rule>[]) {
        if (r.result == want && r.condition['question'] == q) {
          a[q] = r.condition['value'];
          wi++;
          break;
        }
      }
    }
  }
}
