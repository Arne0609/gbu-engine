# -*- coding: utf-8 -*-
"""Erzeugt den eigenständigen GBU-Typ „DIN EN 81-80 (Bestandsanlagen)" als
Teilmenge des mehrfragigen Katalogs:

  python3 gen_en8180_catalog.py

Eingaben : norm_81_20_mf.json (Regelversion 81-20-mf-*), en8180_content.py
Ausgabe  : norm_81_80_mf.json (Regelversion 81-80-mf-*)

Grundsatz (Festlegung Arne 04.09.2026): Der Typ ist inhaltlich deckungsgleich
mit der Variante nach EN 81-20 – nur der Umfang ist geringer. Deshalb wird er
NICHT eigenständig formuliert, sondern aus dem MF-Katalog abgeleitet:

  * Gefährdungen, Fragen, Regeln und Maßnahmen werden UNVERÄNDERT übernommen,
    mit denselben Codes. Eine Anlage kann damit ohne Datenverlust zwischen den
    beiden Typen wechseln, und die EN-81-80-Sicht (en8180_map.json) passt auf
    beide Kataloge.
  * Umfang = die Gefährdungen der 74 Gefährdungssituationen (aus
    en8180_content.ZUORDNUNG) plus die organisatorischen Gefährdungen, ohne
    die keine vollständige Gefährdungsbeurteilung nach BetrSichV entsteht
    (Unterlagen, Betreiberorganisation, Umfeld, Sonderfunktionen) – siehe
    ZUSATZ unten.
  * Mitgenommen werden außerdem alle Fragen, die für die enthaltenen
    Gefährdungen gebraucht werden: Anlagenmerkmale als Filter, Fragen aus
    Regeln und Pflichtbedingungen sowie die vollständige Kette der
    Sichtbarkeitsregeln.
"""
import json, os, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from en8180_content import ZUORDNUNG  # noqa: E402
import catalog_check  # noqa: E402

RULE_VERSION = '81-80-mf-2026.1'

# Gefährdungen ausserhalb der 74 Gefährdungssituationen, die der Typ trotzdem
# führt: ohne sie waere die Beurteilung nach BetrSichV unvollstaendig.
ZUSATZ = [
    'MF-D01',   # Notfallplan
    'MF-D03',   # Wartungsunterlagen / Instandhaltung
    'MF-D04',   # Prüfplakette / Prüffrist ZÜS
    'MF-D05',   # Betreiberorganisation (beauftragte Person, Unterweisung)
    'MF-SF01',  # Feuerwehraufzug / gebäudeseitige Sonderfunktionen
    'MF-U02', 'MF-U03', 'MF-U04', 'MF-U05', 'MF-U06', 'MF-U07', 'MF-U08',
    'MF-U10', 'MF-U11', 'MF-U12', 'MF-U13', 'MF-U14', 'MF-U15',
]


def collect(expr, into):
    if not expr:
        return
    if 'all' in expr:
        for e in expr['all']:
            collect(e, into)
    elif 'any' in expr:
        for e in expr['any']:
            collect(e, into)
    elif 'not' in expr:
        collect(expr['not'], into)
    else:
        into.add(expr['question'])


def build():
    mf = json.load(open(os.path.join(HERE, 'norm_81_20_mf.json'), encoding='utf-8'))
    H = {h['code']: h for h in mf['hazards']}
    Q = {q['code']: q for q in mf['questions']}
    M = {m['code']: m for m in mf['measures']}

    kern = OrderedDict()
    for nr in sorted(ZUORDNUNG):
        for c in ZUORDNUNG[nr][2]:
            kern[c] = True
    fehlend = [c for c in list(kern) + ZUSATZ if c not in H]
    if fehlend:
        sys.exit('unbekannte Gefährdungen: %s' % ', '.join(fehlend))
    behalten = set(kern) | set(ZUSATZ)

    # Reihenfolge des MF-Katalogs beibehalten (Bericht und UI-Gruppierung).
    hazards = [h for h in mf['hazards'] if h['code'] in behalten]
    rules = [r for r in mf['rules'] if r['hazard'] in behalten]

    # Fragen: aus Gefährdungen, Regeln, Pflicht-/Filterbedingungen …
    fragen = set()
    for h in hazards:
        for hq in h.get('questions', []):
            fragen.add(hq['question'])
            for key in ('required_when', 'applicable_when'):
                collect(hq.get(key), fragen)
    for r in rules:
        collect(r['condition'], fragen)
        collect(r.get('applicability'), fragen)
    # … und die vollständige Kette der Sichtbarkeitsregeln.
    todo = list(fragen)
    while todo:
        c = todo.pop()
        neu = set()
        collect(Q.get(c, {}).get('visible_when'), neu)
        for n in neu - fragen:
            fragen.add(n)
            todo.append(n)
    fehlend = sorted(c for c in fragen if c not in Q)
    if fehlend:
        sys.exit('unbekannte Fragen: %s' % ', '.join(fehlend))
    questions = [q for q in mf['questions'] if q['code'] in fragen]

    massnahmen = OrderedDict()
    for r in rules:
        for mb in r.get('measures', []):
            code = mb['measure']
            if code in M:
                massnahmen[code] = M[code]
    measures = list(massnahmen.values())

    return {'rule_version': RULE_VERSION, 'questions': questions,
            'measures': measures, 'hazards': hazards, 'rules': rules}, mf


def main():
    seed, mf = build()
    errors, warnings = catalog_check.check(seed)
    for w in warnings:
        print('WARNUNG', w)
    if errors:
        print('\n'.join('FEHLER ' + e for e in errors))
        sys.exit(1)
    catalog_check.validate_schema(seed)

    # Deckungsgleichheit mit dem MF-Katalog: identische Objekte, nur weniger.
    H = {h['code']: h for h in mf['hazards']}
    Q = {q['code']: q for q in mf['questions']}
    R = {r['code']: r for r in mf['rules']}
    for h in seed['hazards']:
        assert h == H[h['code']], 'Gefährdung weicht ab: ' + h['code']
    for q in seed['questions']:
        assert q == Q[q['code']], 'Frage weicht ab: ' + q['code']
    for r in seed['rules']:
        assert r == R[r['code']], 'Regel weicht ab: ' + r['code']

    ziel = os.path.join(HERE, 'norm_81_80_mf.json')
    json.dump(seed, open(ziel, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    from collections import Counter
    kat = Counter(q['category'] for q in seed['questions'])
    print('%s: %s aus %s' % (os.path.basename(ziel), RULE_VERSION, mf['rule_version']))
    print('  %d Fragen (MF: %d), %d Gefährdungen (MF: %d), %d Regeln, %d Maßnahmen'
          % (len(seed['questions']), len(mf['questions']), len(seed['hazards']),
             len(mf['hazards']), len(seed['rules']), len(seed['measures'])))
    print('  Erhebungsbereiche:', dict(kat))
    print('  Stufen:', dict(Counter(r['result'] for r in seed['rules'])))
    print('  Schema: gültig; Inhalte identisch mit dem MF-Katalog')


if __name__ == '__main__':
    main()
