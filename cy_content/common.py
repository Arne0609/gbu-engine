# -*- coding: utf-8 -*-
"""DSL für den mehrfragigen Cyber-Typ „Cyber-GBU komponentenbasiert" (CY).

Benutzt dieselben Helfer wie der mehrfragige 81-20-Typ (mf_content/common.py):
Frage → Gefährdung (Rolle) → Regel → Stufe, Pflichtfragen, Kein-Risiko-
Auffangregel, Klärungsliste. Umgestellt werden nur die typabhängigen Register
(CATS, GROUPS, PREFIX) – in place auf mf_content.common, deshalb gilt: in einem
Prozess entweder MF, FT oder CY erzeugen, nie mehrere.

Fachliche Grundlage (eigenständig formuliert):
  * TRBS 1115 Teil 1 „Cybersicherheit für sicherheitsrelevante Mess-, Steuer-
    und Regeleinrichtungen" (BAuA, 11/2022, geändert 2026): Systemabgrenzung,
    Schutzbedarf, Maßnahmen (Segmentierung, Funktionsreduzierung,
    Zugangskontrolle HW/SW, Überwachung, Notfallmanagement), Wirksamkeits-
    nachweis (Abschn. 5), Funktionsbestätigung (Abschn. 8.2).
  * EK-ZÜS-Beschluss B-002 rev. 5 mit Anhang 2 (14 Prüfpunkte der ZÜS) und
    BA-017 (Beispiele Aufzug): komponentenbasierte Betrachtung, Vorscreening
    „keine kompromittierbare Schnittstelle".
  * DEKRA-Ausfüllhilfe Cybersicherheit (09/2024): fünf Schnittstellen-
    kategorien, sechs Maßnahmenkategorien.
  * BetrSichV § 3 Abs. 1 (Cyberbedrohungen sind Teil der GBU), § 12
    (Unterweisung); ÜAnlG (erhebliches Risiko bei überwachungsbedürftigen
    Anlagen).

Methode (aus der Schindler-Analyse übernommen, eigenständig umgesetzt und
erweitert): je Komponente „vorhanden? → Schnittstellen? → Zugang frei? →
Maßnahmen?", geteilte Zugangsfragen als Modifier über alle Komponenten,
MAXIMUM/Prioritäts-Aggregation. Anders als im beobachteten Original:
sechs Zustände (unbeantwortet ≠ Kein Risiko), ausdrückliche Kein-Risiko-Regel,
Normbezug je Gefährdung und eine erreichbare Stufe „Hoch".
"""
from mf_content import common as _C

# ---- Erhebungsbereiche (Fragebogen) ----------------------------------------
_C.CATS.clear()
_C.CATS.update([
    ('A', 'A – Anlagenmerkmale und Systemabgrenzung'),
    ('Z', 'Z – Zugang und Zugriff'),
    ('C', 'C – Komponenten und Schnittstellen'),
    ('N', 'N – Netz, Fernzugriff und Härtung'),
    ('O', 'O – Organisation, Notfall und Nachweise'),
])
_C._PREFIX2CAT.clear()
_C._PREFIX2CAT.update({'qa_': 'A', 'qz_': 'Z', 'qc_': 'C', 'qn_': 'N', 'qo_': 'O'})

# ---- Baugruppen (Bewertung/Bericht) ----------------------------------------
_C.GROUPS[:] = [
    'Steuerung und Sicherheitslogik',
    'Antrieb und Türen',
    'Notruf und Kommunikation',
    'Netz, Fernzugriff und Fernwartung',
    'Gebäudeschnittstelle',
    'Zugang und Zugriff',
    'Härtung und Servicegeräte',
    'Organisation und Notfallmanagement',
    'Nachweise und Wirksamkeit',
]

from mf_content.common import *  # noqa: F401,F403,E402
from mf_content.common import (QUESTIONS, HAZARDS, RULES, KLAERUNG, MEASURES,  # noqa: F401,E402
                               CATS, GROUPS)

(GRP_STEUERUNG, GRP_ANTRIEB, GRP_NOTRUF, GRP_NETZ, GRP_GEBAEUDE, GRP_ZUGANG,
 GRP_HAERTUNG, GRP_ORGA, GRP_NACHWEIS) = GROUPS

# ---- Personengruppen --------------------------------------------------------
NUTZER = 'Nutzer'
WARTUNG = 'Wartungspersonal'
BEAUFTRAGTE = 'Beauftragte Person'
BETREIBER = 'Betreiber'
FEUERWEHR = 'Feuerwehr'

# ---- Gefährdungsfaktoren ----------------------------------------------------
F_MANIP = 'Gefährdung durch Manipulation sicherheitsrelevanter Steuerungsfunktionen'
F_AUSFALL = 'Gefährdung durch Ausfall oder Fehlfunktion sicherheitsrelevanter Einrichtungen (Cybervorfall)'
F_NOTRUF = 'Sonstige Gefährdung durch Ausfall der Notrufverbindung (Personeneinschluss)'
F_ZUGANG = 'Gefährdung durch unbefugten Zugang zu sicherheitsrelevanten Einrichtungen'
F_ORGA = 'Gefährdung durch organisatorische Mängel (Verantwortung, Fachkunde, Nachweise)'
F_NOTFALL = 'Sonstige Gefährdung durch fehlende oder unzureichende Notfallorganisation'
F_BRAND = 'Brand- und Explosionsgefährdung (Fehlverhalten im Brandfall)'

# ---- Quellen ----------------------------------------------------------------
def trbs1115(sec=None): return src('TRBS', 'TRBS 1115 Teil 1', sec)
def zues_b002(sec=None): return src('OTHER', 'EK-ZÜS B-002 rev. 5', sec)
def zues_ba017(sec=None): return src('OTHER', 'EK-ZÜS BA-017', sec)
def dekra(sec=None): return src('OTHER', 'DEKRA Ausfüllhilfe Cybersicherheit 09/2024', sec)
def betrsichv(sec=None): return src('LAW', 'BetrSichV', sec)
def ueanlg(sec=None): return src('LAW', 'ÜAnlG', sec)
def en8128(sec=None): return src('EN', 'DIN EN 81-28', sec)
def en8173(sec=None): return src('EN', 'DIN EN 81-73', sec)
def en8172(sec=None): return src('EN', 'DIN EN 81-72', sec)
def en8150(sec=None): return src('EN', 'DIN EN 81-50', sec)

# ---- Schnittstellenkategorien (DEKRA, geordnet nach Angreifbarkeit) --------
IF_KEINE, IF_KABEL, IF_BENUTZER, IF_KABELLOS, IF_FERN = (
    'keine', 'kabelgebunden', 'benutzer', 'kabellos', 'fernzugriff')
IF_OPTIONS = [
    (IF_KEINE, 'Keine bzw. nicht programmierbare Schnittstelle'),
    (IF_KABEL, 'Kabelgebunden, nur vor Ort (USB, RS232/485, CAN, Ethernet, Serviceanschluss, Speicherkarte)'),
    (IF_BENUTZER, 'Benutzerschnittstelle (Bedienfeld, Eingabeterminal, Display mit Parametrierzugang)'),
    (IF_KABELLOS, 'Kabellos im Nahbereich (WLAN, Bluetooth, NFC, Mobilfunk/SIM)'),
    (IF_FERN, 'Fernzugriff (Internet/Cloud, Hersteller-Fernzugriff, Service-App)'),
]
IF_LOKAL = [IF_KABEL, IF_BENUTZER]
IF_ENTFERNT = [IF_KABELLOS, IF_FERN]

# ---- Maßnahmenstand je Komponente -----------------------------------------
M_KEINE, M_TEILWEISE, M_UMGESETZT = 'keine', 'teilweise', 'umgesetzt'
M_OPTIONS = [
    (M_KEINE, 'Keine Schutzmaßnahmen festgelegt'),
    (M_TEILWEISE, 'Festgelegt, aber nicht vollständig umgesetzt oder ohne Wirksamkeitsnachweis'),
    (M_UMGESETZT, 'Festgelegt, umgesetzt und Wirksamkeit nachgewiesen (TRBS 1115-1 Abschn. 5)'),
]
