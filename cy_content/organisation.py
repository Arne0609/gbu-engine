# -*- coding: utf-8 -*-
"""O – Organisation: was von der Betreiberorganisation übrig bleibt.

Umfang gekürzt am 13.10.2026 (Festlegung Arne, nach zwei Mustern eines
TÜV-Prüfers für eine plausible Dokumentation nach TRBS 1115 Teil 1). Beide
Muster sind EINE Seite: Komponenten mit Hersteller/Typ und Schnittstellen,
Folgen einer Manipulation, Maßnahmen, Verfahren zur Aufrechterhaltung – und
zwei stehende Zusagen am Ende. Keine Fragen zu Verantwortlichkeit, Fachkunde,
Unterweisung, Notfallmanagement, Prüffristen, Wirksamkeitsnachweis oder
Rückwirkungsfreiheit; kein ZÜS-Abschlusscheck.

Gestrichen: CY-O01 (Verantwortlichkeit/Fachkunde), CY-O03 (Notfallmanagement),
CY-O04 (Unterweisung), CY-O05 (Prüforganisation und Nachweise, samt der vier
ZÜS-Dokumentationsfragen 5.11–5.14), CY-O07 (Rückwirkungsfreiheit – technisch
je Komponente über „wirkt unabhängig" erfasst, das ist im Muster die Spalte
„nicht digitale Maßnahmen"), CY-O08 (Fortschreibung bei neuen Erkenntnissen).
Die Zusagen zu Überprüfung, Stand der Technik und neuen Erkenntnissen stehen
seitdem als feste Sätze im Bericht, nicht als Fragen im Bogen – genau wie im
Muster des Prüfers.

Geblieben sind die zwei Punkte, die in den Mustern ausdrücklich vorkommen:
Herstellervorgaben (CY-O02, Frage 1.7 im Bereich A – das Muster nennt
Herstellerinformationen als Unterlage, die die ZÜS einsehen kann) und
prüfpflichtige Änderungen (CY-O06 – „nach Änderungen an der Anlage überprüft"
bzw. „sämtliche Änderungen von Parametern, Software und Nachrüstungen werden
im Wartungsbuch dokumentiert")."""
from .common import *

# ---- Fragen ----------------------------------------------------------------
yn('qo_aenderungen', 'Wurden nach Aussage des Betreibers prüfpflichtige Änderungen mit '
   'Einfluss auf die Cybersicherheit durchgeführt (Steuerungstausch, neue '
   'Fernanbindung, Software-Update sicherheitsrelevanter Komponenten)?', ui='5.1')
yn('qo_aenderungen_geprueft', 'Wurden diese Änderungen geprüft (ZÜS-Prüfung nach '
   'prüfpflichtiger Änderung) und in der Gefährdungsbeurteilung nachgezogen?',
   ui='5.1a', visible_when=yes('qo_aenderungen'))

# ---- Klärungen -------------------------------------------------------------
k('K-C18', 'Organisation', 'Ungeprüfte Änderungen',
  'Prüfpflichtige Änderung mit Cyber-Einfluss ohne Prüfung: Hoch?', 'Hoch',
  'Mittel', 'Die Anlage befindet sich möglicherweise nicht mehr im geprüften '
  'Zustand (BetrSichV § 15/16; B-002 Anhang 2 Nr. 14).')
k('K-C25', 'Organisation', 'Herstellervorgaben',
  'Herstellervorgaben vorhanden, aber nicht berücksichtigt: Mittel; nicht '
  'bekannt/nicht angefragt: Niedrig?', 'Mittel / Niedrig', 'Beides Mittel',
  'B-002 Anhang 2 Nr. 7; ohne Anfrage ist der Stand der Technik nicht vollständig '
  'herangezogen.')

# ---- Gefährdungen ----------------------------------------------------------
hz('CY-O02', 'Herstellervorgaben zur Cybersicherheit nicht berücksichtigt', GRP_ORGA,
   [('qa_hersteller_vorgaben', 'TRIGGER', 'ALWAYS')],
   [r(eq('qa_hersteller_vorgaben', 'nicht_beruecksichtigt'), 'MEDIUM', prio=300,
      sofort='Herstellervorgaben sichten und Abweichungen bewerten',
      mittel='Herstellervorgaben in die Maßnahmen übernehmen und dokumentieren',
      klaerung=['K-C25']),
    r(eq('qa_hersteller_vorgaben', 'unbekannt'), 'LOW', prio=250,
      sofort='Cyber-Vorgaben beim Hersteller anfragen',
      mittel='Antwort dokumentieren und Maßnahmen ggf. anpassen',
      klaerung=['K-C25'])],
   sources=[zues_b002('Anhang 2 Nr. 7'), trbs1115('3.3')],
   factor=F_ORGA, persons=[BETREIBER, WARTUNG], bereich='O')

hz('CY-O06', 'Prüfpflichtige Änderung mit Cyber-Einfluss ohne Prüfung', GRP_NACHWEIS,
   [('qo_aenderungen', 'TRIGGER', 'ALWAYS'),
    ('qo_aenderungen_geprueft', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qo_aenderungen')}),
    # Die Prüfpflicht nach § 15/16 BetrSichV hängt an der Überwachungs-
    # bedürftigkeit; die Einordnung steht im Kopf des Berichts („alle zur
    # überwachungsbedürftigen Anlage zugehörigen Einrichtungen"). Hier als
    # Dokumentation, damit die Frage nicht ohne Bezug im Katalog steht –
    # sie wird aus dem GBU-Fragebogen übernommen (Antwort-Brücke 2.1).
    ('qa_ueberwachungsbeduerftig', 'DOCUMENTATION', 'NEVER',
     {'notes': 'ÜAnlG-Einordnung; aus dem GBU-Fragebogen übernommen.'})],
   [r(all_(yes('qo_aenderungen'), no('qo_aenderungen_geprueft')), 'HIGH', prio=300,
      sofort='Prüfung nach prüfpflichtiger Änderung veranlassen (ZÜS); bis dahin '
             'geänderte Fernzugänge/Funktionen deaktivieren',
      mittel='Änderungen in der Gefährdungsbeurteilung nachziehen und Prüfung '
             'dokumentieren',
      klaerung=['K-C18'])],
   sources=[betrsichv('§ 15, § 16'), zues_b002('Anhang 2 Nr. 14')],
   factor=F_ORGA, persons=[NUTZER, BETREIBER], bereich='O')
