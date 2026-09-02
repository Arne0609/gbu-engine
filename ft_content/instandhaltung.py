# -*- coding: utf-8 -*-
"""I – Instandhaltung, Montage und Reinigung (Arbeitsplatz-GBU).

Gliederung nach den drei Arbeitsplätzen der DGUV Information 209-085 Anhang 2:
Zugang zur Anlage · Umkehr- und Antriebsstation · Arbeiten im Stufen- und
Palettenband. Ergänzt um DGUV Information 208-029 (Montage, Demontage,
Instandhaltung).

Die Ampel-Einstufungen der DGUV sind ausdrücklich nur Orientierung; sie sind
hier als eigene Regeln mit Quellenbezug umgesetzt und über die Klärungsliste
zur Bestätigung gestellt. Der gesamte Bereich wird über
qa_teil_instandhaltung abgeschaltet, wenn nur die Betreiber-GBU erstellt wird.

Grundsatz der DGUV 209-085: Bei roter Einstufung darf die Tätigkeit erst
begonnen werden, wenn Sofortmaßnahmen das Risiko auf ein akzeptables Maß
reduziert haben."""
from .common import *

IH = ('qa_teil_instandhaltung', 'APPLICABILITY', 'NEVER')

# ---- Fragen: Zugang und Sicherung des Arbeitsbereichs ----------------------
yn('qi_absperrung', 'Arbeitsbereich wird vor Beginn der Arbeiten vollständig gegen '
   'Publikums- und Fahrzeugverkehr abgesperrt (beide Zugänge, ausreichender '
   'Abstand)?', ui='8.1')
yn('qi_absperrung_material', 'Geeignetes, standsicheres Absperrmaterial ist '
   'vorhanden (nicht nur Flatterband)?', ui='8.2')
yn('qi_absperrung_aufsicht', 'Bei nicht einsehbaren Bereichen oder starkem '
   'Publikumsverkehr ist eine Aufsicht bzw. Postenstellung vorgesehen?', ui='8.3')
yn('qi_zugangsbeleuchtung', 'Ausreichende Beleuchtung im Zugangs- und Arbeitsbereich '
   'vorhanden (auch bei abgeschalteter Anlage)?', ui='8.4')
yn('qi_wege_zustand', 'Wege zum Arbeitsplatz frei, trittsicher und gekennzeichnet '
   '(nicht eng, nicht rutschig, keine Stolperstellen)?', ui='8.5')
yn('qi_absturz_zugang', 'Absturzgefahr auf dem Weg zum Arbeitsplatz (offene '
   'Abdeckung, Treppenauge, Galeriekante, Grube)?', ui='8.6')
yn('qi_absturz_gesichert', 'Absturzstellen im Arbeitsbereich wirksam gesichert '
   '(Umwehrung, Abdeckung, Anschlagpunkt und PSAgA)?', ui='8.6a',
   visible_when=yes('qi_absturz_zugang'))
yn('qi_material_transport', 'Transport von Werkzeug, Ersatzteilen und Hebehilfen zum '
   'Arbeitsplatz ohne besondere Erschwernis möglich?', ui='8.7')

# ---- Fragen: Freischalten und Elektrik -------------------------------------
yn('qi_hauptschalter', 'Hauptschalter vorhanden, gekennzeichnet und aus dem '
   'Arbeitsbereich erreichbar?', ui='9.1')
yn('qi_hauptschalter_sicherbar', 'Hauptschalter in Aus-Stellung abschließbar '
   '(Sicherung gegen Wiedereinschalten)?', ui='9.2')
yn('qi_freischalten_geregelt', 'Freischalten und Sichern gegen Wiedereinschalten ist '
   'im Arbeitsablauf verbindlich geregelt und wird angewendet?', ui='9.3')
yn('qi_elektrik_beruehrsicher', 'Elektrische Bauteile im Arbeitsbereich '
   'berührungssicher abgedeckt (Klemmen, Schaltschrank, Steuerung)?', ui='9.4')
yn('qi_leitungen_zustand', 'Leitungen, Steckvorrichtungen und Betriebsmittel '
   'unbeschädigt und geprüft (DGUV Vorschrift 3)?', ui='9.5')
yn('qi_nothalt_arbeitsbereich', 'Vom Arbeitsplatz aus ist eine NOT-HALT-Einrichtung '
   'erreichbar?', ui='9.6')

# ---- Fragen: Umkehr- und Antriebsstation -----------------------------------
yn('qi_einstiegshilfe', 'Sichere Einstiegshilfe in die Umkehr- bzw. Antriebsstation '
   'vorhanden (Tritt, Leiter, Podest)?', ui='10.1',
   visible_when=yes('qa_station_begehbar'))
yn('qi_stufenabdeckung', 'Abdeckung der geöffneten Stufen-/Palettenöffnung in der '
   'Station vorhanden und tragfähig?', ui='10.2')
yn('qi_abdeckungen_gewicht', 'Bodenbleche und Abdeckungen lassen sich ohne '
   'Überlastung handhaben oder es stehen Hebehilfen zur Verfügung?', ui='10.3')
yn('qi_schutzabdeckungen', 'Schutzabdeckungen an Antrieb, Kette, Rollen und '
   'rotierenden Teilen vollständig und wirksam?', ui='10.4')
yn('qi_station_platz', 'Ausreichend Bewegungsraum in der Station (kein Arbeiten in '
   'dauerhafter Zwangshaltung)?', ui='10.5')
yn('qi_station_sauber', 'Station frei von Öl, Fett, Abfall, Wasser und '
   'Vogelkot/Nagerbefall?', ui='10.6')

# ---- Fragen: Inspektionssteuerung und Arbeiten im Band ---------------------
sel('qi_inspektionssteuerung', 'Inspektionssteuerung für Instandhaltungsarbeiten',
    ui='11.1',
    options=[('zweiknopf', 'Vorhanden, Zweiknopf-/Zustimmungsausführung'),
             ('einknopf', 'Vorhanden, Einknopf-Ausführung'),
             ('keine', 'Nicht vorhanden')])
yn('qi_insp_leitung', 'Leitung der Inspektionssteuerung reicht bis an jeden '
   'Arbeitsplatz im Band?', ui='11.2',
   visible_when=nin('qi_inspektionssteuerung', ['keine']))
yn('qi_band_breite_ok', 'Im geöffneten Stufen-/Palettenband steht eine nutzbare '
   'Breite von mindestens 0,80 m zur Verfügung?', ui='11.3')
yn('qi_band_beleuchtung', 'Ausreichende Beleuchtung im geöffneten Band vorhanden '
   '(ortsveränderliche Leuchte, Schutzkleinspannung)?', ui='11.4')
yn('qi_band_sicherung', 'Stufen-/Palettenband ist während der Arbeiten gegen '
   'unbeabsichtigte Bewegung gesichert (Freischalten oder Zustimmungssteuerung)?',
   ui='11.5')
yn('qi_band_zugang', 'Sicherer Ein- und Ausstieg in das geöffnete Band möglich?',
   ui='11.6')

# ---- Fragen: Koordination und Notfall --------------------------------------
yn('qi_koordination', 'Bei mehreren Beschäftigten oder Gewerken ist eine '
   'koordinierende Person benannt und die Verständigung gesichert (Sicht- oder '
   'Sprechverbindung)?', ui='12.1')
yn('qi_alleinarbeit', 'Wird an der Anlage allein gearbeitet?', ui='12.2')
yn('qi_alleinarbeit_massnahme', 'Bei Alleinarbeit ist eine Überwachung oder '
   'Personen-Notsignal-Anlage vorhanden?', ui='12.2a',
   visible_when=yes('qi_alleinarbeit'))
yn('qi_fremdfirma_koordination', 'Zusammenarbeit von Betreiber und Fremdfirma ist '
   'geregelt (Koordinator, Einweisung, Freigabe des Arbeitsbereichs)?', ui='12.3',
   visible_when=nin('qa_ih_durchfuehrung', ['eigen']))
yn('qi_betriebsanweisung', 'Betriebsanweisung und Herstellervorgaben für die '
   'Instandhaltung liegen am Arbeitsplatz vor?', ui='12.4')
yn('qi_psa', 'Erforderliche PSA ist vorhanden und wird benutzt (Schutzschuhe, '
   'Handschutz, Kopfschutz, ggf. PSAgA)?', ui='12.5')

# ---- Klärungen -------------------------------------------------------------
k('K-I01', 'Instandhaltung', 'Absperrung',
  'Fehlende Absperrung gegen Publikumsverkehr: Hoch wie in DGUV 209-085?',
  'Hoch (Übernahme der DGUV-Einstufung)',
  'Mittel bei geringem Publikumsaufkommen und ständiger Sichtverbindung',
  'DGUV stuft rot ein, weist die Einstufung aber ausdrücklich als Orientierung aus.')
k('K-I02', 'Instandhaltung', 'Einknopf-Inspektionssteuerung',
  'Einknopf-Inspektionssteuerung: Mittel (DGUV) oder Hoch?',
  'Mittel (Übernahme der DGUV-Einstufung)',
  'Hoch, wenn zugleich im geöffneten Band gearbeitet wird', '')
k('K-I03', 'Instandhaltung', 'Bandbreite unter 0,80 m',
  'Arbeiten im Band unter 0,80 m Breite: Hoch mit Tätigkeitsverbot?',
  'Hoch; Arbeiten im Band erst nach zusätzlichen Maßnahmen (z. B. Arbeiten von '
  'außen, Demontage weiterer Stufen)',
  'Mittel, wenn nur kurzzeitig und mit Zustimmungssteuerung gearbeitet wird',
  'DGUV führt die Unterschreitung als roten Zustand.')
k('K-I04', 'Instandhaltung', 'Hauptschalter nicht abschließbar',
  'Hauptschalter nicht in Aus-Stellung abschließbar: Hoch oder Mittel?',
  'Hoch (entspricht der Festlegung beim Aufzugstyp, K-M02)',
  'Mittel, wenn der Schalter im abgesperrten Bereich liegt und beaufsichtigt wird',
  'Beim mehrfragigen Aufzugstyp wurde Hoch entschieden – Konsistenz prüfen.')
k('K-I05', 'Instandhaltung', 'Alleinarbeit',
  'Alleinarbeit an der geöffneten Anlage ohne Überwachung: Hoch oder Mittel?',
  'Hoch bei Arbeiten im geöffneten Band, sonst Mittel',
  'Durchgängig Mittel', 'Die DGUV-Information nennt Alleinarbeit nicht als '
  'eigenen Zustand; die Einstufung ist eigene Festlegung.')
k('K-I06', 'Instandhaltung', 'Vogelkot und biologische Stoffe',
  'Verunreinigung durch Vogelkot oder Nagerbefall in der Station: Mittel?',
  'Mittel mit Sofortmaßnahme fachgerechte Reinigung und Atemschutz',
  'Niedrig, wenn nur kleinflächig', '')

# ---- Gefährdungen: Zugang und Sicherung ------------------------------------
hz('FT-I01', 'Gefährdung durch Publikums- und Fahrzeugverkehr im Arbeitsbereich',
   GRP_ABSPERR,
   [IH,
    ('qi_absperrung', 'TRIGGER', 'ALWAYS'),
    ('qi_absperrung_material', 'TRIGGER', 'ALWAYS'),
    ('qi_absperrung_aufsicht', 'COMPENSATION', 'ALWAYS'),
    ('qa_oeffentlich', 'MODIFIER', 'NEVER')],
   [r(no('qi_absperrung'), 'HIGH', prio=300,
      sofort='Arbeiten erst nach vollständiger Absperrung beider Zugänge beginnen; '
             'laufende Arbeiten unterbrechen',
      mittel='Absperrkonzept mit Material, Abstand und Zuständigkeit festlegen und '
             'in die Betriebsanweisung aufnehmen',
      klaerung=['K-I01']),
    r(no('qi_absperrung_material'), 'MEDIUM', prio=250,
      sofort='Standsicheres Absperrmaterial beschaffen; bis dahin Postenstellung',
      mittel='Absperrmaterial als feste Ausstattung des Wartungsfahrzeugs bzw. der '
             'Anlage vorhalten'),
    r(all_(yes('qa_oeffentlich'), no('qi_absperrung_aufsicht')), 'MEDIUM', prio=200,
      sofort='Bei starkem Publikumsverkehr eine Aufsicht stellen',
      mittel='Postenstellung bzw. zeitliche Verlagerung der Arbeiten in verkehrsarme '
             'Zeiten festlegen')],
   sources=[d209_085('Anh. 2, Zugang'), d208_029(), betrsichv('§ 4')],
   factor=F_STOSS, persons=[WARTUNG, NUTZER, FREMDFIRMEN], bereich='I')

hz('FT-I02', 'Unzureichende Beleuchtung im Zugangs- und Arbeitsbereich', GRP_LICHT,
   [IH, ('qi_zugangsbeleuchtung', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_zugangsbeleuchtung'), 'HIGH',
      sofort='Arbeiten erst nach Aufstellen einer ausreichenden Ersatzbeleuchtung '
             'beginnen',
      mittel='Feste Beleuchtung im Zugangs- und Arbeitsbereich herstellen bzw. '
             'geeignete ortsveränderliche Leuchten als Ausrüstung vorhalten')],
   sources=[d209_085('Anh. 2, Zugang'), asr34(), d208_029()],
   factor=F_BELEUCHTUNG, persons=[WARTUNG, REINIGUNG], bereich='I')

hz('FT-I03', 'Sturz und Stolpern auf dem Weg zum Arbeitsplatz', GRP_ABSPERR,
   [IH, ('qi_wege_zustand', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_wege_zustand'), 'MEDIUM',
      sofort='Weg frei räumen, reinigen und beleuchten; Stolperstellen kennzeichnen',
      mittel='Verkehrsweg zum Arbeitsplatz dauerhaft herrichten und kennzeichnen')],
   sources=[d209_085('Anh. 2, Zugang'), asr18(), d208_029()],
   factor=F_STURZ, persons=[WARTUNG, REINIGUNG], bereich='I')

hz('FT-I04', 'Absturz im Zugangs- und Arbeitsbereich', GRP_ABSPERR,
   [IH,
    ('qi_absturz_zugang', 'TRIGGER', 'ALWAYS'),
    ('qi_absturz_gesichert', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': yes('qi_absturz_zugang')})],
   [r(all_(yes('qi_absturz_zugang'), no('qi_absturz_gesichert')), 'HIGH', prio=300,
      sofort='Arbeiten erst nach Sicherung der Absturzstelle aufnehmen (Abdeckung, '
             'Umwehrung oder Anschlagpunkt und PSAgA)',
      mittel='Dauerhafte Absturzsicherung bzw. Anschlageinrichtung vorsehen und in '
             'die Arbeitsverfahren aufnehmen'),
    r(yes('qi_absturz_zugang'), 'LOW', prio=200,
      sofort='Wirksamkeit der Sicherung vor Arbeitsbeginn prüfen',
      mittel='Absturzsicherung in die wiederkehrende Prüfung der Arbeitsmittel '
             'aufnehmen')],
   sources=[d209_085('Anh. 2, Zugang'), d208_029(), betrsichv('Anh. 1')],
   factor=F_ABSTURZ, persons=[WARTUNG, FREMDFIRMEN], bereich='I')

hz('FT-I05', 'Erschwerter Transport von Material, Werkzeug und Hebehilfen',
   GRP_ABSPERR,
   [IH, ('qi_material_transport', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_material_transport'), 'LOW',
      sofort='Transportweg vorab festlegen; Lasten aufteilen und zu zweit tragen',
      mittel='Transporthilfen bereitstellen und den Zugang für den Materialtransport '
             'herrichten')],
   sources=[d208_029(), src('OTHER', 'DGUV Information 208-005')],
   factor=F_ERGONOMIE, persons=[WARTUNG], bereich='I')

# ---- Gefährdungen: Freischalten und Elektrik -------------------------------
hz('FT-I10', 'Unbeabsichtigtes Ingangsetzen der Anlage während der Arbeiten',
   GRP_ELEKTRO,
   [IH,
    ('qi_hauptschalter', 'TRIGGER', 'ALWAYS'),
    ('qi_hauptschalter_sicherbar', 'TRIGGER', 'ALWAYS'),
    ('qi_freischalten_geregelt', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_hauptschalter'), 'HIGH', prio=300,
      sofort='Arbeiten erst nach sicherer Trennung von der Energieversorgung '
             'beginnen (Sicherungen entfernen und sichern)',
      mittel='Erreichbaren, gekennzeichneten Hauptschalter nachrüsten'),
    r(no('qi_hauptschalter_sicherbar'), 'HIGH', prio=280,
      sofort='Hauptschalter durch eine benannte Person besetzen oder mit '
             'Verriegelungseinrichtung sichern, bevor die Arbeiten beginnen',
      mittel='Abschließbaren Hauptschalter nachrüsten (Sicherung gegen '
             'Wiedereinschalten)',
      klaerung=['K-I04']),
    r(no('qi_freischalten_geregelt'), 'HIGH', prio=250,
      sofort='Vor jeder Arbeit freischalten, gegen Wiedereinschalten sichern und '
             'Spannungsfreiheit feststellen',
      mittel='Verbindliche Regelung zum Freischalten und Sichern in die '
             'Betriebsanweisung aufnehmen und unterweisen')],
   sources=[d209_085('Anh. 2'), d208_029(), betrsichv('§ 8'),
            src('DGUV', 'DGUV Vorschrift 3')],
   factor=F_BEWEGT, persons=[WARTUNG, FREMDFIRMEN, REINIGUNG], bereich='I')

hz('FT-I11', 'Elektrische Gefährdung durch nicht berührungssichere Bauteile und '
   'schadhafte Betriebsmittel', GRP_ELEKTRO,
   [IH,
    ('qi_elektrik_beruehrsicher', 'TRIGGER', 'ALWAYS'),
    ('qi_leitungen_zustand', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_elektrik_beruehrsicher'), 'HIGH', prio=300,
      sofort='Arbeiten erst nach Freischalten oder Herstellen der Berührungs'
             'sicherheit beginnen; Bereich kennzeichnen',
      mittel='Abdeckungen ergänzen und Zustand in die Elektroprüfung aufnehmen'),
    r(no('qi_leitungen_zustand'), 'HIGH', prio=250,
      sofort='Schadhafte Leitungen und Betriebsmittel sofort der Benutzung entziehen',
      mittel='Prüfung ortsveränderlicher Betriebsmittel nach DGUV Vorschrift 3 '
             'organisieren und dokumentieren')],
   sources=[d209_085('Anh. 2'), src('DGUV', 'DGUV Vorschrift 3'), d208_029()],
   factor=F_ELEKTRISCH, persons=[WARTUNG, FREMDFIRMEN], bereich='I')

hz('FT-I12', 'NOT-HALT vom Arbeitsplatz aus nicht erreichbar', GRP_NOTHALT,
   [IH, ('qi_nothalt_arbeitsbereich', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_nothalt_arbeitsbereich'), 'HIGH',
      sofort='Zweite Person an einer NOT-HALT-Einrichtung positionieren oder '
             'ortsveränderliche Not-Halt-/Zustimmungseinrichtung einsetzen',
      mittel='Erreichbare NOT-HALT-Einrichtung im Arbeitsbereich nachrüsten')],
   sources=[d209_085('Anh. 2'), en115_1('5.12'), d208_029()],
   factor=F_BEWEGT, persons=[WARTUNG], bereich='I')

# ---- Gefährdungen: Umkehr- und Antriebsstation -----------------------------
hz('FT-I20', 'Absturz und Sturz beim Einstieg in die Umkehr- und Antriebsstation',
   GRP_STATION,
   [IH,
    ('qa_station_begehbar', 'APPLICABILITY', 'NEVER'),
    ('qi_einstiegshilfe', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qa_station_begehbar')})],
   [r(no('qi_einstiegshilfe'), 'HIGH',
      sofort='Arbeiten erst nach Bereitstellen einer sicheren Einstiegshilfe '
             '(Tritt, Leiter, Podest) beginnen',
      mittel='Feste oder mitgeführte Einstiegshilfe für die Station vorsehen')],
   sources=[d209_085('Anh. 2, Umkehr-/Antriebsstation'), d208_029()],
   factor=F_ABSTURZ, persons=[WARTUNG], bereich='I')

hz('FT-I21', 'Absturz in die geöffnete Stufen-/Palettenöffnung der Station',
   GRP_STATION,
   [IH, ('qi_stufenabdeckung', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_stufenabdeckung'), 'HIGH',
      sofort='Öffnung vor Arbeitsbeginn tragfähig abdecken oder wirksam umwehren; '
             'Bereich absperren',
      mittel='Passende, tragfähige Abdeckung für die Station beschaffen und '
             'vorhalten')],
   sources=[d209_085('Anh. 2, Umkehr-/Antriebsstation'), d208_029()],
   factor=F_ABSTURZ, persons=[WARTUNG, FREMDFIRMEN], bereich='I')

hz('FT-I22', 'Überlastung und Quetschung beim Handhaben von Abdeckungen und '
   'Bodenblechen', GRP_STATION,
   [IH, ('qi_abdeckungen_gewicht', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_abdeckungen_gewicht'), 'MEDIUM',
      sofort='Abdeckungen nur zu zweit und mit geeigneten Griffen bewegen',
      mittel='Hebehilfen bereitstellen bzw. geteilte oder leichtere Abdeckungen '
             'vorsehen')],
   sources=[d208_029(), src('LAW', 'LasthandhabV')],
   factor=F_ERGONOMIE, persons=[WARTUNG], bereich='I')

hz('FT-I23', 'Erfassen und Einziehen an ungeschützten Antriebs- und Umlaufteilen',
   GRP_STATION,
   [IH, ('qi_schutzabdeckungen', 'TRIGGER', 'ALWAYS'),
    ('qi_band_sicherung', 'COMPENSATION', 'ALWAYS')],
   [r(all_(no('qi_schutzabdeckungen'), no('qi_band_sicherung')), 'HIGH', prio=300,
      sofort='Arbeiten erst nach Freischalten und Sichern gegen Wiedereinschalten '
             'beginnen; fehlende Abdeckungen ersetzen',
      mittel='Schutzabdeckungen vollständig herstellen und in die wiederkehrende '
             'Prüfung aufnehmen'),
    r(no('qi_schutzabdeckungen'), 'HIGH', prio=250,
      sofort='Fehlende Schutzabdeckungen vor Wiederinbetriebnahme montieren; bis '
             'dahin Anlage nicht in Betrieb nehmen',
      mittel='Schutzabdeckungen vollständig herstellen und dokumentiert prüfen')],
   sources=[d209_085('Anh. 2, Umkehr-/Antriebsstation'), en115_1('5.9'), d208_029()],
   factor=F_ROTIEREND, persons=[WARTUNG], bereich='I')

hz('FT-I24', 'Zwangshaltung und beengte Verhältnisse in der Station', GRP_STATION,
   [IH, ('qi_station_platz', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_station_platz'), 'LOW',
      sofort='Arbeitszeit im beengten Bereich begrenzen und Pausen einplanen; '
             'Arbeiten möglichst von außen ausführen',
      mittel='Arbeitsverfahren und Hilfsmittel so wählen, dass Zwangshaltungen '
             'vermieden werden')],
   sources=[d208_029(), src('OTHER', 'ASR A1.2')],
   factor=F_ERGONOMIE, persons=[WARTUNG], bereich='I')

hz('FT-I25', 'Gefahrstoffe, Öl, Fett und biologische Arbeitsstoffe im Arbeitsbereich',
   GRP_STOFFE,
   [IH, ('qi_station_sauber', 'TRIGGER', 'ALWAYS'),
    ('qa_aufstellung', 'MODIFIER', 'NEVER')],
   [r(all_(no('qi_station_sauber'), nin('qa_aufstellung', ['innen'])), 'MEDIUM',
      prio=300,
      sofort='Verunreinigung vor Arbeitsbeginn fachgerecht beseitigen; bei Vogelkot '
             'oder Nagerbefall Atemschutz und Einweganzug benutzen',
      mittel='Reinigungsintervall für die Station festlegen; Zugang für Tiere '
             'verschließen',
      klaerung=['K-I06']),
    r(no('qi_station_sauber'), 'MEDIUM', prio=200,
      sofort='Öl- und Fettrückstände sowie Abfall vor Arbeitsbeginn entfernen',
      mittel='Reinigungsintervall festlegen und Leckagen im Antrieb abstellen',
      klaerung=['K-I06'])],
   sources=[d209_085('Anh. 2'), d208_029(), src('LAW', 'GefStoffV'),
            src('LAW', 'BioStoffV')],
   factor=F_GEFAHRSTOFF, persons=[WARTUNG, REINIGUNG], bereich='I')

# ---- Gefährdungen: Inspektionssteuerung und Arbeiten im Band ---------------
hz('FT-I30', 'Fehlende oder unzureichende Inspektionssteuerung', GRP_INSP,
   [IH,
    ('qi_inspektionssteuerung', 'TRIGGER', 'ALWAYS'),
    ('qi_insp_leitung', 'TRIGGER', 'CONDITIONAL',
     {'required_when': nin('qi_inspektionssteuerung', ['keine'])})],
   [r(eq('qi_inspektionssteuerung', 'keine'), 'HIGH', prio=300,
      sofort='Arbeiten am bewegten Band unterlassen; nur freigeschaltet arbeiten '
             'oder eine mitgeführte Zustimmungssteuerung einsetzen',
      mittel='Inspektionssteuerung mit Zustimmungsfunktion nachrüsten'),
    r(all_(nin('qi_inspektionssteuerung', ['keine']), no('qi_insp_leitung')), 'HIGH',
      prio=280,
      sofort='Arbeiten nur im freigeschalteten Zustand ausführen, solange die '
             'Steuerung den Arbeitsplatz nicht erreicht',
      mittel='Leitungslänge der Inspektionssteuerung an die Anlagenlänge anpassen'),
    r(eq('qi_inspektionssteuerung', 'einknopf'), 'MEDIUM', prio=200,
      sofort='Bandbewegung nur auf Zuruf und mit zweiter Person an der NOT-HALT-'
             'Einrichtung; kein Aufenthalt im Gefahrbereich',
      mittel='Auf Zweiknopf- bzw. Zustimmungsausführung umrüsten',
      klaerung=['K-I02'])],
   sources=[d209_085('Anh. 2, Stufen-/Palettenband'), d208_029(), en115_1('5.12')],
   factor=F_BEWEGT, persons=[WARTUNG], bereich='I')

hz('FT-I31', 'Arbeiten im geöffneten Stufen-/Palettenband bei zu geringer Breite',
   GRP_BAND,
   [IH,
    ('qi_band_breite_ok', 'TRIGGER', 'ALWAYS'),
    ('qa_bandbreite', 'DOCUMENTATION', 'NEVER')],
   [r(no('qi_band_breite_ok'), 'HIGH',
      sofort='Arbeiten im Band erst nach zusätzlichen Maßnahmen aufnehmen: weitere '
             'Stufen/Paletten demontieren, von außen arbeiten oder das Bauteil '
             'ausbauen',
      mittel='Arbeitsverfahren für schmale Anlagen festlegen und in die '
             'Betriebsanweisung aufnehmen',
      klaerung=['K-I03'])],
   sources=[d209_085('Anh. 2, Stufen-/Palettenband'), d208_029()],
   factor=F_QUETSCH, persons=[WARTUNG], bereich='I')

hz('FT-I32', 'Unzureichende Beleuchtung im geöffneten Stufen-/Palettenband',
   GRP_BAND,
   [IH, ('qi_band_beleuchtung', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_band_beleuchtung'), 'HIGH',
      sofort='Arbeiten erst nach Aufstellen einer geeigneten Leuchte '
             '(Schutzkleinspannung) beginnen',
      mittel='Geeignete ortsveränderliche Beleuchtung als feste Ausrüstung vorhalten')],
   sources=[d209_085('Anh. 2, Stufen-/Palettenband'), asr34(), d208_029()],
   factor=F_BELEUCHTUNG, persons=[WARTUNG], bereich='I')

hz('FT-I33', 'Quetschen und Einziehen durch unbeabsichtigte Bandbewegung während '
   'der Arbeiten im Band', GRP_BAND,
   [IH,
    ('qi_band_sicherung', 'TRIGGER', 'ALWAYS'),
    ('qi_band_zugang', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_band_sicherung'), 'HIGH', prio=300,
      sofort='Arbeiten unterbrechen; Band freischalten und gegen Wiedereinschalten '
             'sichern oder ausschließlich mit Zustimmungssteuerung bewegen',
      mittel='Arbeitsverfahren mit verbindlicher Sicherung des Bandes festlegen und '
             'unterweisen'),
    r(no('qi_band_zugang'), 'MEDIUM', prio=200,
      sofort='Sicheren Ein- und Ausstieg herstellen (Trittfläche, Haltemöglichkeit)',
      mittel='Zugangslösung für das geöffnete Band beschaffen und vorhalten')],
   sources=[d209_085('Anh. 2, Stufen-/Palettenband'), d208_029()],
   factor=F_QUETSCH, persons=[WARTUNG], bereich='I')

# ---- Gefährdungen: Koordination, Alleinarbeit, Organisation ----------------
hz('FT-I40', 'Fehlende Koordination bei mehreren Beschäftigten oder Gewerken',
   GRP_KOORD,
   [IH,
    ('qi_koordination', 'TRIGGER', 'ALWAYS'),
    ('qa_ih_durchfuehrung', 'MODIFIER', 'NEVER'),
    ('qi_fremdfirma_koordination', 'TRIGGER', 'CONDITIONAL',
     {'required_when': all_(yes('qa_teil_instandhaltung'),
                            nin('qa_ih_durchfuehrung', ['eigen']))})],
   [r(no('qi_koordination'), 'HIGH', prio=300,
      sofort='Vor Arbeitsbeginn eine koordinierende Person benennen und die '
             'Verständigung sicherstellen (Sicht- oder Sprechverbindung)',
      mittel='Koordinationsregelung schriftlich festlegen und unterweisen'),
    r(no('qi_fremdfirma_koordination'), 'MEDIUM', prio=200,
      sofort='Arbeitsbereich förmlich übergeben und die Fremdfirma einweisen',
      mittel='Verfahren zur Freigabe und Rücknahme des Arbeitsbereichs mit der '
             'Fremdfirma vereinbaren')],
   sources=[betrsichv('§ 13'), src('LAW', 'ArbSchG', '§ 8'), d208_029()],
   factor=F_ORGA, persons=[WARTUNG, FREMDFIRMEN, BESCHAEFTIGTE], bereich='I')

hz('FT-I41', 'Alleinarbeit an der geöffneten Anlage', GRP_KOORD,
   [IH,
    ('qi_alleinarbeit', 'TRIGGER', 'ALWAYS'),
    ('qi_alleinarbeit_massnahme', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': yes('qi_alleinarbeit')})],
   [r(all_(yes('qi_alleinarbeit'), no('qi_alleinarbeit_massnahme')), 'HIGH', prio=300,
      sofort='Arbeiten an der geöffneten Anlage nicht allein ausführen; zweite '
             'Person hinzuziehen',
      mittel='Personen-Notsignal-Anlage oder gleichwertige Überwachung einführen und '
             'Alleinarbeit in der Gefährdungsbeurteilung regeln',
      klaerung=['K-I05']),
    r(yes('qi_alleinarbeit'), 'LOW', prio=200,
      sofort='Funktion der Überwachung vor Arbeitsbeginn prüfen',
      mittel='Regelung zur Alleinarbeit regelmäßig überprüfen',
      klaerung=['K-I05'])],
   sources=[d208_029(), src('DGUV', 'DGUV Regel 100-001', 'Abschn. 2.7')],
   factor=F_NOTFALL, persons=[WARTUNG], bereich='I')

hz('FT-I42', 'Fehlende Betriebsanweisung und PSA für die Instandhaltung', GRP_KOORD,
   [IH,
    ('qi_betriebsanweisung', 'TRIGGER', 'ALWAYS'),
    ('qi_psa', 'TRIGGER', 'ALWAYS')],
   [r(no('qi_psa'), 'MEDIUM', prio=200,
      sofort='Erforderliche PSA vor Arbeitsbeginn bereitstellen und benutzen',
      mittel='PSA-Ausstattung festlegen, beschaffen und die Benutzung kontrollieren'),
    r(no('qi_betriebsanweisung'), 'MEDIUM', prio=150,
      sofort='Herstellervorgaben und Betriebsanweisung am Arbeitsplatz bereitstellen',
      mittel='Betriebsanweisung auf Grundlage der Gefährdungsbeurteilung erstellen '
             'und unterweisen')],
   sources=[betrsichv('§ 12'), d208_029(), src('LAW', 'PSA-BV')],
   factor=F_ORGA, persons=[WARTUNG, FREMDFIRMEN], bereich='I', agg='MAXIMUM')
