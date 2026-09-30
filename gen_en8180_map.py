# -*- coding: utf-8 -*-
"""Erzeugt die EN-81-80-Sicht auf den mehrfragigen Katalog:
  python3 gen_en8180_map.py
Eingaben : en8180_content.py, norm_81_20_mf.json
Ausgaben : en8180_map.json                                   (Referenz/Engine)
           ../gbu_aufzug_app/lib/data/en8180_katalog.dart    (App, erzeugt)
           GBU_EN8180_Zuordnung.xlsx                         (Gegenlesung)

Prüft dabei, dass jede zugeordnete MF-Gefährdung im Katalog existiert, und
listet die Gefährdungssituationen ohne Entsprechung als Lücke auf.
"""
import json, os, sys
from en8180_content import (ZUORDNUNG, ZEITPLAN, GRUPPEN, AUSGABE, gruppe,
                            sortierschluessel, GEGENGELESEN,
                            GEGENGELESEN_HINWEIS)

HERE = os.path.dirname(os.path.abspath(__file__))
mf = json.load(open(os.path.join(HERE, 'norm_81_20_mf.json'), encoding='utf-8'))
H = {h['code']: h for h in mf['hazards']}

fehler = []
for nr, (alt2003, titel, prio, hazards, deckung, bem) in ZUORDNUNG.items():
    for c in hazards:
        if c not in H:
            fehler.append('Nr. %s: MF-Gefährdung %s unbekannt' % (nr, c))
    if deckung not in ('voll', 'teilweise', 'offen'):
        fehler.append('Nr. %s: unbekannte Deckung %r' % (nr, deckung))
    if deckung == 'offen' and hazards:
        fehler.append('Nr. %s: „offen" mit Zuordnung' % nr)
    if deckung != 'offen' and not hazards:
        fehler.append('Nr. %s: ohne Zuordnung, aber nicht „offen"' % nr)
    if prio not in ZEITPLAN:
        fehler.append('Nr. %s: unbekannte Prioritätsstufe %r' % (nr, prio))
    if nr.split('.')[0] not in GRUPPEN:
        fehler.append('Nr. %s: unbekannte Gruppe' % nr)
if fehler:
    print('\n'.join(fehler))
    sys.exit(1)

punkte = []
for nr in sorted(ZUORDNUNG, key=sortierschluessel):
    alt2003, titel, prio, hazards, deckung, bem = ZUORDNUNG[nr]
    punkte.append({
        'nr': nr,
        # Nummer der zurückgezogenen Ausgabe 2003, damit sich ältere Berichte
        # zuordnen lassen; leer bei den elf Punkten, die es dort nicht gab.
        'alt2003': '' if alt2003 is None else str(alt2003),
        'gruppe': gruppe(nr),
        'titel': titel,
        'prioritaet': prio,
        'zeitplan': ZEITPLAN[prio],
        'hazards': hazards,
        'deckung': deckung,
        'bemerkung': bem,
    })

daten = {
    'quelle': AUSGABE + ', Anhang A (normativ), Tabelle A.1, sowie '
              'Abschnitt 5.4 mit Tabelle 4 (Prioritäten und Zeitplan)',
    'katalog': mf['rule_version'],
    'gegengelesen': GEGENGELESEN,
    'gegengelesen_hinweis': GEGENGELESEN_HINWEIS,
    'punkte': punkte,
}
ziel = os.path.join(HERE, 'en8180_map.json')
json.dump(daten, open(ziel, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- Dart-Katalog (erzeugt) ------------------------------------------------
def dart_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'").replace('$', r'\$') + "'"


zeilen = [
    '// AUTOMATISCH ERZEUGT von engine_model/gen_en8180_map.py – nicht von Hand',
    '// ändern. Quelle: %s.' % daten['quelle'],
    '// Nummern, die Nummern der Ausgabe 2003 und die Prioritätsstufen stammen',
    '// aus der Norm; die Kurzbezeichnungen sind eigene Formulierungen',
    '// (kein Normtext).',
    '',
    "import 'en8180_map.dart';",
    '',
    '/// Die %d Punkte der Prüfliste (Anhang A) der DIN EN 81-80:2019-11 mit' % len(punkte),
    '/// ihrer Zuordnung zum mehrfragigen Katalog (%s).' % mf['rule_version'],
    "const String en8180Gegengelesen = '%s';" % GEGENGELESEN,
    '',
    'const List<En8180Punkt> en8180Punkte = [',
]
for p in punkte:
    zeilen.append('  En8180Punkt(')
    zeilen.append('    nr: %s,' % dart_str(p['nr']))
    zeilen.append('    alt2003: %s,' % dart_str(p['alt2003']))
    zeilen.append('    gruppe: %s,' % dart_str(p['gruppe']))
    zeilen.append('    titel: %s,' % dart_str(p['titel']))
    zeilen.append('    prioritaet: %s,' % dart_str(p['prioritaet']))
    zeilen.append('    zeitplan: %s,' % dart_str(p['zeitplan']))
    zeilen.append('    deckung: %s,' % dart_str(p['deckung']))
    if p['hazards']:
        zeilen.append('    hazards: [%s],' %
                      ', '.join(dart_str(c) for c in p['hazards']))
    if p['bemerkung']:
        zeilen.append('    bemerkung: %s,' % dart_str(p['bemerkung']))
    zeilen.append('  ),')
zeilen.append('];')
zeilen.append('')

dart_ziel = os.path.join(HERE, '..', 'gbu_aufzug_app', 'lib', 'data',
                         'en8180_katalog.dart')
if len(sys.argv) > 1:
    dart_ziel = sys.argv[1]
open(dart_ziel, 'w', encoding='utf-8').write('\n'.join(zeilen))

# ---- Excel zur Gegenlesung -------------------------------------------------
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter
except ImportError:
    Workbook = None

if Workbook is not None:
    FONT = 'Arial'
    HEAD = PatternFill('solid', fgColor='1F3A5F')
    INPUT = PatternFill('solid', fgColor='FFF2CC')
    LUECKE = PatternFill('solid', fgColor='FCE4E4')
    STRIPE = PatternFill('solid', fgColor='F3F5F8')
    thin = Side(style='thin', color='C9D1DB')
    BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
    WRAP = Alignment(wrap_text=True, vertical='top')
    wb = Workbook()
    ws = wb.active
    ws.title = 'Zuordnung'
    cols = ['Nr. 2019', 'Nr. 2003', 'Gruppe', 'Prüfpunkt (Kurzbezeichnung)',
            'Priorität', 'Zeitplan', 'MF-Gefährdung(en)',
            'Titel der MF-Gefährdung(en)', 'Deckung', 'Bemerkung',
            'Zuordnung OK?', 'Korrektur']
    widths = [9, 9, 30, 52, 10, 34, 20, 52, 11, 40, 12, 34]
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row=1, column=i, value=c)
        cell.font = Font(name=FONT, bold=True, color='FFFFFF', size=10)
        cell.fill = HEAD
        cell.alignment = Alignment(wrap_text=True, vertical='center')
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'A2'
    ws.row_dimensions[1].height = 30
    for r, p in enumerate(punkte, 2):
        werte = [p['nr'], p['alt2003'] or 'neu 2019', p['gruppe'], p['titel'],
                 p['prioritaet'] or 'nicht eingestuft', p['zeitplan'],
                 ', '.join(p['hazards']) or '-',
                 '\n'.join(H[c]['title'] for c in p['hazards']) or '-',
                 p['deckung'], p['bemerkung'], None, None]
        for c, v in enumerate(werte, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font = Font(name=FONT, size=10)
            cell.alignment = WRAP
            cell.border = BORDER
            if c in (11, 12):
                cell.fill = INPUT
            elif p['deckung'] != 'voll':
                cell.fill = LUECKE
            elif r % 2 == 0:
                cell.fill = STRIPE
    dv = DataValidation(type='list', formula1='"OK,Ändern"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add('K2:K%d' % (len(punkte) + 1))
    ws.auto_filter.ref = 'A1:L%d' % (len(punkte) + 1)

    ws2 = wb.create_sheet('Lesehinweise')
    ws2.column_dimensions['A'].width = 120
    luecken = [p for p in punkte if p['deckung'] == 'offen']
    teil = [p for p in punkte if p['deckung'] == 'teilweise']
    zeilen2 = [
        ('EN 81-80 als Sicht auf den mehrfragigen Katalog (%s)' % mf['rule_version'], True),
        ('Quelle: %s' % daten['quelle'], False),
        ('', False),
        ('Der eingefrorene GBU-Typ „vereinfacht (EN 81-80)" wird nicht durch einen zweiten '
         'Fragebogen ersetzt: Eine Bestandsanlage wird einmal nach EN 81-20 (mehrfragig) '
         'erhoben, der Bericht weist den Nachrüstbedarf nach EN 81-80 zusätzlich mit '
         'Nummer und Priorität der Norm aus.', False),
        ('', False),
        ('%d der %d Prüfpunkte sind vollständig abgedeckt, %d teilweise, '
         '%d gar nicht (Zeilen rot hinterlegt).'
         % (len(punkte) - len(luecken) - len(teil), len(punkte), len(teil),
            len(luecken)), False),
        ('Lücken im MF-Katalog: %s' % ', '.join(
            'Nr. %s %s' % (p['nr'], p['titel']) for p in luecken), False),
        ('Teilweise: %s' % ', '.join(
            'Nr. %s %s' % (p['nr'], p['titel']) for p in teil), False),
        ('', False),
        ('Die Prioritätsstufe steht seit der Ausgabe 2019 direkt in der Prüfliste; die '
         'frühere Herleitung über Risikoprofil (A.1) und Prioritätstabelle (A.2) entfällt. '
         'Fünf Punkte sind ohne Stufe: sie verweisen auf eine eigene Norm der Reihe EN 81 '
         '(81-72 Feuerwehraufzug, 81-73 Brandfall, 81-77 Erdbeben, 81-82 Barrierefreiheit, '
         'CEN/TS 81-83 Vandalismus).', False),
        ('', False),
        ('Spalte „Nr. 2003" ist die Nummer der zurückgezogenen Ausgabe 2004-02; „neu 2019" '
         'kennzeichnet die elf Punkte, die es dort nicht gab.', False),
        ('', False),
        ('Gelbe Spalten ausfüllen: „Zuordnung OK?" = OK/Ändern, Korrektur frei.', False),
        ('', False),
        ('Stand der Gegenlesung: %s – %s' % (GEGENGELESEN, GEGENGELESEN_HINWEIS), True),
    ]
    for i, (t, b) in enumerate(zeilen2, 1):
        cell = ws2.cell(row=i, column=1, value=t)
        cell.font = Font(name=FONT, bold=b, size=11 if b else 10)
        cell.alignment = WRAP
    wb.save(os.path.join(HERE, 'GBU_EN8180_Zuordnung.xlsx'))

from collections import Counter
print('geschrieben: en8180_map.json, %s, GBU_EN8180_Zuordnung.xlsx'
      % os.path.normpath(dart_ziel))
print('Punkte: %d | Deckung: %s | Priorität: %s'
      % (len(punkte), dict(Counter(p['deckung'] for p in punkte)),
         dict(Counter(p['prioritaet'] or 'nicht eingestuft' for p in punkte))))
print('abgedeckte MF-Gefährdungen: %d von %d'
      % (len({c for p in punkte for c in p['hazards']}), len(H)))
