# -*- coding: utf-8 -*-
"""Zuordnung DIN EN 81-80 (Bestandsanlagen) -> mehrfragiger Katalog (MF).

Grundlage: DIN EN 81-80:2004-02, Tabelle 1 (74 Gefährdungssituationen mit den
zugehörigen Abschnitten) sowie Anhang A (Tabelle A.1 Ursprüngliches
Risikoprofil, Tabelle A.2 Prioritäten und Zeitplan). Nummern, Abschnitte und
Prioritätsstufen sind aus der Norm übernommen; die Kurzbezeichnungen sind
eigene Formulierungen (kein Normtext).

Der eingefrorene GBU-Typ „vereinfacht (EN 81-80)" wird damit nicht durch einen
zweiten Fragebogen ersetzt, sondern als SICHT auf den MF-Fragebogen geführt:
Eine Bestandsanlage wird einmal nach EN 81-20 (mehrfragig) erhoben, und der
Bericht weist zusätzlich den Nachrüstbedarf nach EN 81-80 mit der Nummerierung
und der Priorität der Norm aus (gleiches Muster wie der ZÜS-Abschlusscheck des
Cyber-Fragebogens).

Feld `deckung`:
  'voll'      – die MF-Gefährdung(en) decken die Gefährdungssituation ab,
  'teilweise' – nur ein Teilaspekt wird im MF-Fragebogen erhoben,
  'offen'     – im MF-Katalog (noch) nicht erhoben; erscheint im Bericht als
                „nicht erhoben" und ist zugleich die Liste der Lücken, die im
                MF-Katalog nachgezogen werden sollten.
"""

# Fachliche Gegenlesung der Zuordnung (Arne). Bezieht sich auf die Spalte
# „Bemerkung" in GBU_EN8180_Zuordnung.xlsx und damit auf die Deckungsangaben:
# die drei Punkte mit „teilweise" (Nr. 25, 33, 58) bleiben als Teilabdeckung
# stehen, die Ergänzungen vom 04.09.2026 sind bestätigt.
GEGENGELESEN = '2026-09-04'
GEGENGELESEN_HINWEIS = ('Zuordnung und Deckungsangaben fachlich gegengelesen; '
                        'die Bemerkungen zu den teilweise abgedeckten Punkten '
                        '(Nr. 25, 33, 58) sind bestätigt.')

# Nr: (Abschnitt, Kurzbezeichnung, [MF-Gefährdungen], deckung, Bemerkung)
ZUORDNUNG = {
    1: ('5.1.4', 'Schädliche Stoffe an der Anlage (z. B. Asbest in Bremsbelägen, '
        'Löschkammern, Verkleidungen)', ['MF-U01'], 'voll', ''),
    2: ('5.2.1', 'Zugänglichkeit für Personen mit eingeschränkter Mobilität',
        ['MF-K10'], 'voll', 'In A.1 nicht risikoprofiliert (besondere Anforderung '
        'nach 5.1.5).'),
    3: ('5.2.2', 'Anhalte- und Nachregulierungsgenauigkeit', ['MF-K03'], 'voll', ''),
    4: ('5.3', 'Widerstand gegen mutwillige Zerstörung (Vandalismus)',
        ['MF-K11'], 'voll', 'In A.1 nicht risikoprofiliert (besondere Anforderung '
        'nach 5.1.5).'),
    5: ('5.4', 'Verhalten und Überwachungsfunktionen im Brandfall',
        ['MF-K08', 'MF-K09', 'MF-U09'], 'voll', 'In A.1 nicht risikoprofiliert '
        '(besondere Anforderung nach 5.1.5).'),
    6: ('5.5.1.1', 'Durchbrochene (nicht geschlossene) Schachtumwehrung',
        ['MF-S03'], 'voll', ''),
    7: ('5.5.1.2', 'Teilumwehrter Schacht mit zu niedriger Umwehrung',
        ['MF-S03'], 'voll', ''),
    8: ('5.5.2', 'Schließeinrichtungen an Zugangstüren zu Schacht und Schachtgrube',
        ['MF-S07', 'MF-G04'], 'voll', ''),
    9: ('5.5.3', 'Senkrechte Fläche unterhalb der Schachttürschwelle',
        ['MF-T07'], 'voll', 'Ergänzt 04.09.2026 (EN 81-20 5.2.5.3.2).'),
    10: ('5.5.4', 'Betretbarer Raum unter dem Schacht ohne Fangvorrichtung am '
         'Gegengewicht', ['MF-G07'], 'voll', ''),
    11: ('5.5.5', 'Abtrennung der Fahrbahn des Gegengewichts/Ausgleichsgewichts',
         ['MF-G07'], 'voll', ''),
    12: ('5.5.6.1', 'Abtrennung in der Schachtgrube bei mehreren Aufzügen im '
         'selben Schacht', ['MF-G08'], 'voll', ''),
    13: ('5.5.6.2', 'Abtrennung über die Schachthöhe bei mehreren Aufzügen im '
         'selben Schacht', ['MF-F03', 'MF-G08'], 'voll', ''),
    14: ('5.5.7', 'Schutzräume in Schachtkopf und Schachtgrube',
         ['MF-F04', 'MF-G02'], 'voll', ''),
    15: ('5.5.8', 'Sicherer Zugang zur Schachtgrube', ['MF-G04'], 'voll', ''),
    16: ('5.5.9', 'Not-Halt in Schachtgrube und Rollenraum',
         ['MF-G03', 'MF-M20'], 'voll', ''),
    17: ('5.5.10', 'Schachtbeleuchtung', ['MF-S01', 'MF-G01'], 'voll', ''),
    18: ('5.5.11', 'Notruf in Schachtgrube und auf dem Fahrkorbdach',
         ['MF-G05', 'MF-F09'], 'voll', ''),
    19: ('5.6.1', 'Zugänge zum Triebwerks- oder Rollenraum',
         ['MF-Z03', 'MF-Z07', 'MF-Z02'], 'voll', ''),
    20: ('5.6.2', 'Rutschiger Boden im Triebwerks- oder Rollenraum',
         ['MF-M06'], 'voll', ''),
    21: ('5.6.3', 'Abstände und Freiflächen im Triebwerksraum', ['MF-M04'], 'voll', ''),
    22: ('5.6.4', 'Unterschiedliche Ebenen im Triebwerks- oder Rollenraum',
         ['MF-M05'], 'voll', ''),
    23: ('5.6.5', 'Beleuchtung im Triebwerks- oder Rollenraum', ['MF-M01'], 'voll', ''),
    24: ('5.6.6', 'Hebezeuge und Anschlagpunkte', ['MF-M14'], 'voll', ''),
    25: ('5.7.1', 'Durchbrochene Schacht- und Fahrkorbtüren (Gittertüren)',
         ['MF-T04', 'MF-T06'], 'teilweise',
         'MF erhebt Glaseinsätze und den Fahrkorbabschluss; Gittertüren nur über '
         'Scherengitter/Lichtgitter.'),
    26: ('5.7.2', 'Ausführung der Schachttürbefestigungen', ['MF-T08'], 'voll',
         'Ergänzt 04.09.2026 (EN 81-20 5.3.5.3.2 Rückhalteeinrichtungen).'),
    27: ('5.7.3', 'Geeignetes Glas in Schachttüren', ['MF-T04'], 'voll', ''),
    28: ('5.7.4', 'Schutz gegen Einziehen von Fingern an Glas-Schiebetüren',
         ['MF-T04'], 'voll', ''),
    29: ('5.7.5', 'Beleuchtung an den Schachtzugängen', ['MF-S02'], 'voll', ''),
    30: ('5.7.6', 'Schutzeinrichtungen an kraftbetätigten Türen '
         '(Schließkantensicherung)', ['MF-T06'], 'voll', ''),
    31: ('5.7.7', 'Verriegelungseinrichtung der Schachttür', ['MF-T01'], 'voll', ''),
    32: ('5.7.8.1', 'Notentriegelung der Schachttür nur mit besonderem Werkzeug',
         ['MF-T02'], 'voll', ''),
    33: ('5.7.8.2', 'Durchbrochene Schachtwand in der Nähe der Türverriegelung',
         ['MF-S03', 'MF-T01'], 'teilweise',
         'MF erhebt Umwehrung und Verriegelung getrennt, nicht ihren Abstand '
         'zueinander.'),
    34: ('5.7.9', 'Selbstschließen der Schachttüren (Sperrmittel)',
         ['MF-T03'], 'voll', ''),
    35: ('5.7.10', 'Verbindung zwischen den Türblättern mehrteiliger Schachttüren',
         ['MF-T09'], 'voll', 'Ergänzt 04.09.2026 (EN 81-20 5.3.11).'),
    36: ('5.7.11', 'Feuerwiderstandsfähigkeit der Schachttüren', ['MF-T05'], 'voll', ''),
    37: ('5.7.12', 'Fahrkorbtür bewegt sich bei geöffneter Schachttür',
         ['MF-K05'], 'voll', 'Über die Fahrkorbtür-Verriegelung außerhalb der '
         'Entriegelungszone.'),
    38: ('5.8.1', 'Verhältnis von Nutzfläche zur Nennlast', ['MF-K06'], 'voll', ''),
    39: ('5.8.2', 'Länge der Fahrkorbtürschürze', ['MF-K04'], 'voll', ''),
    40: ('5.8.3', 'Fahrkorb ohne Abschlusstür', ['MF-T06'], 'voll', ''),
    41: ('5.8.4', 'Verriegelung und Überwachung der Klappe im Fahrkorbdach',
         ['MF-F07'], 'voll', ''),
    42: ('5.8.5', 'Festigkeit des Fahrkorbdachs', ['MF-F07'], 'voll', ''),
    43: ('5.8.6', 'Umwehrung (Geländer) auf dem Fahrkorbdach', ['MF-F01'], 'voll', ''),
    44: ('5.8.7', 'Lüftung des Fahrkorbs', ['MF-K07'], 'voll', ''),
    45: ('5.8.8.1', 'Beleuchtung im Fahrkorb (Normalbetrieb)', ['MF-K15'], 'voll',
         'Ergänzt 04.09.2026 (EN 81-20 5.4.10.1 bis 5.4.10.3: mind. 100 Lux an den '
         'Befehlsgebern und 1 m über dem Boden bis 100 mm an die Wände).'),
    46: ('5.8.8.2', 'Notbeleuchtung im Fahrkorb', ['MF-K02'], 'voll', ''),
    47: ('5.9.1', 'Schutz an Treibscheiben, Rollen und Kettenrädern gegen '
         'Verletzungen', ['MF-M03'], 'voll', ''),
    48: ('5.9.1', 'Schutz gegen Herausspringen von Seilen oder Ketten',
         ['MF-M03'], 'voll', ''),
    49: ('5.9.1', 'Schutz gegen Eindringen von Fremdkörpern in Treibscheibe und '
         'Rollen', ['MF-M03'], 'voll', ''),
    50: ('5.9.2', 'Fangvorrichtung und Geschwindigkeitsbegrenzer bei elektrisch '
         'angetriebenen Aufzügen', ['MF-S05'], 'voll', ''),
    51: ('5.9.3', 'Schlaffseilschalter am Begrenzerseil (Spanngewicht)',
         ['MF-S05'], 'voll', ''),
    52: ('5.9.4', 'Schutz gegen unkontrollierte Aufwärtsbewegung des Fahrkorbs',
         ['MF-K13'], 'voll', ''),
    53: ('5.9.4, 5.12.1', 'Auslegung des Triebwerks und der Bremse',
         ['MF-M08'], 'voll', ''),
    54: ('5.9.5', 'Schutz gegen freien Fall, Übergeschwindigkeit und Absinken bei '
         'Hydraulikaufzügen', ['MF-M13'], 'voll', ''),
    55: ('5.10.1', 'Gegengewicht oder Ausgleichsgewicht durch Seile statt Schienen '
         'geführt', ['MF-S04'], 'voll', ''),
    56: ('5.10.2', 'Puffer für Fahrkorb und Gegengewicht', ['MF-G06'], 'voll', ''),
    57: ('5.10.3', 'Notendschalter', ['MF-M21'], 'voll',
         'Ergänzt 04.09.2026 (EN 81-20 5.12.2).'),
    58: ('5.11.1', 'Abstand zwischen Fahrkorb und der dem Zugang gegenüber-'
         'liegenden Schachtwand', ['MF-F01'], 'teilweise',
         'MF erhebt den Abstand an der Fahrkorbdachkante (Absturzsicherung).'),
    59: ('5.11.2', 'Abstand zwischen Fahrkorbschwelle und Schachttür',
         ['MF-K05'], 'voll', ''),
    60: ('5.12.2', 'Einrichtung für den Notbetrieb und die Personenbefreiung',
         ['MF-M15'], 'voll', ''),
    61: ('5.12.3', 'Absperrventil am Hydraulikaggregat', ['MF-M13'], 'voll', ''),
    62: ('5.12.4', 'Zwei unabhängige Schütze im Antriebsstromkreis',
         ['MF-M10'], 'voll', ''),
    63: ('5.12.5', 'Schlaffseil-/Schlaffketteneinrichtung', ['MF-S05'], 'voll', ''),
    64: ('5.12.6', 'Laufzeitüberwachung des Antriebs', ['MF-M11'], 'voll', ''),
    65: ('5.12.7', 'Einrichtung gegen Absinken des Kolbens', ['MF-M13'], 'voll', ''),
    66: ('5.13.1', 'Schutz gegen elektrischen Schlag und Kennzeichnung '
         'elektrischer Einrichtungen', ['MF-M02', 'MF-M17'], 'voll', ''),
    67: ('5.13.2', 'Schutz des Triebwerksmotors gegen Überhitzen',
         ['MF-M09'], 'voll', ''),
    68: ('5.13.3', 'Abschließbarer Hauptschalter', ['MF-M07'], 'voll', ''),
    69: ('5.14.1', 'Schutz gegen Phasenumkehr und Phasenausfall',
         ['MF-M12'], 'voll', ''),
    70: ('5.14.2', 'Inspektionssteuerung und Not-Halt auf dem Fahrkorbdach',
         ['MF-F05', 'MF-F06'], 'voll', ''),
    71: ('5.14.3', 'Notrufeinrichtung im Fahrkorb (Zweiwege-System nach EN 81-28)',
         ['MF-K01'], 'voll', ''),
    72: ('5.14.4', 'Sprechverbindung Triebwerksraum – Fahrkorb (Förderhöhe > 30 m)',
         ['MF-M18'], 'voll', ''),
    73: ('5.14.5', 'Kontrolle der Beladung des Fahrkorbs (Überlastkontrolle)',
         ['MF-K06'], 'voll', ''),
    74: ('5.15', 'Hinweise, Kennzeichnungen und Bedienungsanleitung',
         ['MF-M17', 'MF-D02'], 'voll', ''),
}

# Tabelle A.1 (Ursprüngliches Risikoprofil): Feld -> Nummern der
# Gefährdungssituationen. Aus dem Normtext übernommen (Häufigkeit, Schwere).
RISIKOPROFIL = {
    ('A', 'III'): [30],
    ('B', 'I'): [6, 25, 30, 60],
    ('B', 'III'): [37, 46, 57],
    ('C', 'I'): [70],
    ('C', 'II'): [3, 9, 15, 17, 19, 22, 23, 27, 40, 50, 56, 71],
    ('C', 'III'): [29, 45],
    ('C-D', 'I'): [1, 3, 7, 8, 12, 13, 14, 16, 17, 26, 27, 31, 32],
    ('C-D', 'II'): [18, 21, 24, 41, 44, 47, 48, 52, 63, 65],
    ('C-D', 'III'): [28, 42, 49, 61, 64],
    ('D', 'I'): [33, 34, 35, 36, 39, 40, 43, 50, 51, 52, 53, 54, 58, 59, 60,
                 62, 66, 68, 71, 72, 74],
    ('D', 'II'): [20, 38, 55, 67, 69, 73],
    ('D-E', 'I'): [10, 11, 24, 55, 73],
}

# Tabelle A.2 (Prioritäten und Zeitplan): (Schwere, Häufigkeit) -> Priorität.
PRIORITAET = {
    ('I', 'A'): 'Extrem', ('I', 'B'): 'Extrem', ('I', 'C'): 'Extrem',
    ('II', 'A'): 'Extrem',
    ('I', 'C-D'): 'Hoch', ('I', 'D'): 'Hoch', ('II', 'B'): 'Hoch',
    ('II', 'C'): 'Hoch', ('II', 'C-D'): 'Hoch', ('III', 'A'): 'Hoch',
    ('III', 'B'): 'Hoch',
    ('I', 'D-E'): 'Mittel', ('II', 'D'): 'Mittel', ('III', 'C'): 'Mittel',
    ('III', 'C-D'): 'Mittel',
    ('I', 'E'): 'Niedrig', ('II', 'D-E'): 'Niedrig', ('II', 'E'): 'Niedrig',
    ('III', 'D'): 'Niedrig',
}

ZEITPLAN = {
    'Extrem': 'Sofort, Aufzug muss stillgelegt werden',
    'Hoch': 'Kurzfristig',
    'Mittel': 'Mittelfristig oder im Rahmen einer umfangreichen Modernisierung',
    'Niedrig': 'Langfristig oder im Rahmen einer Modernisierung der betroffenen '
               'Komponente',
    '': 'Nach Risikobeurteilung im Einzelfall (5.1.5)',
}

RANG = {'Extrem': 4, 'Hoch': 3, 'Mittel': 2, 'Niedrig': 1, '': 0}


def prioritaeten():
    """Nr -> (Priorität, [Felder des Risikoprofils]) nach Tabelle A.1/A.2."""
    out = {}
    for (h, s), nummern in RISIKOPROFIL.items():
        p = PRIORITAET[(s, h)]
        for n in nummern:
            eintrag = out.setdefault(n, ['', []])
            eintrag[1].append('%s/%s' % (s, h))
            if RANG[p] > RANG[eintrag[0]]:
                eintrag[0] = p
    for n in ZUORDNUNG:
        out.setdefault(n, ['', []])
    return {n: (v[0], sorted(v[1])) for n, v in out.items()}
