import 'dart:convert';
import 'package:http/http.dart' as http;

/// Kurzinfo zu einer Regelversion (aus GET /rule-versions).
class RuleVersionInfo {
  final String id;
  final String name;
  final String version;
  final String domain;
  final int hazards;
  const RuleVersionInfo({
    required this.id,
    required this.name,
    required this.version,
    required this.domain,
    required this.hazards,
  });

  factory RuleVersionInfo.fromJson(Map<String, dynamic> j) => RuleVersionInfo(
        id: j['id'] as String,
        name: (j['name'] as String?) ?? 'GBU-Regelwerk',
        version: (j['version'] as String?) ?? '',
        domain: (j['domain'] as String?) ?? 'BOTH',
        hazards: (j['hazards'] as num?)?.toInt() ?? 0,
      );

  /// Sprechender Anzeigename je Regelversion.
  String get label {
    const map = <String, String>{
      'en8141-2026.1': 'Plattformaufzug · EN 81-41',
      '81-80-2026.1': 'GBU vereinfacht · EN 81-80',
      '81-20-2026.1': 'GBU erweitert · EN 81-20',
      '2026add-2026.1': 'Ergänzung 2026 · Gebäude & Cyber-Matrix',
      'cyber-voll-2026.1': 'Cyber · TRBS 1115-1 (voll)',
      'cyber-minimal-2026.1': 'Cyber · minimal',
    };
    return map[version] ?? '$name $version';
  }
}

/// Fehler aus der Engine-API (Statuscode ≥ 400 oder ok:false).
class GbuApiException implements Exception {
  final int? status;
  final String message;
  const GbuApiException(this.message, {this.status});
  @override
  String toString() => 'GbuApiException(${status ?? '-'}): $message';
}

/// Dünner REST-Client für die GBU-Engine-API (siehe engine_api.ts/server.ts).
///
/// Deckt alle Endpunkte ab: Katalog beziehen, Beurteilung anlegen, Antworten
/// speichern + evaluieren, Ergebnisse und Zusammenfassung lesen.
class GbuApiClient {
  final Uri base;
  final http.Client _http;
  final Duration timeout;

  GbuApiClient(String baseUrl, {http.Client? client, this.timeout = const Duration(seconds: 12)})
      : base = Uri.parse(baseUrl.endsWith('/') ? baseUrl.substring(0, baseUrl.length - 1) : baseUrl),
        _http = client ?? http.Client();

  Uri _u(String path) => Uri.parse('$base$path');

  Map<String, dynamic> _decode(http.Response r) {
    Map<String, dynamic> body;
    try {
      body = jsonDecode(r.body) as Map<String, dynamic>;
    } catch (_) {
      throw GbuApiException('Ungültige Antwort (${r.statusCode})', status: r.statusCode);
    }
    if (r.statusCode >= 400 || body['ok'] == false) {
      throw GbuApiException((body['error'] as String?) ?? 'HTTP ${r.statusCode}', status: r.statusCode);
    }
    return body;
  }

  Future<bool> health() async {
    try {
      final r = await _http.get(_u('/health')).timeout(timeout);
      return _decode(r)['ok'] == true;
    } catch (_) {
      return false;
    }
  }

  Future<List<RuleVersionInfo>> ruleVersions() async {
    final r = await _http.get(_u('/rule-versions')).timeout(timeout);
    final list = (_decode(r)['rule_versions'] as List?) ?? const [];
    return list
        .map((e) => RuleVersionInfo.fromJson((e as Map).cast<String, dynamic>()))
        .toList(growable: false);
  }

  /// Vollständiger Anzeige-Katalog (gleiche Form wie die Seed-Dateien).
  Future<Map<String, dynamic>> catalog(String ruleVersionId) async {
    final r = await _http.get(_u('/rule-versions/$ruleVersionId/catalog')).timeout(timeout);
    return (_decode(r)['catalog'] as Map).cast<String, dynamic>();
  }

  /// Legt eine Beurteilung an und liefert deren id.
  Future<String> createAssessment(String ruleVersionId, {String type = 'GBU'}) async {
    final r = await _http
        .post(_u('/assessments'),
            headers: const {'Content-Type': 'application/json'},
            body: jsonEncode({'rule_version_id': ruleVersionId, 'type': type}))
        .timeout(timeout);
    return _decode(r)['assessment_id'] as String;
  }

  /// Speichert Antworten und evaluiert; liefert die Zusammenfassung (Zählung
  /// je RiskStatus, z. B. {"HIGH":2,"INCOMPLETE":5,...}).
  Future<Map<String, dynamic>> saveAnswers(String assessmentId, Map<String, dynamic> answers) async {
    final r = await _http
        .put(_u('/assessments/$assessmentId/answers'),
            headers: const {'Content-Type': 'application/json'},
            body: jsonEncode({'answers': answers}))
        .timeout(timeout);
    return (_decode(r)['summary'] as Map?)?.cast<String, dynamic>() ?? const {};
  }

  Future<List<Map<String, dynamic>>> results(String assessmentId) async {
    final r = await _http.get(_u('/assessments/$assessmentId/results')).timeout(timeout);
    final list = (_decode(r)['results'] as List?) ?? const [];
    return list.map((e) => (e as Map).cast<String, dynamic>()).toList(growable: false);
  }

  Future<Map<String, dynamic>> assessment(String assessmentId) async {
    final r = await _http.get(_u('/assessments/$assessmentId')).timeout(timeout);
    return _decode(r);
  }

  void close() => _http.close();
}
