# -*- coding: utf-8 -*-
"""Regelprüfung der neuen MF-Regeln aus den EN-81-20-Lückenschlüssen
(Stand 04.09.2026): legt die Regeln der fünf am 04.09.2026 ergänzten
Gefährdungen zur fachlichen Freigabe vor.

    python3 gen_mf_regelpruefung_xlsx.py            # nur die fünf neuen
    python3 gen_mf_regelpruefung_xlsx.py --alle     # alle REVIEW_REQUIRED

Eingabe: norm_81_20_mf.json  ->  GBU_MF_Regelpruefung.xlsx

Blätter: Lesehinweise · Regeln (je Regel eine Zeile, Entscheidung als
Auswahl) · Fragen (die zugehörigen Fragen mit Antwortoptionen, damit die
Bedingungen ohne Blick in den Katalog nachvollziehbar sind).
"""
import json, os, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
seed = json.load(open(os.path.join(HERE, 'norm_81_20_mf.json'), encoding='utf-8'))
OUT = os.path.join(HERE, 'GBU_MF_Regelpruefung.xlsx')

# Die Gefährdungen, die am 04.09.2026 ergänzt wurden:
#   MF-T07…MF-M21  aus dem Abgleich mit DIN EN 81-20 (Lücken, die beim
#                  EN-81-80-Abgleich aufgefallen sind)
#   MF-D06         aus der Analyse der Schindler-Anwendung GBU 3.0 – Baujahr
#                  als Steuerfeld, hier für die Konformitätsprüfung
NEUE_HAZARDS = ['MF-T07', 'MF-T08', 'MF-T09', 'MF-K15', 'MF-M21',
                'MF-D06']
ALLE = '--alle' in sys.argv[1:]

Q = {q['code']: q for q in seed['questions']}
H = {h['code']: h for h in seed['hazards']}
M = {m['code']: m for m in seed['measures']}
LAB = {'HIGH': 'Hoch', 'MEDIUM': 'Mittel', 'LOW': 'Niedrig',
       'NO_RISK': 'Kein Risiko', 'NOT_APPLICABLE': 'Nicht anwendbar'}
EVID = {'HIGH_CONFIDENCE': 'hohe Sicherheit', 'INFERRED': 'abgeleitet',
        'HYPOTHESIS': 'Hypothese'}
TYP = {'TECHNICAL': 'technisch', 'ORGANISATIONAL': 'organisatorisch',
       'PERSONAL': 'personenbezogen'}

FONT = 'Arial'
def f(bold=False, color=None, size=10):
    return Font(name=FONT, bold=bold, color=color, size=size)
HEAD_FILL = PatternFill('solid', fgColor='1F3A5F')
INPUT_FILL = PatternFill('solid', fgColor='FFF2CC')
STRIPE = PatternFill('solid', fgColor='F3F5F8')
thin = Side(style='thin', color='C9D1DB')
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical='top')


def val_label(qc, v):
    q = Q.get(qc)
    if q and q.get('type') == 'SELECT':
        for o in q.get('options', []):
            if o['value'] == v:
                return '„%s"' % o['label']
    if v is True: return 'Ja'
    if v is False: return 'Nein'
    return str(v)


def qname(qc):
    q = Q.get(qc)
    if not q: return qc
    return '%s %s' % (q.get('ui_number', ''), q['text'])


def expr(e):
    if 'all' in e: return '(' + ' UND '.join(expr(x) for x in e['all']) + ')'
    if 'any' in e: return '(' + ' ODER '.join(expr(x) for x in e['any']) + ')'
    if 'not' in e: return 'NICHT ' + expr(e['not'])
    qc, op, v = e.get('question'), e.get('operator'), e.get('value')
    if op == 'ANSWERED': return '[%s] ist beantwortet' % qname(qc)
    ops = {'EQ': '=', 'NEQ': '≠', 'GT': '>', 'GTE': '≥', 'LT': '<',
           'LTE': '≤', 'IN': 'ist eines von', 'NOT_IN': 'ist keines von'}
    if isinstance(v, list):
        return '[%s] %s %s' % (qname(qc), ops.get(op, op),
                               ' / '.join(val_label(qc, x) for x in v))
    return '[%s] %s %s' % (qname(qc), ops.get(op, op), val_label(qc, v))


def measures_of(r):
    sofort, mittel = [], []
    for mm in r.get('measures', []):
        m = M.get(mm['measure'])
        if not m: continue
        text = '%s (%s)' % (m.get('title', ''), TYP.get(m.get('type'), ''))
        (sofort if mm.get('group_id') == 'sofort' else mittel).append(text)
    return '\n'.join(sofort), '\n'.join(mittel)


def sources_of(h):
    return '\n'.join('%s %s' % (s.get('document', ''), s.get('section', ''))
                     for s in h.get('sources', []))


def header(ws, cols, widths):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        z = ws.cell(row=1, column=i, value=c)
        z.font = f(bold=True, color='FFFFFF')
        z.fill = HEAD_FILL
        z.alignment = WRAP
        z.border = BORDER
        ws.column_dimensions[chr(64 + i) if i <= 26 else 'A'].width = w
    ws.freeze_panes = 'A2'


def write_rows(ws, rows, input_cols=()):
    for ri, row in enumerate(rows, 2):
        for ci, wert in enumerate(row, 1):
            z = ws.cell(row=ri, column=ci, value=wert)
            z.font = f()
            z.alignment = WRAP
            z.border = BORDER
            if ci in input_cols:
                z.fill = INPUT_FILL
            elif ri % 2 == 0:
                z.fill = STRIPE


review = [r for r in seed['rules']
          if r.get('quality_status') == 'REVIEW_REQUIRED'
          and (ALLE or r.get('hazard') in NEUE_HAZARDS)]
review.sort(key=lambda r: (NEUE_HAZARDS.index(r['hazard'])
                           if r['hazard'] in NEUE_HAZARDS else 99,
                           -r['priority']))

wb = Workbook()

# ---- Blatt 1: Lesehinweise -------------------------------------------------
ws = wb.active
ws.title = 'Lesehinweise'
ws.column_dimensions['A'].width = 118
zeilen = [
    ('Regelprüfung – neue Regeln vom 04.09.2026', True),
    ('', False),
    ('Regelwerk %s, Stand 04.09.2026. Vorgelegt werden %d Regeln zu %d Gefährdungen.'
     % (seed.get('rule_version', ''), len(review),
        len({r['hazard'] for r in review})), False),
    ('', False),
    ('Herkunft, zwei Anlässe: (1) Beim Aufbau des Katalogs „Bestand nach DIN EN 81-80" ist '
     'aufgefallen, dass fünf Sachverhalte der DIN EN 81-20 im Fragebogen bisher nicht abgebildet '
     'waren – MF-T07, MF-T08, MF-T09, MF-K15, MF-M21. (2) Die Analyse der Schindler-Anwendung '
     'GBU 3.0 hat gezeigt, dass dort das Baujahr steuert, welche Fragen im Katalog erscheinen. '
     'Wir blenden bewusst nichts aus, nutzen das Baujahr aber für die neue Gefährdung MF-D06: '
     'Passt die vorgefundene Ausstattung zu dem Regelwerk, unter dem die Anlage in Verkehr '
     'gebracht wurde?', False),
    ('', False),
    ('Was zu entscheiden ist: Trifft die Einstufung (Spalte „Stufe") fachlich zu, und passen die '
     'beiden Maßnahmen? Die Bedingung selbst ist der Normtext – dort geht es nur darum, ob der '
     'Sachverhalt richtig getroffen ist.', False),
    ('', False),
    ('Besonderheit MF-D06: Das Risiko einer fehlenden Fahrkorbtür oder eines fehlenden '
     'UCM-Schutzes ist bereits über die Tür-Gefährdungen bzw. MF-K12 bewertet. MF-D06 '
     'beantwortet eine andere Frage – hätte die Anlage so überhaupt in Verkehr gebracht werden '
     'dürfen? – mit anderem Adressaten (Errichter, Konformitätserklärung, ggf. Marktaufsicht). '
     'Zu prüfen ist deshalb vor allem, ob die Jahresgrenzen stimmen: 1999 Aufzugsrichtlinie '
     '95/16/EG, 2012 EN 81-1/2 + A3 (UCM), 2017 DIN EN 81-20/50.', False),
    ('', False),
    ('Spalte „Entscheidung": Freigeben / Ändern / Streichen. Bei „Ändern" bitte in der Spalte '
     '„Korrektur" angeben, was gilt (z. B. „Stufe Mittel statt Hoch" oder eine andere '
     'Maßnahmenformulierung). Leere Zeilen gelten als noch nicht entschieden.', False),
    ('', False),
    ('Die NO_RISK-Regeln (jeweils die letzte je Gefährdung, Priorität 1) sind die Auffangregeln: '
     'Sie greifen, wenn keine Mangelregel zutrifft und alle Pflichtfragen beantwortet sind. Ohne '
     'sie meldet die Engine eine Regellücke statt „kein Risiko" – sie sind Mechanik, keine '
     'fachliche Wertung, und können in aller Regel freigegeben werden.', False),
    ('', False),
    ('Blatt „Fragen": die in den Bedingungen verwendeten Fragen mit allen Antwortoptionen und dem '
     'Hilfetext aus der App.', False),
]
if not review:
    zeilen.insert(3, ('Derzeit ist keine dieser Regeln mehr offen – alle sind '
                      'freigegeben (siehe mf_content/regelfreigabe.py). Mit '
                      '--alle lassen sich die uebrigen REVIEW_REQUIRED-Regeln '
                      'des Katalogs vorlegen.', True))

for i, (text, bold) in enumerate(zeilen, 1):
    z = ws.cell(row=i, column=1, value=text)
    z.font = f(bold=bold, size=12 if bold else 10)
    z.alignment = WRAP

# ---- Blatt 2: Regeln -------------------------------------------------------
ws = wb.create_sheet('Regeln')
cols = ['Nr.', 'Gefährdung', 'Titel', 'Erhebungsbereich', 'Regel', 'Prio', 'Bedingung',
        'Stufe', 'Evidenz', 'Sofortmaßnahme', 'Mittelfristige Maßnahme',
        'Hinweis im Entwurf', 'Norm-/Quellenbezug', 'Entscheidung', 'Korrektur']
header(ws, cols, [5, 10, 34, 22, 13, 6, 62, 12, 14, 40, 40, 30, 30, 14, 40])
rows = []
for i, r in enumerate(review, 1):
    h = H[r['hazard']]
    sofort, mittel = measures_of(r)
    rows.append([i, r['hazard'], h['title'], h.get('ui_group', ''), r['code'],
                 r['priority'], expr(r['condition']), LAB.get(r['result'], r['result']),
                 EVID.get(r.get('evidence'), ''), sofort, mittel,
                 r.get('notes', ''), sources_of(h), None, None])
write_rows(ws, rows, input_cols=(14, 15))
# Ohne offene Regeln bleibt das Blatt leer – dann keine Datenpruefung und
# kein Autofilter setzen (openpyxl braucht dafuer mindestens eine Zeile).
if rows:
    dv = DataValidation(type='list', formula1='"Freigeben,Ändern,Streichen"',
                        allow_blank=True)
    ws.add_data_validation(dv)
    dv.add('N2:N%d' % (len(rows) + 1))
    ws.auto_filter.ref = 'A1:O%d' % (len(rows) + 1)
n = len(rows) + 1
ws.cell(row=n + 2, column=1, value='Regeln').font = f(bold=True)
ws.cell(row=n + 2, column=2, value=len(rows)).font = f()
ws.cell(row=n + 3, column=1, value='entschieden').font = f(bold=True)
ws.cell(row=n + 3, column=2, value='=COUNTA(N2:N%d)' % n).font = f()

# ---- Blatt 3: Fragen -------------------------------------------------------
ws = wb.create_sheet('Fragen')
cols = ['Nr.', 'Code', 'Frage', 'Erhebungsbereich', 'Typ', 'Antwortoptionen', 'Hilfetext']
header(ws, cols, [8, 26, 46, 24, 10, 60, 60])
codes = []
def sammle(e):
    if 'all' in e:
        for x in e['all']: sammle(x)
    elif 'any' in e:
        for x in e['any']: sammle(x)
    elif 'not' in e:
        sammle(e['not'])
    elif e.get('question') and e['question'] not in codes:
        codes.append(e['question'])
for r in review:
    sammle(r['condition'])
rows = []
for qc in codes:
    q = Q.get(qc, {})
    opts = '\n'.join('• %s' % o['label'] for o in q.get('options', [])) or \
           ('Ja / Nein' if q.get('type', '').startswith('YES_NO') else '')
    rows.append([q.get('ui_number', ''), qc, q.get('text', ''), q.get('category', ''),
                 q.get('type', ''), opts, q.get('help_text', '')])
write_rows(ws, rows)

wb.save(OUT)
print('geschrieben:', OUT, '| Regeln:', len(review),
      '| Gefährdungen:', len({r['hazard'] for r in review}),
      '| Fragen:', len(codes))
