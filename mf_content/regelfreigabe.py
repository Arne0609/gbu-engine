# -*- coding: utf-8 -*-
"""Fachliche Freigabe der Eigenregeln des MF-Typs (EN 81-20, mehrfragig).

Vorlage: gen_mf_regelpruefung_xlsx.py -> GBU_MF_Regelpruefung.xlsx
Rückweg: apply_mf_regelpruefung.py ergänzt diese Datei,
angewendet von gen_mf_catalog.py: freigegebene Regeln werden auf
quality_status = VERIFIED gesetzt; der Katalog EN 81-80 übernimmt das über
gen_en8180_catalog.py.

Format: Regel-Code -> (Entscheidung, Korrektur, Datum, Fingerabdruck)
  Entscheidung: 'Freigeben' | 'Ändern' | 'Streichen'
  Fingerabdruck: mf_content/fingerabdruck.py – passt er nicht mehr zum
  Regelinhalt (Regel geändert oder Code verschoben), bleibt die Regel offen.
  Altformat (Entscheidung, Korrektur) gilt mit DATUM, ohne Prüfung.

Solange eine Regel hier fehlt, bleibt sie REVIEW_REQUIRED. „Ändern" und
„Streichen" werden NICHT automatisch umgesetzt – sie sind im Inhalt
(mf_content/*.py) nachzuziehen; bis dahin bleibt die Regel
REVIEW_REQUIRED und die Korrektur steht als Hinweis in den notes.

Verlauf:
  04.09.2026 – 26 Regeln der sechs ergänzten Gefährdungen (MF-T07…MF-M21
               aus dem EN-81-20-Lückenschluss, MF-D06 Konformität/Baujahr).
  15.09.2026 – Gesamtprüfung aller übrigen offenen Regeln vorgelegt."""

DATUM = '2026-09-04'

FREIGABE = {
    'MF-T07-R1': ('Freigeben', ''),
    'MF-T07-R2': ('Freigeben', ''),
    'MF-T07-R3': ('Freigeben', ''),
    'MF-T08-R1': ('Freigeben', ''),
    'MF-T08-R2': ('Freigeben', ''),
    'MF-T08-R3': ('Freigeben', ''),
    'MF-T08-R4': ('Freigeben', ''),
    'MF-T09-R1': ('Freigeben', ''),
    'MF-T09-R2': ('Freigeben', ''),
    'MF-T09-R3': ('Freigeben', ''),
    'MF-K15-R1': ('Freigeben', ''),
    'MF-K15-R2': ('Freigeben', ''),
    'MF-K15-R3': ('Freigeben', ''),
    'MF-K15-R4': ('Freigeben', ''),
    'MF-K15-R5': ('Freigeben', ''),
    'MF-M21-R1': ('Freigeben', ''),
    'MF-M21-R2': ('Freigeben', ''),
    'MF-M21-R3': ('Freigeben', ''),
    'MF-M21-R4': ('Freigeben', ''),
    'MF-M21-R5': ('Freigeben', ''),
    'MF-D06-R1': ('Freigeben', ''),
    'MF-D06-R2': ('Freigeben', ''),
    'MF-D06-R3': ('Freigeben', ''),
    'MF-D06-R4': ('Freigeben', ''),
    'MF-D06-R5': ('Freigeben', ''),
    'MF-D06-R6': ('Freigeben', ''),
}
