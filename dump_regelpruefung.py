# -*- coding: utf-8 -*-
"""Regeln zur Freigabe als lesbare Textdateien je Prüfpaket.

    python3 dump_regelpruefung.py [ZIELORDNER]

Erzeugt je Paket eine Datei mit ALLEN Regeln der betroffenen Gefährdungen –
auch den bereits freigegebenen –, weil eine Regel nur im Zusammenspiel mit
ihren Geschwistern (Priorität, Aggregation, Kompensation) beurteilbar ist.
Zu prüfen sind die mit „>>> ZU PRÜFEN" markierten.
"""
import json
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ZIEL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'pruefpakete')
os.makedirs(ZIEL, exist_ok=True)

seed = json.load(open(os.path.join(HERE, 'norm_81_20_mf.json'), encoding='utf-8'))
Q = {q['code']: q for q in seed['questions']}
M = {m['code']: m for m in seed['measures']}
H = OrderedDict((h['code'], h) for h in seed['hazards'])

LAB = {'HIGH': 'Hoch', 'MEDIUM': 'Mittel', 'LOW': 'Niedrig', 'NO_RISK': 'Kein Risiko'}
ROLLE = {'TRIGGER': 'Befund', 'APPLICABILITY': 'Anwendbarkeit', 'COMPENSATION': 'Kompensation',
         'MODIFIER': 'Modifikator', 'DOCUMENTATION': 'Dokumentation', 'OPTIONAL': 'optional'}
OPS = {'EQ': '=', 'NEQ': '≠', 'GT': '>', 'GTE': '≥', 'LT': '<', 'LTE': '≤',
       'IN': 'ist eines von', 'NOT_IN': 'ist keines von'}
AGG = {'NONE': 'NONE (Vorrang: höchste Priorität gewinnt – so wirken Kompensationen)',
       'MAXIMUM': 'MAXIMUM (höchste Stufe aller zutreffenden Regeln)',
       'ANY': 'ANY (Ortsmatrix: jede zutreffende Regel ist ein Befund, höchste Stufe zählt)'}


def wert(qc, v):
    q = Q.get(qc)
    if q and q.get('options'):
        for o in q['options']:
            if o['value'] == v:
                return '„%s"' % o['label']
    return {True: 'Ja', False: 'Nein'}.get(v, str(v))


def nr(qc):
    q = Q.get(qc)
    return (q.get('ui_number') or qc) if q else qc


def ausdruck(e, tiefe=0):
    if not e:
        return '–'
    if 'all' in e:
        t = [ausdruck(x, tiefe + 1) for x in e['all']]
        return ' UND '.join(t) if tiefe == 0 else '(' + ' UND '.join(t) + ')'
    if 'any' in e:
        t = [ausdruck(x, tiefe + 1) for x in e['any']]
        return ' ODER '.join(t) if tiefe == 0 else '(' + ' ODER '.join(t) + ')'
    if 'not' in e:
        return 'NICHT ' + ausdruck(e['not'], tiefe + 1)
    qc, op, v = e.get('question'), e.get('operator'), e.get('value')
    if op == 'ANSWERED':
        return '[%s] ist beantwortet' % nr(qc)
    if op == 'NOT_ANSWERED':
        return '[%s] ist unbeantwortet' % nr(qc)
    if isinstance(v, list):
        return '[%s] %s %s' % (nr(qc), OPS.get(op, op), ' / '.join(wert(qc, x) for x in v))
    return '[%s] %s %s' % (nr(qc), OPS.get(op, op), wert(qc, v))


def massnahmen(r, gruppe):
    out = []
    for mb in r.get('measures', []):
        if (mb.get('group_id') == 'sofort') != (gruppe == 'sofort'):
            continue
        m = M.get(mb['measure'])
        if m:
            out.append('%s [%s]' % (m.get('title', ''), m.get('type', '?')[:4]))
    return '; '.join(out) or '–'


def frageblock(h):
    zeilen = []
    for x in h.get('questions', []):
        q = Q.get(x['question'])
        if not q:
            continue
        z = '    %-7s %-28s %-14s %s' % (nr(x['question']), x['question'],
                                         ROLLE.get(x['role'], x['role']),
                                         x.get('required_mode', 'NEVER'))
        zeilen.append(z)
        zeilen.append('            Text: %s' % q['text'])
        if q.get('options'):
            zeilen.append('            Optionen: %s'
                          % ' | '.join('%s=„%s"' % (o['value'], o['label']) for o in q['options']))
        if q.get('visible_when'):
            zeilen.append('            sichtbar wenn: %s' % ausdruck(q['visible_when']))
        if x.get('required_when'):
            zeilen.append('            Pflicht wenn: %s' % ausdruck(x['required_when']))
        if x.get('applicable_when'):
            zeilen.append('            anwendbar wenn: %s' % ausdruck(x['applicable_when']))
        if q.get('help_text'):
            zeilen.append('            Hilfe: %s' % q['help_text'])
    return zeilen


def hazardblock(hcode, offen):
    h = H[hcode]
    regeln = [r for r in seed['rules'] if r['hazard'] == hcode]
    t = []
    t.append('=' * 100)
    t.append('GEFÄHRDUNG %s – %s' % (hcode, h['title']))
    t.append('  Erhebungsbereich: %s | Baugruppe: %s' % (h.get('ui_group', ''), h.get('category', '')))
    t.append('  Aggregation: %s' % AGG.get(h.get('aggregation_type'), h.get('aggregation_type')))
    t.append('  Gefährdungsfaktor: %s' % h.get('hazard_factor', '–'))
    t.append('  Betroffene: %s' % ', '.join(h.get('person_groups', [])) or '–')
    t.append('  Quellen: %s' % '; '.join(('%s %s' % (s.get('document', ''), s.get('section', ''))).strip()
                                         for s in h.get('sources', [])) or '–')
    if h.get('description'):
        t.append('  Beschreibung: %s' % h['description'])
    t.append('  Fragen:')
    t.extend(frageblock(h))
    t.append('  Regeln (nach Priorität absteigend – bei NONE gewinnt die erste zutreffende):')
    for r in sorted(regeln, key=lambda x: -x['priority']):
        mark = '>>> ZU PRÜFEN' if r['code'] in offen else '    freigegeben'
        t.append('')
        t.append('  %s  %s  P%-4d  -> %s' % (mark, r['code'], r['priority'], LAB.get(r['result'], r['result'])))
        t.append('      WENN:        %s' % ausdruck(r.get('condition')))
        if r.get('applicability'):
            t.append('      NUR WENN:    %s' % ausdruck(r['applicability']))
        t.append('      Sofort:      %s' % massnahmen(r, 'sofort'))
        t.append('      Mittelfrist: %s' % massnahmen(r, 'mittel'))
        t.append('      Evidenz: %s | Herkunft: %s' % (r.get('evidence', '?'), r.get('origin', '?')))
        if r.get('notes'):
            t.append('      Hinweis: %s' % r['notes'])
    return t


def main():
    offen = {r['code'] for r in seed['rules'] if r.get('quality_status') == 'REVIEW_REQUIRED'}
    # Auffangregeln (P1, Kein Risiko, Bedingung „… ist beantwortet") bilden ein
    # eigenes Paket: sie sind maschinell erzeugt und gleichförmig.
    auffang = {r['code'] for r in seed['rules']
               if r['code'] in offen and r['result'] == 'NO_RISK' and r['priority'] == 1
               and isinstance(r.get('condition'), dict)
               and r['condition'].get('operator') == 'ANSWERED'}
    rest = offen - auffang

    pakete = OrderedDict([
        ('D', ['MF-D01', 'MF-D02', 'MF-D03', 'MF-D04', 'MF-D05', 'MF-D06', 'MF-SF01']),
        ('F', ['MF-F0%d' % i for i in range(1, 10)]),
        ('G', ['MF-G0%d' % i for i in range(1, 9)]),
        ('K1', ['MF-K0%d' % i for i in range(1, 8)]),
        ('K2', ['MF-K08', 'MF-K09', 'MF-K10', 'MF-K11', 'MF-K12', 'MF-K13', 'MF-K14', 'MF-K15']),
        ('M1', ['MF-M0%d' % i for i in range(1, 8)]),
        ('M2', ['MF-M08', 'MF-M09', 'MF-M10', 'MF-M11', 'MF-M12', 'MF-M13', 'MF-M14']),
        ('M3', ['MF-M15', 'MF-M16', 'MF-M17', 'MF-M18', 'MF-M19', 'MF-M20', 'MF-M21']),
        ('S', ['MF-S0%d' % i for i in range(1, 8)]),
        ('T', ['MF-T0%d' % i for i in range(1, 10)]),
        ('U1', ['MF-U0%d' % i for i in range(1, 9)]),
        ('U2', ['MF-U09', 'MF-U10', 'MF-U11', 'MF-U12', 'MF-U13', 'MF-U14', 'MF-U15']),
        ('Z', ['MF-Z0%d' % i for i in range(1, 10)]),
    ])
    gesehen = set()
    uebersicht = []
    for name, codes in pakete.items():
        codes = [c for c in codes if c in H]
        zu = [c for c in rest if any(r['hazard'] == c for r in seed['rules'] if r['code'] == c) ]
        text = []
        anzahl = 0
        for hc in codes:
            hregeln = {r['code'] for r in seed['rules'] if r['hazard'] == hc}
            zu_pruefen = hregeln & rest
            if not zu_pruefen:
                continue
            gesehen |= zu_pruefen
            anzahl += len(zu_pruefen)
            text.extend(hazardblock(hc, zu_pruefen))
            text.append('')
        pfad = os.path.join(ZIEL, 'paket_%s.txt' % name)
        open(pfad, 'w', encoding='utf-8').write('\n'.join(text))
        uebersicht.append((name, anzahl, os.path.basename(pfad)))

    # Auffangregeln: kompakte Tabelle statt vollem Block – sie sind maschinell
    # erzeugt und gleichförmig; geprüft wird die Ankerfrage, nicht der Wortlaut.
    text = [
        'AUFFANGREGELN „Kein Risiko" (Priorität 1, Bedingung „Ankerfrage ist beantwortet").',
        '',
        'Mechanik: Die Regel greift nur, wenn KEINE Mangelregel der Gefährdung zutrifft und',
        'alle Pflichtfragen beantwortet sind (die Engine setzt sonst INCOMPLETE). Die',
        'Ankerfrage stellt nur sicher, dass überhaupt erhoben wurde. Erzeugt werden sie in',
        'mf_content/common.py (_catch_all): Anker ist die erste TRIGGER-Frage mit',
        'required_mode ALWAYS, sonst die erste Frage, die nicht APPLICABILITY ist.',
        '',
        'Zu prüfen je Zeile:',
        '  1. Ist der Anker eine Pflicht-Befundfrage (Rolle Befund, Pflicht ALWAYS)? Ist er',
        '     nur CONDITIONAL oder gar Modifikator/Dokumentation, kann die Gefährdung bei',
        '     unsichtbarem Anker NIE auf „Kein Risiko" kommen (bleibt unvollständig) oder',
        '     – umgekehrt – zu früh grün werden.',
        '  2. Ist der Anker sichtbarkeitsbeschränkt (Spalte „Anker sichtbar wenn")? Dann',
        '     gilt dasselbe Risiko.',
        '  3. Gibt es in derselben Gefährdung eine fachliche Kein-Risiko-Regel mit höherer',
        '     Priorität? Dann ist die Auffangregel nur Rückfall – das ist in Ordnung.',
        '',
        'Spalten: Regel | Gefährdung | Aggregation | Anker (Nr., Code) | Rolle | Pflicht |',
        '         Anker sichtbar wenn | weitere Kein-Risiko-Regeln | Anzahl Mangelregeln',
        '',
    ]
    for hc in H:
        h = H[hc]
        hregeln = [r for r in seed['rules'] if r['hazard'] == hc]
        zu = [r for r in hregeln if r['code'] in auffang]
        if not zu:
            continue
        rollen = {x['question']: x for x in h.get('questions', [])}
        for r in zu:
            gesehen.add(r['code'])
            ank = r['condition']['question']
            x = rollen.get(ank, {})
            q = Q.get(ank, {})
            andere_kr = [o['code'] for o in hregeln
                         if o['result'] == 'NO_RISK' and o['code'] != r['code']]
            mangel = [o['code'] for o in hregeln if o['result'] != 'NO_RISK']
            text.append('%-12s %-9s %-8s %-7s %-28s %-14s %-12s %-40s %s | %d Mangelregeln'
                        % (r['code'], hc, h.get('aggregation_type', ''), nr(ank), ank,
                           ROLLE.get(x.get('role'), x.get('role', '?')),
                           x.get('required_mode', '?'),
                           (ausdruck(q.get('visible_when'))[:38] if q.get('visible_when') else 'immer'),
                           ('auch ' + ', '.join(andere_kr)) if andere_kr else 'keine weitere',
                           len(mangel)))
            text.append('             Frage: %s' % q.get('text', '?'))
            text.append('             Alle Fragen der Gefährdung: %s'
                        % ', '.join('%s/%s/%s' % (nr(y['question']),
                                                  ROLLE.get(y['role'], y['role']),
                                                  y.get('required_mode', 'NEVER'))
                                    for y in h.get('questions', [])))
            text.append('')
    pfad = os.path.join(ZIEL, 'paket_AUFFANG.txt')
    open(pfad, 'w', encoding='utf-8').write('\n'.join(text))
    uebersicht.append(('AUFFANG', len(auffang), os.path.basename(pfad)))

    fehlend = offen - gesehen
    for name, n, datei in uebersicht:
        print('%-8s %3d Regeln  %s' % (name, n, datei))
    print('Summe: %d von %d offenen Regeln; nicht zugeordnet: %s'
          % (sum(n for _, n, _ in uebersicht), len(offen), sorted(fehlend) or 'keine'))


if __name__ == '__main__':
    main()
