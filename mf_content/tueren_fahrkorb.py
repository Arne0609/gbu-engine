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
TREIB = in_('qa_aufzugsart', ['seil', 'trommel'])   # siehe triebwerksraum.py
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
yn('qt_glas_normgerecht', 'Glaseinsätze in Schacht-/Fahrkorbtüren aus normgerechtem '
   'Glas (Verbundsicherheitsglas nach EN 81-20 5.3.5.3)?', ui='7.8',
   visible_when=GLAS_TUER,
   help='Nur die Glasart. Drahtglas wird unter 7.9 erfasst, Beschädigungen unter 7.8a.')
yn('qt_glas_beschaedigt', 'Glaseinsatz beschädigt, lose oder nicht sicher befestigt?',
   ui='7.8a', visible_when=GLAS_TUER)
yn('qt_glas_drahtglas', 'Drahtglas (Gitterglas) verbaut?', ui='7.9', visible_when=GLAS_TUER)
yn('qt_glas_schiebetuer', 'Verglaste Türen als kraftbetätigte Schiebetüren ausgeführt?',
   ui='7.9a', visible_when=GLAS_TUER)
yn('qt_glas_einzugsschutz', 'Schutz gegen Einziehen von Kinderhänden an Glas-Schiebetüren '
   'vorhanden (Sensorleiste, Abstand, Beschichtung)?', ui='7.10',
   visible_when=all_(GLAS_TUER, yes('qt_glas_schiebetuer')))
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
yn('qt_nur_eingewiesene', 'Ohne Fahrkorbtür: Lastenaufzug, der ausschließlich von '
   'eingewiesenen Personen benutzt wird (Einweisung dokumentiert)?', ui='8.9b',
   visible_when=all_(no('qa_fahrkorbtuer'),
                     any_(yes('qt_lichtgitter_ohne_tuer'), yes('qt_scherengitter'))),
   help='TRBS 3121 Anh. 1 Nr. 14 c): Das Sicherheitslichtgitter ersetzt die '
        'Fahrkorbtür nur bei Lastenaufzügen mit ausschließlich eingewiesenem Nutzerkreis.')

# Ergaenzung 04.09.2026 (Lueckenschluss EN 81-80 Nr. 9, 26, 35):
# EN 81-20 5.2.5.3.2 (Flaeche unterhalb der Schachttuerschwelle),
# 5.3.5.3.2 (Rueckhalteeinrichtungen der Tuerblaetter),
# 5.3.11 (Verbindung mehrteiliger Schachttuerblaetter).
sel('qt_flaeche_unter_schwelle', 'Schachtwand unterhalb der Schachttürschwelle '
    '(vertikale Fläche zur Entriegelungszone)', ui='7.12',
    options=[('normgerecht', 'Durchgehende, glatte und harte vertikale Fläche in voller '
                             'Höhe und Breite (EN 81-20 5.2.5.3.2)'),
             ('maengel', 'Vorhanden, aber mit Mängeln (Vorsprünge über 5 mm, zu geringe '
                         'Höhe oder Breite, nachgiebig, offene Fugen)'),
             ('keine', 'Keine geschlossene Fläche (offene Konstruktion, Gitter, Mauerwerk '
                       'mit Absätzen)')],
    help='Schützt beim Verlassen des Fahrkorbs außerhalb der Haltestelle vor Absturz und '
         'vor dem Einklemmen zwischen Fahrkorbschwelle und Schachtwand. Gefordert sind '
         'mindestens die halbe Entriegelungszone + 50 mm Höhe und die lichte Zugangsbreite '
         '+ 25 mm je Seite.')
yn('qt_rueckhaltung_tuerblatt', 'Rückhalteeinrichtungen an den horizontal bewegten '
   'Schacht-Schiebetüren vorhanden (Türblatt bleibt in seiner Lage, wenn ein '
   'Führungselement versagt)?', ui='7.13',
   help='EN 81-20 5.3.5.3.2. Auch die Aufhängung/Befestigung selbst prüfen: Ein Türblatt, '
        'das aus der Führung fällt, gibt den Schacht frei.')
yn('qt_fuehrung_tuerblatt_ok', 'Führungselemente, Hänger und Befestigungen der Türblätter '
   'unbeschädigt und ohne auffälliges Spiel?', ui='7.13a')
yn('qt_tuer_mehrteilig', 'Schachttüren mehrteilig (Teleskop- oder Mitteltür mit mehreren '
   'Türblättern)?', ui='7.14')
sel('qt_tuerblatt_verbindung', 'Verbindung der Türblätter mehrteiliger Schachttüren',
    ui='7.14a',
    options=[('direkt', 'Unmittelbar mechanisch verbunden (Ineinandergreifen, '
                        'Blechumkantung, Verriegelungselemente am Hänger)'),
             ('mittelbar_ueberwacht', 'Mittelbar verbunden (Seil, Riemen, Kette); '
                                      'Schließstellung der nicht verriegelten Türblätter '
                                      'elektrisch überwacht, keine Griffe'),
             ('mittelbar_ohne_ueberwachung', 'Mittelbar verbunden, Schließstellung der '
                                             'übrigen Türblätter nicht überwacht'),
             ('keine', 'Keine wirksame Verbindung; nur ein Türblatt verriegelt')],
    visible_when=yes('qt_tuer_mehrteilig'),
    help='EN 81-20 5.3.11: Die Verbindung gilt als Teil der Verriegelung und muss auch bei '
         'Bruch eines Führungselements halten.')

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
   'Rückmeldung, Testruf)?', ui='8.4', visible_when=yes('qk_notruf_vorhanden'),
   help='Nur zur Dokumentation – die Bewertung des Notrufs läuft über 8.1 bis 8.3. '
        'Die Antwort wird in den Cyber-Fragebogen übernommen (automatischer Testruf).')
sel('qk_notbeleuchtung', 'Notbeleuchtung im Fahrkorb', ui='8.5',
    options=[('netzersatz', 'Leuchte mit Netzersatzfunktion (mind. 5 Lux, 1 h)'),
             ('nur_taster', 'Keine Notbeleuchtung, aber beleuchteter Notruftaster'),
             ('keine', 'Keine Notbeleuchtung')])
# Schwellenfragen 8.10/8.12/8.14: erhebung.py (SCHWELLEN) stellt sie im Seed auf Bereichsauswahl bzw.
# Ja/Nein um; Regeln hier weiter als Zahlvergleich schreiben (stabile Regel-IDs).
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
   visible_when=any_(yes('qa_nutzung_pmem'), yes('qa_barrierefrei_gefordert')))
yn('qk_bedienelemente', 'Bedienelemente in erreichbarer Höhe und ertastbar?', ui='8.23',
   visible_when=any_(yes('qa_nutzung_pmem'), yes('qa_barrierefrei_gefordert')))
yn('qk_rollstuhl_mass', 'Fahrkorbabmessungen für Rollstuhlnutzung ausreichend '
   '(mind. 1,00 m × 1,25 m, Fahrkorbtyp 1 nach DIN EN 81-70:2022-12)?', ui='8.24',
   visible_when=any_(yes('qa_nutzung_pmem'), yes('qa_barrierefrei_gefordert')),
   help='Typ 1 nach DIN EN 81-70 ist das Mindestmaß für einen Rollstuhl ohne Begleitperson. '
        'Fordert die Genehmigung einen größeren Typ (2 oder 3), gilt dieser.')
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

# Ergaenzung 04.09.2026 (Lueckenschluss EN 81-80 Nr. 45): Fahrkorbbeleuchtung im
# Normalbetrieb, EN 81-20 5.4.10.1 bis 5.4.10.3. Die Notbeleuchtung (8.5) bleibt
# unveraendert bei MF-K02.
sel('qk_beleuchtung', 'Beleuchtung im Fahrkorb (Normalbetrieb)', ui='8.29',
    options=[('normgerecht', 'Mindestens 100 Lux an den Befehlsgebern und 1 m über dem '
                             'Boden bis 100 mm an die Wände'),
             ('gemindert', 'Beleuchtung vorhanden, aber unter 100 Lux, einzelne Lampen '
                           'defekt oder stark vergilbte Abdeckung'),
             ('keine', 'Keine funktionsfähige Beleuchtung im Fahrkorb')],
    help='EN 81-20 5.4.10.1: gemessen an den Befehlsgebern und 1 m über dem Boden an allen '
         'Stellen, die nicht mehr als 100 mm von einer Wand entfernt sind. Schatten durch '
         'Handlauf oder Klappsitz dürfen vernachlässigt werden.')
yn('qk_bel_zwei_lampen', 'Mindestens zwei parallel geschaltete Lampen im Fahrkorb?',
   ui='8.29a', help='EN 81-20 5.4.10.2: Ausfall einer Lampe darf den Fahrkorb nicht '
   'dunkel werden lassen.')
yn('qk_bel_staendig', 'Fahrkorb ständig beleuchtet (Ausnahme: Parken mit geschlossenen '
   'Türen)?', ui='8.29b', help='EN 81-20 5.4.10.3.')

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
      sofort='Schließ- und Verriegelungsfunktion aller Schachttüren prüfen; Beauftragte Person '
             'auf offen stehende Schachttüren hinweisen',
      evidence='HIGH_CONFIDENCE', pb='H11 – Sofortmaßnahme ergänzt')],
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
      sofort='Personenbefreiung bis zur Nachrüstung nur durch das Aufzugsfachunternehmen; '
             'betroffene Haltestellen im Notfallplan kennzeichnen',
      evidence='HIGH_CONFIDENCE', klaerung='K-K06', pb='H11 – Sofortmaßnahme ergänzt'),
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
      sofort='Nach jeder Notentriegelung Schachttür von Hand schließen und Verriegelung prüfen; '
             'Personenbefreiung nur durch unterwiesene Personen',
      evidence='HIGH_CONFIDENCE', pb='H11 – Sofortmaßnahme ergänzt'),
    r(no('qt_selbstschliessend'), 'MEDIUM', mfrom=('N20-K3', 'Keine selbstschließenden'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.3.9.3.4'), trbs3121('Anh. 1 Nr. 12')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER], agg='MAXIMUM', bereich='T')

hz('MF-T04', 'Ungeeignetes Glas oder fehlender Einzugsschutz an Türen mit Glas', GRP_T,
   [('qa_glas_schachttueren', 'APPLICABILITY', 'NEVER', {'applicable_when': GLAS_TUER}),
    ('qa_glas_fahrkorbtueren', 'OPTIONAL', 'NEVER'),
    ('qt_glas_normgerecht', 'TRIGGER', 'ALWAYS'),
    ('qt_glas_drahtglas', 'TRIGGER', 'ALWAYS'),
    ('qt_glas_beschaedigt', 'TRIGGER', 'ALWAYS'),
    ('qt_glas_schiebetuer', 'TRIGGER', 'ALWAYS'),
    ('qt_glas_einzugsschutz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qt_glas_schiebetuer')}),
    ('qa_nutzung_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qt_glas_normgerecht'), no('qt_glas_drahtglas')), 'HIGH',
      mfrom=('N20-K9', 'Ungeeignetes Glas'), evidence='HIGH_CONFIDENCE',
      pb='B06 – Drahtglas ausgenommen, damit die Niedrig-Regel (TRBS 3121 Anh. 1 Nr. 9) greift'),
    r(yes('qt_glas_beschaedigt'), 'HIGH', mfrom=('N20-K9', 'Ungeeignetes Glas'),
      evidence='HIGH_CONFIDENCE',
      pb='B06 – neu: beschädigtes oder loses Glas unabhängig von der Glasart Hoch'),
    r(all_(yes('qt_glas_schiebetuer'), no('qt_glas_einzugsschutz')), 'HIGH',
      mfrom=('N20-K2.2', 'Glas-Kabinentür mit Lichtgitter, aber'), evidence='HIGH_CONFIDENCE',
      pb='Prüfbericht 16.09.2026 – Einzugsschutz nur bei kraftbetätigten Schiebetüren; Glasfestigkeit getrennt'),
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

# Ohne Fahrkorbtür ist ein Ersatz (Lichtgitter oder Scherengitter) nur bei einem
# Lastenaufzug mit ausschließlich eingewiesenem Nutzerkreis eine Kompensation
# (TRBS 3121 Anh. 1 Nr. 14 c). Beide Ersatzlösungen laufen über dieselbe
# Voraussetzung, damit keine die andere mit einer günstigeren Stufe verdrängt
# (zweite Prüfung 16.09.2026, Punkt 1).
T06_ERSATZ = all_(no('qa_fahrkorbtuer'), any_(yes('qt_lichtgitter_ohne_tuer'), yes('qt_scherengitter')))
T06_EINGEWIESEN = all_(yes('qt_nur_eingewiesene'), in_('qa_nutzungsart', ['lasten', 'gueter']))

hz('MF-T06', 'Fahrkorb ohne Abschlusstür oder ohne Schließkantensicherung', GRP_T,
   [('qa_fahrkorbtuer', 'TRIGGER', 'ALWAYS'),
    ('qt_lichtgitter_ohne_tuer', 'COMPENSATION', 'CONDITIONAL', {'required_when': no('qa_fahrkorbtuer')}),
    ('qt_scherengitter', 'COMPENSATION', 'CONDITIONAL', {'required_when': no('qa_fahrkorbtuer')}),
    ('qt_nur_eingewiesene', 'COMPENSATION', 'CONDITIONAL', {'required_when': T06_ERSATZ}),
    ('qa_nutzungsart', 'MODIFIER', 'CONDITIONAL', {'required_when': T06_ERSATZ}),
    ('qt_schliesskante', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_fahrkorbtuer')}),
    ('qt_fk_tuer_automatisch', 'OPTIONAL', 'NEVER'),
    ('qa_nutzung_pmem', 'MODIFIER', 'NEVER'),
    ('qa_nutzung_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qa_fahrkorbtuer'), no('qt_lichtgitter_ohne_tuer'), no('qt_scherengitter')), 'HIGH',
      prio=300, mfrom=('N20-K2.2', 'Keine Kabinenabschlusstür und kein'),
      mittel='Fahrkorbtür nachrüsten (ein Sicherheitslichtgitter genügt nur bei Lastenaufzügen mit '
             'ausschließlich eingewiesenem Nutzerkreis, TRBS 3121 Anh. 1 Nr. 14 c)',
      evidence='HIGH_CONFIDENCE', pb='Prüfbericht 16.09.2026 – Lichtgitter-Alternative auf den zulässigen Fall begrenzt'),
    r(all_(no('qa_fahrkorbtuer'), any_(yes('qa_nutzung_pmem'), yes('qa_nutzung_kinder'))), 'HIGH',
      prio=250, mfrom=('N20-K2.1', 'Keine Kabinenabschlusstür'), evidence='HYPOTHESIS',
      klaerung='K-K09'),
    r(all_(no('qa_fahrkorbtuer'), yes('qt_scherengitter'), T06_EINGEWIESEN), 'MEDIUM', prio=200,
      mfrom=('N20-K2.2', 'Keine Kabinenabschlusstür, jedoch Scherengitter'), evidence='INFERRED',
      pb='Prüfbericht 16.09.2026 – Scherengitter nur mit derselben Voraussetzung wie das Lichtgitter'),
    r(all_(no('qa_fahrkorbtuer'), yes('qt_lichtgitter_ohne_tuer'), T06_EINGEWIESEN), 'MEDIUM', prio=200,
      mfrom=('N20-K2.2', 'Keine Kabinenabschlusstür, jedoch Sicherheitslichtgitter'),
      evidence='HIGH_CONFIDENCE',
      pb='B07 – Kompensation nur bei Lastenaufzug mit ausschließlich eingewiesenen Personen'),
    r(T06_ERSATZ, 'HIGH', prio=150,
      sofort='Aufzug für die Personenbeförderung durch nicht eingewiesene Personen sperren',
      mittel='Fahrkorbtür nachrüsten (Lichtgitter oder Scherengitter genügen nur bei Lastenaufzügen '
             'mit ausschließlich eingewiesenem Nutzerkreis)', evidence='HIGH_CONFIDENCE',
      pb='B07/Prüfbericht 16.09.2026 – Ersatzlösung ohne diese Voraussetzung ist keine zulässige Kompensation'),
    r(all_(yes('qa_fahrkorbtuer'), eq('qt_schliesskante', 'keine'), yes('qa_nutzung_pmem')), 'HIGH',
      prio=220, mfrom=('N20-K2.2', 'Kabinenabschlusstür ohne Lichtgitter'), evidence='INFERRED',
      notes='Folgerichtig zur Einzel-Lichtschranke: fehlt die Schließkantensicherung ganz, darf die Stufe nicht günstiger sein.',
      pb='Prüfbericht 16.09.2026 – neu: keine Schließkantensicherung bei mobilitätseingeschränkten Nutzern Hoch'),
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

hz('MF-T07', 'Unzureichende Fläche unterhalb der Schachttürschwelle', GRP_T,
   [('qt_flaeche_unter_schwelle', 'TRIGGER', 'ALWAYS')],
   [r(eq('qt_flaeche_unter_schwelle', 'keine'), 'HIGH', prio=200,
      sofort='Personenbefreiung nur durch fachkundige Personen; Haltestellen mit '
             'unvollständiger Schachtwand kennzeichnen',
      mittel='Durchgehende, glatte vertikale Fläche unterhalb jeder Schachttürschwelle '
             'herstellen (EN 81-20 5.2.5.3.2)',
      evidence='HIGH_CONFIDENCE'),
    r(eq('qt_flaeche_unter_schwelle', 'maengel'), 'MEDIUM', prio=100,
      sofort='Vorsprünge und offene Fugen im Bereich der Türschwelle beseitigen',
      mittel='Fläche unterhalb der Schachttürschwelle normgerecht ergänzen (Höhe, Breite, '
             'Festigkeit, Abschrägung)',
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.5.3.2')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER, BEAUFTRAGTE, WARTUNG], bereich='T',
   description='Beim Verlassen eines außerhalb der Haltestelle stehenden Fahrkorbs muss die '
   'Schachtwand unterhalb der Schwelle eine durchgehende, glatte und harte vertikale Fläche '
   'bilden (EN 81-20 5.2.5.3.2). Ergänzt EN 81-80 Nr. 9.')

hz('MF-T08', 'Türblatt kann aus der Führung fallen (fehlende Rückhalteeinrichtung)', GRP_T,
   [('qt_rueckhaltung_tuerblatt', 'TRIGGER', 'ALWAYS'),
    ('qt_fuehrung_tuerblatt_ok', 'MODIFIER', 'ALWAYS')],
   [r(all_(no('qt_rueckhaltung_tuerblatt'), no('qt_fuehrung_tuerblatt_ok')), 'HIGH', prio=200,
      sofort='Beschädigte Führungselemente und Aufhängungen sofort instand setzen; '
             'Tür bis dahin außer Betrieb nehmen',
      mittel='Rückhalteeinrichtungen nach EN 81-20 5.3.5.3.2 nachrüsten',
      evidence='HIGH_CONFIDENCE'),
    r(no('qt_rueckhaltung_tuerblatt'), 'MEDIUM', prio=100,
      sofort='Führung, Hänger und Befestigung der Türblätter in die wiederkehrende Prüfung '
             'aufnehmen',
      mittel='Rückhalteeinrichtungen nach EN 81-20 5.3.5.3.2 nachrüsten',
      evidence='HIGH_CONFIDENCE'),
    r(no('qt_fuehrung_tuerblatt_ok'), 'MEDIUM', prio=90,
      sofort='Beschädigte Führungselemente, Hänger und Befestigungen instand setzen',
      mittel='Türführungen in den Wartungsplan aufnehmen und regelmäßig nachstellen',
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.3.5.3.2')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER, WARTUNG], bereich='T',
   description='Horizontal bewegte Schacht-Schiebetüren müssen Einrichtungen haben, die das '
   'Türblatt in seiner Lage halten, wenn das Führungselement versagt (EN 81-20 5.3.5.3.2). '
   'Ergänzt EN 81-80 Nr. 26.')

hz('MF-T09', 'Unzureichende Verbindung der Türblätter mehrteiliger Schachttüren', GRP_T,
   [('qt_tuer_mehrteilig', 'APPLICABILITY', 'NEVER',
     {'applicable_when': yes('qt_tuer_mehrteilig')}),
    ('qt_tuerblatt_verbindung', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qt_tuer_mehrteilig')})],
   [r(eq('qt_tuerblatt_verbindung', 'keine'), 'HIGH', prio=200,
      sofort='Tür außer Betrieb nehmen oder alle Türblätter verriegeln, bis die Verbindung '
             'hergestellt ist',
      mittel='Türblätter mechanisch verbinden oder alle Türblätter verriegeln und überwachen '
             '(EN 81-20 5.3.11)',
      evidence='HIGH_CONFIDENCE'),
    r(eq('qt_tuerblatt_verbindung', 'mittelbar_ohne_ueberwachung'), 'HIGH', prio=150,
      sofort='Griffe an den nicht verriegelten Türblättern entfernen; Schließstellung bei '
             'jeder Wartung prüfen',
      mittel='Schließstellung der nicht verriegelten Türblätter durch eine elektrische '
             'Sicherheitseinrichtung überwachen (EN 81-20 5.3.11.2)',
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.3.11'), en8120('5.3.11.3')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER], bereich='T',
   description='Bei mehrteiligen Schacht-Schiebetüren gilt die Verbindung der Türblätter als '
   'Teil der Verriegelung (EN 81-20 5.3.11.3); ohne sie lässt sich ein unverriegeltes '
   'Türblatt öffnen. Ergänzt EN 81-80 Nr. 35.')

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
    r(eq('qk_notbeleuchtung', 'nur_taster'), 'LOW', evidence='INFERRED',
      sofort='Beleuchtung des Notruftasters bei Netzausfall prüfen; Verhalten bei Stromausfall im Notfallplan festlegen',
      mittel='Notbeleuchtung nach DIN EN 81-20 5.4.10.4 nachrüsten (mind. 5 lx am Notrufauslöser, 1 h)',
      notes='App K10: Leuchte ohne Netzersatzfunktion, jedoch beleuchteter Notruf-Taster = grün.',
      pb='Prüfbericht 16.09.2026 – Tasterbeleuchtung ersetzt keine Notbeleuchtung: Niedrig statt Kein Risiko')],
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
      mittel='Haltegenauigkeit auf ±10 mm und Nachregulierung auf ±20 mm herstellen (geregelter '
             'Antrieb, Nachstelleinrichtung bzw. geregeltes Ventil)',
      evidence='HIGH_CONFIDENCE', klaerung='K-K10', pb='H11 – mittelfristige Maßnahme ergänzt',
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
    ('qa_nutzung_kinder', 'MODIFIER', 'CONDITIONAL', {'required_when': gt('qk_abstand_schwelle_mm', 150)}),
    ('qk_fk_tuer_verriegelt', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': gt('qk_abstand_schwelle_mm', 150)}),
    ('qk_schachttuer_zusatzverriegelung', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': gt('qk_abstand_schwelle_mm', 150)})],
   [r(all_(gt('qk_abstand_schwelle_mm', 150), yes('qk_fk_tuer_verriegelt'),
           yes('qk_schachttuer_zusatzverriegelung')), 'NO_RISK', prio=200,
      evidence='HIGH_CONFIDENCE', klaerung='K-K04',
      notes='Entscheidung 02.09.2026: Kein Risiko nur mit Fahrkorbtür-Verriegelung UND Zusatzverriegelung an der Schachttür.'),
    r(all_(gt('qk_abstand_schwelle_mm', 150),
           any_(all_(yes('qk_fk_tuer_verriegelt'), no('qk_schachttuer_zusatzverriegelung')),
                all_(no('qk_fk_tuer_verriegelt'), yes('qk_schachttuer_zusatzverriegelung')))),
      'LOW', prio=190,
      sofort='Nutzer über die Absturzgefahr bei Selbstbefreiung unterweisen',
      mittel='Zweite Maßnahme (Fahrkorbtür-Verriegelung bzw. Zusatzverriegelung der Schachttüren) bei der nächsten Modernisierung ergänzen',
      evidence='INFERRED',
      notes='TRBS 3121 Anh. 1 Nr. 19 ist mit einer der Alternativen a) oder b) erfüllt. EIGENER STANDARD (strenger): Kein Risiko erst mit beiden Maßnahmen (K-K04).',
      pb='Prüfbericht 16.09.2026 – TRBS-Alternative und eigener Standard getrennt'),
    r(all_(gt('qk_abstand_schwelle_mm', 150), yes('qa_nutzung_kinder')), 'HIGH', prio=150,
      mfrom=('N20-K8', 'Abstand größer'),
      sofort='Nutzer über die Absturzgefahr bei Selbstbefreiung unterweisen; Personenbefreiung nur durch fachkundige Personen',
      mittel='Fahrkorbtür-Verriegelung außerhalb der Entriegelungszone oder Zusatzverriegelung an den Schachttüren nachrüsten oder Abstand auf unter 150 mm reduzieren',
      evidence='INFERRED',
      notes='EIGENER STANDARD (strenger als TRBS 3121 Anh. 1 Nr. 19, dort bis Mittel): Hoch bei Nutzung durch Kinder.',
      pb='Prüfbericht 16.09.2026 – neu: Nutzerkreis Kinder'),
    r(gt('qk_abstand_schwelle_mm', 150), 'MEDIUM', prio=100, mfrom=('N20-K8', 'Abstand größer'),
      sofort='Nutzer über die Absturzgefahr bei Selbstbefreiung unterweisen; Personenbefreiung nur durch fachkundige Personen',
      mittel='Fahrkorbtür-Verriegelung außerhalb der Entriegelungszone oder Zusatzverriegelung an den Schachttüren nachrüsten oder Abstand auf unter 150 mm reduzieren',
      evidence='HIGH_CONFIDENCE',
      notes='TRBS 3121 Anh. 1 Nr. 19: bei Altanlagen niedrig bis mittel je nach Benutzerkreis.',
      pb='Prüfbericht 16.09.2026 – Hoch auf Mittel; Hoch nur bei Nutzung durch Kinder')],
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
   [('qa_nutzung_pmem', 'APPLICABILITY', 'NEVER',
     {'applicable_when': any_(yes('qa_nutzung_pmem'), yes('qa_barrierefrei_gefordert'))}),
    ('qa_barrierefrei_gefordert', 'OPTIONAL', 'NEVER'),
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
      mfrom=('N20-K17', 'Wiederholte'),
      mittel='Vandalismusgeschützte Ausstattung nach DIN EN 81-71 nachrüsten; weitere Maßnahmen '
             '(z. B. Zugangsregelung) erst nach Ursachenanalyse und Verhältnismäßigkeitsprüfung',
      evidence='HIGH_CONFIDENCE', pb='H16 – Videoüberwachung nicht mehr als pauschale Abhilfe')],
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
      sofort='Voraböffnen und Nachregulieren mit offener Tür prüfen; Beauftragte Person und Nutzer '
             'auf Stolper- und Schergefahr an der Schwelle hinweisen',
      mittel='UCM-Schutz nach DIN EN 81-20 5.6.7 nachrüsten; Ausbau der Türüberbrückung nur nach '
             'anlagenspezifischer Prüfung (Haltegenauigkeit, Nachregulierung)',
      pb='H11 – Sofortmaßnahme ergänzt; Prüfbericht 16.09.2026 – Ausbau der Türüberbrückung keine Standardalternative',
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
      sofort='Bremse bei jeder Wartung auf Wirksamkeit beider Bremskreise prüfen',
      pb='H11 – Sofortmaßnahme ergänzt',
      notes='TRBS 3121 Anh. 1 Nr. 16: statisch bestimmte Lagerung und Zweikreisbremse (ohne Überwachung) ausdrücklich mittleres Risiko.'),
    r(no('qa_ucm_a3'), 'HIGH', prio=100, mfrom=('N20-K4.2', 'Einkreis'),
      mittel='UCM-Schutz nach DIN EN 81-20 5.6.7 nachrüsten (baumustergeprüft, zur Anlage passend); '
             'eine überwachte Zweikreisbremse allein senkt das Risiko, ersetzt den UCM-Schutz aber nicht',
      evidence='HIGH_CONFIDENCE', pb='H05 – Maßnahme präzisiert')],
   sources=[en8120('5.6.7'), en8120('5.9.2.2.2'), trbs3121('Anh. 1 Nr. 16')],
   factor=F_UCM, persons=[NUTZER], bereich='K')

hz('MF-K13', 'Fehlender Schutz gegen Übergeschwindigkeit aufwärts / Sturz nach oben',
   GRP_SK,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': all_(TREIB, yes('qa_gegengewicht'))}),
    ('qa_gegengewicht', 'APPLICABILITY', 'NEVER'),
    ('qk_schutz_aufwaerts', 'TRIGGER', 'ALWAYS')],
   [r(eq('qk_schutz_aufwaerts', 'nicht'), 'HIGH', mfrom=('N20-K4.1', 'Sturz nach oben nicht'),
      sofort='Bremse, Treibfähigkeit und Tragmittel bei jeder Wartung prüfen; Arbeiten im Schachtkopf '
             'nur bei gegen Bewegung gesichertem Fahrkorb',
      mittel='Schutzeinrichtung gegen Übergeschwindigkeit aufwärts nachrüsten (z. B. Fangvorrichtung am '
             'Gegengewicht, Seil- oder Treibscheibenbremse), baumustergeprüft und zur Anlage passend',
      evidence='HIGH_CONFIDENCE', pb='H05 – sachfremde Sofortmaßnahme (Ultraschall) ersetzt')],
   sources=[en8120('5.6.6'), trbs3121('Anh. 1 Nr. 16')], factor=F_KINETISCH, persons=[NUTZER],
   bereich='K')

hz('MF-K14', 'Statisch unbestimmt gelagerte Antriebswelle (3-Punkt-Lagerung)', GRP_ANT,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': TREIB}),
    ('qa_lagerung_statisch_bestimmt', 'TRIGGER', 'ALWAYS'),
    ('qk_schutz_aufwaerts', 'COMPENSATION', 'NEVER')],
   [r(all_(no('qa_lagerung_statisch_bestimmt'), eq('qk_schutz_aufwaerts', 'aktiv')), 'LOW', prio=200,
      sofort='Schutzmaßnahmen (SAFÜ/Notbremse) weiterhin aufrechterhalten und prüfen',
      mittel='Bei Modernisierung des Antriebs statisch bestimmte Lagerung vorsehen',
      evidence='INFERRED',
      notes='Blaupause Schindler M004: 3-Punkt-Lagerung mit SAFÜ = Niedrig (DIRECT belegt).'),
    r(no('qa_lagerung_statisch_bestimmt'), 'HIGH', prio=100,
      mfrom=('N20-K4.2', 'Der Antrieb hat eine statisch'),
      mittel='Antrieb mit statisch bestimmter Lagerung einbauen oder Maschinenrahmen umbauen; '
             'bis dahin Schutz gegen Übergeschwindigkeit aufwärts / Sturz nach oben nachrüsten',
      evidence='HIGH_CONFIDENCE', pb='H05 – UCM ist keine Abhilfe gegen Wellenbruch')],
   sources=[en8120('5.9.2.2.2'), trbs3121('Anh. 1 Nr. 16')], factor=F_KINETISCH,
   persons=[NUTZER], bereich='K')


hz('MF-K15', 'Unzureichende Beleuchtung im Fahrkorb (Normalbetrieb)', GRP_BEL,
   [('qk_beleuchtung', 'TRIGGER', 'ALWAYS'),
    ('qk_bel_zwei_lampen', 'MODIFIER', 'ALWAYS'),
    ('qk_bel_staendig', 'MODIFIER', 'ALWAYS')],
   [r(eq('qk_beleuchtung', 'keine'), 'MEDIUM', prio=300,
      sofort='Beleuchtung instand setzen; bis dahin Notbeleuchtung und Notruf prüfen',
      mittel='Fest installierte Fahrkorbbeleuchtung nach EN 81-20 5.4.10.1 herstellen '
             '(mind. 100 Lux)',
      evidence='HIGH_CONFIDENCE'),
    r(eq('qk_beleuchtung', 'gemindert'), 'LOW', prio=200,
      sofort='Defekte Lampen tauschen, Abdeckungen reinigen oder erneuern',
      mittel='Beleuchtungsstärke auf mindestens 100 Lux anheben (Messung an den '
             'Befehlsgebern und 1 m über dem Boden)',
      evidence='HIGH_CONFIDENCE'),
    r(no('qk_bel_zwei_lampen'), 'LOW', prio=150,
      sofort='Ausfall der Beleuchtung in die Betriebsanweisung aufnehmen (Verhalten bei '
             'Dunkelheit im Fahrkorb)',
      mittel='Mindestens zwei parallel geschaltete Lampen einbauen (EN 81-20 5.4.10.2)',
      evidence='HIGH_CONFIDENCE'),
    r(no('qk_bel_staendig'), 'LOW', prio=140,
      sofort='Abschaltung der Fahrkorbbeleuchtung im Betrieb unterbinden',
      mittel='Beleuchtung so schalten, dass der Fahrkorb außer beim Parken mit geschlossenen '
             'Türen ständig beleuchtet ist (EN 81-20 5.4.10.3)',
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.4.10.1'), en8120('5.4.10.2'), en8120('5.4.10.3')],
   factor=F_BELEUCHTUNG, persons=[NUTZER], agg='MAXIMUM', bereich='K',
   description='Der Fahrkorb muss eine fest installierte Beleuchtung haben, die an den '
   'Befehlsgebern und 1 m über dem Boden an allen Stellen bis 100 mm an die Wände '
   'mindestens 100 Lux erreicht (EN 81-20 5.4.10.1). Ergänzt EN 81-80 Nr. 45; die '
   'Notbeleuchtung wird bei MF-K02 bewertet.')
