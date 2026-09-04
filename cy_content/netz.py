# -*- coding: utf-8 -*-
"""N – Netz, Fernzugriff und Härtung (anlagenweit). Die Fragen zu
Segmentierung, Freigabe, Authentifizierung und Protokollierung werden von den
Kanal-Komponenten (Fernüberwachung, Remote-Service, Gateway) mitbenutzt;
Softwarestand und Funktionsreduzierung sind eigene, anlagenweite Gefährdungen.
Sichtbar nur bei vernetzter Anlage (qa_vernetzt), ausgenommen Softwarestand."""
from .common import *

# ---- Fragen ----------------------------------------------------------------
yn('qn_segmentierung', 'Ist das Aufzugsnetz vom Gebäude-/Büronetz und vom Internet '
   'getrennt (eigenes Segment, Firewall, keine direkte Erreichbarkeit der '
   'Steuerung von außen)?', ui='4.1', visible_when=yes('qa_vernetzt'))
yn('qn_fern_freigabe', 'Wird ein Fernzugriff nur nach Freigabe durch den Betreiber '
   'und nur für die Dauer des Bedarfs aktiviert?', ui='4.2',
   visible_when=yes('qa_vernetzt'))
yn('qn_fern_auth', 'Ist der Fernzugriff individuell authentifiziert (personen'
   'bezogene Zugänge, Zwei-Faktor oder gleichwertig) und verschlüsselt?', ui='4.3',
   visible_when=yes('qa_vernetzt'))
yn('qn_protokoll', 'Werden Zugriffe auf die Anlage (vor Ort über Servicegeräte und '
   'per Fernzugriff) protokolliert und die Protokolle ausgewertet?', ui='4.4')
sel('qn_softwarestand', 'Software-/Firmwarestand und bekannte Schwachstellen', ui='4.5',
    options=[('geregelt', 'Stand bekannt; Sicherheitsupdates und Schwachstellen'
                          'hinweise des Herstellers werden geregelt umgesetzt'),
             ('bekannt_ungeregelt', 'Stand bekannt, aber kein Verfahren für Updates/'
                                    'Schwachstellenhinweise'),
             ('unbekannt', 'Stand nicht bekannt / nicht dokumentiert')],
    help='TRBS 1115-1: Herstellerhinweise zu Schwachstellen sind Teil des Stands '
         'der Technik (EK-ZÜS B-002 Anhang 2 Nr. 5 und 10).')
yn('qn_funktionsreduzierung', 'Sind nicht benötigte Funktionen, Ports, Dienste und '
   'Schnittstellen deaktiviert (Funktionsreduzierung)?', ui='4.6')

# ---- Klärungen -------------------------------------------------------------
k('K-C14', 'Netz', 'Unbekannter Softwarestand',
  'Software-/Firmwarestand nicht bekannt: Mittel – oder nur Dokumentation?',
  'Mittel', 'Niedrig / nur Dokumentation',
  'Ohne bekannten Stand kann kein Abgleich mit Schwachstellenhinweisen erfolgen; '
  'B-002 Anhang 2 Nr. 5 und 10 verlangen genau das.')
k('K-C22', 'Netz', 'Fehlende Funktionsreduzierung',
  'Nicht benötigte Funktionen/Ports aktiv: Niedrig – und Mittel bei vernetzter '
  'Anlage?', 'Niedrig; Mittel bei Netz-/Fernanbindung', 'Immer Niedrig',
  'Funktionsreduzierung ist eine der sechs Maßnahmenkategorien der TRBS 1115-1; '
  'ohne Vernetzung ist die Angriffsfläche lokal begrenzt.')

# ---- Gefährdungen ----------------------------------------------------------
hz('CY-N01', 'Unbekannte oder ungepatchte Schwachstellen (Softwarestand)', GRP_HAERTUNG,
   [('qn_softwarestand', 'TRIGGER', 'ALWAYS'),
    ('qa_vernetzt', 'MODIFIER', 'NEVER')],
   [r(all_(eq('qn_softwarestand', 'bekannt_ungeregelt'), yes('qa_vernetzt')), 'HIGH',
      prio=300,
      sofort='Bekannte Schwachstellen mit dem Hersteller abklären; Fernzugänge bis '
             'zur Klärung deaktivieren',
      mittel='Update- und Schwachstellenverfahren mit Hersteller und Wartungsfirma '
             'vertraglich festlegen'),
    r(eq('qn_softwarestand', 'bekannt_ungeregelt'), 'MEDIUM', prio=250,
      sofort='Herstellerhinweise zu Schwachstellen einholen und bewerten',
      mittel='Update- und Schwachstellenverfahren festlegen (Zuständigkeit, Fristen)'),
    r(eq('qn_softwarestand', 'unbekannt'), 'LOW', prio=240,
      sofort='Software-/Firmwarestände aller programmierbaren Komponenten erfassen',
      mittel='Versionsdokumentation einführen und mit Herstellerhinweisen abgleichen',
      klaerung=['K-C14'])],
   sources=[trbs1115('3.3 Stand der Technik'), zues_b002('Anhang 2 Nr. 5, 10')],
   factor=F_MANIP, persons=[NUTZER, WARTUNG, BETREIBER], bereich='N')

hz('CY-N02', 'Fehlende Härtung: nicht benötigte Funktionen und Schnittstellen aktiv',
   GRP_HAERTUNG,
   [('qn_funktionsreduzierung', 'TRIGGER', 'ALWAYS'),
    ('qa_vernetzt', 'MODIFIER', 'NEVER')],
   [r(all_(no('qn_funktionsreduzierung'), yes('qa_vernetzt')), 'MEDIUM', prio=300,
      sofort='Nicht benötigte Netzdienste, Ports und Fernfunktionen deaktivieren',
      mittel='Funktionsumfang je Komponente festlegen und dokumentieren '
             '(Funktionsreduzierung nach TRBS 1115-1)',
      klaerung=['K-C22']),
    r(no('qn_funktionsreduzierung'), 'LOW', prio=250,
      sofort='Nicht benötigte lokale Schnittstellen und Funktionen deaktivieren',
      mittel='Funktionsumfang je Komponente festlegen und dokumentieren',
      klaerung=['K-C22'])],
   sources=[trbs1115('4.5.2 Funktionsreduzierung'), dekra('Schritt 3')],
   factor=F_MANIP, persons=[NUTZER, WARTUNG], bereich='N')
