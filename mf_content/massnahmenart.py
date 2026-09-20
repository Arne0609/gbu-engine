# -*- coding: utf-8 -*-
"""Von Hand bestätigte Maßnahmenarten (TOP).

Die Heuristik in common.massnahmenart() liest das letzte technische bzw.
organisatorische Schlüsselwort des ersten Satzteils. Bei Maßnahmen, die beides
nennen, entscheidet damit die Wortstellung statt der Sache. Hier stehen die
Fälle, in denen die Einstufung von Hand festgelegt ist; common.py zieht die
Tabelle beim Import vor die Heuristik.

Stand: Regelprüfung 20.09.2026.
"""

MASSNAHMENART = {

    # MF-Z01-R3 – der Kern ist die Instandsetzung der Leuchten; die Aufnahme in
    # die Instandhaltung ist nur der nachlaufende organisatorische Teil.
    'Defekte Leuchten und Leuchtmittel instand setzen und die Beleuchtung der Zuwege '
    'in die wiederkehrende Instandhaltung aufnehmen (Prüfintervall festlegen)': 'TECHNICAL',

    # MF-Z02-R1 – Sofortmaßnahme: Prüfen, Kennzeichnen, Freiräumen und Schuhwerk
    # sind sämtlich organisatorisch bzw. personenbezogen; „entfernen lassen“ ist
    # kein technischer Umbau.
    'Verkehrsweg vor dem Begehen prüfen, Stolper- und Rutschstellen kennzeichnen, '
    'abgestellte Gegenstände aus dem Verkehrsweg entfernen lassen; rutschhemmendes '
    'Schuhwerk tragen': 'ORGANISATIONAL',

    # MF-Z07-R4 – Polsterung und Türöffnung sind bauliche Maßnahmen; die
    # Kennzeichnung ist nur die Begleitung.
    'Anstoßschutz (Polsterung) und dauerhafte Kennzeichnung anbringen; Türöffnung '
    'nach DIN EN 81-20 5.2.3.3 anpassen, soweit verhältnismäßig': 'TECHNICAL',

    # MF-Z09-R2 – das Schlüsseldepot ist die technische Lösung, die die Ursache
    # personenunabhängig beseitigt; die ständige Besetzung ist nur der Ersatzweg.
    'Schlüsseldepot bzw. Schlüsseltresor mit Zugriff für den Befreiungsdienst '
    'einrichten; ersatzweise, wo technisch nicht möglich, ständige Besetzung von '
    'Leitwarte oder Pforte vertraglich sicherstellen': 'TECHNICAL',

    # MF-M06-R2 – der Bodenbelag ist die technische Maßnahme, der Wartungsplan
    # nur die Ergänzung.
    'Rutschhemmenden Bodenbelag bzw. rutschhemmende Beschichtung herstellen '
    '(Bewertungsgruppe nach ASR A1.5 / DGUV-Regelwerk); Reinigung zusätzlich in den '
    'Wartungsplan aufnehmen': 'TECHNICAL',

    # MF-M04-R1 – Verlagern und dauerhaftes Herstellen der Freifläche ist baulich.
    'Einbauten und Lagerflächen verlagern, Freifläche dauerhaft herstellen und am '
    'Boden markieren; Freihaltung zusätzlich organisatorisch sicherstellen': 'TECHNICAL',

    # MF-S07-R1 – der Rückbau der Verbauung ist die technische Maßnahme; die
    # Betriebsanweisung tritt daneben.
    'Bauliche Verbauungen und ortsfeste Einbauten vor Schacht- und Inspektionstüren '
    'sowie vor den zugehörigen Schalteinrichtungen zurückbauen, Freihaltefläche '
    'dauerhaft kennzeichnen bzw. abgrenzen (ASR A1.7, ASR A1.3); Freihaltung '
    'zusätzlich in der Betriebsanweisung festlegen und bei Betreiberkontrollen '
    'prüfen': 'TECHNICAL',

    # MF-S07-R3 – Instandsetzung bzw. Nachrüstung im Sicherheitskreis ist
    # technisch; die Funktionsprüfung ist nur der Nachweis.
    'Türkontakt/Verriegelung im Sicherheitskreis instand setzen bzw. nachrüsten und '
    'Wirksamkeit prüfen (DIN EN 81-20 5.3.9.1)': 'TECHNICAL',

    # MF-U07-R2 – Abdichtung, Lüftung, Beheizung und Schutzart sind technisch.
    'Ursache nach Befund beseitigen – bei Wassereintritt abdichten, bei Kondensat '
    'Belüftung bzw. Beheizung von Triebwerksraum oder Schacht herstellen und die '
    'Schutzart der betroffenen Betriebsmittel anheben; betroffene Sicherheitsbauteile '
    'prüfen und bei Korrosionsspuren austauschen lassen': 'TECHNICAL',
}
