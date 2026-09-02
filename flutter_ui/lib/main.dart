import 'package:flutter/material.dart';
import 'api_client.dart';
import 'assessment_controller.dart';
import 'catalog_source.dart';
import 'bewertung_screen.dart';
import 'theme.dart';

/// Basis-URL der Engine-API. Leer = Offline-Modus (gebündelte Assets).
/// Setzen per: flutter run --dart-define=GBU_API_BASE=http://127.0.0.1:8787
const String kApiBase = String.fromEnvironment('GBU_API_BASE');

void main() => runApp(const GbuApp());

class GbuApp extends StatefulWidget {
  const GbuApp({super.key});
  @override
  State<GbuApp> createState() => _GbuAppState();
}

class _GbuAppState extends State<GbuApp> {
  late final AssessmentController ctrl;
  ThemeMode mode = ThemeMode.system;

  @override
  void initState() {
    super.initState();
    if (kApiBase.isNotEmpty) {
      final api = GbuApiClient(kApiBase);
      ctrl = AssessmentController(source: HttpCatalogSource(api), api: api);
    } else {
      ctrl = AssessmentController(); // Assets, offline
    }
    ctrl.load();
  }

  @override
  void dispose() {
    ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'GBU-Bewertung',
        debugShowCheckedModeBanner: false,
        theme: buildTheme(Brightness.light),
        darkTheme: buildTheme(Brightness.dark),
        themeMode: mode,
        home: BewertungScreen(
          ctrl: ctrl,
          onToggleTheme: () => setState(
              () => mode = mode == ThemeMode.dark ? ThemeMode.light : ThemeMode.dark),
        ),
      );
}
