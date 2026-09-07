# -*- coding: utf-8 -*-
"""Fachliche Freigabe der Eigenregeln des MF-Typs (Excel
GBU_MF_Regelpruefung, Blatt „Regeln"). Erzeugt von
gen_mf_regelpruefung_xlsx.py, angewendet von gen_mf_catalog.py:
freigegebene Regeln werden auf quality_status = VERIFIED gesetzt.

Format: Regel-Code -> (Entscheidung, Korrektur)
Entscheidung: 'Freigeben' | 'Ändern' | 'Streichen'.

Solange eine Regel hier fehlt, bleibt sie REVIEW_REQUIRED. „Ändern" und
„Streichen" werden NICHT automatisch umgesetzt – sie sind im Inhalt
(mf_content/*.py) nachzuziehen; bis dahin bleibt die Regel
REVIEW_REQUIRED und die Korrektur steht als Hinweis in den notes.

Diese Freigabe deckt die 26 Regeln der sechs am 04.09.2026 ergänzten
Gefährdungen ab:
  * MF-T07…MF-M21 – Lückenschluss aus dem Abgleich mit DIN EN 81-20
    (Fläche unter der Schachttürschwelle, Rückhaltung und Verbindung der
    Türblätter, Fahrkorbbeleuchtung, Notendschalter)
  * MF-D06 – Konformitätsprüfung Baujahr gegen Ausstattung, aus der
    Analyse der Schindler-Anwendung GBU 3.0

Die übrigen REVIEW_REQUIRED-Regeln des Katalogs sind davon unberührt und
warten weiter auf die Gegenlesung."""

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
