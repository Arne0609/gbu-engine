# -*- coding: utf-8 -*-
"""Entscheidungen zur Klärungsliste (fachliche Gegenlesung durch Arne).
Wird von gen_mf_catalog.py in mf_klaerung.json eingetragen (Felder entscheidung,
datum, festlegung). Die Umsetzung steckt in den Inhaltsmodulen (Suche nach
„Entscheidung 02.09.2026")."""

DATUM = '2026-09-02'

# id -> (Entscheidung, Festlegung im Klartext)
ENTSCHEIDUNGEN = {
    'K-Z01': ('Vorschlag', 'Schlüsseltresor = Kein Risiko.'),
    'K-Z02': ('Alternative', 'Flucht-/Rettungsweg Triebwerksraum: Niedrig (alle drei Befunde).'),
    'K-Z03': ('Alternative', 'Enge Durchgänge nur Dokumentation, keine Stufe.'),
    'K-Z04': ('Alternative', 'Zugang nur über mobile Leiter: Hoch.'),
    'K-M01': ('Alternative', 'Fehlender DGUV-V3-Nachweis: Mittel.'),
    'K-M02': ('Alternative', 'Hauptschalter nicht abschließbar: Hoch (App M5).'),
    'K-M03': ('Alternative', 'Fehlender Motorschutz: Mittel.'),
    'K-M04': ('Vorschlag', 'Ein Fahrschütz mit selbstüberwachender Steuerung: Kein Risiko.'),
    'K-M05': ('Vorschlag', 'Phasenumkehrschutz bei geregelten Antrieben: nicht zutreffend.'),
    'K-M06': ('Alternative', 'Fehlender Potenzialausgleich: Mittel.'),
    'K-M07': ('Vorschlag', 'Notbefreiungsanleitung fehlt: Hoch; veraltet oder nicht zur Anlage passend: Mittel.'),
    'K-M08': ('Vorschlag', 'Ohne Maschinenraum gelten die Elektrik-Fragen für den Steuerschrank.'),
    'K-M09': ('Alternative', 'Zweikreisbremse ohne Überwachung: Mittel nur mit Türüberbrückung (SR-Modul), sonst Kein Risiko.'),
    'K-K01': ('Vorschlag', 'Notruf ohne 24-h-Aufschaltung: Mittel.'),
    'K-K02': ('Alternative', 'Keine Notbeleuchtung im Fahrkorb: Hoch.'),
    'K-K03': ('Vorschlag', 'Stufenbildung 10–20 mm bei PmeM-Nutzung: Hoch.'),
    'K-K04': ('Anders', 'Kein Risiko nur mit Fahrkorbtür-Verriegelung UND Zusatzverriegelung an der Schachttür (neue Frage 8.15a).'),
    'K-K05': ('Alternative', 'Überlastkontrolle nicht nachweislich geprüft: Niedrig.'),
    'K-K06': ('Alternative', 'Notentriegelung fehlt an einzelnen Schachttüren: Hoch.'),
    'K-K07': ('Vorschlag', 'Feuerwiderstand unbekannt: Mittel.'),
    'K-K08': ('Alternative', 'UCM „nicht notwendig" (kein SR-Modul, 2K-Bremse mit Schalter, statisch bestimmt): Niedrig.'),
    'K-K09': ('Vorschlag', 'Fahrkorb ohne Tür bei PmeM-/Kindernutzung: Hoch.'),
    'K-F01': ('Vorschlag', 'Spalt > 850 mm und Geländer < 1.100 mm: Hoch.'),
    'K-F02': ('Vorschlag', 'Absturzsicherung Fahrkorbdach bleibt Hoch.'),
    'K-F03': ('Alternative', 'Reduzierter Schachtkopf / reduzierte Grube mit wirksamer Zusatzeinrichtung: Kein Risiko.'),
    'K-F04': ('Alternative', 'Fehlende Notbeleuchtung auf dem Fahrkorbdach: Hoch.'),
    'K-S01': ('Alternative', 'Fehlende Inspektionssteuerung in der Grube: Mittel.'),
    'K-S02': ('Alternative', 'Grubenleiter nur im Kundendienstfahrzeug: Hoch.'),
    'K-S03': ('Vorschlag', 'Aufzugsfremde Leitungen fachgerecht verlegt: Mittel.'),
    'K-S04': ('Alternative', 'Energiespeichernde Puffer über 1,0 m/s: Hoch.'),
    'K-S05': ('Alternative', 'Zulässig ausgeführte Teilumwehrung: Kein Risiko.'),
    'K-U01': ('Vorschlag', 'Ortsfragen sind alle Pflicht.'),
    'K-U02': ('Alternative', 'Chemische/biologische Gefahrstoffe gelagert: Mittel.'),
    'K-U03': ('Vorschlag', 'Ex-Gemisch bewertet: Mittel; nicht bewertet: Hoch.'),
    'K-U04': ('Alternative', 'Lärm und Unfallhistorie nur Dokumentation, keine Stufe (MF-U16 entfällt).'),
    'K-U05': ('Vorschlag', 'Angrenzende Verkehrswege: Mittel, Hoch mit PmeM-Nutzung.'),
    'K-D01': ('Vorschlag', 'Fehlender Notfallplan: Hoch.'),
    'K-D02': ('Vorschlag', 'Keine regelmäßige Instandhaltung: Hoch.'),
    'K-D03': ('Vorschlag', 'Prüffrist überschritten: Hoch; Plakette fehlt: Mittel.'),
    'K-D04': ('Vorschlag', 'Beauftragte Person, Unterweisung, Betriebsanweisung, Zutritt: jeweils Mittel.'),
    # Neu aus der TRBS-3121-Risikomatrix (02.09.2026):
    'K-T01': ('Vorschlag', 'Intaktes Drahtglas: Niedrig (TRBS 3121 Anh. 1 Nr. 9).'),
    'K-T02': ('Vorschlag', 'Einzel-Lichtschranke 150 N / 10 J: Mittel, Hoch mit PmeM-Nutzung.'),
    'K-K10': ('Alternative', 'Kein Warnhinweis als Kompensation bei Stufenbildung; 10–20 mm bleibt Mittel.'),
    'K-K11': ('Vorschlag', 'Statisch bestimmte Lagerung + Zweikreisbremse ohne Überwachung: Mittel.'),
    'K-F05': ('Vorschlag', 'Schutzraum nach TRA 200 / EN 81-1/-2 als eigene Option: Niedrig (TRBS 3121 Anh. 1 Nr. 5).'),
    'K-K12': ('Anders', 'Fall existiert nicht: ein Hydraulikaufzug hat immer eine Türüberbrückung (Nachregulieren bei Druckverlust). Ohne UCM daher Hoch (MF-K12-R1); Frage 8.27 wird bei Hydraulik nicht gestellt.'),
    'K-SF1': ('Alternative', 'Feuerwehraufzug: Unterlagen, Fremdgewerk-Nachweise, Feuerwehr-Doku und Cyber = Mittel, übrige Punkte Hoch.'),
}
