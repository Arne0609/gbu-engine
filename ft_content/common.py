# -*- coding: utf-8 -*-
"""DSL für den GBU-Typ „Fahrtreppen und Fahrsteige" (FT).

Benutzt dieselben Helfer wie der mehrfragige 81-20-Typ (mf_content/common.py) –
Frage → Gefährdung (Rolle) → Regel → Stufe, Pflichtfragen, Kein-Risiko-Auffang-
regel, Klärungsliste. Umgestellt werden nur die typabhängigen Register:

  * CATS    – Erhebungsbereiche: A (Anlagenmerkmale), B (Betrieb), I (Instandhaltung)
  * GROUPS  – Baugruppen für Bewertung und Bericht
  * PREFIX  – Fragen-Präfix -> Erhebungsbereich

Die Umstellung geschieht **in place** auf dem Modul mf_content.common, weil die
Helfer q()/hz() ihre Register als Modulglobale lesen. Deshalb gilt: in einem
Prozess entweder den MF- oder den FT-Katalog erzeugen, nie beide. Die
Generatoren (gen_mf_catalog.py / gen_ft_catalog.py) laufen getrennt.

Fachliche Besonderheiten gegenüber den Aufzugstypen:
  * Fahrtreppen und Fahrsteige sind KEINE überwachungsbedürftigen Anlagen
    (BetrSichV Anhang 2 Nr. 2 nimmt sie ausdrücklich aus) – keine ZÜS, keine
    TRBS 3121. Geprüft wird als Arbeitsmittel nach § 14 BetrSichV durch eine
    zur Prüfung befähigte Person.
  * Zwei Blickrichtungen in einem Typ: Bereich B bewertet die Gefährdung der
    Nutzer und Beschäftigten durch die Anlage (Betreiber-GBU, ArbStättV/
    ASR A1.8/DGUV 208-028), Bereich I die Gefährdung des Instandhaltungs-
    personals an der Anlage (DGUV 208-029, DGUV 209-085 Anhang 2).
  * Die Ampel-Einstufungen der DGUV 209-085 sind ausdrücklich nur Orientierung
    („Die tatsächliche Einstufung kann je nach Anlage stark abweichen"). Sie
    sind hier als eigene Regeln mit Quellenbezug umgesetzt, nicht als feste
    Voreinstufung übernommen.
"""
from mf_content import common as _C

# ---- Erhebungsbereiche (Fragebogen) ----------------------------------------
_C.CATS.clear()
_C.CATS.update([
    ('A', 'A – Anlagenmerkmale'),
    ('B', 'B – Betrieb und Nutzung (Betreiber)'),
    ('I', 'I – Instandhaltung, Montage und Reinigung'),
])
_C._PREFIX2CAT.clear()
_C._PREFIX2CAT.update({'qa_': 'A', 'qb_': 'B', 'qi_': 'I'})

# ---- Baugruppen (Bewertung/Bericht) ----------------------------------------
_C.GROUPS[:] = [
    'Zu- und Abgänge',
    'Umfeld und Gebäudeschnittstelle',
    'Balustrade, Handlauf und Sockel',
    'Stufen-, Paletten- und Kammbereich',
    'Not-Halt, Bedienung und Sicherheitseinrichtungen',
    'Beleuchtung',
    'Betreiberorganisation und Unterweisung',
    'Kontrollen, Wartung und Prüfung',
    'Absperrung und Sicherung des Arbeitsbereichs',
    'Umkehr- und Antriebsstation',
    'Elektrische Anlage und Freischaltung',
    'Inspektionssteuerung',
    'Arbeiten im Stufen- und Palettenband',
    'Gefahrstoffe, Hygiene und Umgebung',
    'Koordination und Notfallorganisation',
]

from mf_content.common import *  # noqa: F401,F403,E402
from mf_content.common import (QUESTIONS, HAZARDS, RULES, KLAERUNG, MEASURES,  # noqa: F401,E402
                               CATS, GROUPS)

# ---- Baugruppen-Kurznamen ---------------------------------------------------
(GRP_ZUGANG, GRP_UMFELD, GRP_BALUSTRADE, GRP_STUFEN, GRP_NOTHALT, GRP_LICHT,
 GRP_ORGA, GRP_PRUEF, GRP_ABSPERR, GRP_STATION, GRP_ELEKTRO, GRP_INSP,
 GRP_BAND, GRP_STOFFE, GRP_KOORD) = GROUPS

# ---- Personengruppen --------------------------------------------------------
NUTZER = 'Nutzer und Fahrgäste'
KINDER = 'Kinder und besonders gefährdete Personen'
BESCHAEFTIGTE = 'Beschäftigte des Betreibers'
WARTUNG = 'Instandhaltungspersonal'
REINIGUNG = 'Reinigungspersonal'
FREMDFIRMEN = 'Fremdfirmen'
BETREIBER = 'Betreiber'
FEUERWEHR = 'Feuerwehr und Rettungskräfte'

# ---- Gefährdungsfaktoren ----------------------------------------------------
F_STURZ = 'Mechanische Gefährdung durch Stolpern, Rutschen, Stürzen'
F_ABSTURZ = 'Mechanische Gefährdung durch Absturz'
F_EINZUG = 'Mechanische Gefährdung durch Einziehen und Erfassen'
F_QUETSCH = 'Mechanische Gefährdung durch Quetschen und Scheren'
F_BEWEGT = 'Mechanische Gefährdung durch bewegte Teile (Quetschen, Scheren, Einziehen)'
F_ROTIEREND = 'Mechanische Gefährdung durch rotierende Teile (Erfassen, Einziehen)'
F_STOSS = 'Mechanische Gefährdung durch Stoß und Anprall'
F_KINETISCH = 'Mechanische Gefährdung durch Beschleunigung und Abbremsung (kinetische Energie)'
F_LAST = 'Mechanische Gefährdung durch herabfallende oder kippende Lasten'
F_ELEKTRISCH = 'Elektrische Gefährdung durch Berühren spannungsführender Teile'
F_BELEUCHTUNG = 'Gefährdung durch Arbeitsumgebungsbedingungen (unzureichende Beleuchtung)'
F_UMGEBUNG = 'Gefährdung durch Arbeitsumgebungsbedingungen (Klima, Lärm, Emissionen)'
F_ERGONOMIE = 'Physische Belastung / ergonomische Gefährdung'
F_GEFAHRSTOFF = 'Gefährdung durch Gefahrstoffe und biologische Arbeitsstoffe'
F_BRAND = 'Brand- und Explosionsgefährdung'
F_ORGA = 'Gefährdung durch organisatorische Mängel (Unterlagen, Unterweisung, Zuständigkeit)'
F_BEFEHL = 'Gefährdung durch unbeabsichtigtes Betätigen von Befehlsgebern'
F_NOTFALL = 'Sonstige Gefährdung durch fehlende oder unzureichende Notfallorganisation'
F_FLUCHT = 'Gefährdung durch fehlende oder versperrte Flucht- und Rettungswege'

# ---- Quellen ----------------------------------------------------------------
def en115_1(sec=None):  return src('EN', 'DIN EN 115-1', sec)
def en115_2(sec=None):  return src('EN', 'DIN EN 115-2', sec)
def d208_028(sec=None): return src('DGUV', 'DGUV Information 208-028', sec)
def d208_029(sec=None): return src('DGUV', 'DGUV Information 208-029', sec)
def d209_085(sec=None): return src('DGUV', 'DGUV Information 209-085', sec)
def asr18(sec=None):    return src('OTHER', 'ASR A1.8', sec)
def asr34(sec=None):    return src('OTHER', 'ASR A3.4', sec)
def betrsichv(sec=None): return src('LAW', 'BetrSichV', sec)
def arbstaettv(sec=None): return src('LAW', 'ArbStättV', sec)
