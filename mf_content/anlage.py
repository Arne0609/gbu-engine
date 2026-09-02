# -*- coding: utf-8 -*-
"""A – Anlagenmerkmale. Reine Filter-/Modifier-Fragen (keine eigene Gefährdung).

Sie werden von vielen Gefährdungen als APPLICABILITY (schaltet die
Gefährdung ganz ab -> NOT_APPLICABLE) oder MODIFIER (verschärft die Stufe)
benutzt. Nummern in Anlehnung an die Stammdaten der App (Abschnitte 2–4)."""
from .common import *

sel('qa_aufzugsart', 'Aufzugsart', ui='3.1',
    options=[('seil', 'Seil-/Riemenaufzug (Treibscheibe)'),
             ('trommel', 'Trommel- oder Kettenaufzug'),
             ('hydraulik', 'Hydraulikaufzug'),
             ('seil_hydraulik', 'Seil-Hydraulikaufzug (indirekt)')],
    help='Steuert, welche Gefährdungen überhaupt bewertet werden (z. B. Bremse und '
         'Gegengewicht nur bei Seilanlagen, Hydraulikeinrichtungen nur bei Hydraulik).')

sel('qa_antrieb', 'Antriebssystem / Regelung', ui='6.1',
    options=[('eingeschw', 'Eingeschwindigkeitsantrieb'),
             ('zweigeschw', 'Zweigeschwindigkeitsantrieb'),
             ('geregelt', 'Geregelter Antrieb (Frequenzumrichter)'),
             ('hydraulisch', 'Hydraulischer Antrieb')])

num('qa_nenngeschwindigkeit', 'Nenngeschwindigkeit [m/s]', min=0.1, max=10, ui='3.1a',
    help='Für die Pufferbewertung (energiespeichernde Puffer nur bis 1,0 m/s).')

yn('qa_gegengewicht', 'Gegengewicht oder Ausgleichsgewicht vorhanden?', ui='3.1b',
   visible_when=in_('qa_aufzugsart', ['seil', 'trommel', 'seil_hydraulik']),
   help='Trommelaufzüge ohne Gegengewicht: Nein. Schaltet Abtrennung und '
        'Sicherung des Gegengewichts sowie die Sturzverhinderung nach oben.')

yn('qa_maschinenraum', 'Eigener Triebwerks-/Maschinenraum vorhanden?', ui='4.7',
   help='Nein = maschinenraumlose Anlage (Antrieb im Schacht, Steuerung im '
        'Schaltschrank). Raumbezogene Gefährdungen entfallen dann.')

yn('qa_rollenraum', 'Zusätzlicher Rollenraum vorhanden?', ui='4.7a',
   visible_when=yes('qa_maschinenraum'))

yn('qa_mehrere_aufzuege', 'Mehrere Aufzüge in einem gemeinsamen Schacht?', ui='4.8')

yn('qa_raum_unter_schacht', 'Betretbarer Raum unterhalb der Schachtgrube?', ui='4.8a',
   help='Zum Beispiel Keller, Technikraum oder Tiefgarage unter der Grube. '
        'Dann ist eine Fangvorrichtung am Gegengewicht oder ein durchgehendes '
        'Fundament erforderlich.')

yn('qa_fahrkorbtuer', 'Fahrkorbabschlusstür vorhanden?', ui='8.6')
yn('qa_glas_schachttueren', 'Schachttüren mit Glas?', ui='4.1')
yn('qa_glas_fahrkorbtueren', 'Fahrkorbtüren mit Glas?', ui='4.3')
yn('qa_glas_schacht', 'Schacht oder Schachtgerüst mit Glas?', ui='4.2')

sel('qa_nutzungsart', 'Nutzungsart der Anlage', ui='2.1',
    options=[('personen', 'Personenaufzug'),
             ('personen_lasten', 'Personen- und Lastenaufzug'),
             ('lasten', 'Lastenaufzug mit Personenbegleitung'),
             ('gueter', 'Güteraufzug ohne Personenbeförderung')])

yn('qa_nutzung_pmem', 'Nutzung durch Personen mit eingeschränkter Mobilität '
   '(Rollstuhl, Rollator, Sehbehinderung) zu erwarten?', ui='4.9',
   help='Wirkt als Verschärfung (Modifier) bei Haltegenauigkeit, Türen und Zugang '
        'und schaltet die Barrierefreiheits-Gefährdung.')
yn('qa_nutzung_kinder', 'Nutzung durch unbeaufsichtigte Kinder zu erwarten '
   '(Schule, Kita, Wohnanlage)?', ui='4.12')
yn('qa_nutzung_flurfoerderzeug', 'Beladung mit Flurförderzeugen oder Transportwagen?',
   ui='4.10')
yn('qa_oeffentlich', 'Öffentlich zugängliche Anlage (Publikumsverkehr)?', ui='2.2')

sel('qa_norm_inverkehrbringen', 'Regelwerk bei Inverkehrbringen / letzter Modernisierung',
    ui='1.28',
    options=[('tra', 'TRA 200 / TRA 102 (vor 1999)'),
             ('en81_1_2', 'DIN EN 81-1 / 81-2 (1999–2017)'),
             ('en81_20', 'DIN EN 81-20 (ab 2017)'),
             ('unbekannt', 'Unbekannt / keine Unterlagen')],
    help='Nur Dokumentation und Hinweis für die Beurteilung – keine automatische '
         'Stufenänderung.')

yn('qa_feuerwehraufzug', 'Feuerwehraufzug oder Aufzug mit Brandfall-Sonderbetrieb '
   '(EN 81-72 / EN 81-73 Evakuierung)?', ui='15.6')
yn('qa_bfs_gefordert', 'Fordert das Brandschutzkonzept des Gebäudes eine '
   'Brandfallsteuerung?', ui='4.11',
   help='Unbekannt = Ja wählen und in K prüfen lassen.')
yn('qa_bma_vorhanden', 'Brandmeldeanlage (BMA) im Gebäude vorhanden?', ui='15.8')
yn('qa_entrauchung_vorhanden', 'Schachtentrauchung / RWA / Lüftungsöffnung im '
   'Schachtkopf vorhanden?', ui='15.9')
yn('qa_sprinkler_vorhanden', 'Löschanlage / Sprinkler im Schacht oder Triebwerksraum '
   'vorhanden?', ui='15.10')

yn('qa_ucm_a3', 'UCM-Schutz (unbeabsichtigte Fahrkorbbewegung, A3 / EN 81-20 5.6.7) '
   'vorhanden?', ui='4.5')
yn('qa_lagerung_statisch_bestimmt', 'Antriebswelle statisch bestimmt gelagert '
   '(keine 3-Punkt-Lagerung)?', ui='4.6',
   visible_when=in_('qa_aufzugsart', ['seil', 'trommel', 'seil_hydraulik']))

num('qa_grubentiefe', 'Schachtgrubentiefe [m]', min=0, max=6, ui='11.1')
