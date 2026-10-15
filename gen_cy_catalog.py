# -*- coding: utf-8 -*-
"""Erzeugt den mehrfragigen Cyber-Typ „Cyber-GBU komponentenbasiert" (CY) als
Engine-Seed.

    python3 gen_cy_catalog.py   -> norm_cyber_mf.json + cy_klaerung.json

Inhalt liegt in cy_content/ (DSL in common.py, die die Register von
mf_content/common.py auf den Cyber-Typ umstellt). Fünf Erhebungsbereiche:
A Anlagenmerkmale, Z Zugang, C Komponenten, N Netz, O Organisation.

Alle Fragen und Gefährdungen tragen domain = CYBER. Alle Regeln origin=OWN_RULE
und quality_status=REVIEW_REQUIRED, bis die zugehörigen Klärungen in
cy_content/entscheidungen.py entschieden sind. Die Prüf- und Validierungslogik
ist identisch mit gen_ft_catalog.py (check(), validate_schema()).
"""
import json, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from cy_content import common as C  # noqa: E402  (stellt die Register um)

for mod in ['anlage', 'zugang', 'netz', 'komponenten', 'organisation']:
    importlib.import_module('cy_content.' + mod)

import catalog_check as FT  # noqa: E402  (check/validate ohne Nebenwirkungen)

RULE_VERSION = 'cyber-mf-2026.9'  # .9: Schnittstellen je Komponente als Mehrfachauswahl;
                                  #     „Härtung" heißt überall Funktionsreduzierung (16.10.2026)
# .8: Bereich Z auf den physischen Zugang gekürzt, Netzfragen im Bereich N (16.10.2026)
# .7: Bereich O gekürzt, ZÜS-Abschlusscheck entfallen (13.10.2026)
# .6: Maßnahme zur Gefährdung, nicht Schutzkonzept der Anlage (13.10.2026)
# .2 = nach Gegenlesung 03.09.2026, 2026.1 = Entwurf davor

# Der ZÜS-Abschlusscheck (Zuordnung der 14 Prüfpunkte aus EK-ZÜS B-002 rev. 5
# Anhang 2 zu Fragen und Gefährdungen) ist am 13.10.2026 entfallen – mit ihm
# cy_zues_map.json und der gleichnamige Berichtsabschnitt. Grund: die beiden
# Muster eines TÜV-Prüfers für eine plausible Dokumentation nach TRBS 1115-1
# kennen keinen solchen Abschnitt; sie enden mit zwei stehenden Zusagen und
# der Unterschrift des Betreibers (siehe cy_content/organisation.py).
def build():
    order = {c: i for i, c in enumerate(C.CATS.values())}
    questions = sorted(C.QUESTIONS, key=lambda q: (order[q['category']],
                                                   C.QUESTIONS.index(q)))
    hazards = list(C.HAZARDS)
    rules = list(C.RULES)
    measures = list(C.MEASURES.values())
    for q in questions:
        q['domain'] = 'CYBER'
    for h in hazards:
        h['domain'] = 'CYBER'
    # apply_decisions aus gen_ft_catalog liest ft_content.entscheidungen;
    # hier die Cyber-Entscheidungen einsetzen.
    from cy_content.entscheidungen import ENTSCHEIDUNGEN, DATUM
    decided = {k for k, v in ENTSCHEIDUNGEN.items() if v[0] != 'offen'}
    for r in rules:
        notes = r.get('notes', '')
        kids = notes.split('KLÄREN: ')[1].split(', ') if 'KLÄREN: ' in notes else []
        if kids and all(k in decided for k in kids):
            if r.get('evidence') == 'HYPOTHESIS':
                r['evidence'] = 'INFERRED'
            r['quality_status'] = 'VERIFIED'
            r['notes'] = notes.split('KLÄREN: ')[0].rstrip() + \
                (' ' if notes.split('KLÄREN: ')[0].strip() else '') + \
                'Entschieden %s: %s.' % (DATUM, ', '.join(kids))
    # Regelfreigabe (Eigenregeln ohne Klärungspunkt, Excel GBU_Cyber_Regelpruefung):
    # 'Freigeben' -> VERIFIED; 'Ändern'/'Streichen' bleiben REVIEW_REQUIRED mit
    # der Korrektur als Hinweis, bis der Inhalt nachgezogen ist.
    from cy_content.regelfreigabe import FREIGABE, DATUM as FREIGABE_DATUM
    for r in rules:
        fg = FREIGABE.get(r['code'])
        if not fg or r.get('quality_status') == 'VERIFIED':
            continue
        # Drittes Element (optional) ist das Datum dieser einzelnen Entscheidung;
        # ohne Angabe gilt DATUM der Datei. Eingeführt 20.09.2026, damit eine
        # Nachfreigabe die älteren Einträge nicht umdatiert.
        entscheidung, korrektur = fg[0], fg[1]
        datum = fg[2] if len(fg) > 2 and fg[2] else FREIGABE_DATUM
        sep = ' ' if r.get('notes', '').strip() else ''
        if entscheidung == 'Freigeben':
            r['quality_status'] = 'VERIFIED'
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'Freigegeben %s.' % datum
        else:
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'OFFEN (%s %s): %s' % (entscheidung, datum, korrektur or '-')
    seed = {'rule_version': RULE_VERSION, 'questions': questions,
            'measures': measures, 'hazards': hazards, 'rules': rules}
    # Erhebungskarten (Prüfbericht 20.09.2026, Befund R12): reine Darstellung,
    # die Bewertung bleibt unverändert.
    from cy_content import karten
    karten.anreichern(seed)
    return seed


def main():
    seed = build()
    errors, warnings = FT.check(seed)
    from cy_content import karten
    errors += karten.pruefen(seed)
    for w in warnings:
        print('WARNUNG', w)
    if errors:
        for e in errors:
            print('FEHLER', e)
        sys.exit(1)
    FT.validate_schema(seed)
    out = os.path.join(HERE, 'norm_cyber_mf.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(seed, f, ensure_ascii=False, indent=1)
    from cy_content.entscheidungen import ENTSCHEIDUNGEN, DATUM
    for kl in C.KLAERUNG:
        e = ENTSCHEIDUNGEN.get(kl['id'])
        if e and e[0] != 'offen':
            kl['entscheidung'], kl['festlegung'], kl['datum'] = e[0], e[1], DATUM
    offen = [kl['id'] for kl in C.KLAERUNG if not kl.get('entscheidung')]
    with open(os.path.join(HERE, 'cy_klaerung.json'), 'w', encoding='utf-8') as f:
        json.dump(C.KLAERUNG, f, ensure_ascii=False, indent=1)
    print('Klärungen offen:', len(offen), offen if len(offen) < 8 else '')
    from collections import Counter
    res = Counter(r['result'] for r in seed['rules'])
    ev = Counter(r['evidence'] for r in seed['rules'])
    types = Counter(q['type'] for q in seed['questions'])
    cats = Counter(q['category'] for q in seed['questions'])
    grp = Counter(h['category'] for h in seed['hazards'])
    print('%s: %d Fragen (%s), %d Gefährdungen, %d Regeln, %d Maßnahmen, %d Klärungen'
          % (os.path.basename(out), len(seed['questions']), dict(types),
             len(seed['hazards']), len(seed['rules']), len(seed['measures']),
             len(C.KLAERUNG)))
    print('Erhebungsbereiche:', dict(cats), '| Karten:', len(seed.get('question_groups', [])))
    print('Baugruppen:', dict(grp))
    print('Stufen:', dict(res), '| Evidenz:', dict(ev))
    print('Schema: gültig')


if __name__ == '__main__':
    main()
