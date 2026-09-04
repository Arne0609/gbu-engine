# -*- coding: utf-8 -*-
"""Z – Zugang und Zugriff: physischer Zugang zu Steuerung, Triebwerksraum und
Schacht (geteilte Modifier für alle Komponenten, Muster Schindler 14.1–14.4,
eigenständig umgesetzt), logische Zugangskontrolle (Zugangsdaten, Rollen),
Servicegeräte und Wechseldatenträger (TRBS 1115-1 „Zugangskontrolle Hardware/
Software", „Härtung")."""
from .common import *

# ---- Fragen ----------------------------------------------------------------
yn('qz_steuerung_frei', 'Ist die Aufzugssteuerung (Steuerschrank, Bedien-/Service'
   'einheit) für Unbefugte frei zugänglich?', ui='2.1',
   help='Ja = ohne Schlüssel oder Werkzeug erreichbar (z. B. Steuerschrank im '
        'öffentlichen Flur unverschlossen, Schranktür ohne Schloss).')
yn('qz_triebwerksraum_frei', 'Ist der Triebwerks-/Maschinenraum für Unbefugte frei '
   'zugänglich?', ui='2.2', visible_when=yes('qa_maschinenraum'))
yn('qz_schacht_frei', 'Ist der Aufzugsschacht für Unbefugte frei zugänglich '
   '(Grubenzugang, Schachttür ohne Notentriegelungsschutz, offene Wartungs'
   'klappe)?', ui='2.3')
yn('qz_service_gesichert', 'Sind die Service- und Programmierschnittstellen '
   '(Serviceanschluss, USB, Speicherkarte, Diagnosestecker) gegen unbefugte '
   'Nutzung gesichert (verschlossene Abdeckung, Freigabe nur mit Schlüssel/'
   'Code)?', ui='2.4')
yn('qz_default_zugangsdaten', 'Werden Standard-/Werkszugangsdaten (Passwörter, '
   'PINs, Servicecodes) verwendet oder sind die Zugangsdaten nicht bekannt?',
   ui='2.5', help='Ja = Mangel. Gemeint sind alle Zugänge: Steuerung, Notruf, '
                  'Umrichter, Gateway, Fernwartung.')
yn('qz_rollen', 'Sind Zugriffsrechte rollenbasiert vergeben (Betreiber, '
   'Wartungsfirma, Hersteller) und werden sie bei Personal- oder Firmenwechsel '
   'entzogen?', ui='2.6')
yn('qz_servicegeraete', 'Ist geregelt, welche Servicegeräte, Laptops und Wechsel'
   'datenträger an die Anlage angeschlossen werden dürfen (nur freigegebene, '
   'geprüfte Geräte; kein privater Datenträger)?', ui='2.7')

# ---- Klärungen -------------------------------------------------------------
k('K-C12', 'Zugang', 'Frei zugängliche Steuerung',
  'Steuerung für Unbefugte frei zugänglich: Mittel (wie Schindler MC1) – und '
  'Hoch, wenn zusätzlich die Serviceschnittstellen ungesichert sind?',
  'Mittel; Hoch mit ungesicherten Serviceschnittstellen',
  'Durchgängig Mittel (Schindler-Verhalten)',
  'Schindler MC1 kennt nur „Für Unbefugte ist der Zugang möglich" = Mittel; die '
  'Kombination mit offenem Serviceanschluss ist dort nicht abgebildet.')
k('K-C13', 'Zugang', 'Default-Zugangsdaten',
  'Werkszugangsdaten in Gebrauch: Mittel – und Hoch bei vernetzter Anlage?',
  'Mittel; Hoch bei Netz-/Fernanbindung',
  'Immer Mittel',
  'Bei Fernanbindung sind Werkspasswörter aus der Ferne ausnutzbar; TRBS 1115-1 '
  'nennt Zugangskontrolle (Software) als Mindestmaßnahme.')
k('K-C21', 'Zugang', 'Triebwerksraum und Schacht',
  'Freier Zugang zu Triebwerksraum bzw. Schacht als eigene Cyber-Gefährdung '
  '(Mittel) – oder nur als Modifier an den Komponenten?',
  'Eigene Gefährdung Mittel (Muster MC1) und Modifier',
  'Nur Modifier, keine eigene Stufe (Zugang wird in der technischen GBU bewertet)',
  'Schindler MC2/MC3 sind nicht beobachtet; die Ortsfragen 14.2/14.4 wirken dort '
  'nachweislich auf mehrere Komponenten.')

# ---- Gefährdungen ----------------------------------------------------------
hz('CY-Z01', 'Unbefugter physischer Zugang zur Aufzugssteuerung', GRP_ZUGANG,
   [('qz_steuerung_frei', 'TRIGGER', 'ALWAYS'),
    ('qz_service_gesichert', 'TRIGGER', 'ALWAYS')],
   [r(all_(yes('qz_steuerung_frei'), no('qz_service_gesichert')), 'HIGH', prio=300,
      sofort='Steuerschrank verschließen bzw. Zugang beschränken; Service- und '
             'Programmierschnittstellen sofort gegen Nutzung sichern',
      mittel='Verschließeinrichtung nachrüsten; Zugangskontrolle (Hardware) nach '
             'TRBS 1115-1 festlegen und dokumentieren',
      klaerung=['K-C12']),
    r(yes('qz_steuerung_frei'), 'MEDIUM', prio=250,
      sofort='Zugang zur Steuerung auf Berechtigte beschränken (Schloss, '
             'Schlüsselregelung)',
      mittel='Geeignete Verschließeinrichtung nachrüsten und Schlüsselverwaltung '
             'festlegen',
      klaerung=['K-C12'], evidence='HIGH_CONFIDENCE',
      notes='Entspricht dem beobachteten Ergebnis Schindler MC1 (Mittel).'),
    r(no('qz_service_gesichert'), 'LOW', prio=200,
      sofort='Serviceschnittstellen abdecken/verschließen oder Freigabe nur mit '
             'Schlüssel/Code',
      mittel='Zugangskontrolle (Hardware) für Service- und Programmierzugänge '
             'dauerhaft festlegen')],
   sources=[trbs1115('4.5.2 Zugangskontrolle'), zues_ba017(), betrsichv('§ 3 Abs. 1')],
   factor=F_ZUGANG, persons=[NUTZER, WARTUNG, BETREIBER], bereich='Z')

# CY-Z02/CY-Z03 (Triebwerksraum/Schacht frei zugänglich) entfallen nach K-C21:
# die Zugangsfragen wirken nur noch als Modifier an den Komponenten; der
# Zugang selbst wird in der technischen GBU bewertet.

hz('CY-Z04', 'Unzureichende logische Zugangskontrolle (Werkszugangsdaten, fehlende '
   'Rollen)', GRP_ZUGANG,
   [('qz_default_zugangsdaten', 'TRIGGER', 'ALWAYS'),
    ('qz_rollen', 'TRIGGER', 'ALWAYS'),
    ('qa_vernetzt', 'MODIFIER', 'NEVER')],
   [r(all_(yes('qz_default_zugangsdaten'), yes('qa_vernetzt')), 'HIGH', prio=300,
      sofort='Werkszugangsdaten unverzüglich ändern; Fernzugänge bis dahin '
             'deaktivieren',
      mittel='Passwort-/Berechtigungskonzept (Zugangskontrolle Software) mit '
             'individuellen Zugängen einführen',
      klaerung=['K-C13']),
    r(yes('qz_default_zugangsdaten'), 'MEDIUM', prio=250,
      sofort='Werkszugangsdaten ändern und sicher verwahren',
      mittel='Passwort-/Berechtigungskonzept einführen und Wechsel bei '
             'Personal- oder Firmenwechsel festlegen',
      klaerung=['K-C13']),
    r(no('qz_rollen'), 'LOW', prio=200,
      sofort='Zugriffsrechte prüfen und nicht mehr benötigte Zugänge entziehen',
      mittel='Rollenkonzept (Betreiber, Wartung, Hersteller) mit Entzug bei '
             'Wechsel festlegen')],
   sources=[trbs1115('4.5.2 Zugangskontrolle (Software)'), dekra('Schritt 3')],
   factor=F_ZUGANG, persons=[NUTZER, WARTUNG, BETREIBER], bereich='Z')

hz('CY-Z05', 'Ungeregelte Servicegeräte und Wechseldatenträger', GRP_HAERTUNG,
   [('qz_servicegeraete', 'TRIGGER', 'ALWAYS')],
   [r(no('qz_servicegeraete'), 'MEDIUM', prio=250,
      sofort='Anschluss privater oder ungeprüfter Geräte und Datenträger untersagen',
      mittel='Freigabeliste für Servicegeräte und Datenträger mit der Wartungsfirma '
             'vereinbaren (Härtung nach TRBS 1115-1)')],
   sources=[trbs1115('4.5.2 Härtung'), zues_ba017()],
   factor=F_MANIP, persons=[NUTZER, WARTUNG], bereich='Z')
