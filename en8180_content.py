# -*- coding: utf-8 -*-
"""Zuordnung DIN EN 81-80 (Bestandsanlagen) -> mehrfragiger Katalog (MF).

Grundlage: **DIN EN 81-80:2019-11**, Anhang A (normativ), Tabelle A.1
„Prüfliste für die Sicherheit bestehender Aufzüge" mit 94 Punkten, sowie
Abschnitt 5.4 mit Tabelle 3 und Tabelle 4 (Prioritätsstufen und Zeitplan).

Umgestellt am 30.09.2026. Vorher lag die Ausgabe 2004-02 mit 74
Gefährdungssituationen zugrunde; die ist zurückgezogen. Was sich geändert hat:

  * **Elf neue Punkte**, die es 2003 nicht gab (in Tabelle A.1 in der Spalte
    „Nr. in EN 81-80:2003" als nicht abgedeckt geführt): 1.3, 1.5, 2.19, 4.4,
    4.11, 4.21, 5.9, 8.1, 9.5, 10.1, 10.5.
  * **Neue Nummerierung** in elf Gruppen, die der Gliederung der EN 81-20
    folgt. Die alte Nummer steht in [ZUORDNUNG] an erster Stelle, damit sich
    ältere Berichte weiter zuordnen lassen.
  * **Die Prioritätsstufe steht jetzt direkt in der Prüfliste.** Das frühere
    Rechnen über Risikoprofil (Tabelle A.1 alt) und Prioritätstabelle
    (A.2 alt) entfällt; die Tabellen sind aus diesem Modul entfernt.
  * **Keine Stufe „Extrem" mehr.** Die Prüfliste verwendet nur Hoch, Mittel
    und Niedrig (Tabelle 4 kennt zusätzlich „sehr hoch", in der Prüfliste
    kommt die Stufe nicht vor). Sechs Punkte, die nach der Ausgabe 2004 als
    „Extrem" galten, sind jetzt „Hoch".
  * **37 von 83 übernommenen Punkten haben eine andere Priorität als vorher**
    – unter anderem die Aufhängepunkte im Triebwerksraum (Hoch -> Mittel),
    der Schutz gegen unkontrollierte Aufwärtsbewegung (Hoch -> Mittel) und
    die Notendschalter (Hoch -> Mittel).

Aus der Norm übernommen sind ausschließlich die Fakten, die die Zuordnung
braucht: Nummer, Nummer der Ausgabe 2003 und Prioritätsstufe. Die
Kurzbezeichnungen sind eigene Formulierungen und **kein Normtext**.

Der eingefrorene GBU-Typ „vereinfacht (EN 81-80)" wird damit nicht durch einen
zweiten Fragebogen ersetzt, sondern als SICHT auf den MF-Fragebogen geführt:
Eine Bestandsanlage wird einmal nach EN 81-20 (mehrfragig) erhoben, und der
Bericht weist zusätzlich den Nachrüstbedarf nach EN 81-80 mit Nummer und
Priorität der Norm aus (gleiches Muster wie der ZÜS-Abschlusscheck des
Cyber-Fragebogens).

Feld `deckung`:
  'voll'      – die MF-Gefährdung(en) decken den Punkt ab,
  'teilweise' – nur ein Teilaspekt wird im MF-Fragebogen erhoben,
  'offen'     – im MF-Katalog (noch) nicht erhoben; erscheint im Bericht als
                „nicht erhoben" und ist zugleich die Liste der Lücken, die im
                MF-Katalog nachgezogen werden sollten.
"""

AUSGABE = 'DIN EN 81-80:2019-11'
UMGESTELLT = '2026-09-30'

# Fachliche Gegenlesung der Zuordnung (Arne) – bezieht sich auf die Spalte
# „Bemerkung" in GBU_EN8180_Zuordnung.xlsx. Die Gegenlesung vom 04.09.2026 galt
# der Ausgabe 2004; sie ist mit der Nummerierung übernommen, die elf neuen
# Punkte und die geänderten Prioritäten stehen noch aus.
GEGENGELESEN = '2026-09-04'
GEGENGELESEN_HINWEIS = (
    'Zuordnung und Deckungsangaben der Ausgabe 2004 fachlich gegengelesen und '
    'mit der Spalte „Nr. in EN 81-80:2003" auf die Nummerierung der Ausgabe '
    '2019 gehoben. Noch nicht gegengelesen: die elf neuen Punkte und die '
    '37 geänderten Prioritätsstufen.')

# Prioritätsstufe -> Zeitplan (Tabelle 4). Die Länge der Fristen ist laut
# Anmerkung zu Tabelle 4 Gegenstand der nationalen Filterung; die Norm nennt
# als Beispiel kurzfristig innerhalb von 5 und mittelfristig innerhalb von
# 10 Jahren.
ZEITPLAN = {
    'Sehr hoch': 'Sofort',
    'Hoch': 'Kurzfristig',
    'Mittel': 'Mittelfristig oder im Rahmen einer umfangreichen Modernisierung',
    'Niedrig': 'Langfristig oder im Rahmen einer Modernisierung der '
               'betroffenen Komponente',
    '': 'Kein Zeitplan; der Punkt verweist auf eine eigene Norm der Reihe EN 81',
}

RANG = {'Sehr hoch': 4, 'Hoch': 3, 'Mittel': 2, 'Niedrig': 1, '': 0}

# Gruppen der Prüfliste (Tabelle A.1).
GRUPPEN = {
    '1': 'Allgemeines',
    '2': 'Schacht',
    '3': 'Betriebsräume und Rollenräume',
    '4': 'Schachttüren und Fahrkorbtüren',
    '5': 'Fahrkorb, Gegengewicht und Ausgleichsgewicht',
    '6': 'Aufhängungsmittel, Ausgleichsmittel, Schutz gegen freien Fall, '
         'Übergeschwindigkeit, unbeabsichtigte Bewegung und Absinken des '
         'Fahrkorbs',
    '7': 'Führungsschienen, Puffer und Notendschalter',
    '8': 'Triebwerk',
    '9': 'Elektrische Installationen und Einrichtungen',
    '10': 'Schutz gegen elektrische Fehler, Steuerungen, Vorrechte',
    '11': 'Hinweise, Kennzeichnungen und Betriebsanleitungen',
}


def sortierschluessel(nr):
    """Natürliche Reihenfolge: '2.9' vor '2.10', '9.5' vor '10.1'."""
    return tuple(int(t) for t in nr.split('.'))


# Nr (2019) -> (Nr 2003 oder None, Kurzbezeichnung, Priorität,
#               [MF-Gefährdungen], deckung, Bemerkung)
ZUORDNUNG = {
    # 1 Allgemeines
    '1.1': (2, 'Zugänglichkeit für Personen mit eingeschränkter Mobilität (EN 81-82)', '',
        ['MF-K10'], 'voll', ('In der Prüfliste ohne Prioritätsstufe: der Punkt verweist auf eine '
        'eigene Norm der Reihe EN 81.')),
    '1.2': (4, 'Widerstand gegen mutwillige Zerstörung (CEN/TS 81-83)', '',
        ['MF-K11'], 'voll', ('In der Prüfliste ohne Prioritätsstufe: der Punkt verweist auf eine '
        'eigene Norm der Reihe EN 81.')),
    '1.3': (None, 'Feuerwehraufzug (EN 81-72)', '',
        ['MF-SF01'], 'teilweise', ('MF-SF01 erhebt die gebäudeseitige Sonderfunktion Feuerwehraufzug; die '
        'Bauartanforderungen nach EN 81-72 selbst sind nicht Gegenstand des '
        'MF-Fragebogens.')),
    '1.4': (5, 'Verhalten des Aufzugs im Brandfall (EN 81-73)', '',
        ['MF-K08', 'MF-K09', 'MF-U09'], 'voll', ('In der Prüfliste ohne Prioritätsstufe: der Punkt verweist auf eine '
        'eigene Norm der Reihe EN 81.')),
    '1.5': (None, 'Erdbebensicherheit (EN 81-77)', '',
        [], 'offen', 'Erdbebensicherheit (EN 81-77) wird im MF-Fragebogen nicht erhoben.'),
    '1.6': (1, 'Anlage frei von schädlichen Stoffen (z. B. Asbest)', 'Hoch',
        ['MF-U01'], 'voll', ''),

    # 2 Schacht
    '2.1': (8, ('Schließeinrichtungen an Zugangs-, Notfall- und Inspektionstüren zu '
        'Schacht und Schachtgrube'), 'Hoch',
        ['MF-S07', 'MF-G04'], 'voll', ''),
    '2.2': (8, ('Anhalten des Fahrkorbs bei geöffneten Zugangs-, Notfall- und '
        'Inspektionstüren'), 'Hoch',
        ['MF-S07', 'MF-G04'], 'voll', ''),
    '2.3': (6, 'Vollwandige Schachtumwehrung', 'Hoch',
        ['MF-S03'], 'voll', ''),
    '2.4': (33, ('Zugang zu den Verriegelungseinrichtungen der Schachttür bei '
        'durchbrochener Umwehrung'), 'Hoch',
        ['MF-S03', 'MF-T01'], 'teilweise', ('Nr. 33 (2003): MF erhebt Umwehrung und Verriegelung getrennt, nicht '
        'ihren Abstand zueinander.')),
    '2.5': (7, 'Teilumwehrter Schacht', 'Hoch',
        ['MF-S03'], 'voll', ''),
    '2.6': (9, 'Höhe der senkrechten Fläche unterhalb der Schachttürschwelle', 'Hoch',
        ['MF-T07'], 'voll', 'Nr. 9 (2003): Ergänzt 04.09.2026 (EN 81-20 5.2.5.3.2).'),
    '2.7': (10, ('Schutz der Zugangsbereiche unter dem Schacht (Fangvorrichtung am '
        'Gegengewicht)'), 'Niedrig',
        ['MF-G07'], 'voll', ''),
    '2.8': (11, 'Abtrennung der Fahrbahn des Gegen- oder Ausgleichsgewichts', 'Niedrig',
        ['MF-G07'], 'voll', ''),
    '2.9': (12, 'Abtrennung in der Schachtgrube bei mehreren Aufzügen im selben Schacht', 'Hoch',
        ['MF-G08'], 'voll', ''),
    '2.10': (13, ('Abtrennung beweglicher Teile über die volle Höhe bei gemeinsam '
        'genutztem Schacht'), 'Hoch',
        ['MF-F03', 'MF-G08'], 'voll', ''),
    '2.11': (14, 'Schutzräume und Freiräume im Schachtkopf', 'Hoch',
        ['MF-F04', 'MF-G02'], 'voll', ''),
    '2.12': (14, 'Schutzräume und Freiräume in der Schachtgrube', 'Hoch',
        ['MF-F04', 'MF-G02'], 'voll', ''),
    '2.13': (15, 'Maßnahmen für den Zugang zur Schachtgrube', 'Hoch',
        ['MF-G04'], 'voll', ''),
    '2.14': (17, 'Schachtbeleuchtung', 'Hoch',
        ['MF-S01', 'MF-G01'], 'voll', ''),
    '2.15': (16, 'Notbremsschalter in der Schachtgrube', 'Hoch',
        ['MF-G03', 'MF-M20'], 'voll', ''),
    '2.16': (18, ('Notrufauslöseeinrichtungen in der Schachtgrube und auf dem '
        'Fahrkorbdach'), 'Mittel',
        ['MF-G05', 'MF-F09'], 'voll', ''),
    '2.17': (58, ('Horizontaler Abstand zwischen innerer Schachtwand und Türschwelle bzw. '
        'Türrahmen des Fahrkorbs'), 'Hoch',
        ['MF-F01'], 'teilweise', ('Nr. 58 (2003): MF erhebt den Abstand an der Fahrkorbdachkante '
        '(Absturzsicherung).')),
    '2.18': (59, 'Horizontaler Abstand zwischen geschlossener Fahrkorbtür und Schachttür', 'Hoch',
        ['MF-K05'], 'voll', ''),
    '2.19': (None, 'Abstand zwischen den Führungskanten von Fahrkorbtür und Schachttür', 'Hoch',
        [], 'offen', ('Wird nicht erhoben; MF-K05 erfasst den Abstand '
        'Fahrkorbschwelle/Schachtwand, nicht den Abstand der Führungskanten.')),

    # 3 Betriebsräume und Rollenräume
    '3.1': (19, 'Zugänge zu den Aufstellungsorten von Triebwerks- und Rollenraum', 'Hoch',
        ['MF-Z03', 'MF-Z07', 'MF-Z02'], 'voll', ''),
    '3.2': (23, 'Beleuchtung in den Betriebsräumen und Rollenräumen', 'Hoch',
        ['MF-M01'], 'voll', ''),
    '3.3': (16, 'Notbremsschalter in Rollenräumen', 'Hoch',
        ['MF-G03', 'MF-M20'], 'voll', ''),
    '3.4': (24, ('Aufhängepunkte für die Handhabung von Einrichtungen in Betriebsräumen '
        'und oben im Schacht'), 'Mittel',
        ['MF-M14'], 'voll', ''),
    '3.5': (20, ('Rutschhemmender Boden an den Aufstellungsorten von Triebwerks- und '
        'Rollenraum'), 'Niedrig',
        ['MF-M06'], 'voll', ''),
    '3.6': (21, ('Horizontale und vertikale Freiräume in den Betriebsräumen für sicheres '
        'Arbeiten'), 'Mittel',
        ['MF-M04'], 'voll', ''),
    '3.7': (22, 'Arbeitsebenen und Vertiefungen im Triebwerksraum', 'Hoch',
        ['MF-M05'], 'voll', ''),
    '3.8': (72, 'Gegensprechanlage zwischen Fahrkorb und Ort des Notbetriebs', 'Mittel',
        ['MF-M18'], 'voll', ''),

    # 4 Schachttüren und Fahrkorbtüren
    '4.1': (25, 'Vollwandige Schachttüren', 'Hoch',
        ['MF-T04', 'MF-T06'], 'teilweise', ('Nr. 25 (2003): MF erhebt Glaseinsätze und den Fahrkorbabschluss; '
        'Gittertüren nur über Scherengitter/Lichtgitter.')),
    '4.2': (25, 'Vollwandige Fahrkorbtüren', 'Hoch',
        ['MF-T04', 'MF-T06'], 'teilweise', ('Nr. 25 (2003): MF erhebt Glaseinsätze und den Fahrkorbabschluss; '
        'Gittertüren nur über Scherengitter/Lichtgitter.')),
    '4.3': (26, 'Festigkeit von Schachttüren', 'Hoch',
        ['MF-T08'], 'voll', ('Nr. 26 (2003): Ergänzt 04.09.2026 (EN 81-20 5.3.5.3.2 '
        'Rückhalteeinrichtungen).')),
    '4.4': (None, 'Festigkeit von Fahrkorbtüren', 'Mittel',
        [], 'offen', ('Festigkeit der Fahrkorbtüren wird nicht erhoben; MF-T02/T04 betreffen '
        'die Schachttüren.')),
    '4.5': (27, 'Glas in den Schachttüren außer Schauöffnungen', 'Hoch',
        ['MF-T04'], 'voll', ''),
    '4.6': (27, 'Glas in den Fahrkorbtüren außer Schauöffnungen', 'Hoch',
        ['MF-T04'], 'voll', ''),
    '4.7': (27, 'Glasschauöffnungen in den Schachttüren', 'Hoch',
        ['MF-T04'], 'voll', ''),
    '4.8': (27, 'Glasschauöffnungen in den Fahrkorbtüren', 'Hoch',
        ['MF-T04'], 'voll', ''),
    '4.9': ('30b', ('Nichttrennende Schutzeinrichtung (z. B. Lichtschranke) an '
        'kraftbetätigten Türen'), 'Hoch',
        ['MF-T06'], 'voll', ''),
    '4.10': ('30a', ('Begrenzung des Kraftaufwands beim Schließen kraftbetätigter '
        'Schiebetüren (150 N)'), 'Hoch',
        ['MF-T06'], 'voll', ''),
    '4.11': (None, ('Begrenzung des Kraftaufwands (150 N) beim Schließen anderer als '
        'automatisch kraftbetätigter Schiebetüren'), 'Hoch',
        [], 'offen', ('Kraftbegrenzung an anderen als automatisch kraftbetätigten '
        'Schiebetüren wird nicht erhoben.')),
    '4.12': (28, ('Schutz gegen das Einziehen von Kinderhänden bei waagerecht bewegten '
        'Glastüren'), 'Mittel',
        ['MF-T04'], 'voll', ''),
    '4.13': (29, 'Beleuchtung der Ladestellen in der Nähe der Schachttüren', 'Mittel',
        ['MF-S02'], 'voll', ''),
    '4.14': (31, 'Schachttürverriegelungen', 'Hoch',
        ['MF-T01'], 'voll', ''),
    '4.15': (32, ('Notentriegelung der Schachttüren nur mit besonderen Mitteln (z. B. '
        'Dreikantschlüssel)'), 'Hoch',
        ['MF-T02'], 'voll', ''),
    '4.16': (34, ('Selbsttätiges Schließen und Verriegeln einer geöffneten Schachttür bei '
        'Fahrkorb außerhalb der Entriegelungszone'), 'Hoch',
        ['MF-T03'], 'voll', ''),
    '4.17': (35, ('Schachtschiebetüren mit mehreren Türblättern: Verbindung und '
        'elektrische Prüfung der geschlossenen Position'), 'Mittel',
        ['MF-T09'], 'voll', 'Nr. 35 (2003): Ergänzt 04.09.2026 (EN 81-20 5.3.11).'),
    '4.18': (36, 'Feuerwiderstand von Schachttüren', 'Mittel',
        ['MF-T05'], 'voll', ''),
    '4.19': (37, ('Kraftbetriebene Fahrkorb-Schiebetür bewegt sich erst nach dem '
        'Schließen der Schachtdrehtür'), 'Mittel',
        ['MF-K05'], 'voll', ('Nr. 37 (2003): Über die Fahrkorbtür-Verriegelung außerhalb der '
        'Entriegelungszone.')),
    '4.20': (40, 'Vorhandensein der Fahrkorbtür(en)', 'Hoch',
        ['MF-T06'], 'voll', ''),
    '4.21': (None, ('Fahrkorbtürdrossel, wo die Verriegelungseinrichtung der Schachttür '
        'zugänglich ist'), 'Mittel',
        [], 'offen', ('Fahrkorbtürdrossel bei zugänglicher Schachttürverriegelung wird nicht '
        'erhoben.')),

    # 5 Fahrkorb, Gegengewicht und Ausgleichsgewicht
    '5.1': (38, 'Verhältnis von Nutzfläche zur Nennlast', 'Niedrig',
        ['MF-K06'], 'voll', ''),
    '5.2': (39, 'Fahrkorbschürze', 'Hoch',
        ['MF-K04'], 'voll', ''),
    '5.3': (41, 'Verriegelung der Notklappe auf dem Fahrkorb', 'Mittel',
        ['MF-F07'], 'voll', ''),
    '5.4': (42, 'Festigkeit des Fahrkorbdachs und der Notklappe', 'Niedrig',
        ['MF-F07'], 'voll', ''),
    '5.5': (43, 'Schutz gegen Absturz vom Fahrkorbdach (Umwehrung)', 'Hoch',
        ['MF-F01'], 'voll', ''),
    '5.6': (44, 'Fahrkorbbelüftung', 'Mittel',
        ['MF-K07'], 'voll', ''),
    '5.7': (45, 'Normale Beleuchtung im Fahrkorb', 'Mittel',
        ['MF-K15'], 'voll', ('Nr. 45 (2003): Ergänzt 04.09.2026 (EN 81-20 5.4.10.1 bis 5.4.10.3: '
        'mind. 100 Lux an den Befehlsgebern und 1 m über dem Boden bis 100 mm '
        'an die Wände).')),
    '5.8': (46, 'Notbeleuchtung im Fahrkorb', 'Mittel',
        ['MF-K02'], 'voll', ''),
    '5.9': (None, 'Notbeleuchtung auf dem Fahrkorbdach', 'Niedrig',
        ['MF-F08'], 'voll', ('Im MF-Fragebogen bereits enthalten (Frage 9.12), obwohl in der Ausgabe '
        '2003 nicht abgedeckt.')),
    '5.10': (73, ('Kontrolle der Beladung, um einen Start des Fahrkorbs bei Überladung zu '
        'verhindern'), 'Niedrig',
        ['MF-K06'], 'voll', ''),
    '5.11': (71, 'Fernnotrufeinrichtung mit Zweiwegeverständigung', 'Hoch',
        ['MF-K01'], 'voll', ''),

    # 6 Aufhängungsmittel, Ausgleichsmittel, Schutz gegen freien Fall, Übergeschwindigkeit, unbeabsichtigte Bewegung und Absinken des Fahrkorbs
    '6.1': (47, ('Schutz gegen Verletzungen an Treibscheiben, Seilrollen oder '
        'Kettenrädern'), 'Mittel',
        ['MF-M03'], 'voll', ''),
    '6.2': (48, 'Schutz gegen das Herausspringen von Seilen oder Ketten', 'Mittel',
        ['MF-M03'], 'voll', ''),
    '6.3': (49, ('Schutz gegen das Eindringen von Fremdkörpern zwischen Seil/Kette und '
        'Scheibe'), 'Niedrig',
        ['MF-M03'], 'voll', ''),
    '6.4': ('50, 54', ('Schutz gegen freien Fall und Abwärtsbewegung mit überhöhter '
        'Geschwindigkeit'), 'Hoch',
        ['MF-S05', 'MF-M13'], 'voll', ''),
    '6.5': (52, ('Schutz gegen unkontrollierte Aufwärtsbewegung (Treibscheibenaufzug mit '
        'Gegengewicht)'), 'Mittel',
        ['MF-K13'], 'voll', ''),
    '6.6': (53, ('Schutz gegen unbeabsichtigte Bewegung des Fahrkorbs bei offenen Türen '
        '(UCM)'), 'Hoch',
        ['MF-M08'], 'voll', ''),
    '6.7': (54, 'Schutz gegen Absinken bei Hydraulikaufzügen (oder Klemmvorrichtung)', 'Hoch',
        ['MF-M13'], 'voll', ''),
    '6.8': (51, 'Schlaffseilschalter am Begrenzerseil für Übergeschwindigkeit', 'Mittel',
        ['MF-S05'], 'voll', ''),
    '6.9': (63, 'Sicherheitseinrichtung gegen Schlaffseil oder Schlaffkette', 'Mittel',
        ['MF-S05'], 'voll', ''),

    # 7 Führungsschienen, Puffer und Notendschalter
    '7.1': (55, 'Führungen für Gegengewicht oder Ausgleichsgewicht', 'Niedrig',
        ['MF-S04'], 'voll', ''),
    '7.2': (56, 'Fahrkorb- und Gegengewichtspuffer', 'Hoch',
        ['MF-G06'], 'voll', ''),
    '7.3': (57, 'Notendschalter', 'Mittel',
        ['MF-M21'], 'voll', 'Nr. 57 (2003): Ergänzt 04.09.2026 (EN 81-20 5.12.2).'),

    # 8 Triebwerk
    '8.1': (None, 'Mindestens zwei unabhängige Bremssätze', 'Hoch',
        ['MF-M08'], 'voll', 'MF-M08 erhebt die Zweikreisbremse (Frage 6.2) und ihre Überwachung.'),
    '8.2': (60, 'Notbetriebssystem', 'Hoch',
        ['MF-M15'], 'voll', ''),
    '8.3': (62, 'Mittel zum Stillsetzen des Antriebs und Überwachung seines Stillstands', 'Hoch',
        ['MF-M10'], 'voll', ''),
    '8.4': (64, 'Motorlaufzeitüberwachung', 'Niedrig',
        ['MF-M11'], 'voll', ''),
    '8.5': (61, 'Absperrventil (Hydraulikaufzüge)', 'Niedrig',
        ['MF-M13'], 'voll', ''),
    '8.6': (65, 'Kolbenabsinkvorrichtung bei Hydraulikaufzügen', 'Mittel',
        ['MF-M13'], 'voll', ''),

    # 9 Elektrische Installationen und Einrichtungen
    '9.1': (66, 'Schutz gegen elektrischen Schlag (direktes Berühren)', 'Hoch',
        ['MF-M02', 'MF-M17'], 'voll', ''),
    '9.2': (66, ('Kennzeichnung von Anschlussklemmen, die nach dem Ausschalten des '
        'Hauptschalters unter Strom bleiben'), 'Hoch',
        ['MF-M02', 'MF-M17'], 'voll', ''),
    '9.3': (67, 'Schutz gegen Überhitzung des Triebwerksmotors', 'Niedrig',
        ['MF-M09'], 'voll', ''),
    '9.4': (68, 'Abschließbarer Hauptschalter', 'Hoch',
        ['MF-M07'], 'voll', ''),
    '9.5': (None, ('Bremseinrichtung an der Anlage am Aufstellungsort von Triebwerk und '
        'Steuerung'), 'Niedrig',
        [], 'offen', ('Bremseinrichtung am Aufstellungsort von Triebwerk und Steuerung wird '
        'nicht gesondert erhoben.')),

    # 10 Schutz gegen elektrische Fehler, Steuerungen, Vorrechte
    '10.1': (None, ('Erdfehlerschutz in Stromkreisen mit elektrischen '
        'Sicherheitseinrichtungen und in Bremsen-/Abwärtsventil-Schaltkreisen'), 'Mittel',
        [], 'offen', ('Erdfehlerschutz in Sicherheits- und Bremsstromkreisen wird nicht '
        'erhoben.')),
    '10.2': (69, 'Schutz gegen Stromphasenumkehr', 'Niedrig',
        ['MF-M12'], 'voll', ''),
    '10.3': (3, 'Nachregulierungs- und Anhaltegenauigkeit des Fahrkorbs', 'Hoch',
        ['MF-K03'], 'voll', ''),
    '10.4': (70, 'Inspektionssteuerung und Bremseinrichtung auf dem Fahrkorbdach', 'Hoch',
        ['MF-F05', 'MF-F06'], 'voll', ''),
    '10.5': (None, 'Inspektionskontrolle in der Schachtgrube', 'Niedrig',
        ['MF-G03'], 'teilweise', ('MF-G03 erhebt die Inspektionssteuerung in der Schachtgrube (Frage '
        '11.5) zusammen mit dem Not-Halt.')),

    # 11 Hinweise, Kennzeichnungen und Betriebsanleitungen
    '11.1': (74, 'Hinweise zum sicheren Betrieb und zur Instandhaltung des Aufzugs', 'Mittel',
        ['MF-M17', 'MF-D02'], 'voll', ''),
}


def gruppe(nr):
    """Gruppenüberschrift zu einer Nummer der Prüfliste."""
    return GRUPPEN[nr.split('.')[0]]


def prioritaeten():
    """Nr -> Prioritätsstufe. Steht seit der Ausgabe 2019 direkt in der
    Prüfliste; die frühere Berechnung aus Risikoprofil und Prioritätstabelle
    entfällt."""
    return {nr: eintrag[2] for nr, eintrag in ZUORDNUNG.items()}


def nach_alt():
    """Alte Nummer (Ausgabe 2003) -> Liste der neuen Nummern. Für die
    Zuordnung älterer Berichte."""
    out = {}
    for nr, eintrag in ZUORDNUNG.items():
        alt = eintrag[0]
        if alt is None:
            continue
        for teil in str(alt).replace(' ', '').split(','):
            out.setdefault(teil, []).append(nr)
    return {a: sorted(v, key=sortierschluessel) for a, v in out.items()}
