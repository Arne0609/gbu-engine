# -*- coding: utf-8 -*-
"""O – Organisation, Notfall und Nachweise. Bildet die organisatorischen
Prüfpunkte des EK-ZÜS-Beschlusses B-002 rev. 5 Anhang 2 (Nr. 4, 6–14) und die
TRBS-1115-1-Prüffelder „Organisation / Verantwortlichkeiten", „Überwachung /
Cybervorfall / Wiederinbetriebnahme" und „Wirksamkeitsprüfung / Änderungen /
Dokumentation" als eigene Gefährdungen ab.

Die Prüfpunkte 1, 2, 3 und 5 sind nach Entscheidung K-C20 Dokumentationsfragen
(5.11–5.14, Pflicht an CY-O05, ohne eigene Stufe); Nr. 6 (Mindestinhalte 4.5.2)
folgt aus den Komponentenbewertungen (siehe cy_zues_map.json)."""
from .common import *

# ---- Fragen ----------------------------------------------------------------
yn('qo_verantwortlich', 'Ist eine verantwortliche Person des Betreibers für die '
   'Cybersicherheit der Anlage benannt und die Zuständigkeit der Wartungsfirma '
   'vertraglich geregelt?', ui='5.1')
yn('qo_fachkunde', 'Wurden die Cyber-Schutzmaßnahmen durch fachkundige Personen '
   'festgelegt (TRBS 1115-1 Abschnitt 3.3.2)?', ui='5.2')
yn('qo_notfall', 'Ist ein Notfallmanagement für Cybervorfälle festgelegt (Erkennen, '
   'Anlage in sicheren Zustand bringen/außer Betrieb nehmen, Meldung, '
   'Wiederinbetriebnahme erst nach Prüfung)?', ui='5.3')
yn('qo_unterweisung', 'Sind die Beschäftigten (beauftragte Person, Betreiberpersonal) '
   'zur Cybersicherheit der Anlage unterwiesen?', ui='5.4')
yn('qo_pruefung_fristen', 'Sind Art, Umfang und Fristen der Überprüfung und Kontrolle '
   'der Cyber-Schutzmaßnahmen schriftlich festgelegt?', ui='5.5')
yn('qo_wirksamkeit', 'Liegt ein Nachweis der Wirksamkeit der Cyber-Schutzmaßnahmen vor '
   '(TRBS 1115-1 Abschnitt 5)?', ui='5.6')
yn('qo_funktion', 'Liegt eine Bestätigung der Funktionsfähigkeit der Cyber-Schutz'
   'maßnahmen vor (TRBS 1115-1 Abschnitt 8.2)?', ui='5.7')
yn('qo_rueckwirkung', 'Ist sichergestellt, dass die Cyber-Schutzmaßnahmen die '
   'Sicherheitsfunktionen der Anlage nicht negativ beeinflussen (Rückwirkungs'
   'freiheit, z. B. keine Abschaltung des Notrufs durch die Firewall)?', ui='5.8')
yn('qo_erkenntnisse', 'Werden neue Erkenntnisse zur Cybersicherheit (Herstellerhinweise, '
   'Schwachstellenmeldungen, CERT-Warnungen) in die Gefährdungsbeurteilung '
   'eingebunden?', ui='5.9')
yn('qo_aenderungen', 'Wurden nach Aussage des Betreibers prüfpflichtige Änderungen mit '
   'Einfluss auf die Cybersicherheit durchgeführt (Steuerungstausch, neue '
   'Fernanbindung, Software-Update sicherheitsrelevanter Komponenten)?', ui='5.10')
yn('qo_aenderungen_geprueft', 'Wurden diese Änderungen geprüft (ZÜS-Prüfung nach '
   'prüfpflichtiger Änderung) und in der Gefährdungsbeurteilung nachgezogen?',
   ui='5.10a', visible_when=yes('qo_aenderungen'))

# ZÜS-Prüfpunkte 1, 2, 3, 5 als Dokumentationsfragen (Entscheidung K-C20): Pflicht,
# ohne eigene Stufe; gehen in den Berichtsabschnitt „ZÜS-Abschlusscheck" ein.
yn('qo_zues_beruecksichtigt', 'Wurden Cyberbedrohungen gemäß TRBS 1115 Teil 1 bei der '
   'Gefährdungsbeurteilung der Anlage berücksichtigt (diese Cyber-GBU vollständig '
   'bearbeitet und in die Gesamt-GBU übernommen)?', ui='5.11',
   help='EK-ZÜS B-002 Anhang 2 Nr. 1. Dokumentation, keine Stufe.')
yn('qo_zues_erfasst', 'Sind alle sicherheitsrelevanten MSR-Einrichtungen und weiteren '
   'schutzbedürftigen Einrichtungen erfasst und dokumentiert (Komponentenliste '
   'vollständig, weitere Komponenten als Freitext ergänzt)?', ui='5.12',
   help='EK-ZÜS B-002 Anhang 2 Nr. 2. Dokumentation, keine Stufe.')
yn('qo_zues_erhebliches_risiko', 'Wurde bei der Festlegung der Maßnahmen berücksichtigt, '
   'dass bei überwachungsbedürftigen Anlagen nach ÜAnlG stets von einem erheblichen '
   'Risiko für Sicherheit und Gesundheit auszugehen ist?', ui='5.13',
   visible_when=yes('qa_ueberwachungsbeduerftig'),
   help='EK-ZÜS B-002 Anhang 2 Nr. 3. Dokumentation, keine Stufe.')
yn('qo_zues_stand_technik', 'Wurde der Stand der Technik herangezogen (TRBS 1115 Teil 1, '
   'EK-ZÜS B-002/BA-017, Herstellervorgaben, aktuelle Schwachstellenhinweise)?', ui='5.14',
   help='EK-ZÜS B-002 Anhang 2 Nr. 5. Dokumentation, keine Stufe.')

# ---- Klärungen -------------------------------------------------------------
k('K-C15', 'Organisation', 'Notfallmanagement',
  'Kein Notfallmanagement für Cybervorfälle: Mittel – und Hoch bei vernetzter '
  'Anlage?', 'Mittel; Hoch bei Netz-/Fernanbindung', 'Immer Mittel',
  'TRBS 1115-1 nennt Notfallmanagement als Mindestinhalt (4.5.2); bei Vernetzung '
  'ist ein Vorfall wahrscheinlicher und schneller wirksam.')
k('K-C16', 'Organisation', 'Unterweisung',
  'Fehlende Cyber-Unterweisung der Beschäftigten: Mittel (wie fehlende '
  'Unterweisung im 81-20-Typ, K-D04) – oder Niedrig?', 'Mittel', 'Niedrig',
  'BetrSichV § 12; B-002 Anhang 2 Nr. 11 fragt ausdrücklich danach.')
k('K-C17', 'Organisation', 'Nachweise fehlen vollständig',
  'Prüffristen, Wirksamkeitsnachweis und Funktionsbestätigung fehlen alle drei: '
  'Hoch – oder Mittel (organisatorischer Mangel)?', 'Hoch', 'Mittel',
  'Ohne jeden Nachweis ist nicht belegbar, dass überhaupt Maßnahmen wirken; die '
  'ZÜS wird die GBU als unvollständig werten (Anhang 2 Nr. 8, 12, 13).')
k('K-C18', 'Organisation', 'Ungeprüfte Änderungen',
  'Prüfpflichtige Änderung mit Cyber-Einfluss ohne Prüfung: Hoch?', 'Hoch',
  'Mittel', 'Die Anlage befindet sich möglicherweise nicht mehr im geprüften '
  'Zustand (BetrSichV § 15/16; B-002 Anhang 2 Nr. 14).')
k('K-C19', 'Organisation', 'Rückwirkungsfreiheit',
  'Rückwirkung der Cyber-Maßnahmen auf Sicherheitsfunktionen nicht '
  'ausgeschlossen: Hoch – oder Mittel?', 'Hoch', 'Mittel',
  'Eine Schutzmaßnahme, die den Notruf oder den Sicherheitskreis stören kann, '
  'ist selbst eine Gefährdung (B-002 Anhang 2 Nr. 9).')
k('K-C20', 'Organisation', 'ZÜS-Prüfpunkte 1, 2, 3, 5 ohne Frage',
  'Die Prüfpunkte 1 (Cyberbedrohungen berücksichtigt), 2 (Komponenten erfasst), '
  '3 (ÜAnlG-Annahme) und 5 (Stand der Technik) werden durch die Struktur des '
  'Katalogs erfüllt und im Bericht als erfüllt ausgewiesen – ohne eigene Frage. '
  'Einverstanden?', 'Ja, strukturell erfüllt', 'Als Dokumentationsfragen aufnehmen',
  'Eine Ja/Nein-Frage „Wurden Cyberbedrohungen berücksichtigt?" in der GBU, die '
  'genau das tut, wäre inhaltsleer.')
k('K-C25', 'Organisation', 'Herstellervorgaben',
  'Herstellervorgaben vorhanden, aber nicht berücksichtigt: Mittel; nicht '
  'bekannt/nicht angefragt: Niedrig?', 'Mittel / Niedrig', 'Beides Mittel',
  'B-002 Anhang 2 Nr. 7; ohne Anfrage ist der Stand der Technik nicht vollständig '
  'herangezogen.')

# ---- Gefährdungen ----------------------------------------------------------
hz('CY-O01', 'Fehlende Verantwortlichkeit und Fachkunde für die Cybersicherheit',
   GRP_ORGA,
   [('qo_verantwortlich', 'TRIGGER', 'ALWAYS'),
    ('qo_fachkunde', 'TRIGGER', 'ALWAYS'),
    ('qa_ueberwachungsbeduerftig', 'DOCUMENTATION', 'ALWAYS',
     {'notes': 'ÜAnlG-Einordnung für den ZÜS-Prüfpunkt 3 (B-002 Anhang 2).'})],
   [r(all_(no('qo_verantwortlich'), no('qo_fachkunde')), 'HIGH', prio=300,
      sofort='Verantwortliche Person benennen; fachkundige Festlegung der Maßnahmen '
             'veranlassen (Hersteller, Wartungsfirma oder externer Sachverständiger)',
      mittel='Zuständigkeiten Betreiber/Wartungsfirma/Hersteller vertraglich regeln'),
    r(no('qo_fachkunde'), 'MEDIUM', prio=250,
      sofort='Festgelegte Maßnahmen durch eine fachkundige Person prüfen lassen',
      mittel='Fachkunde nach TRBS 1115-1 3.3.2 sicherstellen (Beauftragung, Schulung)'),
    r(no('qo_verantwortlich'), 'MEDIUM', prio=240,
      sofort='Verantwortliche Person des Betreibers benennen',
      mittel='Zuständigkeit der Wartungsfirma für Cybersicherheit vertraglich regeln')],
   sources=[trbs1115('3.3.2'), zues_b002('Anhang 2 Nr. 4'), betrsichv('§ 3 Abs. 3')],
   factor=F_ORGA, persons=[BETREIBER, BEAUFTRAGTE, WARTUNG], bereich='O')

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

hz('CY-O03', 'Fehlendes Notfallmanagement für Cybervorfälle', GRP_ORGA,
   [('qo_notfall', 'TRIGGER', 'ALWAYS'),
    ('qa_vernetzt', 'MODIFIER', 'NEVER')],
   [r(all_(no('qo_notfall'), yes('qa_vernetzt')), 'HIGH', prio=300,
      sofort='Vorgehen bei Verdacht auf Cybervorfall festlegen: Anlage außer Betrieb '
             'nehmen/Fernzugänge trennen, Meldung an Betreiber und Wartungsfirma',
      mittel='Notfallmanagement nach TRBS 1115-1 schriftlich festlegen '
             '(Erkennen, sicherer Zustand, Meldung, Wiederinbetriebnahme nach Prüfung)',
      klaerung=['K-C15']),
    r(no('qo_notfall'), 'MEDIUM', prio=250,
      sofort='Vorgehen bei Verdacht auf Cybervorfall festlegen und bekannt machen',
      mittel='Notfallmanagement nach TRBS 1115-1 schriftlich festlegen',
      klaerung=['K-C15'])],
   sources=[trbs1115('4.5.2 Notfallmanagement'), dekra('Schritt 3')],
   factor=F_NOTFALL, persons=[NUTZER, BETREIBER, BEAUFTRAGTE], bereich='O')

hz('CY-O04', 'Fehlende Unterweisung zur Cybersicherheit', GRP_ORGA,
   [('qo_unterweisung', 'TRIGGER', 'ALWAYS')],
   [r(no('qo_unterweisung'), 'LOW', prio=250,
      sofort='Beauftragte Person und Betreiberpersonal zu Zugang, Servicegeräten und '
             'Verhalten bei Cybervorfall unterweisen',
      mittel='Cyber-Unterweisung in die jährliche Unterweisung aufnehmen und '
             'dokumentieren',
      klaerung=['K-C16'])],
   sources=[betrsichv('§ 12'), zues_b002('Anhang 2 Nr. 11')],
   factor=F_ORGA, persons=[BEAUFTRAGTE, BETREIBER], bereich='O')

hz('CY-O05', 'Fehlende Prüforganisation und Nachweise der Wirksamkeit', GRP_NACHWEIS,
   [('qo_pruefung_fristen', 'TRIGGER', 'ALWAYS'),
    ('qo_wirksamkeit', 'TRIGGER', 'ALWAYS'),
    ('qo_funktion', 'TRIGGER', 'ALWAYS'),
    ('qo_zues_beruecksichtigt', 'DOCUMENTATION', 'ALWAYS',
     {'notes': 'ZÜS-Prüfpunkt 1 (K-C20).'}),
    ('qo_zues_erfasst', 'DOCUMENTATION', 'ALWAYS', {'notes': 'ZÜS-Prüfpunkt 2 (K-C20).'}),
    ('qo_zues_erhebliches_risiko', 'DOCUMENTATION', 'CONDITIONAL',
     {'required_when': yes('qa_ueberwachungsbeduerftig'), 'notes': 'ZÜS-Prüfpunkt 3 (K-C20).'}),
    ('qo_zues_stand_technik', 'DOCUMENTATION', 'ALWAYS', {'notes': 'ZÜS-Prüfpunkt 5 (K-C20).'})],
   [r(all_(no('qo_pruefung_fristen'), no('qo_wirksamkeit'), no('qo_funktion')), 'HIGH',
      prio=300,
      sofort='Wirksamkeit und Funktion der Maßnahmen durch fachkundige Person '
             'feststellen lassen',
      mittel='Prüforganisation aufbauen: Art, Umfang, Fristen; Wirksamkeitsnachweis '
             '(Abschn. 5) und Funktionsbestätigung (Abschn. 8.2) dokumentieren',
      klaerung=['K-C17']),
    r(no('qo_wirksamkeit'), 'MEDIUM', prio=260,
      sofort='Wirksamkeitsnachweis der Maßnahmen nachholen',
      mittel='Wirksamkeitsnachweis nach TRBS 1115-1 Abschnitt 5 dokumentieren'),
    r(no('qo_funktion'), 'MEDIUM', prio=250,
      sofort='Funktionsfähigkeit der Maßnahmen bestätigen lassen',
      mittel='Funktionsbestätigung nach TRBS 1115-1 Abschnitt 8.2 dokumentieren'),
    r(no('qo_pruefung_fristen'), 'MEDIUM', prio=240,
      sofort='Prüfumfang und -fristen für die Cyber-Maßnahmen festlegen',
      mittel='Prüforganisation schriftlich festlegen und in den Wartungsvertrag '
             'aufnehmen')],
   sources=[trbs1115('5, 8.2'), zues_b002('Anhang 2 Nr. 8, 12, 13')],
   factor=F_ORGA, persons=[BETREIBER, WARTUNG], bereich='O')

hz('CY-O06', 'Prüfpflichtige Änderung mit Cyber-Einfluss ohne Prüfung', GRP_NACHWEIS,
   [('qo_aenderungen', 'TRIGGER', 'ALWAYS'),
    ('qo_aenderungen_geprueft', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qo_aenderungen')})],
   [r(all_(yes('qo_aenderungen'), no('qo_aenderungen_geprueft')), 'HIGH', prio=300,
      sofort='Prüfung nach prüfpflichtiger Änderung veranlassen (ZÜS); bis dahin '
             'geänderte Fernzugänge/Funktionen deaktivieren',
      mittel='Änderungen in der Gefährdungsbeurteilung nachziehen und Prüfung '
             'dokumentieren',
      klaerung=['K-C18'])],
   sources=[betrsichv('§ 15, § 16'), zues_b002('Anhang 2 Nr. 14')],
   factor=F_ORGA, persons=[NUTZER, BETREIBER], bereich='O')

hz('CY-O07', 'Rückwirkung der Cyber-Schutzmaßnahmen auf Sicherheitsfunktionen nicht '
   'ausgeschlossen', GRP_NACHWEIS,
   [('qo_rueckwirkung', 'TRIGGER', 'ALWAYS')],
   [r(no('qo_rueckwirkung'), 'HIGH', prio=300,
      sofort='Notruf, Sicherheitskreis und Brandfallsteuerung nach Einführung der '
             'Maßnahmen funktional prüfen',
      mittel='Rückwirkungsfreiheit je Maßnahme bewerten und dokumentieren '
             '(TRBS 1115-1; B-002 Anhang 2 Nr. 9)',
      klaerung=['K-C19'])],
   sources=[zues_b002('Anhang 2 Nr. 9'), trbs1115('4.5')],
   factor=F_AUSFALL, persons=[NUTZER, FEUERWEHR], bereich='O')

hz('CY-O08', 'Keine Fortschreibung bei neuen Erkenntnissen', GRP_NACHWEIS,
   [('qo_erkenntnisse', 'TRIGGER', 'ALWAYS')],
   [r(no('qo_erkenntnisse'), 'LOW', prio=250,
      sofort='Bezugsquellen für Schwachstellenhinweise festlegen (Hersteller, CERT)',
      mittel='Fortschreibung der Gefährdungsbeurteilung bei neuen Erkenntnissen '
             'als Verfahren festlegen')],
   sources=[zues_b002('Anhang 2 Nr. 10'), betrsichv('§ 3 Abs. 7')],
   factor=F_ORGA, persons=[BETREIBER], bereich='O')
