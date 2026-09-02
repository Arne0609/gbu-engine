# -*- coding: utf-8 -*-
"""SF – Sonderfunktionen (Feuerwehraufzug, aus Ergänzung 2026 SF1) und
D – Unterlagen und Betreiberorganisation (Blaupause: Schindler M112, M113,
M115, M116; eigene Ergänzungen E1–E5 der Stammdaten nach BetrSichV/TRBS 3121)."""
from .common import *

GRP_SF = 'Sonderfunktionen'
GRP_DOC = 'Beschilderung und Unterlagen'
GRP_ORG = 'Betreiberorganisation'
GRP_NOT = 'Notruf und Personenbefreiung'

# ---- Fragen SF -------------------------------------------------------------
FW = yes('qa_feuerwehraufzug')
SF_ITEMS = [
    ('qsf_unterlagen', 'Anforderungen und Unterlagen des Feuerwehraufzugs (EN 81-72, '
     'Brandschutzkonzept) vorhanden und erfüllt?', '16.1', 'Sind Anforderungen/Unterlagen'),
    ('qsf_bma', 'Brandmeldeanlage und Feuerwehraufzugsfunktion aufeinander abgestimmt?', '16.2',
     'Sind Brandmeldeanlage'),
    ('qsf_druckbelueftung', 'Druckbelüftungs-/Rauchschutzanlagen für Schacht und Vorräume '
     'vorhanden und geprüft?', '16.3', 'Sind Druckbelüftungs'),
    ('qsf_loeschwasser', 'Löschwasser-/Pumpeneinrichtungen mit Schnittstelle zum Aufzug '
     'berücksichtigt?', '16.4', 'Sind Löschwasser'),
    ('qsf_ersatzstrom', 'Sicherheits-/Ersatzstromversorgung vorhanden und geprüft?', '16.5',
     'Ist die erforderliche Sicherheits'),
    ('qsf_ersatzstrom_test', 'Funktion des Aufzugs unter Ersatzstrombedingungen geprüft?', '16.6',
     'Wurde die Funktion'),
    ('qsf_nachweise', 'Erforderliche Prüfnachweise der Fremdgewerke verfügbar?', '16.7',
     'Sind erforderliche Fremdgewerk'),
    ('qsf_feuerwehr_doku', 'Schnittstellen zur Feuerwehr / Brandschutzdienststelle dokumentiert '
     '(Feuerwehrplan, Schlüsseldepot)?', '16.8', 'Sind Schnittstellen'),
    ('qsf_organisation', 'Betreiberorganisation auf den Sonderbetrieb abgestimmt '
     '(Zuständigkeit, Unterweisung, Übungen)?', '16.9', 'Ist die Betreiberorganisation'),
    ('qsf_cyber', 'Cyber-Auswirkungen auf die Feuerwehrfunktionen gesondert betrachtet?', '16.10',
     'Sind Cyber-Auswirkungen'),
]
for code, text, ui, _ in SF_ITEMS:
    yn(code, text, ui=ui, visible_when=FW)
# Entscheidung 02.09.2026 (K-SF1): Dokumentations- und Cyber-Punkte nur Mittel.
SF_MITTEL = {'qsf_unterlagen', 'qsf_nachweise', 'qsf_feuerwehr_doku', 'qsf_cyber'}

# ---- Fragen D --------------------------------------------------------------
yn('qd_notfallplan', 'Notfallplan für die Anlage vorhanden und aktuell (Ansprechpartner, '
   'Befreiungsdienst, Meldewege)?', ui='3.2')
sel('qd_notbefreiungsanleitung', 'Anlagenbezogene Notbefreiungs-/Evakuierungsanleitung', ui='3.3',
    options=[('aktuell', 'Vorhanden, zur Anlage passend und aktuell'),
             ('veraltet', 'Vorhanden, aber veraltet oder nicht zur Anlage passend'),
             ('fehlt', 'Nicht vorhanden')])
yn('qd_wartungsunterlagen', 'Wartungsunterlagen und Prüfbuch vorhanden und aktuell?', ui='3.9')
yn('qd_regelmaessige_wartung', 'Wird die Anlage regelmäßig durch ein Fachunternehmen '
   'instand gehalten (Wartungsvertrag)?', ui='3.10')
yn('qd_pruefplakette', 'Prüfplakette der ZÜS vorhanden und lesbar?', ui='3.6')
yn('qd_pruefung_ueberfaellig', 'Prüffrist der wiederkehrenden Prüfung (ZÜS) überschritten?',
   ui='3.8')
yn('qd_beauftragte_person', 'Beauftragte Person für die Aufzugsanlage (Aufzugswärter) '
   'schriftlich benannt?', ui='E1')
yn('qd_unterweisung', 'Unterweisung der beauftragten Person dokumentiert?', ui='E2',
   visible_when=yes('qd_beauftragte_person'))
yn('qd_betriebsanweisung', 'Betriebsanweisung für die Anlage vorhanden und ausgehängt?', ui='E3')
yn('qd_zugang_mr_geregelt', 'Zutritt zum Triebwerksraum / Steuerschrank organisatorisch '
   'geregelt (Schlüsselverwaltung, nur befugte Personen)?', ui='E4')
yn('qd_gbu_vorhanden', 'Liegt für die Anlage bereits eine dokumentierte Gefährdungsbeurteilung '
   'des Betreibers vor?', ui='E5')

# ---- Klärungen -------------------------------------------------------------
k('K-D01', 'Organisation', 'Notfallplan',
  'Fehlender oder veralteter Notfallplan: Hoch (Schindler M113) – oder Mittel?', 'Hoch',
  'Mittel', 'Im App-Katalog nur als Stammdatenfeld 3.2, ohne Stufe.')
k('K-D02', 'Organisation', 'Keine regelmäßige Instandhaltung',
  'Anlage ohne regelmäßige Instandhaltung durch ein Fachunternehmen: Hoch (eigener Vorschlag)?',
  'Hoch', 'Mittel', 'Im App-Katalog nur als Stammdatenfeld 3.10, ohne Stufe.')
k('K-D03', 'Organisation', 'Überschrittene Prüffrist',
  'ZÜS-Prüffrist überschritten: Hoch (eigener Vorschlag); Plakette fehlt, Frist eingehalten: '
  'Mittel (Schindler M115)?', 'Hoch / Mittel', 'Immer Mittel', 'Abgestufter eigener Vorschlag.')
k('K-D04', 'Organisation', 'Beauftragte Person, Unterweisung, Betriebsanweisung',
  'Fehlende beauftragte Person, fehlende Unterweisung, fehlende Betriebsanweisung: jeweils '
  'Mittel (eigener Vorschlag nach BetrSichV § 12 / Anh. 1 Nr. 4)?', 'Mittel', 'Niedrig / Hoch',
  'Eigene Ergänzung E1–E5, nicht aus einer Vorlage.')
k('K-SF1', 'Sonderfunktionen', 'Feuerwehraufzug Einzelpunkte',
  'Jeder der zehn Feuerwehraufzug-Punkte ergibt bei Nein Hoch (wie Ergänzung 2026 SF1). '
  'Sollen einzelne Punkte (Cyber, Dokumentation) nur Mittel ergeben?', 'Alle Hoch',
  'Cyber und Dokumentation Mittel', 'Ergänzung 2026 kennt nur Hoch.')

# ---- Gefährdungen SF -------------------------------------------------------
hz('MF-SF01', 'Feuerwehraufzug / gebäudeseitige Sonderfunktionen nicht nachgewiesen', GRP_SF,
   [('qa_feuerwehraufzug', 'APPLICABILITY', 'NEVER')] +
   [(code, 'TRIGGER', 'ALWAYS') for code, _, _, _ in SF_ITEMS],
   [r(no(code), 'MEDIUM' if code in SF_MITTEL else 'HIGH', mfrom=('E26-SF1', pref),
      evidence='HIGH_CONFIDENCE', klaerung='K-SF1')
    for code, _, _, pref in SF_ITEMS],
   sources=[en('DIN EN 81-72'), trbs3121('Anhang 3'), trbs('TRBS 1201 Teil 4', 'Anhang 4')],
   factor=F_BRAND, persons=[FEUERWEHR, NUTZER, BETREIBER], agg='MAXIMUM', bereich='SF')

# ---- Gefährdungen D --------------------------------------------------------
hz('MF-D01', 'Notfallplan unvollständig oder nicht vorhanden', GRP_NOT,
   [('qd_notfallplan', 'TRIGGER', 'ALWAYS')],
   [r(no('qd_notfallplan'), 'HIGH',
      sofort='Ansprechpartner und Befreiungsdienst mit Rufnummern am Aufzug aushängen',
      mittel='Notfallplan nach BetrSichV Anh. 1 Nr. 4.1 erstellen und an der Anlage hinterlegen',
      evidence='INFERRED', klaerung='K-D01')],
   sources=[law('BetrSichV', 'Anh. 1 Nr. 4.1'), trbs3121('4.4')], factor=F_NOTFALL,
   persons=[NUTZER, BETREIBER], bereich='D')

hz('MF-D02', 'Keine oder unpassende Notbefreiungsanleitung', GRP_NOT,
   [('qd_notbefreiungsanleitung', 'TRIGGER', 'ALWAYS')],
   [r(eq('qd_notbefreiungsanleitung', 'fehlt'), 'HIGH',
      sofort='Personenbefreiung bis zur Bereitstellung nur durch das Wartungsunternehmen',
      mittel='Anlagenbezogene Notbefreiungsanleitung vom Hersteller/Instandhalter beschaffen '
             'und im Triebwerksraum hinterlegen', evidence='INFERRED', klaerung='K-M07'),
    r(eq('qd_notbefreiungsanleitung', 'veraltet'), 'MEDIUM',
      mfrom=('N20-M13', 'Notbefreiungsanleitung'), evidence='HIGH_CONFIDENCE', klaerung='K-M07')],
   sources=[law('BetrSichV', 'Anh. 1 Nr. 4.1'), en8120('7.2.2')], factor=F_NOTFALL,
   persons=[NUTZER, BEAUFTRAGTE], bereich='D')

hz('MF-D03', 'Wartungsunterlagen fehlen oder keine regelmäßige Instandhaltung', GRP_DOC,
   [('qd_wartungsunterlagen', 'TRIGGER', 'ALWAYS'),
    ('qd_regelmaessige_wartung', 'TRIGGER', 'ALWAYS')],
   [r(no('qd_regelmaessige_wartung'), 'HIGH',
      sofort='Betreiber auf die Instandhaltungspflicht hinweisen; Zustand der Anlage prüfen',
      mittel='Instandhaltungsvertrag mit einem Fachunternehmen abschließen (BetrSichV § 10)',
      evidence='HYPOTHESIS', klaerung='K-D02'),
    r(no('qd_wartungsunterlagen'), 'MEDIUM',
      sofort='Vorhandene Unterlagen beim Instandhalter anfordern',
      mittel='Prüfbuch und Wartungsnachweise an der Anlage oder beim Betreiber führen',
      evidence='INFERRED')],
   sources=[law('BetrSichV', '§ 10'), law('BetrSichV', '§ 17'), trbs3121('4.6')], factor=F_ORGA,
   persons=[BETREIBER, NUTZER], agg='MAXIMUM', bereich='D')

hz('MF-D04', 'Prüfplakette fehlt oder Prüffrist der ZÜS überschritten', GRP_DOC,
   [('qd_pruefplakette', 'TRIGGER', 'ALWAYS'),
    ('qd_pruefung_ueberfaellig', 'TRIGGER', 'ALWAYS')],
   [r(yes('qd_pruefung_ueberfaellig'), 'HIGH',
      sofort='Betreiber informieren; Prüfung durch die ZÜS unverzüglich veranlassen',
      mittel='Prüffristen im Prüfbuch führen und Wiedervorlage einrichten', evidence='INFERRED',
      klaerung='K-D03'),
    r(no('qd_pruefplakette'), 'MEDIUM',
      sofort='Prüfbescheinigung einsehen; Plakette nachbeschaffen',
      mittel='Prüfplakette im Fahrkorb anbringen (BetrSichV § 17 Abs. 3)', evidence='INFERRED',
      klaerung='K-D03')],
   sources=[law('BetrSichV', '§ 16'), law('BetrSichV', '§ 17 Abs. 3'), law('BetrSichV', 'Anh. 2 Abschn. 2')],
   factor=F_ORGA, persons=[BETREIBER, NUTZER], agg='MAXIMUM', bereich='D')

hz('MF-D05', 'Betreiberorganisation: beauftragte Person, Unterweisung, Betriebsanweisung, '
   'Zutrittsregelung', GRP_ORG,
   [('qd_beauftragte_person', 'TRIGGER', 'ALWAYS'),
    ('qd_unterweisung', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qd_beauftragte_person')}),
    ('qd_betriebsanweisung', 'TRIGGER', 'ALWAYS'),
    ('qd_zugang_mr_geregelt', 'TRIGGER', 'ALWAYS'),
    ('qd_gbu_vorhanden', 'DOCUMENTATION', 'NEVER')],
   [r(no('qd_beauftragte_person'), 'MEDIUM',
      sofort='Betreiber auf die Pflicht zur Benennung einer beauftragten Person hinweisen',
      mittel='Beauftragte Person schriftlich bestellen und anlagenbezogen einweisen (BetrSichV Anh. 1 Nr. 4)',
      evidence='INFERRED', klaerung='K-D04'),
    r(no('qd_unterweisung'), 'MEDIUM',
      sofort='Unterweisung nachholen', mittel='Unterweisung jährlich wiederholen und dokumentieren',
      evidence='INFERRED', klaerung='K-D04'),
    r(no('qd_betriebsanweisung'), 'MEDIUM',
      sofort='Vorläufige Betriebsanweisung mit Verhalten bei Störung und Personeneinschluss aushängen',
      mittel='Anlagenbezogene Betriebsanweisung nach BetrSichV § 12 erstellen', evidence='INFERRED',
      klaerung='K-D04'),
    r(no('qd_zugang_mr_geregelt'), 'MEDIUM',
      sofort='Triebwerksraum abschließen, Schlüsselausgabe nur an befugte Personen',
      mittel='Zutrittsregelung in der Betriebsanweisung festlegen', evidence='INFERRED',
      klaerung='K-D04')],
   sources=[law('BetrSichV', '§ 12'), law('BetrSichV', 'Anh. 1 Nr. 4'), trbs3121('4.2'), trbs('TRBS 1116')],
   factor=F_ORGA, persons=[BETREIBER, BEAUFTRAGTE], agg='MAXIMUM', bereich='D')
