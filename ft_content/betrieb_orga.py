# -*- coding: utf-8 -*-
"""B – Betreiberorganisation: Kontrollen, Prüfung, Unterweisung, Störungen.

Fahrtreppen und Fahrsteige sind ausdrücklich KEINE überwachungsbedürftigen
Anlagen (BetrSichV Anhang 2 Nr. 2 nimmt sie aus). Es gibt daher weder ZÜS noch
Zwischenprüfung; maßgeblich sind § 3 (Gefährdungsbeurteilung) und § 14
(Prüfung durch eine zur Prüfung befähigte Person) sowie die Herstellervorgaben."""
from .common import *

# ---- Fragen ----------------------------------------------------------------
yn('qb_kontrolle_taeglich', 'Tägliche Sicht- und Funktionskontrolle vor dem '
   'Einschalten festgelegt und durchgeführt?', ui='7.1',
   help='Nach DGUV Information 208-028 gehört dazu mindestens ein beobachteter '
        'Umlauf des Stufen-/Palettenbandes.')
yn('qb_kontrolle_umlauf', 'Umfasst die Kontrolle einen beobachteten vollständigen '
   'Umlauf des Stufen-/Palettenbandes?', ui='7.2',
   visible_when=yes('qb_kontrolle_taeglich'))
yn('qb_kontrolle_doku', 'Ergebnis der Kontrolle wird dokumentiert?', ui='7.3',
   visible_when=yes('qb_kontrolle_taeglich'))
yn('qb_kontrolle_person', 'Die kontrollierende Person ist benannt und unterwiesen?',
   ui='7.4', visible_when=yes('qb_kontrolle_taeglich'))

yn('qb_pruefung_bp', 'Wiederkehrende Prüfung durch eine zur Prüfung befähigte Person '
   'festgelegt (Art, Umfang, Frist aus der Gefährdungsbeurteilung)?', ui='7.5')
sel('qb_pruefung_frist', 'Tatsächlicher Prüfabstand der letzten Prüfungen', ui='7.6',
    visible_when=yes('qb_pruefung_bp'),
    options=[('bis_12', 'Bis 12 Monate'),
             ('bis_24', 'Über 12 bis 24 Monate'),
             ('ueber_24', 'Über 24 Monate'),
             ('unbekannt', 'Nicht nachvollziehbar')],
    help='Bewährte Orientierung ist ein jährlicher Abstand; maßgeblich ist die '
         'Festlegung aus der Gefährdungsbeurteilung.')
yn('qb_pruefung_maengel', 'Mängel aus der letzten Prüfung vollständig abgearbeitet?',
   ui='7.7', visible_when=yes('qb_pruefung_bp'))
yn('qb_wartungsvertrag', 'Wartung nach Herstellervorgaben vertraglich geregelt und '
   'die Intervalle werden eingehalten?', ui='7.8')
yn('qb_unterlagen', 'Betriebsanleitung, Wartungs- und Prüfnachweise vorhanden und '
   'verfügbar?', ui='7.9')

yn('qb_unterweisung', 'Beschäftigte, die die Anlage bedienen oder in ihrem Umfeld '
   'arbeiten, sind unterwiesen (Bedienung, NOT-HALT, Verhalten bei Störung)?',
   ui='7.10')
yn('qb_unterweisung_jaehrlich', 'Unterweisung wird mindestens jährlich wiederholt und '
   'dokumentiert?', ui='7.10a', visible_when=yes('qb_unterweisung'))
yn('qb_stoerung_geregelt', 'Verhalten bei Störung und Stillstand ist geregelt '
   '(Abschalten, Absperren, Meldung, Freigabe erst nach Kontrolle)?', ui='7.11')
yn('qb_absperrmaterial', 'Geeignetes Absperrmaterial ist vor Ort verfügbar?', ui='7.12')
yn('qb_reinigung_betrieb', 'Wird die Anlage im laufenden Betrieb gereinigt?', ui='7.13')
yn('qb_reinigung_unterwiesen', 'Reinigungskräfte sind für Arbeiten an der Anlage '
   'unterwiesen und die zulässigen Reinigungsverfahren sind festgelegt?', ui='7.14')
yn('qb_notfall_meldung', 'Meldekette für Unfälle und eingeklemmte Personen ist '
   'festgelegt und bekannt?', ui='7.15')

# ---- Klärungen -------------------------------------------------------------
k('K-B11', 'Betreiberorganisation', 'Prüffrist',
  'Prüfabstand über 24 Monate ohne besondere Begründung: Mittel oder Hoch?',
  'Mittel; Hoch nur, wenn zusätzlich Mängel aus der letzten Prüfung offen sind',
  'Hoch (faktisch ungeprüfte Anlage im Publikumsverkehr)',
  'Die BetrSichV nennt keine feste Frist; jährlich ist die bewährte Orientierung '
  'der DGUV Information 208-028.')
k('K-B12', 'Betreiberorganisation', 'Fehlende tägliche Kontrolle',
  'Keine tägliche Sicht- und Funktionskontrolle: Mittel oder Hoch?',
  'Mittel; Hoch bei öffentlich zugänglicher Anlage',
  'Durchgängig Mittel (organisatorischer Mangel ohne unmittelbare Gefährdung)', '')
k('K-B13', 'Betreiberorganisation', 'Reinigung im laufenden Betrieb',
  'Reinigung des laufenden Bandes durch Reinigungskräfte: eigene Stufe Hoch?',
  'Hoch, wenn die Reinigungskräfte nicht unterwiesen sind; sonst Mittel',
  'Immer Hoch (Einzugsgefahr an Kamm und Sockel)', '')
k('K-B14', 'Betreiberorganisation', 'Dokumentation der Kontrolle',
  'Kontrolle wird durchgeführt, aber nicht dokumentiert: Niedrig oder nur Hinweis?',
  'Niedrig', 'Nur Dokumentation ohne Stufe',
  'Ohne Nachweis ist die Durchführung im Schadensfall nicht belegbar.')

# ---- Gefährdungen ----------------------------------------------------------
hz('FT-B30', 'Unerkannte Mängel durch fehlende tägliche Sicht- und Funktions'
   'kontrolle', GRP_PRUEF,
   [('qb_kontrolle_taeglich', 'TRIGGER', 'ALWAYS'),
    ('qb_kontrolle_umlauf', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_kontrolle_taeglich')}),
    ('qb_kontrolle_person', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_kontrolle_taeglich')}),
    ('qb_kontrolle_doku', 'DOCUMENTATION', 'CONDITIONAL',
     {'required_when': yes('qb_kontrolle_taeglich')}),
    ('qa_oeffentlich', 'MODIFIER', 'NEVER')],
   [r(all_(no('qb_kontrolle_taeglich'), yes('qa_oeffentlich')), 'HIGH', prio=300,
      sofort='Tägliche Sicht- und Funktionskontrolle sofort einführen und eine '
             'verantwortliche Person benennen',
      mittel='Kontrollumfang, Zuständigkeit und Nachweisführung schriftlich festlegen '
             '(Betriebsanweisung)',
      klaerung=['K-B12']),
    r(no('qb_kontrolle_taeglich'), 'MEDIUM', prio=250,
      sofort='Tägliche Sicht- und Funktionskontrolle einführen',
      mittel='Kontrollumfang und Zuständigkeit schriftlich festlegen',
      klaerung=['K-B12']),
    r(no('qb_kontrolle_umlauf'), 'MEDIUM', prio=200,
      sofort='Kontrolle um einen beobachteten vollständigen Bandumlauf erweitern',
      mittel='Checkliste für die tägliche Kontrolle erstellen (Stufen, Paletten, '
             'Kämme, Handläufe, NOT-HALT, freie Zugänge)'),
    r(no('qb_kontrolle_person'), 'MEDIUM', prio=180,
      sofort='Kontrollierende Person benennen und unterweisen',
      mittel='Unterweisung und Vertretungsregelung dauerhaft festlegen'),
    r(no('qb_kontrolle_doku'), 'LOW', prio=150,
      sofort='Kontrollergebnis ab sofort dokumentieren',
      mittel='Nachweisführung (Kontrollbuch, digitale Erfassung) einführen',
      klaerung=['K-B14'])],
   sources=[betrsichv('§ 4'), d208_028('Abschn. 6'), asr18()],
   factor=F_ORGA, persons=[NUTZER, BESCHAEFTIGTE, BETREIBER], bereich='B')

hz('FT-B31', 'Fehlende oder überfällige Prüfung durch eine zur Prüfung befähigte '
   'Person', GRP_PRUEF,
   [('qb_pruefung_bp', 'TRIGGER', 'ALWAYS'),
    ('qb_pruefung_frist', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_pruefung_bp')}),
    ('qb_pruefung_maengel', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_pruefung_bp')})],
   [r(no('qb_pruefung_bp'), 'HIGH', prio=300,
      sofort='Prüfung durch eine zur Prüfung befähigte Person unverzüglich '
             'veranlassen',
      mittel='Art, Umfang und Frist der wiederkehrenden Prüfung in der '
             'Gefährdungsbeurteilung festlegen und die Prüforganisation aufbauen'),
    r(all_(in_('qb_pruefung_frist', ['ueber_24', 'unbekannt']),
           no('qb_pruefung_maengel')), 'HIGH', prio=280,
      sofort='Prüfung nachholen und die offenen Mängel unverzüglich abarbeiten',
      mittel='Prüffristen und Mängelverfolgung verbindlich regeln und überwachen',
      klaerung=['K-B11']),
    r(in_('qb_pruefung_frist', ['ueber_24', 'unbekannt']), 'MEDIUM', prio=250,
      sofort='Prüfung kurzfristig nachholen',
      mittel='Prüffrist an der bewährten jährlichen Orientierung ausrichten und '
             'begründet in der Gefährdungsbeurteilung festlegen',
      klaerung=['K-B11']),
    r(no('qb_pruefung_maengel'), 'MEDIUM', prio=200,
      sofort='Offene Mängel bewerten und die sicherheitsrelevanten sofort abstellen',
      mittel='Mängelverfolgung mit Fristen und Verantwortlichkeit einführen'),
    r(eq('qb_pruefung_frist', 'bis_24'), 'LOW', prio=150,
      sofort='Prüfabstand begründen oder verkürzen',
      mittel='Festlegung des Prüfabstands in der Gefährdungsbeurteilung '
             'nachvollziehbar dokumentieren',
      klaerung=['K-B11'])],
   sources=[betrsichv('§ 14'), betrsichv('§ 3'), d208_028('Abschn. 7')],
   factor=F_ORGA, persons=[NUTZER, BESCHAEFTIGTE, BETREIBER], bereich='B')

hz('FT-B32', 'Wartung nicht nach Herstellervorgaben und fehlende Unterlagen',
   GRP_PRUEF,
   [('qb_wartungsvertrag', 'TRIGGER', 'ALWAYS'),
    ('qb_unterlagen', 'TRIGGER', 'ALWAYS'),
    ('qa_normstand', 'DOCUMENTATION', 'NEVER'),
    ('qa_vernetzt', 'DOCUMENTATION', 'NEVER')],
   [r(no('qb_wartungsvertrag'), 'MEDIUM', prio=200,
      sofort='Wartung kurzfristig beauftragen und die versäumten Leistungen nachholen',
      mittel='Wartungsvertrag nach Herstellervorgaben abschließen und die Intervalle '
             'überwachen'),
    r(no('qb_unterlagen'), 'MEDIUM', prio=150,
      sofort='Fehlende Unterlagen beim Hersteller oder Wartungsunternehmen anfordern',
      mittel='Anlagendokumentation vollständig aufbauen und zugänglich vorhalten')],
   sources=[betrsichv('§ 3'), d208_028(), en115_2()],
   factor=F_ORGA, persons=[BETREIBER, WARTUNG], bereich='B', agg='MAXIMUM')

hz('FT-B33', 'Fehlende Unterweisung der Beschäftigten', GRP_ORGA,
   [('qb_unterweisung', 'TRIGGER', 'ALWAYS'),
    ('qb_unterweisung_jaehrlich', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_unterweisung')}),
    ('qa_arbeitsstaette', 'MODIFIER', 'NEVER')],
   [r(no('qb_unterweisung'), 'MEDIUM', prio=200,
      sofort='Beschäftigte vor der nächsten Schicht zu Bedienung, NOT-HALT und '
             'Verhalten bei Störung unterweisen',
      mittel='Unterweisungskonzept mit Inhalten, Turnus und Nachweis festlegen'),
    r(no('qb_unterweisung_jaehrlich'), 'LOW', prio=150,
      sofort='Unterweisung auffrischen und dokumentieren',
      mittel='Jährliche Wiederholungsunterweisung fest einplanen')],
   sources=[src('LAW', 'ArbSchG', '§ 12'), betrsichv('§ 12'), d208_028()],
   factor=F_ORGA, persons=[BESCHAEFTIGTE], bereich='B', agg='MAXIMUM')

hz('FT-B34', 'Unklares Verhalten bei Störung und Stillstand', GRP_ORGA,
   [('qb_stoerung_geregelt', 'TRIGGER', 'ALWAYS'),
    ('qb_absperrmaterial', 'TRIGGER', 'ALWAYS'),
    ('qb_notfall_meldung', 'TRIGGER', 'ALWAYS')],
   [r(no('qb_stoerung_geregelt'), 'MEDIUM', prio=200,
      sofort='Vorgehen bei Störung schriftlich festlegen und bekannt machen '
             '(abschalten, absperren, melden, Freigabe erst nach Kontrolle)',
      mittel='Betriebsanweisung erstellen und in die Unterweisung aufnehmen'),
    r(no('qb_absperrmaterial'), 'MEDIUM', prio=180,
      sofort='Absperrmaterial beschaffen und an der Anlage bereitstellen',
      mittel='Absperrmaterial als feste Ausstattung vorhalten und den Lagerort '
             'bekannt machen'),
    r(no('qb_notfall_meldung'), 'MEDIUM', prio=150,
      sofort='Meldekette festlegen und an der Anlage aushängen',
      mittel='Notfallorganisation mit Rettungsdienst und Wartungsunternehmen '
             'abstimmen')],
   sources=[betrsichv('§ 4'), d208_028(), asr18()],
   factor=F_NOTFALL, persons=[NUTZER, BESCHAEFTIGTE], bereich='B', agg='MAXIMUM')

hz('FT-B35', 'Gefährdung von Reinigungskräften bei Arbeiten an der Anlage',
   GRP_ORGA,
   [('qb_reinigung_betrieb', 'TRIGGER', 'ALWAYS'),
    ('qb_reinigung_unterwiesen', 'COMPENSATION', 'ALWAYS')],
   [r(all_(yes('qb_reinigung_betrieb'), no('qb_reinigung_unterwiesen')), 'HIGH',
      prio=300,
      sofort='Reinigung des laufenden Bandes sofort einstellen; Reinigung nur bei '
             'abgeschalteter und gegen Wiedereinschalten gesicherter Anlage',
      mittel='Reinigungsverfahren festlegen, Reinigungskräfte unterweisen und die '
             'Freigabe durch eine benannte Person regeln',
      klaerung=['K-B13']),
    r(yes('qb_reinigung_betrieb'), 'MEDIUM', prio=250,
      sofort='Reinigung im laufenden Betrieb auf das unvermeidbare Maß beschränken '
             'und Einzugsstellen aussparen',
      mittel='Reinigung außerhalb der Betriebszeit bei abgeschalteter Anlage '
             'organisieren',
      klaerung=['K-B13']),
    r(no('qb_reinigung_unterwiesen'), 'MEDIUM', prio=200,
      sofort='Reinigungskräfte vor dem nächsten Einsatz unterweisen',
      mittel='Zulässige Reinigungsmittel und -verfahren mit dem Hersteller abstimmen '
             'und schriftlich festlegen')],
   sources=[d208_028(), d208_029(), betrsichv('§ 12')],
   factor=F_EINZUG, persons=[REINIGUNG, FREMDFIRMEN], bereich='B')
