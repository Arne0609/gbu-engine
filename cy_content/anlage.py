# -*- coding: utf-8 -*-
"""A – Anlagenmerkmale und Systemabgrenzung. Reine Filter-/Modifier-Fragen
(keine eigene Gefährdung), entsprechend TRBS 1115-1 Schritt „Systemabgrenzung".
"""
from .common import *

sel('qa_aufzugsart', 'Aufzugsart', ui='1.1',
    options=[('seil', 'Seil-/Riemenaufzug (Treibscheibe)'),
             ('trommel', 'Trommel- oder Kettenaufzug'),
             ('hydraulik', 'Hydraulikaufzug'),
             ('seil_hydraulik', 'Seil-Hydraulikaufzug'),
             ('plattform', 'Plattformaufzug / Kleingüteraufzug')],
    help='Steuert die Komponente „Hydraulischer Steuerblock".')

yn('qa_ueberwachungsbeduerftig', 'Überwachungsbedürftige Anlage nach ÜAnlG '
   '(Personen- oder Lastenaufzug mit ZÜS-Prüfpflicht)?', ui='1.2',
   help='Bei überwachungsbedürftigen Anlagen ist nach ÜAnlG stets von einem '
        'erheblichen Risiko für Sicherheit und Gesundheit auszugehen (EK-ZÜS '
        'B-002 Anhang 2 Nr. 3). Nein = z. B. Plattformaufzug nach MRL ohne '
        'ZÜS-Pflicht.')

sel('qa_steuerungsart', 'Art der Aufzugssteuerung', ui='1.3',
    options=[('relais', 'Relais-/Schützsteuerung ohne programmierbare Komponenten'),
             ('mikroprozessor', 'Mikroprozessor-/SPS-Steuerung ohne Netzanbindung'),
             ('vernetzt', 'Programmierbare Steuerung mit Netz-/Fernanbindung')],
    help='„Relais" schaltet die komponentenbasierte Betrachtung weitgehend ab: '
         'ohne programmierbare Komponente gibt es keine kompromittierbare '
         'Datenschnittstelle (Vorscreening nach BA-017).')

yn('qa_maschinenraum', 'Triebwerks-/Maschinenraum vorhanden?', ui='1.4',
   help='Nein = maschinenraumlos; die Steuerung sitzt dann im Steuerschrank an '
        'der Haltestelle oder im Schacht.')

yn('qa_vernetzt', 'Anlage mit Netzwerk- oder Internetanbindung (Fernüberwachung, '
   'Fernwartung, Gateway/Router/Modem, Gebäudeleittechnik)?', ui='1.5',
   help='Steuert den Erhebungsbereich N sowie die Komponenten Fernüberwachung, '
        'Remote-Service und Gateway.')

yn('qa_gebaeude_anbindung', 'Anbindung an bauseitige Systeme vorhanden '
   '(Brandmeldeanlage/Brandfallsteuerung, Entrauchung, Gebäudeleittechnik, '
   'Zutrittssystem)?', ui='1.6')

sel('qa_hersteller_vorgaben', 'Vorgaben des Herstellers zur Cybersicherheit', ui='1.7',
    options=[('beruecksichtigt', 'Vorhanden und bei den Maßnahmen berücksichtigt'),
             ('nicht_beruecksichtigt', 'Vorhanden, aber nicht berücksichtigt'),
             ('keine', 'Hersteller stellt keine Vorgaben bereit'),
             ('unbekannt', 'Nicht bekannt / nicht angefragt')],
    help='EK-ZÜS B-002 Anhang 2 Nr. 7. Bewertet in O (Organisation).')
