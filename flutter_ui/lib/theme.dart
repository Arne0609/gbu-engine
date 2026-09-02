import 'package:flutter/material.dart';
import 'package:gbu_engine/gbu_engine.dart';

/// Farben und Beschriftung der sechs Bewertungszustände (Ampel-Semantik,
/// getrennt vom UI-Akzent). Hell/Dunkel je nach Theme-Helligkeit.
class RiskStyle {
  static const _light = {
    RiskStatus.high: Color(0xFFC62D43),
    RiskStatus.medium: Color(0xFFBD6F16),
    RiskStatus.low: Color(0xFF8F7C0E),
    RiskStatus.noRisk: Color(0xFF2B855A),
    RiskStatus.notApplicable: Color(0xFF6B7684),
    RiskStatus.incomplete: Color(0xFF356AA0),
  };
  static const _dark = {
    RiskStatus.high: Color(0xFFFF6A7E),
    RiskStatus.medium: Color(0xFFF0A24E),
    RiskStatus.low: Color(0xFFD8C257),
    RiskStatus.noRisk: Color(0xFF4EC489),
    RiskStatus.notApplicable: Color(0xFF8B97A6),
    RiskStatus.incomplete: Color(0xFF6EA6E6),
  };
  static const _label = {
    RiskStatus.high: 'Hoch',
    RiskStatus.medium: 'Mittel',
    RiskStatus.low: 'Niedrig',
    RiskStatus.noRisk: 'Kein Risiko',
    RiskStatus.notApplicable: 'Nicht zutreffend',
    RiskStatus.incomplete: 'Unvollständig',
  };

  static Color color(BuildContext ctx, RiskStatus s) =>
      (Theme.of(ctx).brightness == Brightness.dark ? _dark : _light)[s]!;

  /// Getönter Hintergrund (für Badges/Kacheln).
  static Color bg(BuildContext ctx, RiskStatus s) =>
      color(ctx, s).withValues(alpha: Theme.of(ctx).brightness == Brightness.dark ? 0.16 : 0.13);

  static String label(RiskStatus s) => _label[s]!;

  /// Reihenfolge für die Übersichtskacheln.
  static const order = [
    RiskStatus.high, RiskStatus.medium, RiskStatus.low,
    RiskStatus.noRisk, RiskStatus.notApplicable, RiskStatus.incomplete,
  ];
}

ThemeData buildTheme(Brightness b) {
  final dark = b == Brightness.dark;
  final accent = dark ? const Color(0xFF6BA0D6) : const Color(0xFF2F5D86);
  final bg = dark ? const Color(0xFF0E141B) : const Color(0xFFEEF1F5);
  final surface = dark ? const Color(0xFF161E28) : Colors.white;
  final ink = dark ? const Color(0xFFE7EDF4) : const Color(0xFF18222E);
  final line = dark ? const Color(0xFF26313D) : const Color(0xFFDBE1E9);
  final scheme = ColorScheme(
    brightness: b,
    primary: accent,
    onPrimary: dark ? const Color(0xFF0E141B) : Colors.white,
    secondary: accent,
    onSecondary: dark ? const Color(0xFF0E141B) : Colors.white,
    error: const Color(0xFFC62D43),
    onError: Colors.white,
    surface: surface,
    onSurface: ink,
    surfaceContainerHighest: dark ? const Color(0xFF222E3B) : const Color(0xFFE9EDF2),
    outline: line,
    outlineVariant: line,
  );
  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: bg,
    dividerColor: line,
    textTheme: Typography.material2021(platform: TargetPlatform.linux)
        .black
        .apply(bodyColor: ink, displayColor: ink),
  );
}
