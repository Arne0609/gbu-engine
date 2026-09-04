# -*- coding: utf-8 -*-
"""Entscheidungen zur Klärungsliste des Cyber-Typs (fachliche Gegenlesung Arne,
Excel GBU_Cyber_Klaerungsliste vom 03.09.2026: 17 × Vorschlag, 8 × Alternative).

Format wie mf_content/entscheidungen.py:  id -> (Entscheidung, Festlegung).
Entscheidung: 'Vorschlag' | 'Alternative' | 'Anders' | 'offen'.
Solange ein Punkt hier fehlt, gilt er als offen; die zugehörigen Regeln bleiben
quality_status = REVIEW_REQUIRED."""

DATUM = '2026-09-03'

ENTSCHEIDUNGEN = {
    # Komponentenlogik
    'K-C01': ('Vorschlag', 'Stufe Hoch im Cyber-Teil erreichbar (Fernzugriff/kabellos ohne '
                           'umgesetzte Maßnahmen an sicherheitsrelevanter Komponente).'),
    'K-C02': ('Vorschlag', 'Komponente ohne kompromittierbare Schnittstelle: Kein Risiko '
                           '(Vorscreening BA-017/DEKRA).'),
    'K-C03': ('Vorschlag', 'Je Komponente wird die höchste Schnittstellenkategorie erfasst '
                           '(eine Auswahl); konkrete Schnittstellen bleiben App-Dokumentation.'),
    'K-C04': ('Vorschlag', 'Reihenfolge keine < kabelgebunden < Benutzerschnittstelle < kabellos '
                           '< Fernzugriff; Benutzerschnittstelle wird wie lokal bewertet.'),
    'K-C05': ('Vorschlag', 'Lokale Schnittstelle, keine Maßnahmen, Zugang frei: Hoch.'),
    'K-C06': ('Alternative', 'Fernzugriff/kabellos mit umgesetzten, nachgewiesenen Maßnahmen: '
                             'Kein Risiko (statt Niedrig).'),
    'K-C07': ('Vorschlag', 'Frequenzumrichter mit unabhängiger Sicherheitskette: Deckel Niedrig.'),
    'K-C08': ('Vorschlag', 'Unabhängige Sicherheitseinrichtung als Kompensation: Hoch -> Mittel.'),
    'K-C09': ('Vorschlag', 'Notruf: automatischer Testruf mit Ausfallmeldung (EN 81-28) als '
                           'Kompensation Hoch -> Mittel.'),
    'K-C10': ('Alternative', 'Rein lesende Fernüberwachung ohne Netztrennung: Niedrig (statt Mittel).'),
    'K-C11': ('Vorschlag', 'Gebäudeschnittstelle ohne Rückwirkungsfreiheit: Hoch.'),
    'K-C23': ('Alternative', 'Fernwartung dauerhaft aktiv, aber individuell authentifiziert: '
                             'Niedrig (statt Mittel).'),
    'K-C24': ('Alternative', 'Kein Platzhalter „weitere Komponente" im Katalog; weitere Komponenten '
                             'nur als Freitext in der App.'),
    # Zugang / Netz
    'K-C12': ('Vorschlag', 'Steuerung frei zugänglich: Mittel; mit ungesicherten Service'
                           'schnittstellen: Hoch.'),
    'K-C13': ('Vorschlag', 'Werkszugangsdaten: Mittel; bei Netz-/Fernanbindung Hoch.'),
    'K-C21': ('Alternative', 'Freier Zugang zu Triebwerksraum und Schacht nur als Modifier an den '
                             'Komponenten, keine eigene Cyber-Gefährdung (Zugang wird in der '
                             'technischen GBU bewertet).'),
    'K-C14': ('Alternative', 'Software-/Firmwarestand nicht bekannt: Niedrig (statt Mittel).'),
    'K-C22': ('Vorschlag', 'Fehlende Funktionsreduzierung: Niedrig; Mittel bei Netz-/Fernanbindung.'),
    # Organisation
    'K-C15': ('Vorschlag', 'Kein Notfallmanagement: Mittel; Hoch bei Netz-/Fernanbindung.'),
    'K-C16': ('Alternative', 'Fehlende Cyber-Unterweisung: Niedrig (statt Mittel).'),
    'K-C17': ('Vorschlag', 'Prüffristen, Wirksamkeitsnachweis und Funktionsbestätigung fehlen alle '
                           'drei: Hoch.'),
    'K-C18': ('Vorschlag', 'Prüfpflichtige Änderung mit Cyber-Einfluss ohne Prüfung: Hoch.'),
    'K-C19': ('Vorschlag', 'Rückwirkungsfreiheit der Cyber-Maßnahmen nicht sichergestellt: Hoch.'),
    'K-C20': ('Alternative', 'ZÜS-Prüfpunkte 1, 2, 3 und 5 werden als Dokumentationsfragen '
                             'aufgenommen (Pflicht, ohne eigene Stufe; Fragen 5.11–5.14).'),
    'K-C25': ('Vorschlag', 'Herstellervorgaben nicht berücksichtigt: Mittel; nicht bekannt/nicht '
                           'angefragt: Niedrig.'),
}
