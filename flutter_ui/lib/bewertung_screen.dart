import 'package:flutter/material.dart';
import 'package:gbu_engine/gbu_engine.dart';
import 'assessment_controller.dart';
import 'detail_panel.dart';
import 'theme.dart';

class BewertungScreen extends StatefulWidget {
  final AssessmentController ctrl;
  final VoidCallback onToggleTheme;
  const BewertungScreen({super.key, required this.ctrl, required this.onToggleTheme});
  @override
  State<BewertungScreen> createState() => _BewertungScreenState();
}

class _BewertungScreenState extends State<BewertungScreen> {
  RiskStatus? filter;

  @override
  Widget build(BuildContext context) {
    final ctrl = widget.ctrl;
    return Scaffold(
      appBar: AppBar(
        titleSpacing: 16,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: const [
            Text('GBU-Bewertung', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            Text('Regelengine · Frage → Gefährdung → Regel → Risikostufe',
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.w400)),
          ],
        ),
        actions: [
          IconButton(
            tooltip: 'Hell/Dunkel',
            onPressed: widget.onToggleTheme,
            icon: const Icon(Icons.brightness_6_outlined),
          ),
          const SizedBox(width: 6),
        ],
      ),
      body: AnimatedBuilder(
        animation: ctrl,
        builder: (context, _) {
          if (ctrl.loading) return const Center(child: CircularProgressIndicator());
          if (ctrl.error != null) {
            return Center(child: Padding(padding: const EdgeInsets.all(24), child: Text('Fehler: ${ctrl.error}')));
          }
          return LayoutBuilder(builder: (context, cns) {
            final wide = cns.maxWidth >= 900;
            final list = _content(context, ctrl, wide);
            if (!wide) return list;
            return Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(child: list),
                Container(
                  width: 372,
                  padding: const EdgeInsets.fromLTRB(0, 16, 16, 16),
                  child: _detail(context, ctrl),
                ),
              ],
            );
          });
        },
      ),
    );
  }

  Widget _detail(BuildContext context, AssessmentController ctrl) {
    final res = ctrl.results;
    if (res.isEmpty) return const SizedBox.shrink();
    final code = ctrl.selectedHazard ??
        (res.firstWhere((r) => r.status == RiskStatus.high, orElse: () => res.first)).hazard;
    return DetailPanel(ctrl: ctrl, hazardCode: code);
  }

  Widget _content(BuildContext context, AssessmentController ctrl, bool wide) {
    final res = ctrl.results;
    final summary = ctrl.summary;
    final total = res.length;
    final answered = res.where((r) => r.status != RiskStatus.incomplete).length;

    // Kategorien gruppieren
    final groups = <String, List<Hazard>>{};
    for (final h in ctrl.catalog.hazards) {
      groups.putIfAbsent(h.category ?? 'Ohne Kategorie', () => []).add(h);
    }
    final resByCode = {for (final r in res) r.hazard: r};

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 40),
      children: [
        _catalogSelector(context, ctrl),
        const SizedBox(height: 14),
        _overview(context, ctrl, summary, answered, total),
        const SizedBox(height: 18),
        for (final entry in groups.entries)
          _categorySection(context, ctrl, entry.key, entry.value, resByCode),
      ],
    );
  }

  Widget _catalogSelector(BuildContext context, AssessmentController ctrl) {
    final cs = Theme.of(context).colorScheme;
    return Row(children: [
      Text('GBU-TYP',
          style: TextStyle(
              fontSize: 11, letterSpacing: .8, fontWeight: FontWeight.w600,
              color: cs.onSurface.withValues(alpha: .5))),
      const SizedBox(width: 10),
      Expanded(
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          decoration: BoxDecoration(
              color: cs.surface, border: Border.all(color: cs.outline), borderRadius: BorderRadius.circular(9)),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              isExpanded: true,
              value: ctrl.current,
              items: [
                for (final l in ctrl.catalogLabels)
                  DropdownMenuItem(value: l, child: Text(l, style: const TextStyle(fontSize: 14))),
              ],
              onChanged: (v) {
                if (v != null) {
                  setState(() => filter = null);
                  ctrl.selectCatalog(v);
                }
              },
            ),
          ),
        ),
      ),
    ]);
  }

  Widget _overview(BuildContext context, AssessmentController ctrl, Map<RiskStatus, int> summary, int answered, int total) {
    final cs = Theme.of(context).colorScheme;
    final rv = ctrl.catalog.ruleVersion;
    return Container(
      decoration: BoxDecoration(
          color: cs.surface, border: Border.all(color: cs.outline), borderRadius: BorderRadius.circular(14)),
      clipBehavior: Clip.antiAlias,
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 14, 16, 0),
          child: Row(children: [
            const Text('Bewertungsübersicht', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            const SizedBox(width: 10),
            _connectionChip(context, ctrl),
            const Spacer(),
            if (rv != null)
              Flexible(
                child: Text('Regelwerk $rv',
                    textAlign: TextAlign.right,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(fontSize: 12, color: cs.onSurface.withValues(alpha: .5))),
              ),
          ]),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 10, 16, 12),
          child: Row(children: [
            Expanded(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(99),
                child: LinearProgressIndicator(
                  value: total == 0 ? 0 : answered / total,
                  minHeight: 7,
                  backgroundColor: cs.surfaceContainerHighest,
                ),
              ),
            ),
            const SizedBox(width: 12),
            Text('$answered / $total bewertet',
                style: TextStyle(fontSize: 12.5, color: cs.onSurface.withValues(alpha: .7))),
          ]),
        ),
        Divider(height: 1, color: cs.outline),
        LayoutBuilder(builder: (context, c) {
          final cols = c.maxWidth > 620 ? 6 : 3;
          final tileW = (c.maxWidth - (cols - 1)) / cols;
          return Wrap(
            spacing: 1,
            runSpacing: 1,
            children: [
              for (final s in RiskStyle.order)
                SizedBox(width: tileW, child: _tile(context, s, summary[s] ?? 0)),
            ],
          );
        }),
      ]),
    );
  }

  /// Kleiner Statuschip: Offline (Assets) oder Server (HTTP) inkl. Sync-Zustand.
  Widget _connectionChip(BuildContext context, AssessmentController ctrl) {
    final cs = Theme.of(context).colorScheme;
    Color dot;
    String txt;
    if (!ctrl.isRemote) {
      dot = cs.onSurface.withValues(alpha: .35);
      txt = 'Offline';
    } else if (ctrl.syncError != null) {
      dot = const Color(0xFFD1495B);
      txt = 'Server – Fehler';
    } else if (ctrl.syncing) {
      dot = const Color(0xFFE0A458);
      txt = 'Server – sync…';
    } else {
      dot = const Color(0xFF2E9E6B);
      txt = 'Server';
    }
    return Tooltip(
      message: ctrl.syncError ?? (ctrl.isRemote ? 'Katalog & Persistenz über die Engine-API' : 'Gebündelte Kataloge, lokale Auswertung'),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
        decoration: BoxDecoration(
            color: cs.surfaceContainerHighest, borderRadius: BorderRadius.circular(99)),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Container(width: 8, height: 8, decoration: BoxDecoration(color: dot, shape: BoxShape.circle)),
          const SizedBox(width: 6),
          Text(txt, style: TextStyle(fontSize: 11, color: cs.onSurface.withValues(alpha: .7))),
        ]),
      ),
    );
  }

  Widget _tile(BuildContext context, RiskStatus s, int n) {
    final cs = Theme.of(context).colorScheme;
    final rc = RiskStyle.color(context, s);
    final on = filter == s;
    return InkWell(
      onTap: () => setState(() => filter = on ? null : s),
      child: Container(
        decoration: BoxDecoration(
          color: on ? cs.surfaceContainerHighest : cs.surface,
          border: Border(top: BorderSide(color: rc, width: 3)),
        ),
        padding: const EdgeInsets.fromLTRB(13, 11, 13, 12),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
          Text('$n',
              style: TextStyle(fontFamily: 'monospace', fontSize: 25, fontWeight: FontWeight.w600, color: rc, height: 1)),
          const SizedBox(height: 3),
          Text(RiskStyle.label(s),
              style: TextStyle(fontSize: 11.5, color: cs.onSurface.withValues(alpha: .7)), maxLines: 1, overflow: TextOverflow.ellipsis),
        ]),
      ),
    );
  }

  Widget _categorySection(BuildContext context, AssessmentController ctrl, String cat,
      List<Hazard> hazards, Map<String, EvaluationResult> resByCode) {
    final cs = Theme.of(context).colorScheme;
    final vis = filter == null ? hazards : hazards.where((h) => resByCode[h.code]!.status == filter).toList();
    if (vis.isEmpty) return const SizedBox.shrink();
    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      decoration: BoxDecoration(
          color: cs.surface, border: Border.all(color: cs.outline), borderRadius: BorderRadius.circular(12)),
      clipBehavior: Clip.antiAlias,
      child: Theme(
        data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          initiallyExpanded: true,
          tilePadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
          backgroundColor: cs.surface,
          collapsedBackgroundColor: cs.surface,
          title: Text(cat, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
          trailing: Text('${vis.length} Prüfpunkt${vis.length > 1 ? 'e' : ''}',
              style: TextStyle(fontSize: 11.5, color: cs.onSurface.withValues(alpha: .5))),
          childrenPadding: EdgeInsets.zero,
          children: [for (final h in vis) _hazardRow(context, ctrl, h, resByCode[h.code]!)],
        ),
      ),
    );
  }

  Widget _hazardRow(BuildContext context, AssessmentController ctrl, Hazard h, EvaluationResult res) {
    final cs = Theme.of(context).colorScheme;
    final rc = RiskStyle.color(context, res.status);
    final qc = h.questions.isNotEmpty ? h.questions.first.question : null;
    final opts = qc != null ? (ctrl.catalog.questionByCode(qc)?.options ?? const <OptionDef>[]) : const <OptionDef>[];
    final sel = ctrl.selectedHazard == h.code;
    return InkWell(
      onTap: () async {
        ctrl.selectHazard(h.code);
        if (MediaQuery.of(context).size.width < 900) {
          await Navigator.of(context).push(MaterialPageRoute(
            builder: (_) => Scaffold(
              appBar: AppBar(title: Text(h.code)),
              body: AnimatedBuilder(
                animation: ctrl,
                builder: (_, __) => SingleChildScrollView(
                    padding: const EdgeInsets.all(16), child: DetailPanel(ctrl: ctrl, hazardCode: h.code)),
              ),
            ),
          ));
        }
      },
      child: Container(
        decoration: BoxDecoration(
          color: sel ? cs.primary.withValues(alpha: .08) : null,
          border: Border(
            top: BorderSide(color: cs.outline),
            left: BorderSide(color: sel ? cs.primary : rc, width: 3),
          ),
        ),
        padding: const EdgeInsets.fromLTRB(13, 12, 14, 12),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Padding(
              padding: const EdgeInsets.only(top: 1, right: 10),
              child: Text(h.code,
                  style: TextStyle(fontFamily: 'monospace', fontSize: 11.5, color: cs.onSurface.withValues(alpha: .5))),
            ),
            Expanded(child: Text(h.title, style: const TextStyle(fontSize: 13.5, height: 1.4))),
          ]),
          const SizedBox(height: 9),
          Row(children: [
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                decoration: BoxDecoration(
                    color: cs.surface, border: Border.all(color: cs.outline), borderRadius: BorderRadius.circular(7)),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String?>(
                    isExpanded: true,
                    isDense: true,
                    value: qc != null ? ctrl.answers[qc] as String? : null,
                    hint: const Text('— nicht bewertet —', style: TextStyle(fontSize: 13)),
                    items: [
                      const DropdownMenuItem<String?>(value: null, child: Text('— nicht bewertet —', style: TextStyle(fontSize: 13))),
                      for (final o in opts)
                        DropdownMenuItem<String?>(
                            value: o.value,
                            child: Text(o.label, style: const TextStyle(fontSize: 13), overflow: TextOverflow.ellipsis)),
                    ],
                    onChanged: qc == null ? null : (v) => ctrl.setAnswer(qc, v),
                  ),
                ),
              ),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 4),
              decoration: BoxDecoration(color: RiskStyle.bg(context, res.status), borderRadius: BorderRadius.circular(99)),
              child: Text(RiskStyle.label(res.status),
                  style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: rc)),
            ),
          ]),
        ]),
      ),
    );
  }
}
