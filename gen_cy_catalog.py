# -*- coding: utf-8 -*-
"""Erzeugt den mehrfragigen Cyber-Typ „Cyber-GBU komponentenbasiert" (CY) als
Engine-Seed.

    python3 gen_cy_catalog.py   -> norm_cyber_mf.json + cy_klaerung.json + cy_zues_map.json

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

RULE_VERSION = 'cyber-mf-2026.2'  # 2026.1 = Entwurf vor Gegenlesung 03.09.2026

# Zuordnung der 14 ZÜS-Prüfpunkte (EK-ZÜS B-002 rev. 5 Anhang 2) zu Fragen und
# Gefährdungen dieses Katalogs – Grundlage für den Berichtsabschnitt
# „ZÜS-Abschlusscheck". 'dokumentiert' = Dokumentationsfrage (K-C20),
# 'abgeleitet' = aus den Komponentenbewertungen.
ZUES_MAP = [
    {'nr': 1, 'frage': 'Wurden Cyberbedrohungen gemäß TRBS 1115 Teil 1 bei der Gefährdungsbeurteilung berücksichtigt?',
     'erfuellung': 'dokumentiert', 'fragen': ['qo_zues_beruecksichtigt'], 'hazards': ['CY-O05'],
     'hinweis': 'Dokumentationsfrage 5.11 (K-C20).'},
    {'nr': 2, 'frage': 'Sind die sicherheitsrelevanten MSR-Einrichtungen und weitere schutzbedürftige Einrichtungen erfasst und dokumentiert?',
     'erfuellung': 'dokumentiert', 'fragen': ['qo_zues_erfasst'],
     'hazards': ['CY-O05', 'CY-C01', 'CY-C02', 'CY-C03', 'CY-C04', 'CY-C05', 'CY-C06', 'CY-C07', 'CY-C08', 'CY-C09', 'CY-C10'],
     'hinweis': 'Dokumentationsfrage 5.12 (K-C20); Komponentenliste = Erhebungsbereich C.'},
    {'nr': 3, 'frage': 'Wurde berücksichtigt, dass bei überwachungsbedürftigen Anlagen gemäß ÜAnlG stets von einem erheblichen Risiko auszugehen ist?',
     'erfuellung': 'dokumentiert', 'fragen': ['qa_ueberwachungsbeduerftig', 'qo_zues_erhebliches_risiko'], 'hazards': ['CY-O05'],
     'hinweis': 'Dokumentationsfrage 5.13 (K-C20); Stufe Hoch ist im Cyber-Teil erreichbar (K-C01).'},
    {'nr': 4, 'frage': 'Erfolgte die Festlegung der Maßnahmen durch fachkundige Personen (TRBS 1115-1 3.3.2)?',
     'fragen': ['qo_fachkunde'], 'hazards': ['CY-O01']},
    {'nr': 5, 'frage': 'Wurde der Stand der Technik herangezogen?',
     'erfuellung': 'dokumentiert', 'fragen': ['qo_zues_stand_technik', 'qn_softwarestand', 'qa_hersteller_vorgaben'],
     'hazards': ['CY-O05', 'CY-N01', 'CY-O02'], 'hinweis': 'Dokumentationsfrage 5.14 (K-C20).'},
    {'nr': 6, 'frage': 'Wurden Maßnahmen mit den Mindestinhalten nach TRBS 1115-1 4.5.2 im erforderlichen Umfang festgelegt?',
     'erfuellung': 'abgeleitet', 'hinweis': 'Erfüllt, wenn alle Komponenten-Gefährdungen Kein Risiko/Niedrig ergeben (Maßnahmenstand „umgesetzt").',
     'hazards': ['CY-C01', 'CY-C02', 'CY-C03', 'CY-C04', 'CY-C05', 'CY-C06', 'CY-C07', 'CY-C08', 'CY-C09', 'CY-C10', 'CY-C11', 'CY-C12', 'CY-C13', 'CY-C14']},
    {'nr': 7, 'frage': 'Gibt es Vorgaben von Herstellern und wurden diese berücksichtigt?',
     'fragen': ['qa_hersteller_vorgaben'], 'hazards': ['CY-O02']},
    {'nr': 8, 'frage': 'Sind Art, Umfang und Fristen der Überprüfungen und Kontrollen der Maßnahmen schriftlich festgelegt?',
     'fragen': ['qo_pruefung_fristen'], 'hazards': ['CY-O05']},
    {'nr': 9, 'frage': 'Wird sichergestellt, dass CS-Maßnahmen die Sicherheitsmaßnahmen nicht negativ beeinflussen (Rückwirkungsfreiheit)?',
     'fragen': ['qo_rueckwirkung', 'qc_geb_rueckwirkungsfrei'], 'hazards': ['CY-O07', 'CY-C14']},
    {'nr': 10, 'frage': 'Werden neue Erkenntnisse zur Cybersicherheit in die Gefährdungsbeurteilung eingebunden?',
     'fragen': ['qo_erkenntnisse', 'qn_softwarestand'], 'hazards': ['CY-O08', 'CY-N01']},
    {'nr': 11, 'frage': 'Sind Unterweisungen von Beschäftigten zur Cybersicherheit durchgeführt?',
     'fragen': ['qo_unterweisung'], 'hazards': ['CY-O04']},
    {'nr': 12, 'frage': 'Liegt für die CS-Maßnahmen ein Nachweis der Wirksamkeit (TRBS 1115-1 Abschn. 5) vor?',
     'fragen': ['qo_wirksamkeit'], 'hazards': ['CY-O05']},
    {'nr': 13, 'frage': 'Liegt für die CS-Maßnahmen eine Bestätigung der Funktionsfähigkeit (TRBS 1115-1 Abschn. 8.2) vor?',
     'fragen': ['qo_funktion'], 'hazards': ['CY-O05']},
    {'nr': 14, 'frage': 'Wurden nach Aussage des Betreibers prüfpflichtige Änderungen mit Einfluss auf die Cybersicherheit durchgeführt?',
     'fragen': ['qo_aenderungen', 'qo_aenderungen_geprueft'], 'hazards': ['CY-O06']},
]


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
        entscheidung, korrektur = fg
        sep = ' ' if r.get('notes', '').strip() else ''
        if entscheidung == 'Freigeben':
            r['quality_status'] = 'VERIFIED'
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'Freigegeben %s.' % FREIGABE_DATUM
        else:
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'OFFEN (%s %s): %s' % (entscheidung, FREIGABE_DATUM, korrektur or '-')
    return {'rule_version': RULE_VERSION, 'questions': questions,
            'measures': measures, 'hazards': hazards, 'rules': rules}


def check_zues_map(seed):
    qs = {q['code'] for q in seed['questions']}
    hs = {h['code'] for h in seed['hazards']}
    errors = []
    for z in ZUES_MAP:
        for q in z.get('fragen', []):
            if q not in qs: errors.append('ZÜS Nr. %d: Frage %s unbekannt' % (z['nr'], q))
        for h in z.get('hazards', []):
            if h not in hs: errors.append('ZÜS Nr. %d: Gefährdung %s unbekannt' % (z['nr'], h))
    return errors


def main():
    seed = build()
    errors, warnings = FT.check(seed)
    errors += check_zues_map(seed)
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
    with open(os.path.join(HERE, 'cy_zues_map.json'), 'w', encoding='utf-8') as f:
        json.dump({'quelle': 'EK-ZÜS B-002 rev. 5, Anhang 2', 'rule_version': RULE_VERSION,
                   'punkte': ZUES_MAP}, f, ensure_ascii=False, indent=1)
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
    print('Erhebungsbereiche:', dict(cats))
    print('Baugruppen:', dict(grp))
    print('Stufen:', dict(res), '| Evidenz:', dict(ev))
    print('Schema: gültig')


if __name__ == '__main__':
    main()
