# -*- coding: utf-8 -*-
"""GBU-Variante „Riedl" – Zuordnung der VFA-Blattstruktur zum mehrfragigen
Katalog (MF) und der Cyber-Komponenten zum Cyber-Katalog (CY).

Anlass (Arne, 17.09.2026): Für Riedl Aufzüge wird eine eigene GBU-Variante
gebraucht, die die beiden bisher genutzten Excel-Vorlagen ersetzt:

  * „GBU Anlage leer.xlsx" – VFA-Interlift-Vorlage R 1.7.2 (21.08.2024):
    Deckblatt, je ein Blatt für Kabine, Zugang, Maschinenraum, Fahrkorbdach,
    Schacht und Cybersicherheit; je Blatt 4–5 Gefährdungszeilen mit
    Istzustand-Auswahl, Nohl-Matrix (W/S/R), Schutzmaßnahme, Verantwortlich,
    Termin; Block Z (Aufgaben Verwender / Wartungsfirma / Hinweise
    Servicetechniker) und Block F (Fotos, Bemerkungen).
  * „Vorlage_GBU Cybersicherheit_ab 04-26.xlsx" – anlagenbezogene Beurteilung
    nach TRBS 1115-1 mit sieben Komponenten (Steuerung, PESSRAL, Frequenz-
    umrichter, Notruf, Türsteuergerät, Schachtentrauchung, bauseitige
    Einrichtungen), je Komponente Hersteller/Typ, Gefährdung, Schutzmaßnahme,
    W/S/R, Verantwortlich, Termin; Blatt „Erläuterungen für Standard".

Entscheidungen (Arne, 17.09.2026, per Auswahl):
  1. Aufbau: ABGELEITET aus MF + CY (wie der Typ EN 81-80) – Fragen, Regeln,
     Maßnahmen, Karten, Nachweise und Freigaben bleiben identisch, nur der
     Umfang ist kleiner. Keine eigenen Fragen.
  2. Bewertung: Engine-Stufe als Ampel (Kein Risiko/Niedrig = Grün,
     Mittel = Gelb, Hoch = Rot). Keine W/S-Eingabe durch den Techniker; die
     Nohl-Matrix erscheint nur als Legende (wie Blatt „Risiko-Ende PDF").
  3. Cyber: CY-Teilmenge mit den sieben Riedl-Komponenten (+ Zugang,
     Herstellervorgaben, Rückwirkungsfreiheit, Nachweise). Hersteller/Typ je
     Komponente als Stammdaten; Standard-Erläuterungen im Bericht.
  4. Nutzung: Wir erstellen die GBUs für Riedl-Anlagen (Riedl = Kunde/
     Partner); der Bericht folgt dem gewohnten VFA-/Riedl-Layout.

Umfangsregel (damit die Auswahl nachvollziehbar bleibt und nicht wächst):
  Eine MF-Gefährdung gehört in die Riedl-Variante, wenn
    a) eine Zeile oder ein Istzustand der VFA-Vorlage sie abfragt, oder
    b) sie einen der 22 Punkte des TRBS-3121-Anhangs 1 trägt (das VFA-Blatt
       „Bezug zum Stand der Technik" führt genau diese 22 Punkte), oder
    c) sie eine Betreiberpflicht ist, die die Vorlage im Block Z / auf dem
       Deckblatt voraussetzt (Notfallplan, Notbefreiungsanleitung, Wartung,
       Prüfung, beauftragte Person).
  Alles andere bleibt dem vollen MF-Typ vorbehalten (siehe NICHT_ENTHALTEN).

Die Texte hier (Zeilentitel, Erläuterungen) sind eigene Formulierungen; die
Excel-Istzustände stehen nur als Vergleichsliste für die Gegenlesung
(GBU_Riedl_Zuordnung.xlsx) – sie werden nicht in den Katalog übernommen.
"""

TITEL = 'Gefährdungsbeurteilung und Sicherheitskonzept für Aufzugsanlagen'
UNTERTITEL = ('Anlagenbezogene Beurteilung nach ArbSchG, BetrSichV, TRBS 3121 '
              'und TRBS 1115 unter Berücksichtigung der DIN EN 81-20/80')
VARIANTE = 'Riedl'                 # Anzeigename der Variante
TYP_SCHLUESSEL = 'riedl'           # Vorschlag für GbuTypen in der App
RULE_VERSION_GBU = 'riedl-mf-2026.2'      # .2: Prüfbericht Fragenkatalog 20.09.2026
RULE_VERSION_CYBER = 'riedl-cyber-2026.2'  # .2: Prüfbericht + Erhebungskarten 20.09.2026
VORLAGE_GBU = 'VFA Interlift, Version 21.08.2024 R 1.7.2 (Nutzungsrecht VFA-Akademie)'
VORLAGE_CYBER = 'Vorlage GBU Cybersicherheit ab 04-26 (TRBS 1115-1, IEC 62443)'

# ---------------------------------------------------------------------------
# Ampel: Engine-Stufe -> Farbe (Entscheidung 2, 17.09.2026)
# ---------------------------------------------------------------------------
AMPEL = {
    'NO_RISK': 'gruen', 'LOW': 'gruen',
    'MEDIUM': 'gelb',
    'HIGH': 'rot',
    'INCOMPLETE': 'offen',        # Blatt bleibt „offen", solange etwas fehlt
    'NOT_APPLICABLE': 'na',       # wird im Blatt nicht gewertet
}
AMPEL_TEXT = {'gruen': 'Grün', 'gelb': 'Gelb', 'rot': 'Rot', 'offen': 'offen',
              'na': 'n. a.'}

# Prüfbericht 20.09.2026: „Niedrig" zählt in der Ampel weiter als Grün (so ist die
# Riedl-/VFA-Vorlage gebaut), wird im Bericht aber als eigene Kategorie ausgewiesen.
# Sonst stehen Maßnahmen zu Befunden wie Drahtglas (MF-T04-R3), Schutzraum nach
# Altnorm (MF-F04-R3/MF-G02-R2) oder einer von zwei Verriegelungen (MF-K05-R4)
# ohne erkennbaren Anlass in einer grünen Zeile.
STUFE_ANZEIGE = {
    'NO_RISK': ('Kein Risiko', 'gruen', ''),
    'LOW': ('Niedrig', 'gruen', 'Hinweis – Maßnahme bei nächster Gelegenheit'),
    'MEDIUM': ('Mittel', 'gelb', ''),
    'HIGH': ('Hoch', 'rot', ''),
    'INCOMPLETE': ('unvollständig', 'offen', 'Pflichtangabe fehlt'),
    'NOT_APPLICABLE': ('nicht zutreffend', 'na', ''),
}

# Brücke zwischen der Engine-Stufe und der Riedl-Risikomatrix (W × S -> R).
# Die Engine bewertet regelbasiert und kennt kein W/S; die Vorlage erwartet je
# Zeile ein R. Festgelegt 20.09.2026 (Prüfbericht): Die Engine-Stufe ist führend,
# der R-Wert wird daraus abgeleitet und ist vom Prüfer nach oben überschreibbar.
# Rückrichtung wie in der App (stufeAusR): R >= 7 Hoch, >= 3 Mittel, 1 Niedrig, 0 Kein.
STUFE_ZU_R = {'NO_RISK': 0, 'LOW': 1, 'MEDIUM': 5, 'HIGH': 7}
R_ZU_STUFE = [(7, 'HIGH'), (3, 'MEDIUM'), (1, 'LOW'), (0, 'NO_RISK')]


def r_aus_stufe(status):
    """R-Wert der Riedl-Matrix zu einer Engine-Stufe (None = nicht bewertbar)."""
    return STUFE_ZU_R.get(status)


def stufe_aus_r(r):
    """Umkehrung – für von Hand gesetzte oder verschärfte R-Werte."""
    for grenze, stufe in R_ZU_STUFE:
        if r >= grenze:
            return stufe
    return 'NO_RISK'
# Legende des Deckblatts (VFA): Grün = kein Handlungsbedarf, Gelb = kurz- bis
# mittelfristiger Handlungsbedarf, Rot = sofortiger Handlungsbedarf.
AMPEL_LEGENDE = {
    'gruen': 'kein Handlungsbedarf',
    'gelb': 'kurz- bis mittelfristiger Handlungsbedarf',
    'rot': 'sofortiger Handlungsbedarf',
}
# Nohl-Matrix nur als Legende (Blatt „Risiko-Ende PDF" der Vorlage). Die
# R-Werte dienen der Zuordnung der Engine-Stufe zur gewohnten Skala, nicht
# der Bewertung.
NOHL_LEGENDE = [
    ('Kein Risiko', 'R = 0', 'ohne', 'keine Maßnahme'),
    ('Niedrig', 'R = 1', 'Kleinst', 'Risiko noch akzeptabel, wenn möglich Maßnahmen umsetzen'),
    ('Mittel', 'R = 3 … 5', 'Klein / Mittel', 'Maßnahmen mittel- bzw. kurzfristig planen und umsetzen'),
    ('Hoch', 'R = 7 … 10', 'Groß / Sehr groß', 'Sofortmaßnahmen notwendig, sonst Arbeiten einstellen'),
]


def ampel_zeile(stati):
    """Ampel einer Zeile aus den Stati ihrer Gefährdungen.
    Nicht zutreffende Gefährdungen zählen nicht; eine unvollständige macht die
    Zeile „offen"; sonst gilt die schlechteste Farbe."""
    farben = [AMPEL[s] for s in stati if AMPEL[s] != 'na']
    if not farben:
        return 'na'
    if 'offen' in farben:
        return 'offen'
    for f in ('rot', 'gelb', 'gruen'):
        if f in farben:
            return f
    return 'gruen'


def ampel_blatt(zeilen_ampeln):
    """Ampel eines Blatts (VFA-Formel K7: alles Grün -> Grün; irgendwo Rot ->
    Rot; sonst Gelb). Offene Zeilen halten das Blatt offen."""
    return ampel_zeile_farben(zeilen_ampeln)


def ampel_zeile_farben(farben):
    farben = [f for f in farben if f != 'na']
    if not farben:
        return 'na'
    if 'offen' in farben:
        return 'offen'
    for f in ('rot', 'gelb', 'gruen'):
        if f in farben:
            return f
    return 'gruen'


ampel_gesamt = ampel_zeile_farben   # Deckblatt-Formel G24: gleiche Logik


# ---------------------------------------------------------------------------
# Auswahllisten der Vorlage (Blatt „Daten") – für Maßnahmenverfolgung im
# Bericht (Spalten „Verantwortlich" und „Termin").
# ---------------------------------------------------------------------------
VERANTWORTLICH = ['Nicht anwendbar', 'Betreiber', 'Wartungsfirma',
                  'Servicetechniker', 'Aufzugswärter']
TERMIN = ['Nicht anwendbar', 'Sofort', 'Kurzfristig', 'Mittelfristig',
          'Vor Arbeitsbeginn', 'Ständig', 'Bis Quartalsende', 'Bis Jahresende',
          'Bis zur ZÜS-Prüfung']
# Vorbelegung der Spalten aus der Maßnahmengruppe der Engine
# (group_id „sofort" / „mittel") – der Ersteller kann sie überschreiben.
TERMIN_AUS_GRUPPE = {'sofort': 'Sofort', 'mittel': 'Mittelfristig'}

# ---------------------------------------------------------------------------
# Blätter der GBU (Teil 1, abgeleitet aus dem MF-Katalog)
#   nr      – Zeilennummer wie auf dem VFA-Blatt (Anzeige)
#   vfa     – Nummer der VFA-Maßnahmentabelle (K1…, Z1…, M1…, F1…, S1…) oder ''
#   titel   – eigene Zeilenbezeichnung (Bericht)
#   hazards – MF-Gefährdungen, die die Zeile bilden (Reihenfolge = Bericht)
#   excel   – Istzustände der Vorlage, die die Zeile ersetzt (nur Gegenlesung)
#   deckung – 'voll' | 'teilweise' | 'freitext'
#   bemerkung
# ---------------------------------------------------------------------------
BLAETTER = [
 {
  'key': 'kabine', 'kuerzel': 'K',
  'titel': 'Kabine und Aufzugsbenutzung',
  'anlagenbereich': 'In der Kabine / Aufzugsbenutzung',
  'zeilen': [
   {'nr': 1, 'vfa': 'K1', 'titel': 'Notrufsystem / Personenbefreiung',
    'hazards': ['MF-K01', 'MF-D01', 'MF-D02'], 'deckung': 'voll',
    'excel': ['Notruf-/Sprechverbindung zu ständig besetzter Stelle',
              'Klingel zu einer ständig besetzten Stelle',
              'Sprechverbindung oder Klingel zu einer nicht ständig besetzten Stelle',
              'Klingel im Schacht ohne Weiterleitung', 'Keine Notruffunktion'],
    'bemerkung': 'Art der Notrufeinrichtung (8.2) bildet die Excel-Liste 1:1 ab; '
                 'Notfallplan und Notbefreiungsanleitung (D01/D02) sind die '
                 'organisatorische Seite der Personenbefreiung (Excel K10 „Kein Alarmplan").'},
   {'nr': 2, 'vfa': 'K2', 'titel': 'Kabinenabschlusstür / Schließkantensicherung',
    'hazards': ['MF-T06'], 'deckung': 'voll',
    'excel': ['Kabinenabschlußtür mit Lichtgitter',
              'Kabinenabschlußtür mit anderer Schließkantensicherung',
              'Keine Kabinenabschlußtür, jedoch Sicherheitslichtgitter',
              'Keine Kabinenabschlußtür und kein Sicherheitslichtgitter'],
    'bemerkung': '„Keine selbstschließenden Schachttüren" aus K2 steht in Zeile 9 (MF-T03).'},
   {'nr': 3, 'vfa': 'K3', 'titel': 'Kabinenbeleuchtung / Notbeleuchtung',
    'hazards': ['MF-K15', 'MF-K02'], 'deckung': 'voll',
    'excel': ['Helle Leuchte mit Akkupufferung', 'Helle Leuchte und zusätzliche Notbeleuchtung',
              'Helle Leuchte ohne Notbeleuchtung', 'Dunkle Leuchte mit Notbeleuchtung',
              'Dunkle Leuchte ohne Notbeleuchtung', 'Keine ausreichende Beleuchtungssituation'],
    'bemerkung': ''},
   {'nr': 4, 'vfa': 'K4', 'titel': 'Haltegenauigkeit / Bündigkeit',
    'hazards': ['MF-K03'], 'deckung': 'voll',
    'excel': ['Präzise Haltegenauigkeit durch Motorregelung',
              'Präzise Haltegenauigkeit durch Aufsetzvorrichtung oder andere technische Maßnahme',
              'Stufenbildung > 5 mm', 'Stufenbildung > 15 mm'],
    'bemerkung': 'Schwellen im MF-Katalog: bis 10 / 11–20 / über 20 mm (EN 81-20 5.4.5.2, '
                 'Entscheidung Fragenkatalog 2026.9) statt 5 / 15 mm der Vorlage.'},
   {'nr': 5, 'vfa': 'K5', 'titel': 'Überlastsicherung / Nennlast',
    'hazards': ['MF-K06'], 'deckung': 'voll',
    'excel': ['Überlastsicherung verhindert Fahrt bei Überlastung',
              'Keine Überlastsicherung bei Personenaufzügen < 750 kg',
              'Keine Überlastsicherung bei Personen-/Lastenaufzügen > 750 kg'],
    'bemerkung': 'MF-K06 fragt zusätzlich Nennlastkennzeichnung und Nutzfläche (EN 81-80 Nr. 38).'},
   {'nr': 6, 'vfa': 'K6', 'titel': 'Sturzverhinderung nach oben / unbeabsichtigte Fahrkorbbewegung (UCM)',
    'hazards': ['MF-K13', 'MF-K12', 'MF-K14'], 'deckung': 'voll',
    'excel': ['Sturz nach oben durch aktive technische Maßnahmen (z. B. Notbremssystem) verhindert',
              'Sturz nach oben durch passive technische Maßnahmen verhindert',
              'Sturzverhinderung nach oben konstruktiv nicht notwendig',
              'Sturzverhinderung nach oben nicht vorhanden, regelmäßige Kontrolle durch ZÜS',
              'Sturzverhinderung nach oben nicht vorhanden',
              'Fahrtverhinderung bei geöffneter Schachttüre vorhanden (A3)',
              'Keine Fahrtverhinderung bei geöffneten Schachttüren'],
    'bemerkung': 'TRBS 3121 Anh. 1 Nr. 16 fasst UCM und Aufwärts-Übergeschwindigkeit zusammen; '
                 'die A3-Zeilen aus Excel K10 gehören deshalb hierher.'},
   {'nr': 7, 'vfa': 'K7', 'titel': 'Kabinentürschürze / Abstand zur Schachtwand',
    'hazards': ['MF-K04', 'MF-K05'], 'deckung': 'voll',
    'excel': ['Ausreichend lange (750 mm) und stabile Schürze vorhanden',
              'Zu kurze Kabinentürschürze (300 - 700 mm)',
              'Keine Kabinentürschürze (< 300 mm), Personenbefreiung ausschließlich durch fachkundige Person',
              'Keine Kabinentürschürze (< 300 mm)'],
    'bemerkung': 'MF-K05 (Schwellenabstand, TRBS Anh. 1 Nr. 19) hat in der Vorlage keine Zeile.'},
   {'nr': 8, 'vfa': 'K8', 'titel': 'Brandfallsteuerung / Verhalten im Brandfall / Schachtentrauchung',
    'hazards': ['MF-K08', 'MF-K09', 'MF-U09', 'MF-U10'], 'deckung': 'voll',
    'excel': ['Feuerwehraufzug mit entsprechenden Funktionen',
              'Dynamische oder statische Brandfallsteuerung vorhanden, angeschlossen an das Brandmeldesystem des Gebäudes',
              'Brandfallsteuerung mit manueller Auslösung',
              'Keine Brandfallsteuerung trotz Erfordernis',
              'Einbindung des Aufzugs in Brandschutzkonzept des Gebäudes unbekannt'],
    'bemerkung': 'MF-K08 nur, wenn das Brandschutzkonzept eine Brandfallsteuerung fordert (4.11); '
                 '„Einbindung unbekannt" über MF-U09 (BMA-Schnittstelle). MF-U10 wegen der '
                 'Schachtentrauchung in der Riedl-Cyber-Vorlage.'},
   {'nr': 9, 'vfa': 'K10', 'titel': 'Schachttüren: Verriegelung, Selbstschließen, Notentriegelung, Glas',
    'hazards': ['MF-T01', 'MF-T03', 'MF-T02', 'MF-T04'], 'deckung': 'voll',
    'excel': ['Selbstschließende Schachttüren', 'Keine selbstschließende Schachttüren',
              'Keine Fehlschließeinrichtung an den Schachttüren'],
    'bemerkung': 'Ersetzt die alte Cyber-Zeile K9 der Vorlage; TRBS Anh. 1 Nr. 9, 11, 12. '
                 'Glas (T04) nur bei Türen mit Glas (Anlagenmerkmal 4.1).'},
   {'nr': 10, 'vfa': 'K10', 'titel': 'Betrieb und Organisation: Wartung, Prüfung, beauftragte Person',
    'hazards': ['MF-D03', 'MF-D04', 'MF-D05'], 'deckung': 'voll',
    'excel': ['Keine ausreichende Wartung / Prüfung gewährleistet',
              'Fehlende ZÜS Prüfung', 'Kein Aufzugswärter für Personenbefreiung vorhanden'],
    'bemerkung': 'Betreiberpflichten nach BetrSichV (Vorabbogen D); Zutrittsregelung E4 in D05.'},
   {'nr': 11, 'vfa': 'K10', 'titel': 'Sonstiges: Nutzung, Ausstattung, Umfeld',
    'hazards': ['MF-K11', 'MF-K10', 'MF-U03'], 'deckung': 'teilweise',
    'excel': ['Vandalismus', 'Kein Handlauf in der Kabine', 'Brandfördernde Stoffe in der Kabine',
              'Denkmalschutz', 'Unruhige Fahrt, starke Beschleunigungs- und Verzögerungsstöße',
              'Laute Fahrgeräusche in der Kabine', 'Technische Mängel', 'Missbräuchliche Nutzung'],
    'bemerkung': 'Denkmalschutz, unruhige Fahrt, Fahrgeräusche, technische Mängel und '
                 'missbräuchliche Nutzung haben keine MF-Gefährdung – dafür die Freitextzeile '
                 '„Sonstige Gefährdung" des Blatts (Lärm/Unfälle sind im MF nur Dokumentation).'},
  ]},
 {
  'key': 'zugang', 'kuerzel': 'Z',
  'titel': 'Zugang zum Maschinenraum',
  'anlagenbereich': 'Zugang zum Aufzug, Maschinen- oder Steuerungsraum',
  'zeilen': [
   {'nr': 1, 'vfa': 'Z1', 'titel': 'Beleuchtung',
    'hazards': ['MF-Z01'], 'deckung': 'voll',
    'excel': ['Helle Leuchtstofflampen', 'Weiße Wände, helle Leuchten', 'Dunkle Schiffsarmaturen',
              'Leuchten an ungeeigneter Stelle', 'Defekte Leuchtkörper', 'Keine Beleuchtung vorhanden'],
    'bemerkung': ''},
   {'nr': 2, 'vfa': 'Z2', 'titel': 'Leitern, Aufstiege, Absturzkanten',
    'hazards': ['MF-Z03', 'MF-Z04'], 'deckung': 'voll',
    'excel': ['Treppe mit Handlauf', 'Ordnungsgemäße Zugtreppe', 'Treppe ohne Handlauf',
              'Zugtreppe ist verbraucht (alt)', 'Absturzgefahr', 'Bruchgefahr', 'Sicherer Aufstieg fehlt'],
    'bemerkung': 'Art des Aufstiegs (5.5) bildet die Excel-Liste ab; Absturzkanten über MF-Z04.'},
   {'nr': 3, 'vfa': 'Z3', 'titel': 'Wege',
    'hazards': ['MF-Z02', 'MF-Z05'], 'deckung': 'voll',
    'excel': ['Wege trocken, sauber, hell', 'Wege zugänglich, sicher', 'Wege rutschig, nass', 'Wege dunkel',
              'Wege mit Stolpergefahr', 'Wege mit Einsperrrisiko', 'Wege mit Absturzgefahr'],
    'bemerkung': '„Wege dunkel" über Zeile 1, „Absturzgefahr" über Zeile 2, „Einsperrrisiko" über MF-Z05.'},
   {'nr': 4, 'vfa': 'Z4', 'titel': 'Zugangstür und Zutritt (nur befugte Personen)',
    'hazards': ['MF-Z07'], 'deckung': 'voll',
    'excel': ['Maschinenraumtür verschlossen/verschließbar', 'Maschinenraumtür nicht verschlossen/verschließbar'],
    'bemerkung': 'In der Vorlage die Cyber-Zeile Z4; hier die technische Seite (abschließbare Tür), '
                 'die Zugangsfrage der Cyber-GBU (2.1/2.2) bleibt im Cyber-Blatt.'},
   {'nr': 5, 'vfa': 'Z6', 'titel': 'Zugang für die Notbefreiung (Schlüsseltresor)',
    'hazards': ['MF-Z09'], 'deckung': 'voll',
    'excel': ['Zugang jederzeit möglich durch im Schlüsseltresor hinterlegten Schlüssel',
              'Zugang nur möglich durch an der Leitwarte / Pforte hinterlegten Schlüssel',
              'Zugang nicht jederzeit möglich, Personenbefreiung nicht garantiert!'],
    'bemerkung': 'Frage 3.4 bildet die drei Excel-Werte 1:1 ab.'},
  ]},
 {
  'key': 'maschinenraum', 'kuerzel': 'M',
  'titel': 'Maschinenraum',
  'anlagenbereich': 'Maschinen- oder Steuerungsraum (wenn nicht im Fahrschacht)',
  'zeilen': [
   {'nr': 1, 'vfa': 'M1', 'titel': 'Elektrische Berührungssicherheit',
    'hazards': ['MF-M02', 'MF-M16'], 'deckung': 'voll',
    'excel': ['Ausschließlich berührungssichere Bauteile', 'Ordnungsgemäße Abdeckungen',
              'Nur teilweise Berührungssicherheit', 'Unsichere Teile im Schaltschrank verbaut',
              'Offene Schalttafel ohne Schaltschrank', 'Offene Kontakte oder Schalter an der Maschine'],
    'bemerkung': 'MF-M16 (Potenzialausgleich, bauseitige Installation) ergänzt TRBS Anh. 1 Nr. 21.'},
   {'nr': 2, 'vfa': 'M2', 'titel': 'Einzugsgefahr',
    'hazards': ['MF-M03'], 'deckung': 'voll',
    'excel': ['Komplett abgedeckte Einzugstellen', 'Hydraulikanlage ohne Einzugstellen',
              'Teilweise Abdeckungen', 'Treibscheibe ist abgedeckt, Geschwindigkeitsbegrenzer nicht',
              'Einzugsstellen offen', 'Ungeschützt bewegte Maschinenteile'],
    'bemerkung': 'Auch Excel M4 „Ungeschützt bewegte Maschinenteile".'},
   {'nr': 3, 'vfa': 'M3', 'titel': 'Beleuchtung',
    'hazards': ['MF-M01'], 'deckung': 'voll',
    'excel': ['Helle Leuchtstofflampen', 'Weiße Wände, helle Leuchten', 'Dunkle Schiffsarmaturen',
              'Leuchten an ungeeigneter Stelle', 'Defekte Leuchtkörper', 'Keine Beleuchtung vorhanden'],
    'bemerkung': ''},
   {'nr': 4, 'vfa': '', 'titel': 'Antrieb, Bremse und Hydraulik',
    'hazards': ['MF-M08', 'MF-M13'], 'deckung': 'voll',
    'excel': [],
    'bemerkung': 'TRBS Anh. 1 Nr. 16/17 (Bremse, Hydraulik) – in der Vorlage ohne eigene Zeile, '
                 'aber im Blatt „Bezug zum Stand der Technik" geführt.'},
   {'nr': 5, 'vfa': 'M6', 'titel': 'Stand der Technik: unabhängige Fahrschütze, abschließbarer Hauptschalter, Kennzeichnung und Stromlaufpläne',
    'hazards': ['MF-M10', 'MF-M07', 'MF-M17'], 'deckung': 'voll',
    'excel': ['Unabhängige Fahrschütze vorhanden', 'Nur ein Fahrschütz vorhanden, jedoch selbst überwachende Steuerung',
              'Abschließbarer Hauptschalter vorhanden', 'Kennzeichnung elektrischer Einrichtungen und Stromlaufpläne vorhanden',
              'Mangelhafte Kennzeichnung elektrischer Einrichtungen', 'Fehlende unabhängige Fahrschütze',
              'Kein abschließbarer Hauptschalter vorhanden', 'Fehlender oder unrichtiger Stromlaufplan'],
    'bemerkung': 'Drei Unterzeilen wie in der Vorlage (Zeilen 24/26/28).'},
   {'nr': 6, 'vfa': '', 'titel': 'Notbetrieb und Personenbefreiung',
    'hazards': ['MF-M15'], 'deckung': 'voll',
    'excel': [],
    'bemerkung': 'Handrad/Bremslüftung/Evakuierungssteuerung und Einweisung (EN 81-80 Nr. 60) – '
                 'Grundlage der Aufgaben „Personenbefreiung" auf dem Deckblatt.'},
  ]},
 {
  'key': 'fahrkorbdach', 'kuerzel': 'F',
  'titel': 'Kabinendach',
  'anlagenbereich': 'Auf dem Fahrkorbdach',
  'zeilen': [
   {'nr': 1, 'vfa': 'F1', 'titel': 'Absturzgefahr',
    'hazards': ['MF-F01'], 'deckung': 'voll',
    'excel': ['Keine Spaltabstände größer 30 cm', 'Geländerhöhe 70 -110 cm bei Spaltbreite bis 50 cm',
              'Geländerhöhe größer/gleich 110 cm', 'Geländerhöhe 70- < 110 cm bei Spaltbreite > 50 cm',
              'Spaltbreite geringfügig zu groß', 'Geländerhöhe < 70 cm bei Spaltbreite > 30 cm',
              'Kein Geländer bei Spaltmaß größer 30 cm'],
    'bemerkung': 'Schwellen 300/500/850 mm und 700/1100 mm wie EN 81-20 5.4.7.'},
   {'nr': 2, 'vfa': 'F2', 'titel': 'Einzugsgefahr',
    'hazards': ['MF-F02'], 'deckung': 'voll',
    'excel': ['Komplett abgedeckte Einzugsstellen', 'Keine Einzugsstellen vorhanden', 'Teilweise Abdeckungen',
              'Einzugsstellen offen'],
    'bemerkung': ''},
   {'nr': 3, 'vfa': 'F3', 'titel': 'Gegengewicht / Nachbaraufzug',
    'hazards': ['MF-F03'], 'deckung': 'voll',
    'excel': ['Gefahrenstellen komplett abgedeckt', 'Engmaschiger Zaun', 'Ausreichende Abstände',
              'Teilweise Abdeckungen oder Geländer', 'Grobmaschiger Zaun oder Spanndrähte', 'Fehlender Zaun',
              'Fehlende Abdeckungen'],
    'bemerkung': 'Frage 9.6 bildet die Excel-Liste ab; nur bei mehreren Aufzügen im Schacht (4.8).'},
   {'nr': 4, 'vfa': 'F5', 'titel': 'Stand der Technik: Schutzraum, Not-Halt und Inspektionssteuerung auf dem Fahrkorbdach',
    'hazards': ['MF-F04', 'MF-F06', 'MF-F05'], 'deckung': 'voll',
    'excel': ['Ausreichender Schutzraum im Schachtkopf', 'Flacher Schachtkopf, aber Schutzraum durch temporäre Maßnahme gegeben',
              'Not-Aus und Inspektionssteuerung auf FK-Dach vorhanden', 'Not-Aus auf FK-Dach vorhanden, aber keine Inspektionssteuerung',
              'Ungenügender Schutzraum im Schachtkopf', 'Not-Aus und Inspektionssteuerung auf FK-Dach nicht vorhanden',
              'Inspektionsgeschwindigkeit > 0,63 m/s'],
    'bemerkung': 'Inspektionsgeschwindigkeit ist Frage 9.8c in MF-F05.'},
   {'nr': 5, 'vfa': 'K11', 'titel': 'Notruf auf dem Fahrkorbdach',
    'hazards': ['MF-F09'], 'deckung': 'voll',
    'excel': ['Notrufverbindung vom FK-Dach und der Grube (oder Unterseite FK) zu ständig besetzter Stelle vorhanden',
              'Keine Notrufverbindung vom FK-Dach und der Grube (oder Unterseite FK) zu ständig besetzter Stelle'],
    'bemerkung': 'Die Grube steht im Schacht-Blatt (MF-G05).'},
  ]},
 {
  'key': 'schacht', 'kuerzel': 'S',
  'titel': 'Fahrschacht und Schachtgrube',
  'anlagenbereich': 'In der Schachtgrube und im Fahrschacht',
  'zeilen': [
   {'nr': 1, 'vfa': 'S1', 'titel': 'Beleuchtung',
    'hazards': ['MF-S01', 'MF-G01'], 'deckung': 'voll',
    'excel': ['Helle Leuchtstofflampen', 'Weiße Wände, helle Leuchten', 'Dunkle Schiffsarmaturen',
              'Leuchten an ungeeigneter Stelle', 'Defekte Leuchtkörper', 'Keine Beleuchtung vorhanden'],
    'bemerkung': 'Schacht und Grube getrennt (TRBS Anh. 1 Nr. 8).'},
   {'nr': 2, 'vfa': 'S2', 'titel': 'Schachtzugänge, Schachtabsperrungen, Selbstbefreiung und Notruf in der Grube',
    'hazards': ['MF-S07', 'MF-G05'], 'deckung': 'teilweise',
    'excel': ['Verschließbare Schachttür, Nothalt im Schacht, Türverschluss von innen erreichbar',
              'Ausreichende Absperrungen sind vor Ort vorhanden',
              'Leichte transportable Absperrungen im Kundendienstfahrzeug der Wartungsfirma vorhanden',
              'Keine Absperrungen vorhanden', 'Flatterband', 'Fehlender Notruf in der Schachtgrube'],
    'bemerkung': 'Absperrungen (Kundendienstfahrzeug, Flatterband) sind Arbeitsmittel des Monteurs '
                 '(DGUV 209-085) und keine Anlageneigenschaft – im MF bewusst nicht erhoben; '
                 'bei Bedarf Freitext oder Hinweis für den Servicetechniker.'},
   {'nr': 3, 'vfa': 'S3', 'titel': 'Grubenleiter / Zugang zur Schachtgrube',
    'hazards': ['MF-G04'], 'deckung': 'voll',
    'excel': ['Fest installierte Grubenleiter', 'Grubenleiter mobil im Schacht',
              'Grubenleiter ist beim Kunden deponiert und kann benutzt werden',
              'Grubenleiter wird in Kundendienstfahrzeug mitgeführt',
              'Grubenleiter an ungünstiger Stelle angebracht', 'Keine Grubenleiter vorhanden'],
    'bemerkung': 'Frage 11.6 bildet die Excel-Liste ab (fest, mobil, schwer, kunde, fahrzeug, keine).'},
   {'nr': 4, 'vfa': 'S5', 'titel': 'Stand der Technik: Schutzraum, Not-Halt und Inspektionssteuerung in der Schachtgrube, Puffer',
    'hazards': ['MF-G02', 'MF-G03', 'MF-G06'], 'deckung': 'voll',
    'excel': ['Ausreichender Schutzraum in der Schachtgrube', 'Flache Schachtgrube, aber Schutzraum durch temporäre Maßnahme gegeben',
              'Puffer als GG- oder Fahrkorbwegbegrenzung vorhanden', 'Not-Aus Schachtgrube vorhanden',
              'Not-Aus Schachtgrube vorhanden, aber schwer erreichbar', 'Keine Puffer als GG- oder Fahrkorbwegbegrenzung',
              'Ungenügender Schutzraum in der Schachtgrube', 'Kein Not-Aus in der Schachtgrube',
              'Keine Inspektionssteuerung in der Schachtgrube', 'Fehlender Notaus in der Schachtgrube'],
    'bemerkung': 'Auch Excel S4 (Inspektionssteuerung, Not-Aus Grube).'},
   {'nr': 5, 'vfa': '', 'titel': 'Gegengewicht und Nachbaraufzug in der Schachtgrube',
    'hazards': ['MF-G07', 'MF-G08'], 'deckung': 'voll',
    'excel': [],
    'bemerkung': 'TRBS Anh. 1 Nr. 2 und 3 – in der Vorlage nur im Blatt „Bezug zum Stand der Technik".'},
   {'nr': 6, 'vfa': 'S4', 'titel': 'Verschmutzung, Wasser und Umgebungsbedingungen',
    'hazards': ['MF-U02', 'MF-U07'], 'deckung': 'voll',
    'excel': ['Betriebsbedingte Verschmutzung', 'Nichtbetriebsbedingte Verschmutzung'],
    'bemerkung': 'MF-U02/U07 sind Ortsfragen über alle Bereiche (Zugang, Triebwerksraum, Schacht, '
                 'Grube); im Bericht hier zusammengefasst.'},
  ]},
]

# Jedes Blatt hat zusätzlich die Freitextzeile „Sonstige Gefährdung" (Befund-
# Bereich der App: Freitext mit manueller Einstufung) für alles, was der
# Katalog nicht kennt (Denkmalschutz, unruhige Fahrt, Absperrmaterial …).
SONSTIGES = {'titel': 'Sonstiges (Freitext, eigene Einstufung)',
             'hinweis': 'Für Feststellungen ohne Katalogzeile; Einstufung Kein/Niedrig/Mittel/Hoch '
                        'durch den Ersteller, geht in die Blatt-Ampel ein.'}

# ---------------------------------------------------------------------------
# Cyber-Blatt (Teil 2, abgeleitet aus dem Cyber-Katalog CY)
#   komponente – Schlüssel für Hersteller/Typ im Anlagenstamm (App)
#   erlaeuterung – Standardtext für den Bericht, wenn die Zeile Grün ist
#                  (eigene Formulierung nach dem Blatt „Erläuterungen für
#                  Standard" der Riedl-Vorlage); leer = kein Standardtext
# ---------------------------------------------------------------------------
CYBER_BLATT = {
 'key': 'cyber', 'kuerzel': 'C',
 'titel': 'Cybersicherheit',
 'anlagenbereich': 'Cybersicherheit – anlagenbezogene Beurteilung nach TRBS 1115-1',
 'zeilen': [
  {'nr': 1, 'komponente': 'steuerung', 'titel': 'Steuerung',
   'hazards': ['CY-C01'], 'deckung': 'voll',
   'excel': ['nicht vorhanden', 'Schnittstelle vorhanden', 'manuelle Manipulation: Tastatur vorhanden',
             'manuelle Manipulation: Schnittstelle Handterminal', 'Fernzugriff über Netzwerk'],
   'erlaeuterung': 'Die Steuerung sitzt in einem geschlossenen Schaltschrank im Maschinenraum bzw. '
                   'im Steuerschrank (maschinenraumlos) ohne Zugriff von außen. Einstellungen sind '
                   'nur vor Ort möglich; Parameteränderungen sind durch ein Passwort gesichert. '
                   'Ergänzend gelten die Festlegungen zu Maschinenraum/Steuerschrank.',
   'bemerkung': 'Schnittstellenkategorie 3.1.2 deckt die Excel-Gefährdungen ab (keine / kabelgebunden / '
                'Benutzer / kabellos / Fernzugriff); Relais-Steuerungen sind nicht zutreffend.'},
  {'nr': 2, 'komponente': 'pessral', 'titel': 'PESSRAL-Komponenten',
   'hazards': ['CY-C02'], 'deckung': 'voll',
   'excel': ['nicht vorhanden', 'S1-Box', 'S2-Box', 'Limax'],
   'erlaeuterung': 'PESSRAL-Komponenten befinden sich im Maschinenraum, im Schaltschrank oder im '
                   'Schacht und sind von außen nicht erreichbar. Ein Eingriff ist nur manuell vor Ort '
                   'möglich und setzt die Anlage dabei still.',
   'bemerkung': 'Elektronische UCM-/SAFÜ-Module (CY-C07/C08) laufen in dieser Variante unter '
                'PESSRAL (Klärung K-R03).'},
  {'nr': 3, 'komponente': 'fu', 'titel': 'Frequenzumrichter',
   'hazards': ['CY-C03'], 'deckung': 'voll',
   'excel': ['nicht vorhanden', 'Schnittstelle vorhanden', 'manuelle Manipulation: Tastatur vorhanden',
             'manuelle Manipulation: Schnittstelle Handterminal'],
   'erlaeuterung': 'Der Umrichter befindet sich im Maschinenraum, im Schaltschrank oder im Schacht. '
                   'Einstellungen sind nur vor Ort möglich; das Handterminal wird nur zum Parametrieren '
                   'angesteckt und danach sicher verwahrt. Ergänzend gelten die Festlegungen zu '
                   'Maschinenraum/Steuerschrank und Aufzugsschacht.',
   'bemerkung': ''},
  {'nr': 4, 'komponente': 'notruf', 'titel': 'Notruf',
   'hazards': ['CY-C04'], 'deckung': 'voll',
   'excel': ['nicht vorhanden', 'Zugriff über Telefonnetz', 'manuelle Manipulation: Tastatur vorhanden',
             'manuelle Manipulation: Schnittstelle Handterminal'],
   'erlaeuterung': 'Das Notrufgerät sitzt auf dem Fahrkorbdach; ein Zugriff über die Telefon-/'
                   'Mobilfunkverbindung ist grundsätzlich möglich. Die Rufnummer ist nur dem '
                   'Befreiungsdienst bekannt und an der Anlage nicht dokumentiert. Das Gerät setzt in '
                   'festen Abständen einen Routineruf ab; bleibt er aus, wird ein Serviceeinsatz ausgelöst.',
   'bemerkung': 'Routineruf/Testruf = Frage 3.4.4 (Kompensation).'},
  {'nr': 5, 'komponente': 'tuer', 'titel': 'Türsteuergerät',
   'hazards': ['CY-C06'], 'deckung': 'voll',
   'excel': ['nicht vorhanden', 'Schnittstelle vorhanden', 'manuelle Manipulation: Tastatur vorhanden',
             'manuelle Manipulation: Schnittstelle Handterminal'],
   'erlaeuterung': 'Das Türsteuergerät ist auf dem Fahrkorbdach verbaut und nur über den Schacht '
                   'erreichbar. Einstellungen sind nur vor Ort möglich; das Handterminal wird nur zum '
                   'Parametrieren angesteckt und danach sicher verwahrt. Ergänzend gelten die '
                   'Festlegungen zum Aufzugsschacht.',
   'bemerkung': ''},
  {'nr': 6, 'komponente': 'gebaeude', 'titel': 'Schachtentrauchung und bauseitige Einrichtungen (Gebäudeschnittstelle)',
   'hazards': ['CY-C14'], 'deckung': 'voll',
   'excel': ['Schachtentrauchung: nicht vorhanden / Schnittstelle vorhanden / manuelle Manipulation',
             'bauseitige Einrichtungen: Zutrittskontrolle, Kartenleser, Notstromversorgung, Brandfallsteuerung'],
   'erlaeuterung': 'Die Steuerung der Schachtentrauchung sitzt im Maschinenraum oder in einem '
                   'abgeschlossenen Schaltschrank; Einstellungen sind nur vor Ort möglich. Bei Störung '
                   'oder Stromausfall öffnet der Rauchabzug, ein gefährlicher Zustand entsteht nicht. '
                   'Bauseitige Systeme (Zutrittskontrolle, Brandmeldeanlage, Kartenleser, Notstrom) '
                   'wirken über potenzialfreie Kontakte auf den nicht sicherheitsgerichteten Teil der '
                   'Steuerung; die Schnittstelle ist rückwirkungsfrei. Die Cybersicherheit dieser '
                   'Systeme selbst beurteilt deren Hersteller bzw. der Betreiber.',
   'bemerkung': 'Die Riedl-Vorlage führt Schachtentrauchung und bauseitige Einrichtungen getrennt; '
                'im CY-Katalog ist beides die Gebäudeschnittstelle (3.14.1 rückwirkungsfrei, '
                '3.14.2 sicherer Zustand). Hersteller/Typ werden trotzdem getrennt erfasst.'},
  {'nr': 7, 'komponente': '', 'titel': 'Zugang und Zugriff: Maschinenraum/Steuerschrank, Aufzugsschacht, Schlüsseldepot, Servicegeräte',
   'hazards': ['CY-Z01', 'CY-Z04', 'CY-Z05'], 'deckung': 'voll',
   'excel': ['Maschinenraum verschlossen halten', 'Schaltschrank verschlossen halten',
             'Handterminal nur bei Montage / Wartungsarbeiten anstecken', 'Steuerung/FU/Notrufgerät passwortgeschützt'],
   'erlaeuterung': 'Maschinenraum und Steuerschrank sind nur befugten Personen zugänglich; das Schloss '
                   'hat keine Standardschließung, der Schlüssel liegt für die Notbefreiung im '
                   'Schlüsseldepot. Der Schacht ist nur über die Schachttüren mit dem vorgesehenen '
                   'Werkzeug (Dreikant) betretbar; das Werkzeug ist im Maschinenraum gesichert '
                   'hinterlegt. Die Schließung des Schlüsseldepots legt der Befreiungsdienst fest, die '
                   'Ausgabe der Schlüssel ist organisatorisch geregelt.',
   'bemerkung': 'Die Zugangsfragen 2.1–2.3 wirken zusätzlich als Modifier an jeder Komponente (K-C21).'},
  {'nr': 8, 'komponente': '', 'titel': 'Netz, Fernzugriff und Fernwartung (nur bei vernetzter Anlage)',
   'hazards': ['CY-C11', 'CY-C12', 'CY-C13', 'CY-N01', 'CY-N02'], 'deckung': 'voll',
   'excel': ['Fernzugriff über Netzwerk', 'Vorlage der Beurteilung des vorhandenen Netzes durch Betreiber'],
   'erlaeuterung': '',
   'bemerkung': 'Ohne Netzanbindung (1.5) sind C11–C13 nicht zutreffend; Softwarestand (4.5) und '
                'Härtung (4.6) werden immer gefragt.'},
  {'nr': 9, 'komponente': '', 'titel': 'Organisation und Nachweise: Herstellervorgaben, Rückwirkungsfreiheit, Wirksamkeit, Änderungen',
   'hazards': ['CY-O02', 'CY-O07', 'CY-O05', 'CY-O06', 'CY-O08'], 'deckung': 'voll',
   'excel': ['Allgemeines (Absätze 2–5 der Vorlage)', 'Überprüfung der Wirksamkeit der Cybersicherheitsmaßnahmen'],
   'erlaeuterung': '',
   'bemerkung': 'Bildet die Textblöcke „Allgemeines" und „Überprüfung der Wirksamkeit" der Vorlage als '
                'Fragen ab; Verantwortlichkeit/Notfallmanagement/Unterweisung (O01/O03/O04) bewusst nicht.'},
 ]}

# Texte des Cyber-Deckblatts (eigene Formulierung nach der Vorlage).
CYBER_ALLGEMEINES = [
    'Bei überwachungsbedürftigen Anlagen nach ÜAnlG ist grundsätzlich von einem erheblichen '
    'Risiko für die Sicherheit und Gesundheit von Beschäftigten und weiteren Personen im '
    'Gefahrenbereich auszugehen; das wurde bei der Beurteilung berücksichtigt.',
    'Grundlage der Bewertung der Cybersicherheitsmaßnahmen sind TRBS 1115 Teil 1 und IEC 62443.',
    'Die Umsetzung von Cybersicherheitsmaßnahmen darf bestehende Sicherheitsfunktionen nicht '
    'beeinträchtigen; die Rückwirkungsfreiheit ist sicherzustellen.',
    'Die Vorgaben der Hersteller der eingesetzten Komponenten werden bei der Festlegung der '
    'Maßnahmen berücksichtigt.',
    'Wirksamkeit und Funktionsfähigkeit der Maßnahmen werden regelmäßig nach TRBS 1115 Teil 1 '
    '(Abschnitte 5 und 8.2) geprüft.',
]
CYBER_WIRKSAMKEIT = [
    'Die Maßnahmen sind in geeigneten Zeitabständen, nach Änderungen an der Anlage, bei '
    'Änderung des Stands der Technik und bei neuen Erkenntnissen zu Cyberbedrohungen zu überprüfen.',
    'Änderungen im Umfeld der Aufzugsanlage sind der Wartungsfirma unverzüglich mitzuteilen und in '
    'der Gefährdungsbeurteilung zur Cybersicherheit zu vermerken; Maßnahmen sind anzupassen.',
]
CYBER_UNTERSCHRIFT = ('Mit der Unterschrift wird bestätigt, dass die grundlegenden Anforderungen und '
                      'Prinzipien der Cybersicherheit an Aufzugsanlagen bekannt sind. Das Dokument '
                      'wird mit beiden Unterschriften gültig.')

# Herstellerlisten der Vorlage (Blatt „Daten") – Vorschlagslisten für die
# Stammdatenfelder „Hersteller" je Komponente; freie Eingabe bleibt möglich.
HERSTELLER = {
    'steuerung': ['NEW', 'Schneider Lisa', 'Hydroware', 'KLST', 'Kollmorgen', 'Riedl'],
    'pessral': ['NEW', 'Elgo'],
    'fu': ['Ziehl-Abegg', 'LiftEquip', 'Brunner & Fecher', 'Nidec', 'KEB', 'Danfoss'],
    'notruf': ['Base', 'Telegärtner', 'Safeline', 'Telenot', 'Behnke', 'Ascendor', 'MS AG'],
    'tuer': ['Riedl Quantum', 'Meiller', 'Fermator', 'Wittur', 'Langer & Laumann'],
    'entrauchung': ['B.A.S.E.', 'D&H'],
    'bauseitig': [],
}
# Stammdatenfelder je Komponente (App: Gruppe „Cyber-Komponenten (Riedl)"):
# Hersteller + Typ; „gebaeude" wird als Schachtentrauchung und bauseitige
# Einrichtungen getrennt erfasst.
KOMPONENTEN_STAMM = [
    ('steuerung', 'Steuerung'), ('pessral', 'PESSRAL-Komponenten'),
    ('fu', 'Frequenzumrichter'), ('notruf', 'Notruf'), ('tuer', 'Türsteuergerät'),
    ('entrauchung', 'Schachtentrauchung'), ('bauseitig', 'bauseitige Einrichtungen'),
]

# ---------------------------------------------------------------------------
# Deckblatt / Blattkopf (aus der Vorlage; Felder kommen aus dem Anlagenstamm)
# ---------------------------------------------------------------------------
DECKBLATT_FELDER = [
    ('ersteller', 'Beurteilungs-/Konzeptersteller'),
    ('verwender', 'Anlagenverwender (Betreiber)'),
    ('stand', 'Bearbeitungsstand'),
    ('bezeichnung', 'Bezeichnung / Bauvorhaben'),
    ('standort', 'Standort der Anlage'),
    ('fabriknummer', 'Anl.- / Fabrik-Nr.'),
]
DECKBLATT_UNTERTITEL = ('Beurteilung der Gefahrenorte der Aufzugsanlage für Verwender (Betreiber), '
                        'Instandhalter und Benutzer')
# Block Z je Blatt (Freitext, auf dem Deckblatt zusammengefasst). Vorbelegung
# aus den Maßnahmen der roten/gelben Zeilen nach Verantwortlichem.
BLOCK_Z = [
    ('verwender', 'Aufgaben für den Verwender', ['Betreiber', 'Aufzugswärter']),
    ('wartung', 'Aufgaben für die Wartungsfirma', ['Wartungsfirma']),
    ('service', 'Hinweise für den Servicetechniker', ['Servicetechniker']),
]
UNTERSCHRIFTEN = ['Ort, Datum, Ersteller', 'Ort, Datum, Verwender (Betreiber)']

# ---------------------------------------------------------------------------
# Bewusst nicht enthalten (bleiben dem vollen MF-/CY-Typ vorbehalten). Jede
# Zeile kann durch Eintrag in BLAETTER/CYBER_BLATT nachgeholt werden – der
# Generator prüft, dass jede MF-/CY-Gefährdung entweder zugeordnet oder hier
# begründet ist.
# ---------------------------------------------------------------------------
NICHT_ENTHALTEN = {
    # Zugang
    'MF-Z06': 'Zugang über fremde Räume / Materialtransport – in der Vorlage nicht abgefragt.',
    'MF-Z08': 'Flucht- und Rettungswege – Arbeitsstätte (ASR A2.3), in der Vorlage nicht abgefragt.',
    # Triebwerksraum
    'MF-M04': 'Raumhöhe/Freiflächen – Konstruktionspunkt, in der Vorlage nicht abgefragt.',
    'MF-M05': 'Ebenen/Podeste im Triebwerksraum – in der Vorlage nicht abgefragt.',
    'MF-M06': 'Boden im Triebwerksraum – in der Vorlage nicht abgefragt (Verschmutzung über MF-U02).',
    'MF-M09': 'Motorschutz – EN 81-80 Nr. 67, kein TRBS-Anhang-1-Punkt, in der Vorlage nicht abgefragt.',
    'MF-M11': 'Laufzeitüberwachung – wie MF-M09.',
    'MF-M12': 'Phasenumkehrschutz – wie MF-M09.',
    'MF-M14': 'Hebezeuge/Anschlagpunkte – Instandhaltungsthema, in der Vorlage nicht abgefragt.',
    'MF-M18': 'Sprechverbindung Triebwerksraum–Fahrkorb – nur bei Förderhöhe > 30 m, in der Vorlage nicht abgefragt.',
    'MF-M19': 'Aufzugsfremde Einrichtungen im Triebwerksraum – in der Vorlage nicht abgefragt.',
    'MF-M20': 'Not-Halt im Rollenraum – Sonderfall, in der Vorlage nicht abgefragt.',
    'MF-M21': 'Notendschalter – EN 81-80 Nr. 57, kein TRBS-Anhang-1-Punkt.',
    # Türen
    'MF-T05': 'Feuerwiderstand der Schachttüren – Bauaufsicht, in der Vorlage nicht abgefragt.',
    'MF-T07': 'Fläche unter der Schachttürschwelle – EN 81-80 Nr. 9, kein TRBS-Anhang-1-Punkt.',
    'MF-T08': 'Rückhaltung der Türblätter – EN 81-80 Nr. 26, kein TRBS-Anhang-1-Punkt.',
    'MF-T09': 'Verbindung mehrteiliger Türblätter – EN 81-80 Nr. 35, kein TRBS-Anhang-1-Punkt.',
    # Fahrkorb
    'MF-K07': 'Lüftung des Fahrkorbs – EN 81-80 Nr. 44, in der Vorlage nicht abgefragt.',
    # Fahrkorbdach
    'MF-F07': 'Tragfähigkeit Fahrkorbdach / Dachklappe – EN 81-80 Nr. 41/42, in der Vorlage nicht abgefragt.',
    'MF-F08': 'Notbeleuchtung Fahrkorbdach – in der Vorlage nicht abgefragt.',
    # Schacht
    'MF-S02': 'Beleuchtung an den Schachtzugängen – Arbeitsstätte, in der Vorlage nicht abgefragt.',
    'MF-S03': 'Schachtumwehrung – Konstruktionspunkt (Gitterschächte), in der Vorlage nicht abgefragt.',
    'MF-S04': 'Führungsschienen nicht aus Stahl – Sonderfall Altanlagen.',
    'MF-S05': 'Fangvorrichtung/Begrenzer/Schlaffseil – Prüfumfang der ZÜS und Wartung (Entscheidung 17.09.2026: Prüfpunkte ohne Katalogfrage bleiben Wartung/ZÜS).',
    'MF-S06': 'Aufzugsfremde Einrichtungen im Schacht – in der Vorlage nicht abgefragt.',
    # Umfeld
    'MF-U01': 'Asbest/Schadstoffe – eigenes Thema (Schadstoffkataster), in der Vorlage nicht abgefragt.',
    'MF-U04': 'Gefahrstofflagerung chemisch/biologisch – Sondernutzung.',
    'MF-U05': 'Gefahrstofftransport – Sondernutzung.',
    'MF-U06': 'Explosionsschutz – Sondernutzung.',
    'MF-U08': 'Bauliche Änderungen/Statik – in der Vorlage nicht abgefragt.',
    'MF-U11': 'Löschanlage/Sprinkler – Sonderfall.',
    'MF-U12': 'Fremdgewerke/Reinigung – Betreiberorganisation, in der Vorlage nicht abgefragt.',
    'MF-U13': 'Prüfnachweise der Gewerkeschnittstellen – in der Vorlage nicht abgefragt.',
    'MF-U14': 'Aufzugszugang an Fahrwegen – Sonderfall (Tiefgarage).',
    'MF-U15': 'Abgase/Emissionen, Lärm, Unfallhistorie – Dokumentation; in der Vorlage nur als Freitext.',
    # Sonderfunktionen / Unterlagen
    'MF-SF01': 'Feuerwehraufzug – Sonderfunktion mit eigenem Prüfumfang (EN 81-72); in der Vorlage nur als Istzustand „Feuerwehraufzug" (Grün).',
    'MF-D06': 'Konformität Baujahr/Ausstattung – Plausibilitätsprüfung des vollen Typs, für den Riedl-Bericht nicht vorgesehen.',
    # Cyber
    'CY-C05': 'Schachtkopierung – nicht unter den sieben Riedl-Komponenten.',
    'CY-C07': 'UCM-Erkennung – in dieser Variante Teil der PESSRAL-Zeile (K-R03).',
    'CY-C08': 'SAFÜ – in dieser Variante Teil der PESSRAL-Zeile (K-R03).',
    'CY-C09': 'Tragmittelüberwachung – nicht unter den sieben Riedl-Komponenten.',
    'CY-C10': 'Hydraulischer Steuerblock – nicht unter den sieben Riedl-Komponenten.',
    'CY-O01': 'Verantwortlichkeit/Fachkunde – in der Vorlage nicht abgefragt (Unterschrift des Verwenders).',
    'CY-O03': 'Notfallmanagement Cyber – in der Vorlage nicht abgefragt.',
    'CY-O04': 'Unterweisung Cyber – in der Vorlage nur über die Unterschriftserklärung.',
}

# ---------------------------------------------------------------------------
# Klärungen für Arne (Gegenlesung)
# ---------------------------------------------------------------------------
KLAERUNGEN = [
    ('K-R01', 'Umfangsregel',
     'Umfang = VFA-Zeilen + 22 TRBS-Anhang-1-Punkte + Betreiberpflichten (63 von 100 MF-Gefährdungen). '
     'Vorschlag: so lassen; einzelne Gefährdungen aus NICHT_ENTHALTEN bei Bedarf in eine Zeile ziehen.',
     'Alternative: nur die VFA-Zeilen (ohne Nr. M4 Antrieb/Bremse/Hydraulik, S5 Gegengewicht/Nachbaraufzug, '
     'K9 Schachttüren) – dann fehlen TRBS-Anhang-1-Punkte 2, 3, 9, 11, 12, 16, 17 im Bericht.'),
    ('K-R02', 'Freitextzeile „Sonstiges" je Blatt',
     'Vorschlag: die Freitext-Gefährdung des Befund-Bereichs (eigene Einstufung Kein/Niedrig/Mittel/Hoch) '
     'als letzte Zeile jedes Blatts drucken; sie zählt in die Blatt-Ampel.',
     'Alternative: kein Freitext, alles über den Katalog.'),
    ('K-R03', 'PESSRAL-Zeile',
     'Vorschlag: elektronische UCM-/SAFÜ-Module unter „PESSRAL-Komponenten" (CY-C02) führen; '
     'CY-C07/C08 bleiben draußen.',
     'Alternative: C07 und C08 als eigene Zeilen 2a/2b aufnehmen (je 7 Fragen, meist nicht zutreffend).'),
    ('K-R04', 'Schachtentrauchung im Cyber-Blatt',
     'Vorschlag: mit den bauseitigen Einrichtungen als Gebäudeschnittstelle (CY-C14) bewerten, '
     'Hersteller/Typ getrennt erfassen.',
     'Alternative: eigene Komponente im CY-Katalog anlegen (neue Fragen 3.15.x, Regeln REVIEW_REQUIRED).'),
    ('K-R05', 'Zeilen ohne Excel-Vorbild',
     'Vorschlag: M4 „Antrieb, Bremse und Hydraulik", M6 „Notbetrieb und Personenbefreiung", '
     'S5 „Gegengewicht und Nachbaraufzug in der Grube" und K9 „Schachttüren" bleiben (TRBS-Punkte / '
     'Grundlage des Deckblatts).',
     'Alternative: streichen (siehe K-R01).'),
    ('K-R06', 'Nohl-Legende',
     'Vorschlag: die Nohl-Matrix als Legende drucken und die Engine-Stufe daneben mit R-Bereich '
     '(0 / 1 / 3–5 / 7–10) ausweisen, damit die Leser die gewohnte Skala wiederfinden.',
     'Alternative: nur Kein/Niedrig/Mittel/Hoch mit Ampel, ohne R-Werte.'),
    ('K-R07', 'Block Z (Aufgaben Verwender / Wartungsfirma / Servicetechniker)',
     'Vorschlag: aus den Maßnahmen der roten/gelben Zeilen nach „Verantwortlich" vorbelegen '
     '(Betreiber/Aufzugswärter -> Verwender; Wartungsfirma; Servicetechniker) und als Freitext '
     'nachbearbeitbar halten.',
     'Alternative: reiner Freitext wie in der Vorlage.'),
    ('K-R08', 'Spalte „Termin"',
     'Vorschlag: aus der Maßnahmengruppe vorbelegen (sofort -> „Sofort", mittel -> „Mittelfristig"), '
     'Auswahlliste der Vorlage (Sofort … Bis zur ZÜS-Prüfung) zum Überschreiben.',
     'Alternative: Termin als Datum.'),
]
