import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import 'package:gbu_engine/gbu_engine.dart';
import 'api_client.dart';

/// Referenz auf einen wählbaren Katalog (GBU-Typ) – unabhängig davon, ob er
/// aus gebündelten Assets oder über HTTP kommt.
class CatalogRef {
  final String label; // Anzeigename im GBU-Typ-Auswähler
  final String key; // Asset-Pfad ODER rule_version_id
  final String? ruleVersionId; // nur remote gesetzt
  const CatalogRef({required this.label, required this.key, this.ruleVersionId});
  bool get isRemote => ruleVersionId != null;
}

/// Bezugsquelle für Kataloge. Zwei Implementierungen: lokale Assets (offline)
/// und die Engine-API (HTTP). Die Datenform ist identisch, daher lädt beide
/// dasselbe [Ruleset].
abstract class CatalogSource {
  bool get isRemote;

  /// Verfügbare Kataloge (GBU-Typen) auflisten.
  Future<List<CatalogRef>> list();

  /// Regelwerk zu einer Referenz laden.
  Future<Ruleset> load(CatalogRef ref);
}

/// Kataloge aus gebündelten Assets (assets/catalogs/*.json). Standard, offline.
class AssetCatalogSource implements CatalogSource {
  static const _files = <MapEntry<String, String>>[
    MapEntry('assets/catalogs/norm_en8141.json', 'Plattformaufzug · EN 81-41'),
    MapEntry('assets/catalogs/norm_81_80.json', 'GBU vereinfacht · EN 81-80'),
    MapEntry('assets/catalogs/norm_81_20.json', 'GBU erweitert · EN 81-20'),
    MapEntry('assets/catalogs/norm_2026.json', 'Ergänzung 2026 · Gebäude & Cyber-Matrix'),
    MapEntry('assets/catalogs/norm_cyber_voll.json', 'Cyber · TRBS 1115-1 (voll)'),
    MapEntry('assets/catalogs/norm_cyber_minimal.json', 'Cyber · minimal'),
  ];

  @override
  bool get isRemote => false;

  @override
  Future<List<CatalogRef>> list() async =>
      _files.map((e) => CatalogRef(label: e.value, key: e.key)).toList(growable: false);

  @override
  Future<Ruleset> load(CatalogRef ref) async {
    final txt = await rootBundle.loadString(ref.key);
    return Ruleset.fromJson(jsonDecode(txt) as Map<String, dynamic>);
  }
}

/// Kataloge über die Engine-API. Reihenfolge der GBU-Typen wie im Asset-Modus.
class HttpCatalogSource implements CatalogSource {
  final GbuApiClient api;
  HttpCatalogSource(this.api);

  static const _order = <String>[
    'en8141-2026.1',
    '81-80-2026.1',
    '81-20-2026.1',
    '2026add-2026.1',
    'cyber-voll-2026.1',
    'cyber-minimal-2026.1',
  ];

  @override
  bool get isRemote => true;

  @override
  Future<List<CatalogRef>> list() async {
    final rvs = await api.ruleVersions();
    rvs.sort((a, b) {
      final ia = _order.indexOf(a.version);
      final ib = _order.indexOf(b.version);
      return (ia < 0 ? 99 : ia).compareTo(ib < 0 ? 99 : ib);
    });
    return rvs
        .map((rv) => CatalogRef(label: rv.label, key: rv.id, ruleVersionId: rv.id))
        .toList(growable: false);
  }

  @override
  Future<Ruleset> load(CatalogRef ref) async {
    final map = await api.catalog(ref.ruleVersionId ?? ref.key);
    return Ruleset.fromJson(map);
  }
}
