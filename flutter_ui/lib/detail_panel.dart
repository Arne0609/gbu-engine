import 'package:flutter/material.dart';
import 'package:gbu_engine/gbu_engine.dart';
import 'assessment_controller.dart';
import 'theme.dart';

/// Gefährdungsdetail: Status, zutreffende Regel, gewählter Istzustand,
/// Maßnahmen und Norm-/Quellenbezug.
class DetailPanel extends StatelessWidget {
  final AssessmentController ctrl;
  final String hazardCode;
  const DetailPanel({super.key, required this.ctrl, required this.hazardCode});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    final cat = ctrl.catalog;
    final hazard = cat.hazards.firstWhere((h) => h.code == hazardCode);
    final res = ctrl.resultFor(hazardCode)!;
    final rc = RiskStyle.color(context, res.status);
    final q = hazard.questions.isNotEmpty ? hazard.questions.first.question : null;
    final chosen = q != null ? ctrl.answers[q] : null;
    OptionDef? opt;
    if (q != null && chosen != null) {
      final qd = cat.questionByCode(q);
      for (final o in qd?.options ?? const <OptionDef>[]) {
        if (o.value == chosen) opt = o;
      }
    }

    return Container(
      decoration: BoxDecoration(
        color: cs.surface,
        border: Border.all(color: cs.outline),
        borderRadius: BorderRadius.circular(14),
      ),
      clipBehavior: Clip.antiAlias,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          // Kopf
          Container(
            width: double.infinity,
            padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
            decoration: BoxDecoration(
              border: Border(top: BorderSide(color: rc, width: 4)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('${hazard.code}${res.matchedRule != null ? ' · ${res.matchedRule}' : ''}',
                    style: TextStyle(
                        fontFamily: 'monospace', fontSize: 12, color: cs.onSurface.withValues(alpha: .55))),
                const SizedBox(height: 3),
                Text(hazard.title,
                    style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600, height: 1.35)),
                const SizedBox(height: 10),
                Row(mainAxisSize: MainAxisSize.min, children: [
                  Container(width: 11, height: 11, decoration: BoxDecoration(color: rc, shape: BoxShape.circle)),
                  const SizedBox(width: 7),
                  Text(RiskStyle.label(res.status),
                      style: TextStyle(color: rc, fontWeight: FontWeight.w600, fontSize: 13)),
                ]),
              ],
            ),
          ),
          Flexible(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(16, 14, 16, 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (hazard.description != null && hazard.description!.isNotEmpty)
                    _section(context, 'Sollzustand / Kriterium',
                        Text(hazard.description!, style: _soft(context))),
                  _section(
                    context,
                    'Gewählter Istzustand',
                    Text(opt?.label ?? '— noch nicht bewertet (Unvollständig) —',
                        style: opt == null ? _soft(context) : const TextStyle(fontSize: 13.5, height: 1.5)),
                  ),
                  _section(context, 'Maßnahmen', _measures(context, res)),
                  _section(context, 'Norm-/Quellenbezug', _sources(context, hazard)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  TextStyle _soft(BuildContext c) => TextStyle(
      fontSize: 13.5, height: 1.5, color: Theme.of(c).colorScheme.onSurface.withValues(alpha: .6));

  Widget _section(BuildContext c, String title, Widget body) => Padding(
        padding: const EdgeInsets.only(bottom: 15),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title.toUpperCase(),
              style: TextStyle(
                  fontSize: 11, letterSpacing: .8, fontWeight: FontWeight.w600,
                  color: Theme.of(c).colorScheme.onSurface.withValues(alpha: .5))),
          const SizedBox(height: 6),
          body,
        ]),
      );

  Widget _measures(BuildContext context, EvaluationResult res) {
    final cs = Theme.of(context).colorScheme;
    Rule? rule;
    if (res.matchedRule != null) {
      for (final r in ctrl.catalog.rules) {
        if (r.code == res.matchedRule) {
          rule = r;
          break;
        }
      }
    }
    if (rule == null || rule.measures.isEmpty) {
      return Text('Keine Maßnahme hinterlegt.', style: _soft(context).copyWith(fontStyle: FontStyle.italic));
    }
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        for (final mb in rule.measures)
          Builder(builder: (_) {
            final m = ctrl.catalog.measureByCode(mb.measure);
            final t = m?.type ?? '';
            final kind = t == 'ORGANISATIONAL'
                ? 'ORG'
                : t == 'TECHNICAL'
                    ? 'TECH'
                    : (t.isEmpty ? '–' : (t.length > 4 ? t.substring(0, 4) : t));
            return Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Container(
                  margin: const EdgeInsets.only(top: 1, right: 9),
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                      color: cs.surfaceContainerHighest, borderRadius: BorderRadius.circular(5)),
                  child: Text(kind.isEmpty ? '–' : kind,
                      style: TextStyle(
                          fontFamily: 'monospace', fontSize: 10, fontWeight: FontWeight.w600,
                          color: cs.onSurface.withValues(alpha: .7))),
                ),
                Expanded(child: Text(m?.title ?? mb.measure, style: const TextStyle(fontSize: 13, height: 1.45))),
              ]),
            );
          }),
      ],
    );
  }

  Widget _sources(BuildContext context, Hazard hazard) {
    final cs = Theme.of(context).colorScheme;
    if (hazard.sources.isEmpty) {
      return Text('Kein Normbezug hinterlegt.', style: _soft(context).copyWith(fontStyle: FontStyle.italic));
    }
    return Wrap(
      spacing: 6,
      runSpacing: 6,
      children: [
        for (final s in hazard.sources)
          Container(
            padding: const EdgeInsets.fromLTRB(3, 3, 8, 3),
            decoration: BoxDecoration(
              color: cs.surfaceContainerHighest,
              border: Border.all(color: cs.outline),
              borderRadius: BorderRadius.circular(7),
            ),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 2),
                decoration: BoxDecoration(color: cs.primary, borderRadius: BorderRadius.circular(4)),
                child: Text(s.type,
                    style: TextStyle(
                        fontFamily: 'monospace', fontSize: 9.5, fontWeight: FontWeight.w600, color: cs.onPrimary)),
              ),
              const SizedBox(width: 6),
              Text(s.document, style: const TextStyle(fontSize: 12)),
              if (s.section != null && s.section!.isNotEmpty) ...[
                const SizedBox(width: 5),
                Text(s.section!,
                    style: TextStyle(fontSize: 12, color: cs.onSurface.withValues(alpha: .6))),
              ],
            ]),
          ),
      ],
    );
  }
}
