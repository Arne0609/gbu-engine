# -*- coding: utf-8 -*-
"""T – Schachttüren / Fahrkorbtür und K – Fahrkorb (Blaupause: Schindler M001,
M002, M004, M023, M027, M032, M057, M063, M064, M067, M074, M076, M079, M083,
M085, M086, M119; Inhalte aus App-Kategorien K1–K10, K13–K17, F5)."""
from .common import *

GRP_T = 'Türen und Verriegelung'
GRP_K = 'Fahrkorb und Nutzung'
GRP_NOT = 'Notruf und Personenbefreiung'
GRP_ANT = 'Antrieb, Bremse und Hydraulik'
GRP_SK = 'Sicherheitskomponenten'
GRP_BEL = 'Beleuchtung'
GRP_BRAND = 'Brandschutz und Gebäudeschnittstelle'

SEIL = in_('qa_aufzugsart', ['seil', 'trommel', 'seil_hydraulik'])
HYDR = in_('qa_aufzugsart', ['hydraulik', 'seil_hydraulik'])
GLAS_TUER = any_(yes('qa_glas_schachttueren'), yes('qa_glas_fahrkorbtueren'))

# ---- Fragen T --------------------------------------------------------------
yn('qt_verriegelung_elektrisch', 'Schachttürverriegelung vom Sicherheitskreis elektrisch '
   'überwacht?', ui='7.1')
yn('qt_fehlschliess', 'Fehlschließsicherung / Nachschließeinrichtung an den Schachttüren '
   'vorhanden?', ui='7.2')
yn('qt_selbstschliessend', 'Schachttüren selbstschließend (Feder oder Gewicht)?', ui='7.3')
yn('qt_schliesst_nach_notentriegelung', 'Schließt die Schachttür nach einer '
   'Notentriegelung selbsttätig?', ui='7.4')
yn('qt_notentriegelung_alle', 'Notentriegelung an allen Schachttüren vorhanden?', ui='7.5')
yn('qt_dreikant_hinterlegt', 'Passender Entriegelungsschlüssel (Dreikant) für die '
   'Personenbefreiung vor Ort hinterlegt?', ui='7.6')
yn('qt_notentriegelung_hoehe', 'Notentriegelung erreichbar (max. 2,00 m über Boden im '
   'Türblatt bzw. 2,70 m im Rahmen mit langem Schlüssel)?', ui='7.7',
   visible_when=yes('qt_notentriegelung_alle'))
yn('qt_glas_normgerecht', 'Glaseinsätze in Schacht-/Fahrkorbtüren aus normgerechtem, '
   'unbeschädigtem Glas (Verbundsicherheitsglas nach EN 81-20 5.3.5.3)?', ui='7.8',
   visible_when=GLAS_TUER)
yn('qt_glas_drahtglas', 'Drahtglas (Gitterglas) verbaut?', ui='7.9', visible_when=GLAS_TUER)
yn('qt_glas_einzugsschutz', 'Schutz gegen Einziehen von Kinderhänden an Glas-Schiebetüren '
   'vorhanden (Sensorleiste, Abstand, Beschichtung)?', ui='7.10', visible_when=GLAS_TUER)
sel('qt_feuerwiderstand', 'Feuerwiderstandsfähigkeit der Schachttüren (EN 81-58 / '
    'bauaufsichtliche Anforderung)', ui='7.11',
    options=[('nachgewiesen', 'Nachgewiesen (Zertifikat vorhanden)'),
             ('nicht_gefordert', 'Nicht gefordert (kein Brandschutzerfordernis)'),
             ('unbekannt', 'Unbekannt / kein Nachweis'),
             ('nicht_gegeben', 'Gefordert, aber nicht gegeben')])
yn('qt_fk_tuer_automatisch', 'Fahrkorbtür kraftbetätigt (automatisch)?', ui='8.7',
   visible_when=yes('qa_fahrkorbtuer'))
sel('qt_schliesskante', 'Schließkantensicherung der Fahrkorbtür', ui='8.8',
    options=[('lichtgitter', 'Lichtgitter / Lichtvorhang (vollflächige Personenerkennung)'),
             ('lichtschranke', 'Einzel-Lichtschranke mit Kraftbegrenzung 150 N / 10 J (ältere Ausführung)'),
             ('umsteuer', 'Umsteuereinrichtung (Schachtdrehtür)'),
             ('andere', 'Andere Schließkantensicherung'),
             ('keine', 'Keine Schließkantensicherung')],
    visible_when=yes('qa_fahrkorbtuer'))
yn('qt_lichtgitter_ohne_tuer', 'Ohne Fahrkorbtür: Sicherheitslichtgitter vorhanden?',
   ui='8.9', visible_when=no('qa_fahrkorbtuer'))
yn('qt_scherengitter', 'Ohne Fahrkorbtür: Scherengitter vorhanden?', ui='8.9a',
   visible_when=no('qa_fahrkorbtuer'))

# ---- Fragen K --------------------------------------------------------------
yn('qk_notruf_vorhanden', 'Notrufeinrichtung im Fahrkorb vorhanden?', ui='8.1')
sel('qk_notruf_art', 'Art der Notrufeinrichtung', ui='8.2',
    options=[('sprech_staendig', 'Sprechverbindung zu ständig besetzter Stelle'),
             ('klingel_staendig', 'Klingel zu ständig besetzter Stelle'),
             ('nicht_staendig', 'Sprechverbindung oder Klingel zu nicht ständig besetzter Stelle'),
             ('klingel_schacht', 'Klingel im Schacht ohne Weiterleitung')],
    visible_when=yes('qk_notruf_vorhanden'))
yn('qk_notruf_24h', 'Notruf auf eine rund um die Uhr besetzte Stelle aufgeschaltet?',
   ui='8.3', visible_when=yes('qk_notruf_vorhanden'))
yn('qk_notruf_en8128', 'Zweiwege-Notrufsystem nach EN 81-28 (Identifikation, '
   'Rückmeldung, Testruf)?', ui='8.4', visible_when=yes('qk_notruf_vorhanden'))
sel('qk_notbeleuchtung', 'Notbeleuchtung im Fahrkorb', ui='8.5',
    options=[('netzersatz', 'Leuchte mit Netzersatzfunktion (mind. 5 Lux, 1 h)'),
             ('nur_taster', 'Keine Notbeleuchtung, aber beleuchteter Notruftaster'),
             ('keine', 'Keine Notbeleuchtung')])
num('qk_stufe_mm', 'Größte gemessene Stufenbildung / Haltegenauigkeit [mm]', min=0, max=300, ui='8.10')
yn('qk_nachregulierung', 'Nachregulierung / geregelter Antrieb mit präziser Haltegenauigkeit?',
   ui='8.11')
num('qk_schuerze_mm', 'Länge der Fahrkorbtürschürze [mm]', min=0, max=2500, ui='8.12')
yn('qk_befreiung_nur_fachkundig', 'Personenbefreiung ausschließlich durch fachkundige '
   'Personen (Betriebsanweisung, keine Selbstbefreiung durch Aufzugswärter)?', ui='8.13',
   visible_when=lt('qk_schuerze_mm', 300))
num('qk_abstand_schwelle_mm', 'Größter Abstand Fahrkorbschwelle – Schachtwand [mm]', min=0, max=1500, ui='8.14')
yn('qk_fk_tuer_verriegelt', 'Fahrkorbtür-Verriegelung (Fahrkorbtür außerhalb der '
   'Entriegelungszone verriegelt)?', ui='8.15', visible_when=gt('qk_abstand_schwelle_mm', 150))
yn('qk_schachttuer_zusatzverriegelung', 'Zusatzverriegelung an den Schachttüren vorhanden?',
   ui='8.15a', visible_when=gt('qk_abstand_schwelle_mm', 150))
yn('qk_nennlast_gekennz', 'Nennlast und zulässige Personenzahl im Fahrkorb gekennzeichnet?',
   ui='8.16')
yn('qk_nutzflaeche_ok', 'Nutzfläche des Fahrkorbs passt zur Nennlast (Tabelle EN 81-20 5.4.2)?',
   ui='8.17')
yn('qk_ueberlast', 'Überlastkontrolle / Lastmessung vorhanden?', ui='8.18')
yn('qk_ueberlast_geprueft', 'Funktion der Überlastkontrolle nachweislich geprüft?',
   ui='8.18a', visible_when=yes('qk_ueberlast'))
sel('qk_lueftung', 'Lüftung des Fahrkorbs', ui='8.19',
    options=[('ausreichend', 'Lüftungsöffnungen ausreichend (≥ 1 % der Grundfläche) und frei'),
             ('verdeckt', 'Lüftungsöffnungen teilweise verdeckt oder verschmutzt'),
             ('keine_zwang', 'Keine Zwangsbelüftung bei langen Fahrzeiten / hoher Belegung'),
             ('unzureichend', 'Lüftungsöffnungen fehlen oder unzureichend')])
yn('qk_hinweis_brandfall', 'Hinweisschild „Aufzug im Brandfall nicht benutzen" an allen '
   'Haltestellen vorhanden und lesbar?', ui='8.20')
yn('qk_bfs_vorhanden', 'Brandfallsteuerung vorhanden und in die Brandmeldeanlage '
   'eingebunden?', ui='8.21', visible_when=yes('qa_bfs_gefordert'))
yn('qk_bfs_geprueft', 'Funktion der Brandfallsteuerung regelmäßig geprüft (Nachweis)?',
   ui='8.21a', visible_when=yes('qk_bfs_vorhanden'))
yn('qk_en8170', 'Anlage nach DIN EN 81-70 barrierefrei ausgeführt?', ui='8.22',
   visible_when=yes('qa_nutzung_pmem'))
yn('qk_bedienelemente', 'Bedienelemente in erreichbarer Höhe und ertastbar?', ui='8.23',
   visible_when=yes('qa_nutzung_pmem'))
yn('qk_rollstuhl_mass', 'Fahrkorbabmessungen für Rollstuhlnutzung ausreichend '
   '(mind. 1,00 m × 1,25 m)?', ui='8.24', visible_when=yes('qa_nutzung_pmem'))
sel('qk_ausstattung', 'Zustand der Fahrkorbausstattung', ui='8.25',
    options=[('ok', 'Unbeschädigt, keine Hinweise auf Vandalismus'),
             ('ohne_gef', 'Beschädigt ohne unmittelbare Gefährdung (Tableau, Spiegel, Verkleidung)'),
             ('mit_gef', 'Beschädigt mit unmittelbarer Gefährdung (freiliegende Elektrik, '
                         'gebrochenes Glas, defekter Notruf)')])
yn('qk_vandalismus_wiederholt', 'Wiederholte Vandalismusschäden?', ui='8.26')
yn('qk_en8171', 'Vandalismussichere Ausführung nach DIN EN 81-71?', ui='8.26a',
   visible_when=yes('qk_vandalismus_wiederholt'))
yn('qk_ucm_sr_modul', 'Türüberbrückung (SR-Modul) für Nachregulieren / Voraböffnen '
   'mit offener Tür vorhanden?', ui='8.27',
   visible_when=not_(in_('qa_aufzugsart', ['hydraulik', 'seil_hydraulik'])),
   help='Bei Hydraulikaufzügen nicht gefragt: das Nachregulieren bei Druckverlust setzt die '
   'Türüberbrückung immer voraus (Entscheidung 02.09.2026, K-K12).')
sel('qk_schutz_aufwaerts', 'Schutz gegen Übergeschwindigkeit aufwärts / Sturz nach oben',
    ui='8.28',
    options=[('aktiv', 'Aktive Maßnahme (Notbremssystem / SAFÜ auf Seil oder Treibscheibe)'),
             ('passiv', 'Passive Maßnahme (geringer Beschleunigungsweg, Gegengewichtsverhältnis)'),
             ('nicht', 'Nicht verhindert')],
    visible_when=all_(SEIL, yes('qa_gegengewicht')))

# ---- Klärungen -------------------------------------------------------------
k('K-K01', 'Fahrkorb', 'Notruf ohne 24-h-Aufschaltung',
  'Notruf vorhanden, aber nicht auf eine rund um die Uhr besetzte Stelle aufgeschaltet: '
  'eigene Stufe Mittel?', 'Mittel', 'Kein eigener Beitrag (so verhält sich die Schindler-App)',
  'Schindler M032 wertet nur „Notruf vorhanden?"; 24 h und EN 81-28 ohne Beitrag – fachlich fragwürdig.')
k('K-K02', 'Fahrkorb', 'Fehlende Notbeleuchtung',
  'Keine Notbeleuchtung im Fahrkorb: Mittel (App K10) oder Hoch (Schindler M023)?',
  'Mittel (App)', 'Hoch (Schindler)', 'Abweichung App/Schindler.')
k('K-K03', 'Fahrkorb', 'Stufenbildung bei Personen mit eingeschränkter Mobilität',
  'Stufenbildung 10–20 mm bei zu erwartender Nutzung durch Personen mit eingeschränkter '
  'Mobilität: Hochstufung auf Hoch?', 'Ja (Modifier)', 'Nein, bleibt Mittel',
  'Eigene Regel nach Schindler-Muster (A73 Behindertennutzung als Modifier bei M001).')
k('K-K04', 'Fahrkorb', 'Schwellenabstand',
  'Abstand Fahrkorbschwelle–Schachtwand > 150 mm mit verriegelter Fahrkorbtür: Kein '
  'Risiko (App K8) – reicht die Verriegelung als vollständige Kompensation?', 'Kein Risiko',
  'Niedrig', 'Eigene Nachfrage.')
k('K-K05', 'Fahrkorb', 'Überlastkontrolle nicht geprüft',
  'Überlastkontrolle vorhanden, Funktion nicht nachweislich geprüft: Mittel?', 'Mittel (App K13)',
  'Niedrig', 'Eigene Nachfrage.')
k('K-K06', 'Türen', 'Notentriegelung nicht an allen Zugängen',
  'Notentriegelung fehlt an einzelnen Schachttüren: Mittel (App F5) oder Hoch (Schindler M079)?',
  'Mittel, wenn einzelne fehlen; Hoch, wenn Dreikant/Werkzeug fehlt', 'Immer Hoch',
  'Abweichung App/Schindler.')
k('K-K07', 'Türen', 'Feuerwiderstand unbekannt',
  'Feuerwiderstand der Schachttüren unbekannt (kein Nachweis): Mittel oder nur Dokumentation?',
  'Mittel', 'Dokumentation', 'Schindler M083 = Mittel; im App-Katalog nicht enthalten.')
k('K-K08', 'Fahrkorb', 'UCM „nicht notwendig"',
  'Kein UCM, aber kein SR-Modul, Zweikreisbremse mit Schalter und statisch bestimmte Lagerung: '
  'Mittel (App K4.2) oder Kein Risiko / Niedrig?', 'Mittel (App)', 'Niedrig',
  'Der App-Text sagt „UCM nicht notwendig", bewertet aber gelb.')
k('K-K09', 'Fahrkorb', 'Fahrkorb ohne Tür',
  'Fahrkorb ohne Abschlusstür, aber mit Sicherheitslichtgitter: Mittel (App K2.2). Bei '
  'Nutzung durch Personen mit eingeschränkter Mobilität oder Kinder Hoch?', 'Ja (Modifier)',
  'Nein', 'Schindler M076 nutzt A73 Behindertennutzung als Modifier.')

k('K-T01', 'Türen', 'Drahtglas (TRBS-Matrix)',
  'TRBS 3121 Anh. 1 Nr. 9 nennt das Risiko bei intaktem, sicher befestigtem Drahtglas ausdrücklich '
  'niedrig; der App-Katalog K9 bewertet Gitterglas gelb (Mittel). Umgesetzt: Niedrig.',
  'Niedrig (TRBS-explizit)', 'Mittel (App K9)', 'Neu aus der TRBS-Risikomatrix vom 02.09.2026.')
k('K-T02', 'Türen', 'Einzel-Lichtschranke (TRBS-Matrix)',
  'Neue Option „Einzel-Lichtschranke mit 150 N / 10 J": TRBS 3121 Anh. 1 Nr. 10 = ausdrücklich '
  'Mittel, bei behinderten/alten/gebrechlichen Personen höher. Umgesetzt: Mittel, Hoch mit PmeM-Nutzung.',
  'Mittel / Hoch mit PmeM', 'Option nicht aufnehmen', 'Neu aus der TRBS-Risikomatrix vom 02.09.2026.')
k('K-K10', 'Fahrkorb', 'Warnhinweis als Kompensation bei Stufenbildung (TRBS-Matrix)',
  'TRBS 3121 Anh. 1 Nr. 1 lässt einen Warnhinweis nur bei eingeschränktem Benutzerkreis zu, nicht '
  'bei behindertengerechten Aufzügen. Umgesetzt: Stufe 10–20 mm + eingewiesener Benutzerkreis + '
  'Warnhinweis, keine PmeM-Nutzung = Niedrig (neue Frage 8.10a).',
  'Niedrig als Kompensation', 'Keine Kompensation, bleibt Mittel', 'Neu aus der TRBS-Risikomatrix vom 02.09.2026.')
k('K-K11', 'Fahrkorb', 'UCM ohne Bremsüberwachung (TRBS-Matrix)',
  'TRBS 3121 Anh. 1 Nr. 16: statisch bestimmte Lagerung und Zweikreisbremse OHNE Überwachung = '
  'ausdrücklich Mittel (bisher fiel dieser Fall auf Hoch). Mit Überwachung bleibt es bei der '
  'Entscheidung K-K08 (Niedrig).', 'Mittel (TRBS-explizit)', 'Hoch', 'Neu aus der TRBS-Risikomatrix vom 02.09.2026.')
k('K-K12', 'Fahrkorb', 'Hydraulikaufzug ohne UCM',
  'Hydraulikaufzug ohne UCM-Schutz und ohne Türüberbrückung: Mittel (eigene Annahme; Absinken wird '
  'über MF-M13 Hydraulikeinrichtungen bewertet) – oder Hoch wie bei Seilaufzügen?', 'Mittel', 'Hoch',
  'Letzte Regel ohne Vorlage (HYPOTHESIS); aus dem Review vom 02.09.2026. Entscheidung: der Fall '
  'existiert nicht – ein Hydraulikaufzug hat immer eine Türüberbrückung (Nachregulieren bei Druckverlust).')
# ---- Gefährdungen T --------------------------------------------------------
hz('MF-T01', 'Unsichere Verriegelung der Schachttüren', GRP_T,
   [('qt_verriegelung_elektrisch', 'TRIGGER', 'ALWAYS'),
    ('qt_fehlschliess', 'TRIGGER', 'ALWAYS')],
   [r(no('qt_verriegelung_elektrisch'), 'HIGH', mfrom=('N20-F5', 'Keine Schachttür-Verriegelungen'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qt_fehlschliess'), 'MEDIUM', mfrom=('N20-F5', 'Fehlschließeinrichtung'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.3.9.1'), trbs3121('Anh. 1 Nr. 11')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER], agg='MAXIMUM', bereich='T')

hz('MF-T02', 'Fehlende oder schlecht erreichbare Notentriegelung der Schachttüren', GRP_T,
   [('qt_notentriegelung_alle', 'TRIGGER', 'ALWAYS'),
    ('qt_dreikant_hinterlegt', 'TRIGGER', 'ALWAYS'),
    ('qt_notentriegelung_hoehe', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qt_notentriegelung_alle')})],
   [r(no('qt_dreikant_hinterlegt'), 'HIGH',
      sofort='Entriegelungsschlüssel beschaffen und an der Anlage (Schlüsseltresor) hinterlegen',
      mittel='Schlüsselverwaltung für die Personenbefreiung in der Betriebsanweisung regeln',
      evidence='INFERRED'),
    r(no('qt_notentriegelung_alle'), 'HIGH', mfrom=('N20-F5', 'Notentriegelung nicht'),
      evidence='HIGH_CONFIDENCE', klaerung='K-K06'),
    r(no('qt_notentriegelung_hoehe'), 'MEDIUM',
      sofort='Leiter/Tritt für die Personenbefreiung bereithalten, Beauftragte unterweisen',
      mittel='Notentriegelung in erreichbarer Höhe (max. 2,00 m) nachrüsten oder langen '
             'Entriegelungsschlüssel hinterlegen', evidence='INFERRED')],
   sources=[en8120('5.3.9.3'), trbs3121('Anh. 1 Nr. 11')], factor=F_NOTFALL,
   persons=[NUTZER, BEAUFTRAGTE], agg='MAXIMUM', bereich='T')

hz('MF-T03', 'Schachttüren nicht selbstschließend', GRP_T,
   [('qt_selbstschliessend', 'TRIGGER', 'ALWAYS'),
    ('qt_schliesst_nach_notentriegelung', 'TRIGGER', 'ALWAYS')],
   [r(no('qt_schliesst_nach_notentriegelung'), 'HIGH', mfrom=('N20-K3', 'Schachttür kann'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qt_selbstschliessend'), 'MEDIUM', mfrom=('N20-K3', 'Keine selbstschließenden'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.3.9.3.4'), trbs3121('Anh. 1 Nr. 12')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER], agg='MAXIMUM', bereich='T')

hz('MF-T04', 'Ungeeignetes Glas oder fehlender Einzugsschutz an Türen mit Glas', GRP_T,
   [('qa_glas_schachttueren', 'APPLICABILITY', 'NEVER', {'applicable_when': GLAS_TUER}),
    ('qa_glas_fahrkorbtueren', 'OPTIONAL', 'NEVER'),
    ('qt_glas_normgerecht', 'TRIGGER', 'ALWAYS'),
    ('qt_glas_drahtglas', 'TRIGGER', 'ALWAYS'),
    ('qt_glas_einzugsschutz', 'TRIGGER', 'ALWAYS'),
    ('qa_nutzung_kinder', 'MODIFIER', 'NEVER')],
   [r(no('qt_glas_normgerecht'), 'HIGH', mfrom=('N20-K9', 'Ungeeignetes Glas'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qt_glas_einzugsschutz'), 'HIGH', mfrom=('N20-K2.2', 'Glas-Kabinentür mit Lichtgitter, aber'),
      evidence='HIGH_CONFIDENCE'),
    r(yes('qt_glas_drahtglas'), 'LOW', mfrom=('N20-K9', 'Verwendetes Glas'),
      evidence='HIGH_CONFIDENCE', klaerung='K-T01',
      notes='TRBS 3121 Anh. 1 Nr. 9: Risiko bei intaktem, sicher befestigtem Drahtglas ausdrücklich niedrig (App K9: gelb).')],
   sources=[en8120('5.3.5.3.5'), en8120('5.3.5.3.6'), en8120('5.3.5.3.7'), trbs3121('Anh. 1 Nr. 9')],
   factor=F_GLAS, persons=[NUTZER], agg='MAXIMUM', bereich='T')

hz('MF-T05', 'Unzureichende Feuerwiderstandsfähigkeit der Schachttüren', GRP_BRAND,
   [('qt_feuerwiderstand', 'APPLICABILITY', 'NEVER',
     {'applicable_when': neq('qt_feuerwiderstand', 'nicht_gefordert')}),
    ('qt_feuerwiderstand', 'TRIGGER', 'ALWAYS')],
   [r(eq('qt_feuerwiderstand', 'nicht_gegeben'), 'MEDIUM',
      sofort='Betreiber informieren; Abstimmung mit Brandschutzkonzept / Bauaufsicht',
      mittel='Schachttüren mit nachgewiesener Feuerwiderstandsfähigkeit (EN 81-58) einbauen',
      evidence='INFERRED'),
    r(eq('qt_feuerwiderstand', 'unbekannt'), 'MEDIUM',
      sofort='Nachweis (Zertifikat, Baugenehmigung) beim Betreiber anfordern',
      mittel='Feuerwiderstandsanforderung aus dem Brandschutzkonzept klären und dokumentieren',
      evidence='HYPOTHESIS', klaerung='K-K07')],
   sources=[en('DIN EN 81-58'), en8120('5.3.1.2')], factor=F_BRAND, persons=[NUTZER],
   agg='MAXIMUM', bereich='T')

hz('MF-T06', 'Fahrkorb ohne Abschlusstür oder ohne Schließkantensicherung', GRP_T,
   [('qa_fahrkorbtuer', 'TRIGGER', 'ALWAYS'),
    ('qt_lichtgitter_ohne_tuer', 'COMPENSATION', 'CONDITIONAL', {'required_when': no('qa_fahrkorbtuer')}),
    ('qt_scherengitter', 'COMPENSATION', 'CONDITIONAL', {'required_when': no('qa_fahrkorbtuer')}),
    ('qt_schliesskante', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_fahrkorbtuer')}),
    ('qt_fk_tuer_automatisch', 'OPTIONAL', 'NEVER'),
    ('qa_nutzung_pmem', 'MODIFIER', 'NEVER'),
    ('qa_nutzung_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qa_fahrkorbtuer'), no('qt_lichtgitter_ohne_tuer'), no('qt_scherengitter')), 'HIGH',
      prio=300, mfrom=('N20-K2.2', 'Keine Kabinenabschlusstür und kein'), evidence='HIGH_CONFIDENCE'),
    r(all_(no('qa_fahrkorbtuer'), any_(yes('qa_nutzung_pmem'), yes('qa_nutzung_kinder'))), 'HIGH',
      prio=250, mfrom=('N20-K2.1', 'Keine Kabinenabschlusstür'), evidence='HYPOTHESIS',
      klaerung='K-K09'),
    r(all_(no('qa_fahrkorbtuer'), yes('qt_scherengitter')), 'MEDIUM', prio=200,
      mfrom=('N20-K2.2', 'Keine Kabinenabschlusstür, jedoch Scherengitter'), evidence='HIGH_CONFIDENCE'),
    r(all_(no('qa_fahrkorbtuer'), yes('qt_lichtgitter_ohne_tuer')), 'MEDIUM', prio=200,
      mfrom=('N20-K2.2', 'Keine Kabinenabschlusstür, jedoch Sicherheitslichtgitter'),
      evidence='HIGH_CONFIDENCE'),
    r(all_(yes('qa_fahrkorbtuer'), eq('qt_schliesskante', 'keine')), 'MEDIUM', prio=200,
      mfrom=('N20-K2.2', 'Kabinenabschlusstür ohne Lichtgitter'), evidence='HIGH_CONFIDENCE'),
    r(all_(yes('qa_fahrkorbtuer'), eq('qt_schliesskante', 'lichtschranke'), yes('qa_nutzung_pmem')), 'HIGH',
      prio=210, mfrom=('N20-K2.2', 'Kabinenabschlusstür ohne Lichtgitter'), evidence='INFERRED',
      klaerung='K-T02',
      notes='TRBS 3121 Anh. 1 Nr. 10: 150 N + Lichtschranke + 10 J = Mittel, ausdrücklich NICHT bei behinderten, alten oder gebrechlichen Personen.'),
    r(all_(yes('qa_fahrkorbtuer'), eq('qt_schliesskante', 'lichtschranke')), 'MEDIUM', prio=200,
      mfrom=('N20-K2.2', 'Kabinenabschlusstür ohne Lichtgitter'), evidence='HIGH_CONFIDENCE',
      klaerung='K-T02', notes='TRBS 3121 Anh. 1 Nr. 10: ausdrücklich mittleres Risiko.')],
   sources=[en8120('5.3'), en8120('5.3.6'), trbs3121('Anh. 1 Nr. 10'), trbs3121('Anh. 1 Nr. 14')],
   factor=F_BEWEGT, persons=[NUTZER], bereich='T')

# ---- Gefährdungen K --------------------------------------------------------
hz('MF-K01', 'Fehlende oder unzulängliche Notrufeinrichtung im Fahrkorb', GRP_NOT,
   [('qk_notruf_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qk_notruf_art', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qk_notruf_vorhanden')}),
    ('qk_notruf_24h', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qk_notruf_vorhanden')}),
    ('qk_notruf_en8128', 'DOCUMENTATION', 'NEVER')],
   [r(no('qk_notruf_vorhanden'), 'HIGH', mfrom=('N20-K1', 'Keine Notruffunktion'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qk_notruf_art', 'klingel_schacht'), 'MEDIUM', mfrom=('N20-K1', 'Klingel im Schacht'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qk_notruf_art', 'nicht_staendig'), 'MEDIUM', mfrom=('N20-K1', 'Sprechverbindung oder Klingel'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qk_notruf_art', 'klingel_staendig'), 'MEDIUM', mfrom=('N20-K1', 'Klingel zu einer'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qk_notruf_24h'), 'MEDIUM',
      sofort='Betreiber informieren; Erreichbarkeit der Notrufstelle außerhalb der Betriebszeiten regeln',
      mittel='Notruf auf einen 24 h besetzten Notrufdienst (EN 81-28) aufschalten',
      evidence='HYPOTHESIS', klaerung='K-K01')],
   sources=[en8120('5.12.3'), en('DIN EN 81-28'), law('BetrSichV', 'Anh. 1 Nr. 4.1'),
            trbs3121('Anh. 1 Nr. 7')],
   factor=F_NOTFALL, persons=[NUTZER, BEAUFTRAGTE], agg='MAXIMUM', bereich='K')

hz('MF-K02', 'Fehlende oder unzulängliche Notbeleuchtung im Fahrkorb', GRP_BEL,
   [('qk_notbeleuchtung', 'TRIGGER', 'ALWAYS')],
   [r(eq('qk_notbeleuchtung', 'keine'), 'HIGH', mfrom=('N20-K10', 'Keine ausreichende'),
      evidence='HIGH_CONFIDENCE', klaerung='K-K02'),
    r(eq('qk_notbeleuchtung', 'nur_taster'), 'NO_RISK', evidence='HIGH_CONFIDENCE',
      notes='App K10: Leuchte ohne Netzersatzfunktion, jedoch beleuchteter Notruf-Taster = grün')],
   sources=[en8120('5.4.10.4'), trbs3121('Anh. 1 Nr. 7')], factor=F_BELEUCHTUNG,
   persons=[NUTZER], bereich='K')

hz('MF-K03', 'Unzureichende Haltegenauigkeit / Stufenbildung an den Haltestellen', GRP_ANT,
   [('qk_stufe_mm', 'TRIGGER', 'ALWAYS'),
    ('qk_nachregulierung', 'DOCUMENTATION', 'NEVER'),
    ('qa_nutzung_pmem', 'MODIFIER', 'NEVER')],
   [r(gt('qk_stufe_mm', 20), 'HIGH', prio=300, mfrom=('N20-K7', 'Stufenbildung größer 20'),
      evidence='HIGH_CONFIDENCE'),
    r(all_(gt('qk_stufe_mm', 10), yes('qa_nutzung_pmem')), 'HIGH', prio=250,
      mfrom=('N20-K7', 'Stufenbildung größer 20'), evidence='HYPOTHESIS', klaerung='K-K03'),
    r(gt('qk_stufe_mm', 10), 'MEDIUM', prio=200, mfrom=('N20-K7', 'Stufenbildung größer 10'),
      evidence='HIGH_CONFIDENCE', klaerung='K-K10',
      notes='Entscheidung 02.09.2026: kein Warnhinweis als Kompensation, bleibt Mittel.')],
   sources=[en8120('5.12.1.1.4'), trbs3121('Anh. 1 Nr. 1')], factor=F_STURZ,
   persons=[NUTZER], bereich='K')

hz('MF-K04', 'Unzureichende Fahrkorbtürschürze', GRP_K,
   [('qk_schuerze_mm', 'TRIGGER', 'ALWAYS'),
    ('qk_befreiung_nur_fachkundig', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': lt('qk_schuerze_mm', 300)})],
   [r(all_(lt('qk_schuerze_mm', 300), yes('qk_befreiung_nur_fachkundig')), 'MEDIUM', prio=300,
      mfrom=('N20-K6', 'Keine Kabinentürschürze (< 300 mm), Personenbefreiung'),
      evidence='HIGH_CONFIDENCE'),
    r(lt('qk_schuerze_mm', 300), 'HIGH', prio=200, mfrom=('N20-K6', 'Keine Kabinentürschürze (< 300 mm)'),
      evidence='HIGH_CONFIDENCE'),
    r(lt('qk_schuerze_mm', 750), 'MEDIUM', prio=100, mfrom=('N20-K6', 'Zu kurze'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.4.5'), trbs3121('Anh. 1 Nr. 13')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER, WARTUNG], bereich='K')

hz('MF-K05', 'Zu großer Abstand zwischen Fahrkorbschwelle und Schachtwand', GRP_K,
   [('qk_abstand_schwelle_mm', 'TRIGGER', 'ALWAYS'),
    ('qk_fk_tuer_verriegelt', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': gt('qk_abstand_schwelle_mm', 150)}),
    ('qk_schachttuer_zusatzverriegelung', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': gt('qk_abstand_schwelle_mm', 150)})],
   [r(all_(gt('qk_abstand_schwelle_mm', 150), yes('qk_fk_tuer_verriegelt'),
           yes('qk_schachttuer_zusatzverriegelung')), 'NO_RISK', prio=200,
      evidence='HIGH_CONFIDENCE', klaerung='K-K04',
      notes='Entscheidung 02.09.2026: Kein Risiko nur mit Fahrkorbtür-Verriegelung UND Zusatzverriegelung an der Schachttür.'),
    r(gt('qk_abstand_schwelle_mm', 150), 'HIGH', prio=100, mfrom=('N20-K8', 'Abstand größer'),
      sofort='Nutzer über die Absturzgefahr bei Selbstbefreiung unterweisen; Personenbefreiung nur durch fachkundige Personen',
      mittel='Fahrkorbtür-Verriegelung außerhalb der Entriegelungszone und Zusatzverriegelung an den Schachttüren nachrüsten oder Abstand auf unter 150 mm reduzieren',
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.5.3.1'), trbs3121('Anh. 1 Nr. 19')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER], bereich='K')

hz('MF-K06', 'Fehlende Kennzeichnung der Nennlast, unpassende Nutzfläche oder fehlende '
   'Überlastkontrolle', GRP_K,
   [('qk_nennlast_gekennz', 'TRIGGER', 'ALWAYS'),
    ('qk_nutzflaeche_ok', 'TRIGGER', 'ALWAYS'),
    ('qk_ueberlast', 'TRIGGER', 'ALWAYS'),
    ('qk_ueberlast_geprueft', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qk_ueberlast')}),
    ('qa_nutzungsart', 'MODIFIER', 'NEVER'),
    ('qa_nutzung_flurfoerderzeug', 'DOCUMENTATION', 'NEVER')],
   [r(no('qk_nutzflaeche_ok'), 'HIGH', mfrom=('N20-K13', 'Nutzfläche'), evidence='HIGH_CONFIDENCE'),
    r(all_(no('qk_ueberlast'), in_('qa_nutzungsart', ['lasten', 'gueter', 'personen_lasten'])), 'HIGH',
      mfrom=('N20-K12', 'Keine Überlastsicherung bei Lastenaufzügen'), evidence='HIGH_CONFIDENCE'),
    r(no('qk_ueberlast'), 'MEDIUM', mfrom=('N20-K13', 'Keine Überlastkontrolle'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qk_nennlast_gekennz'), 'MEDIUM', mfrom=('N20-K13', 'Nennlast und zulässige'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qk_ueberlast_geprueft'), 'LOW', mfrom=('N20-K13', 'Überlastkontrolle vorhanden'),
      evidence='HIGH_CONFIDENCE', klaerung='K-K05')],
   sources=[en8120('5.4.2'), en8120('5.12.1.2')], factor=F_UEBERLAST, persons=[NUTZER],
   agg='MAXIMUM', bereich='K')

hz('MF-K07', 'Unzureichende Lüftung des Fahrkorbs', GRP_K,
   [('qk_lueftung', 'TRIGGER', 'ALWAYS')],
   [r(eq('qk_lueftung', 'unzureichend'), 'HIGH', mfrom=('N20-K14', 'Lüftungsöffnungen fehlen'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qk_lueftung', 'verdeckt'), 'MEDIUM', mfrom=('N20-K14', 'Lüftungsöffnungen teilweise'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qk_lueftung', 'keine_zwang'), 'MEDIUM', mfrom=('N20-K14', 'Keine Zwangsbelüftung'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.4.9')], factor=F_UMGEBUNG, persons=[NUTZER], bereich='K')

hz('MF-K08', 'Fehlende Brandfallsteuerung trotz Anforderung im Brandschutzkonzept', GRP_BRAND,
   [('qa_bfs_gefordert', 'APPLICABILITY', 'NEVER'),
    ('qk_bfs_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qk_bfs_geprueft', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qk_bfs_vorhanden')})],
   [r(no('qk_bfs_vorhanden'), 'HIGH', mfrom=('N20-K15', 'Brandschutzkonzept fordert'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qk_bfs_geprueft'), 'MEDIUM', mfrom=('N20-K15', 'Brandfallsteuerung vorhanden, Funktion'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en('DIN EN 81-73'), trbs3121('Anh. 4')], factor=F_BRAND, persons=[NUTZER, FEUERWEHR],
   agg='MAXIMUM', bereich='K')

hz('MF-K09', 'Fehlender Hinweis „Aufzug im Brandfall nicht benutzen"', GRP_BRAND,
   [('qk_hinweis_brandfall', 'TRIGGER', 'ALWAYS')],
   [r(no('qk_hinweis_brandfall'), 'MEDIUM', mfrom=('N20-K15', 'Hinweisschild'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en('DIN EN 81-73', '5.3'), en8120('7.2')], factor=F_BRAND, persons=[NUTZER], bereich='K')

hz('MF-K10', 'Eingeschränkte Zugänglichkeit für Personen mit eingeschränkter Mobilität',
   GRP_K,
   [('qa_nutzung_pmem', 'APPLICABILITY', 'NEVER'),
    ('qk_en8170', 'TRIGGER', 'ALWAYS'),
    ('qk_bedienelemente', 'TRIGGER', 'ALWAYS'),
    ('qk_rollstuhl_mass', 'TRIGGER', 'ALWAYS')],
   [r(no('qk_rollstuhl_mass'), 'HIGH', mfrom=('N20-K16', 'Fahrkorbabmessungen'), evidence='HIGH_CONFIDENCE'),
    r(no('qk_en8170'), 'MEDIUM', mfrom=('N20-K16', 'Hinweise auf Nutzung'), evidence='HIGH_CONFIDENCE'),
    r(no('qk_bedienelemente'), 'MEDIUM', mfrom=('N20-K16', 'Bedienelemente'), evidence='HIGH_CONFIDENCE')],
   sources=[en('DIN EN 81-70')], factor=F_STURZ, persons=[NUTZER], agg='MAXIMUM', bereich='K')

hz('MF-K11', 'Beschädigte Fahrkorbausstattung / Vandalismus', GRP_K,
   [('qk_ausstattung', 'TRIGGER', 'ALWAYS'),
    ('qk_vandalismus_wiederholt', 'TRIGGER', 'ALWAYS'),
    ('qk_en8171', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes('qk_vandalismus_wiederholt')}),
    ('qa_oeffentlich', 'DOCUMENTATION', 'NEVER')],
   [r(eq('qk_ausstattung', 'mit_gef'), 'HIGH', mfrom=('N20-K17', 'Beschädigung mit'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qk_ausstattung', 'ohne_gef'), 'MEDIUM', mfrom=('N20-K17', 'Beschädigte Ausstattung'),
      evidence='HIGH_CONFIDENCE'),
    r(all_(yes('qk_vandalismus_wiederholt'), no('qk_en8171')), 'MEDIUM',
      mfrom=('N20-K17', 'Wiederholte'), evidence='HIGH_CONFIDENCE')],
   sources=[en('DIN EN 81-71')], factor=F_GLAS, persons=[NUTZER], agg='MAXIMUM', bereich='K')

hz('MF-K12', 'Fehlender Schutz gegen unbeabsichtigte Fahrkorbbewegung bei offenen Türen (UCM)',
   GRP_SK,
   [('qa_ucm_a3', 'TRIGGER', 'ALWAYS'),
    ('qk_ucm_sr_modul', 'TRIGGER', 'CONDITIONAL',
     {'required_when': all_(no('qa_ucm_a3'), not_(HYDR)),
      'notes': 'Bei Hydraulik nicht gefragt: Türüberbrückung immer vorhanden (K-K12).'}),
    ('qm_zweikreisbremse', 'COMPENSATION', 'NEVER'),
    ('qm_bremse_ueberwacht', 'COMPENSATION', 'NEVER'),
    ('qa_lagerung_statisch_bestimmt', 'COMPENSATION', 'NEVER'),
    ('qa_aufzugsart', 'MODIFIER', 'NEVER')],
   [r(all_(no('qa_ucm_a3'), any_(yes('qk_ucm_sr_modul'), HYDR)), 'HIGH', prio=300,
      mfrom=('N20-K4.2', 'UCM nicht vorhanden trotz'), evidence='HIGH_CONFIDENCE', klaerung='K-K12',
      notes='Entscheidung 02.09.2026: Hydraulikaufzug hat immer eine Türüberbrückung (Nachregulieren '
      'bei Druckverlust) – ohne UCM daher Hoch wie bei Seilaufzügen mit SR-Modul.'),
    r(all_(no('qa_ucm_a3'), no('qk_ucm_sr_modul'), yes('qm_zweikreisbremse'),
           yes('qm_bremse_ueberwacht'), yes('qa_lagerung_statisch_bestimmt')), 'LOW', prio=250,
      mfrom=('N20-K4.2', 'UCM nicht notwendig'),
      sofort='Bremsüberwachung und Bremsprüfung im Wartungsumfang halten',
      mittel='Bei Steuerungs- oder Antriebsmodernisierung UCM-Schutz nach EN 81-20 5.6.7 vorsehen',
      evidence='HIGH_CONFIDENCE', klaerung='K-K08'),
    r(all_(no('qa_ucm_a3'), no('qk_ucm_sr_modul'), yes('qm_zweikreisbremse'),
           yes('qa_lagerung_statisch_bestimmt')), 'MEDIUM', prio=245,
      mfrom=('N20-K4.2', 'Zweikreisbremse vorhanden'), evidence='HIGH_CONFIDENCE', klaerung='K-K11',
      notes='TRBS 3121 Anh. 1 Nr. 16: statisch bestimmte Lagerung und Zweikreisbremse (ohne Überwachung) ausdrücklich mittleres Risiko.'),
    r(no('qa_ucm_a3'), 'HIGH', prio=100, mfrom=('N20-K4.2', 'Einkreis'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.6.7'), en8120('5.9.2.2.2'), trbs3121('Anh. 1 Nr. 16')],
   factor=F_UCM, persons=[NUTZER], bereich='K')

hz('MF-K13', 'Fehlender Schutz gegen Übergeschwindigkeit aufwärts / Sturz nach oben',
   GRP_SK,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': all_(SEIL, yes('qa_gegengewicht'))}),
    ('qa_gegengewicht', 'APPLICABILITY', 'NEVER'),
    ('qk_schutz_aufwaerts', 'TRIGGER', 'ALWAYS')],
   [r(eq('qk_schutz_aufwaerts', 'nicht'), 'HIGH', mfrom=('N20-K4.1', 'Sturz nach oben nicht'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.6.6'), trbs3121('Anh. 1 Nr. 16')], factor=F_KINETISCH, persons=[NUTZER],
   bereich='K')

hz('MF-K14', 'Statisch unbestimmt gelagerte Antriebswelle (3-Punkt-Lagerung)', GRP_ANT,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': SEIL}),
    ('qa_lagerung_statisch_bestimmt', 'TRIGGER', 'ALWAYS'),
    ('qk_schutz_aufwaerts', 'COMPENSATION', 'NEVER')],
   [r(all_(no('qa_lagerung_statisch_bestimmt'), eq('qk_schutz_aufwaerts', 'aktiv')), 'LOW', prio=200,
      sofort='Schutzmaßnahmen (SAFÜ/Notbremse) weiterhin aufrechterhalten und prüfen',
      mittel='Bei Modernisierung des Antriebs statisch bestimmte Lagerung vorsehen',
      evidence='INFERRED',
      notes='Blaupause Schindler M004: 3-Punkt-Lagerung mit SAFÜ = Niedrig (DIRECT belegt).'),
    r(no('qa_lagerung_statisch_bestimmt'), 'HIGH', prio=100,
      mfrom=('N20-K4.2', 'Der Antrieb hat eine statisch'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.9.2.2.2'), trbs3121('Anh. 1 Nr. 16')], factor=F_KINETISCH,
   persons=[NUTZER], bereich='K')
