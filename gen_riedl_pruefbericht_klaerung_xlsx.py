# -*- coding: utf-8 -*-
"""Klärungsliste aus dem externen Prüfbericht zum Riedl-Fragenkatalog.

Quelle: pruefbericht_riedl_2026-09-20.json – die 53 Befunde der externen
Gegenlesung, jeder mit eigener Nachprüfung gegen die Katalog-JSON, einem
Umsetzungsvorschlag und einer Aufwandsschätzung.

    python3 gen_riedl_pruefbericht_klaerung_xlsx.py
    -> GBU_Riedl_Pruefbericht_Klaerung.xlsx

Blätter:
  Übersicht        Zählung nach Status, Schwere und Kategorie (Formeln),
                   empfohlene Reihenfolge
  Offene Befunde   die noch zu entscheidenden Punkte, Spalten „Entscheidung“
                   und „Bemerkung“ zum Ausfüllen
  Eingearbeitet    was am 20.09.2026 umgesetzt wurde
  Ohne Befund      die Prüfschritte des Berichts ohne Beanstandung
"""
from __future__ import annotations

import json
import pathlib

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HIER = pathlib.Path(__file__).resolve().parent
QUELLE = HIER / 'pruefbericht_riedl_2026-09-20.json'
ZIEL = HIER / 'GBU_Riedl_Pruefbericht_Klaerung.xlsx'

SCHRIFT = 'Arial'
KOPF_FUELL = PatternFill('solid', fgColor='1F3864')
KOPF_FONT = Font(name=SCHRIFT, size=10, bold=True, color='FFFFFF')
TITEL_FONT = Font(name=SCHRIFT, size=13, bold=True)
BASIS = Font(name=SCHRIFT, size=10)
FETT = Font(name=SCHRIFT, size=10, bold=True)
OBEN = Alignment(vertical='top', wrap_text=True)
OBEN_MITTE = Alignment(vertical='top', horizontal='center', wrap_text=True)
RAHMEN = Border(*(Side(style='thin', color='BFBFBF'),) * 4)

FARBE_SCHWERE = {'Hoch': 'F8CBAD', 'Mittel': 'FFE699', 'Niedrig': 'E2EFDA'}
FARBE_PRUEF = {'bestätigt': 'FCE4D6', 'teilweise': 'FFF2CC',
               'nicht bestätigt': 'E2EFDA', 'bewusste Entscheidung': 'DEEBF7'}

# Spalten der beiden Befundblätter: (Überschrift, Breite, Feld)
SPALTEN = [
    ('Nr.', 6, 'nr'),
    ('Schwere', 9, 'schwere'),
    ('Katalog', 9, 'katalog'),
    ('Kategorie', 15, 'kategorie'),
    ('Fundstelle', 24, 'fundstelle'),
    ('Befund (extern)', 46, 'befund'),
    ('Auswirkung (extern)', 34, 'auswirkung'),
    ('Empfehlung (extern)', 40, 'empfehlung'),
    ('Nachprüfung', 13, 'nachpruefung'),
    ('Ergebnis der Nachprüfung', 50, 'nachpruefung_text'),
    ('Vorschlag zur Umsetzung', 56, 'vorschlag'),
    ('Aufwand', 9, 'aufwand'),
    ('Entscheidung im Katalog', 22, 'entscheidung'),
    ('Fundstelle im Code', 32, 'fundstelle_code'),
]
ZUSATZ_OFFEN = [('Entscheidung', 16), ('Bemerkung', 30)]

REIHENFOLGE = [
    ('1. Regelfreigabe',
     'Durch die inhaltlichen Änderungen stehen 354 von 415 MF-Regeln wieder auf „Freigabe offen“ '
     '(94 Auffangregeln, 120 inhaltlich geändert). GBU_MF_Regelpruefung.xlsx ist mit diesem Stand '
     'neu erzeugt; Rücklauf über apply_mf_regelpruefung.py. Im Cyber-Teil sind es drei Regeln '
     '(CY-Z04-R5, CY-N01-R5, CY-C12-R3).'),
    ('2. Regelversionen ausrollen',
     'Die Versionen sind gehoben (81-20-mf-2026.10, cyber-mf-2026.3, 81-80-mf-2026.8, '
     'riedl-mf-2026.2, riedl-cyber-2026.2). Entscheiden, wann die App-Assets neu erzeugt '
     '(gen_app_asset.py) und die Kataloge in die Datenbank geladen werden.'),
    ('3. Erhebungsaufwand nachrechnen',
     'B36 (acht Baujahr-Annahmen auf Zustandsfragen gestrichen) und B06 (weniger Nachweis-'
     'Vorbelegungen) erhöhen den Erhebungsaufwand. sim_karten.py zeigt die Wirkung je Profil; '
     'falls einzelne Fragen zu teuer werden, Frage für Frage nachsteuern.'),
]


def _kopfzeile(ws, zeile, ueberschriften):
    for i, text in enumerate(ueberschriften, start=1):
        c = ws.cell(row=zeile, column=i, value=text)
        c.font, c.fill, c.alignment, c.border = KOPF_FONT, KOPF_FUELL, OBEN, RAHMEN
    ws.freeze_panes = ws.cell(row=zeile + 1, column=1)


def _befundblatt(wb, titel, befunde, mit_entscheidung):
    ws = wb.create_sheet(titel)
    spalten = [(u, b) for u, b, _ in SPALTEN] + (ZUSATZ_OFFEN if mit_entscheidung else [])
    for i, (_, breite) in enumerate(spalten, start=1):
        ws.column_dimensions[get_column_letter(i)].width = breite
    _kopfzeile(ws, 1, [u for u, _ in spalten])
    for z, b in enumerate(befunde, start=2):
        for i, (_, _, feld) in enumerate(SPALTEN, start=1):
            c = ws.cell(row=z, column=i, value=b[feld])
            c.font, c.alignment, c.border = BASIS, OBEN, RAHMEN
        ws.cell(row=z, column=1).font = FETT
        ws.cell(row=z, column=2).alignment = OBEN_MITTE
        ws.cell(row=z, column=2).fill = PatternFill('solid', fgColor=FARBE_SCHWERE[b['schwere']])
        _sp = {f: i for i, (_, _, f) in enumerate(SPALTEN, start=1)}
        ws.cell(row=z, column=_sp['nachpruefung']).alignment = OBEN_MITTE
        ws.cell(row=z, column=_sp['nachpruefung']).fill = \
            PatternFill('solid', fgColor=FARBE_PRUEF[b['nachpruefung']])
        ws.cell(row=z, column=_sp['aufwand']).alignment = OBEN_MITTE
        if mit_entscheidung:
            for i in (13, 14):
                c = ws.cell(row=z, column=i, value='')
                c.font, c.alignment, c.border = BASIS, OBEN, RAHMEN
                c.fill = PatternFill('solid', fgColor='FFFF00')
        ws.row_dimensions[z].height = 78
    if mit_entscheidung and befunde:
        dv = DataValidation(type='list', allow_blank=True,
                            formula1='"umsetzen,umsetzen später,anders umsetzen,ablehnen,offen"')
        ws.add_data_validation(dv)
        sp = get_column_letter(len(SPALTEN) + 1)
        dv.add(f'{sp}2:{sp}{len(befunde) + 1}')
    ws.auto_filter.ref = f'A1:{get_column_letter(len(spalten))}{len(befunde) + 1}'
    return ws


def bauen():
    doc = json.loads(QUELLE.read_text(encoding='utf-8'))
    befunde = doc['befunde']
    offen = [b for b in befunde if b['status'] == 'offen']
    fertig = [b for b in befunde if b['status'] == 'umgesetzt']

    wb = Workbook()
    ws = wb.active
    ws.title = 'Übersicht'
    ws.column_dimensions['A'].width = 34
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 104

    ws['A1'] = 'Externer Prüfbericht Riedl-Fragenkatalog – Klärungsliste'
    ws['A1'].font = TITEL_FONT
    ws['A2'] = f"Quelle: {doc['quelle']} · Stand der Prüfung: {doc['stand_pruefung']}"
    ws['A3'] = f"Geprüft gegen: {doc['geprueft_gegen']}"
    ws['A4'] = f"Eingearbeitet in: {', '.join(doc['eingearbeitet_in'])}"
    ws['A5'] = doc['nachpruefung_durch']
    for r in range(2, 6):
        ws.cell(row=r, column=1).font = BASIS
        ws.cell(row=r, column=1).alignment = Alignment(vertical='top')

    z = 7
    ws.cell(row=z, column=1, value='Stand der Bearbeitung').font = TITEL_FONT
    z += 1
    _kopfzeile(ws, z, ['Gruppe', 'Anzahl', 'Bedeutung'])
    ws.freeze_panes = 'A1'
    daten = [
        ('Eingearbeitet 20.09.2026', f'=COUNTIF(Eingearbeitet!A:A,"B*")',
         'Stand 20.09.2026: 52 erledigt, 7 teilweise, 10 bewusst nicht übernommen – Spalte „Entscheidung im Katalog“; inhaltlich ist kein Befund mehr offen'),
        ('Offen gesamt', f'=COUNTA(\'Offene Befunde\'!A2:A{len(offen) + 1})',
         'noch zu entscheiden – Spalte „Entscheidung“ im Blatt „Offene Befunde“'),
        ('davon Mittel', "=COUNTIF('Offene Befunde'!B:B,\"Mittel\")",
         'Dopplung, unnötiger Schritt oder unklare Bedingung mit Wirkung auf Bericht und Bedienung'),
        ('davon Niedrig', "=COUNTIF('Offene Befunde'!B:B,\"Niedrig\")",
         'formal, kosmetisch oder Vereinfachungsvorschlag'),
        ('Nachprüfung: bestätigt', "=COUNTIF('Offene Befunde'!I:I,\"bestätigt\")",
         'Befund gegen die Katalog-JSON nachvollzogen'),
        ('Nachprüfung: teilweise', "=COUNTIF('Offene Befunde'!I:I,\"teilweise\")",
         'Kern des Befunds trifft zu, die Begründung nicht vollständig – siehe Spalte „Ergebnis der Nachprüfung“'),
        ('Nachprüfung: nicht bestätigt', "=COUNTIF('Offene Befunde'!I:I,\"nicht bestätigt\")",
         'kein Fehler – Erklärung in der Spalte „Ergebnis der Nachprüfung“'),
        ('Nachprüfung: bewusste Entscheidung', "=COUNTIF('Offene Befunde'!I:I,\"bewusste Entscheidung\")",
         'so gewollt; die Anregung des Prüfers steht trotzdem im Vorschlag'),
        ('Aufwand klein', "=COUNTIF('Offene Befunde'!L:L,\"klein\")",
         'eine Regel, eine Bedingung oder ein Text – im laufenden Durchgang erledigt'),
        ('Aufwand mittel', "=COUNTIF('Offene Befunde'!L:L,\"mittel\")",
         'neue Frage, neue Gefährdung oder Eingriff in Erhebung bzw. Bericht'),
    ]
    for name, formel, sinn in daten:
        z += 1
        for i, wert in enumerate((name, formel, sinn), start=1):
            c = ws.cell(row=z, column=i, value=wert)
            c.font, c.alignment, c.border = BASIS, OBEN, RAHMEN
        ws.cell(row=z, column=1).font = FETT
        ws.cell(row=z, column=2).alignment = OBEN_MITTE

    z += 2
    ws.cell(row=z, column=1, value='Empfohlene Reihenfolge').font = TITEL_FONT
    z += 1
    _kopfzeile_zeile = z
    for i, text in enumerate(('Paket', '', 'Inhalt'), start=1):
        c = ws.cell(row=_kopfzeile_zeile, column=i, value=text)
        c.font, c.fill, c.alignment, c.border = KOPF_FONT, KOPF_FUELL, OBEN, RAHMEN
    for name, inhalt in REIHENFOLGE:
        z += 1
        for i, wert in enumerate((name, '', inhalt), start=1):
            c = ws.cell(row=z, column=i, value=wert)
            c.font, c.alignment, c.border = BASIS, OBEN, RAHMEN
        ws.cell(row=z, column=1).font = FETT
        ws.row_dimensions[z].height = 46

    _befundblatt(wb, 'Offene Befunde', offen, mit_entscheidung=True)
    _befundblatt(wb, 'Eingearbeitet', fertig, mit_entscheidung=False)

    ws = wb.create_sheet('Ohne Befund')
    ws.column_dimensions['A'].width = 72
    ws.column_dimensions['B'].width = 74
    _kopfzeile(ws, 1, ['Prüfschritt', 'Ergebnis'])
    for z, s in enumerate(doc['geprueft_ohne_befund'], start=2):
        for i, wert in enumerate((s['schritt'], s['ergebnis']), start=1):
            c = ws.cell(row=z, column=i, value=wert)
            c.font, c.alignment, c.border = BASIS, OBEN, RAHMEN
        ws.row_dimensions[z].height = 30

    wb.save(ZIEL)
    print(f'{ZIEL.name}: {len(offen)} offen, {len(fertig)} eingearbeitet, '
          f"{len(doc['geprueft_ohne_befund'])} Prüfschritte ohne Befund")


if __name__ == '__main__':
    bauen()
