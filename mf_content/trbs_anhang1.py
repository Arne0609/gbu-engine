# -*- coding: utf-8 -*-
"""Zuordnung Gefährdung -> Punkt(e) in TRBS 3121 Anhang 1 (22 Gefährdungspunkte),
abgeglichen mit „TRBS_3121_Master_Risikomatrix_22_Punkte.xlsx" (02.09.2026).
gen_mf_catalog.py ersetzt damit alle Quellenangaben „TRBS 3121 Anh. 1 Nr. …";
Gefährdungen ohne Eintrag bekommen keinen Anhang-1-Bezug (der Anhang deckt sie
nicht ab), andere TRBS-3121-Abschnitte (4.x, Anhang 3/4) bleiben unberührt."""

ANHANG1 = {
    1: 'Anhalte- und Nachregulierungsgenauigkeit',
    2: 'Gegen- und Ausgleichsgewichtsumwehrung',
    3: 'Benachbarte Aufzüge in der Schachtgrube',
    4: 'Benachbarte Aufzüge im Fahrschacht',
    5: 'Schutzräume in Grube und Schachtkopf',
    6: 'Zugang zur Schachtgrube',
    7: 'Stoppeinrichtungen in Grube und Rollenraum',
    8: 'Schachtbeleuchtung',
    9: 'Glas und Sichtfenster in Schachttüren',
    10: 'Schutz an kraftbetätigten Türen',
    11: 'Schachttürverriegelung',
    12: 'Selbstschließung von Schiebetüren',
    13: 'Fahrkorbschürze',
    14: 'Fahrkorbabschlusstüren',
    15: 'Fahrkorbdachumwehrung',
    16: 'UCM und Aufwärts-Übergeschwindigkeit bei Seilaufzügen',
    17: 'Absturz-, Übergeschwindigkeits- und Absinkschutz Hydraulik',
    18: 'Puffer in den Endlagen',
    19: 'Verriegelung der Fahrkorbtür bei großem Schachtwandabstand',
    20: 'Redundante Abschaltung des Antriebs',
    21: 'Schutz gegen elektrischen Schlag und Kennzeichnung',
    22: 'Inspektionssteuerung und Stoppeinrichtung auf dem Fahrkorbdach',
}

HAZARD_TO_NR = {
    'MF-M02': [21], 'MF-M07': [21], 'MF-M08': [16], 'MF-M10': [20], 'MF-M13': [17],
    'MF-M17': [21], 'MF-M20': [7],
    'MF-T01': [11], 'MF-T02': [11], 'MF-T03': [12], 'MF-T04': [9, 10], 'MF-T06': [10, 14],
    'MF-T09': [11],
    'MF-K03': [1], 'MF-K04': [13], 'MF-K05': [19], 'MF-K12': [16], 'MF-K13': [16], 'MF-K14': [16],
    'MF-F01': [15], 'MF-F03': [4], 'MF-F04': [5], 'MF-F05': [22], 'MF-F06': [22],
    'MF-S01': [8], 'MF-S05': [16],
    'MF-G01': [8], 'MF-G02': [5], 'MF-G03': [7], 'MF-G04': [6], 'MF-G06': [18],
    'MF-G07': [2], 'MF-G08': [3],
}
