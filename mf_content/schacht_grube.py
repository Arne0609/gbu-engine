# -*- coding: utf-8 -*-
"""S – Schacht und G – Schachtgrube (Blaupause: Schindler M007, M008, M009, M014,
M021, M024a, M034, M038, M039, M042, M043, M049, M051, M052, M059, M107;
Inhalte aus App-Kategorien S1–S3, S5–S13)."""
from .common import *

GRP_S = 'Schacht und Gegengewicht'
GRP_G = 'Schachtgrube'
GRP_BEL = 'Beleuchtung'
GRP_SK = 'Sicherheitskomponenten'
GRP_NOT = 'Notruf und Personenbefreiung'
GRP_Z = 'Zugang und Verkehrswege'

SEIL = in_('qa_aufzugsart', ['seil', 'trommel', 'seil_hydraulik'])
GG = all_(SEIL, yes('qa_gegengewicht'))

# ---- Fragen S --------------------------------------------------------------
yn('qs_bel_vorhanden', 'Schachtbeleuchtung vorhanden?', ui='10.1')
yn('qs_bel_ausreichend', 'Schachtbeleuchtung ausreichend (mind. 50 Lux 1 m über dem Fahrkorbdach, '
   'mind. 20 Lux im übrigen Schacht)?', ui='10.1a', visible_when=yes('qs_bel_vorhanden'),
   help='TRBS 3121 Anh. 1 Nr. 8 / DIN EN 81-20 5.2.1.4.1: Arbeitsbereiche auf dem Fahrkorbdach '
        'und in der Grube mindestens 50 lx. Die Grube wird unter 11.2a erfasst.')
yn('qs_bel_altnorm', 'Falls nicht ausreichend: erfüllt die Schachtbeleuchtung die Anforderungen '
   'des Errichtungs-Regelwerks (TRA 200 bzw. DIN EN 81-1/-2)?', ui='10.1c',
   visible_when=no('qs_bel_ausreichend'))
yn('qs_bel_splitterschutz', 'Leuchten im Schacht mit Splitterschutz und an geeigneter Stelle?',
   ui='10.1b', visible_when=yes('qs_bel_vorhanden'))
yn('qs_zugang_bel', 'Beleuchtung an den Schachtzugängen (Haltestellen) mind. 50 lx?',
   ui='10.2',
   help='Sollwert DIN EN 81-20:2020-06 5.3.7.1: mindestens 50 lx am Boden im Bereich der '
        'Schachttüren. Der bisherige Wert „75 Lux" stammte aus dem übernommenen Katalog und '
        'stand im Widerspruch zur eigenen Quellenangabe (Entscheidung Arne 20.09.2026 zum '
        'Prüfbericht, Befund B42).')
yn('qs_vollumwehrt', 'Schacht vollständig umwehrt (Wände, Decke, Boden)?', ui='10.3')
yn('qs_teilumwehrt_zulaessig', 'Teilumwehrung nach EN 81-20 5.2.5.2.3 zulässig ausgeführt '
   '(Höhen, Abstände)?', ui='10.3a', visible_when=no('qs_vollumwehrt'))
yn('qs_wand_fest', 'Schachtwände ausreichend fest (100 kg auf 0,30 m × 0,30 m, keine '
   'Durchbrüche)?', ui='10.4')
yn('qs_glas_vsg', 'Nachweis Verbundsicherheitsglas für die Schachtverglasung vorhanden?',
   ui='10.5', visible_when=yes('qa_glas_schacht'))
yn('qs_schienen_stahl', 'Führungsschienen für Fahrkorb und Gegengewicht aus Stahl?', ui='10.6')
yn('qs_fang', 'Fangvorrichtung am Fahrkorb vorhanden?', ui='10.7', visible_when=SEIL)
yn('qs_begrenzer', 'Geschwindigkeitsbegrenzer vorhanden?', ui='10.8', visible_when=SEIL)
yn('qs_fang_geprueft', 'Prüfung von Fangvorrichtung und Begrenzer dokumentiert?', ui='10.9',
   visible_when=all_(yes('qs_fang'), yes('qs_begrenzer')))
yn('qs_spanngewicht_schalter', 'Spanngewicht des Begrenzerseils mit Schlaffseilschalter?',
   ui='10.10', visible_when=yes('qs_begrenzer'))
yn('qs_fang_ersatzausloesung',
   'Fangvorrichtung durch Bruch der Tragmittel oder durch ein Sicherheitsseil ausgelöst, '
   'in Verbindung mit Leitungsbruchventil oder Drossel?', ui='10.8a',
   visible_when=all_(eq('qa_aufzugsart', 'seil_hydraulik'), no('qs_begrenzer')),
   help='Regelprüfung 20.09.2026: Folgefrage zu 10.8 für den indirekt angetriebenen Hydraulikaufzug. '
        'DIN EN 81-20 Tabelle 12 lässt dort drei Kombinationen zu: Fangvorrichtung, '
        'eingerückt durch Geschwindigkeitsbegrenzer (5.6.2.2.1) – ODER Leitungsbruchventil '
        '(5.6.3) bzw. Drossel (5.6.4) zusammen mit einer Fangvorrichtung, die durch Bruch der '
        'Tragmittel (5.6.2.2.2) oder durch ein Sicherheitsseil (5.6.2.2.3) ausgelöst wird. '
        'Ohne Geschwindigkeitsbegrenzer ist der Aufzug also nur dann normgerecht, wenn eine '
        'dieser beiden Ersatzkombinationen vollständig vorhanden ist. Im Zweifel Nein – dann '
        'wird der Mangel ausgewiesen. Nicht zu verwechseln mit der Schlaffseilüberwachung '
        'nach 5.5.5.3 b) (Frage 10.11): Die ist eine eigene elektrische Sicherheitseinrichtung '
        'und kein Auslösemittel der Fangvorrichtung.')

yn('qs_schlaffseil', 'Schlaffseil-/Schlaffkettensicherung vorhanden?', ui='10.11',
   visible_when=in_('qa_aufzugsart', ['trommel', 'seil_hydraulik']),
   help='Regelprüfung 20.09.2026: Sichtbarkeit auf den Seil-Hydraulikaufzug (indirekt) erweitert. DIN EN 81-20 '
        '5.5.5.3 b) verlangt die Schlaffseil-/Schlaffkettenüberwachung bei Ketten- und '
        'Trommelaufzügen sowie bei Hydraulikaufzügen, sobald eine Gefährdung durch '
        'Schlaffseil oder Schlaffkette besteht – also überall dort, wo Tragmittel vorhanden '
        'sind. Beim direkt angetriebenen Hydraulikaufzug gibt es keine Tragmittel, deshalb '
        'bleibt die Frage dort aus. Sie ist eine elektrische Sicherheitseinrichtung, die das '
        'Triebwerk stillsetzt – KEIN Auslösemittel der Fangvorrichtung; das regelt getrennt '
        '10.8 bzw. 10.8a.')
yn('qs_fremd_frei', 'Schacht frei von aufzugsfremden Einrichtungen?', ui='10.12')
yn('qs_fremd_fachgerecht', 'Aufzugsfremde Leitungen fachgerecht verlegt und gekennzeichnet?',
   ui='10.12a', visible_when=no('qs_fremd_frei'))
yn('qs_fremd_behindert', 'Behindern aufzugsfremde Einrichtungen Arbeiten oder Rettungswege '
   'im Schacht?', ui='10.12b', visible_when=no('qs_fremd_frei'))
yn('qs_zugang_schacht_sicher', 'Zugänge zum Schacht (Schachttüren, Inspektionstüren) frei '
   'und sicher erreichbar (nicht zugestellt, nicht verbaut)?', ui='10.13',
   help='Nur die Erreichbarkeit. Die Wirksamkeit der zugehörigen Sicherheitsschalter steht '
        'unter 10.13a (Prüfbericht 20.09.2026: bisher beides in einer Frage mit Stufe Hoch).')
yn('qs_zugang_schalter_wirksam', 'Elektrische Sicherheitseinrichtungen der Schacht- und '
   'Inspektionstüren vorhanden und wirksam (Türkontakt im Sicherheitskreis)?', ui='10.13a')

# ---- Fragen G --------------------------------------------------------------
yn('qg_bel_vorhanden', 'Beleuchtung in der Schachtgrube vorhanden?', ui='11.2')
yn('qg_bel_50lux', 'Grubenbeleuchtung ausreichend (mind. 50 Lux), Leuchten geeignet '
   'angeordnet?', ui='11.2a', visible_when=yes('qg_bel_vorhanden'))
sel('qg_schutzraum', 'Schutzraum in der Schachtgrube', ui='11.3',
    options=[('normgerecht', 'Schutzraum nach EN 81-20 vorhanden, Abmessungen eingehalten'),
             ('altnorm', 'Schutzraum nach TRA 200 / EN 81-1/-2 (kleiner als EN 81-20)'),
             ('reduziert', 'Reduzierte Grube mit wirksamer Zusatzeinrichtung und Kennzeichnung'),
             ('nicht', 'Schutzraum nicht gegeben')])
yn('qg_nothalt', 'Notbremsschalter in der Schachtgrube vorhanden?', ui='11.4')
yn('qg_nothalt_aussen', 'Notbremsschalter von der Schachttür aus erreichbar?', ui='11.4a',
   visible_when=yes('qg_nothalt'))
yn('qg_nothalt_zwei', 'Bei Grubentiefe über 1,60 m: zweiter Notbremsschalter am Grubenboden '
   'vorhanden?', ui='11.4b', visible_when=all_(yes('qg_nothalt'), gt('qa_grubentiefe', 1.6)))
yn('qg_inspektion', 'Inspektionssteuerung in der Schachtgrube vorhanden?', ui='11.5')
yn('qg_zugangstuer', 'Zugang zur Grube über eine separate Grubenzugangstür '
   '(ebenerdig, ohne Abstieg über eine Leiter)?', ui='11.7',
   help='Zuerst die Zugangsart klären: Nur wenn der Zugang über eine Leiter erfolgt, '
        'werden die Leiterfragen gestellt (TRBS 3121 Anh. 1 Nr. 6 a/b).')
sel('qg_leiter', 'Grubenleiter', ui='11.6', visible_when=no('qg_zugangstuer'),
    options=[('fest', 'Fest installierte Grubenleiter'),
             ('mobil_schacht', 'Mobile Leiter im Schacht deponiert'),
             ('schwer', 'Grubenleiter vorhanden, aber schwer erreichbar'),
             ('kunde', 'Leiter beim Kunden deponiert'),
             ('fahrzeug', 'Leiter wird im Kundendienstfahrzeug mitgeführt'),
             ('keine', 'Keine Grubenleiter')])
yn('qg_zugangstuer_schalter', 'Elektrische Sicherheitseinrichtung an der Grubenzugangstür?',
   ui='11.7a', visible_when=yes('qg_zugangstuer'))
yn('qg_selbstbefreiung', 'Selbstbefreiung aus der Grube über die Schachttür möglich '
   '(Verschluss innerhalb 1,80 m Höhe / 0,80 m horizontal)?', ui='11.8')
yn('qg_notruf', 'Notrufeinrichtung in der Schachtgrube vorhanden?', ui='11.9')
yn('qg_puffer', 'Puffer für Fahrkorb und Gegengewicht vorhanden?', ui='11.10')
sel('qg_puffer_zustand', 'Zustand der Puffer', ui='11.10a', visible_when=yes('qg_puffer'),
    options=[('ok', 'Fest verankert, unbeschädigt und funktionsfähig'),
             ('verschleiss', 'Verschleiß ohne Beeinträchtigung der Funktion (Oberflächenrisse, '
                             'Verhärtung, Korrosion)'),
             ('defekt', 'Beschädigung oder Funktionsverlust (Puffer lose oder gerissen, '
                        'hydraulischer Puffer ohne Öl oder ohne Rückstellung)')],
    help='Regelprüfung 20.09.2026: Aus der Ja/Nein-Frage „unbeschädigt und nicht verschlissen?" geworden. '
         'Sie fasste Verschleiß und Funktionsverlust zusammen und belegte beides mit Hoch '
         'samt Stilllegung der gesamten Anlage – bei bloßem Alterungsverschleiß mit '
         'erhaltener Funktion ist das unverhältnismäßig. Maßgeblich ist die Funktion: '
         'Ein gerissener oder loser Puffer, ein hydraulischer Puffer ohne Öl oder ohne '
         'Rückstellung ist Funktionsverlust; Oberflächenrisse, Verhärtung und Korrosion am '
         'sonst festen, funktionsfähigen Puffer sind Verschleiß. Im Zweifel „Beschädigung '
         'oder Funktionsverlust".')
sel('qg_puffer_art', 'Bauart der Puffer', ui='11.10b',
    options=[('speichernd', 'Energiespeichernd (Feder / Polyurethan)'),
             ('verzehrend', 'Energieverzehrend (hydraulisch)')],
    visible_when=yes('qg_puffer'))
yn('qg_puffer_oelstand', 'Ölstand hydraulischer Puffer prüfbar (Schauglas, Peilstab oder '
   'gleichwertig)?', ui='11.10c', visible_when=eq('qg_puffer_art', 'verzehrend'),
   help='Regelprüfung 20.09.2026: Aus der früheren Doppelfrage „Ölstand prüfbar UND Kennzeichnung vorhanden" '
        'herausgelöst. Der nicht prüfbare Ölstand lässt die Funktion des Sicherheitsbauteils '
        'unbelegt (Mittel); die fehlende Kennzeichnung ist ein Mangel ohne unmittelbaren '
        'Gefährdungsbeitrag und steht jetzt unter 11.10d (Niedrig).')
yn('qg_puffer_kennz', 'Hydraulische Puffer gekennzeichnet (Typ, Füllmenge bzw. Ölsorte, '
   'zulässiger Ölstand)?', ui='11.10d', visible_when=eq('qg_puffer_art', 'verzehrend'),
   help='Regelprüfung 20.09.2026: Aus 11.10c herausgelöst; eigener Befund mit Stufe Niedrig.')
sel('qg_gg_abtrennung', 'Abtrennung der Gegengewichtsfahrbahn in der Grube', ui='11.11',
    options=[('normgerecht', 'Vollwandig oder engmaschig, normgerechte Höhe'),
             ('mangelhaft', 'Vorhanden, aber zu niedrig oder grobmaschig'),
             ('keine', 'Keine Abtrennung')],
    visible_when=GG)
num('qg_gg_abtrennung_hoehe_mm', 'Höhe der Gegengewichtsabtrennung [mm]', min=0, max=6000, ui='11.11a',
    visible_when=neq('qg_gg_abtrennung', 'keine'))
yn('qg_gg_fuellung', 'Gegengewichtsfüllung gegen Herausfallen gesichert (Rahmen)?', ui='11.12',
   visible_when=GG)
yn('qg_gg_fang', 'Fangvorrichtung am Gegengewicht (oder durchgehendes Fundament) bei '
   'betretbarem Raum unter der Grube?', ui='11.13',
   visible_when=all_(GG, yes('qa_raum_unter_schacht')))
yn('qg_nachbar_abtrennung', 'Abtrennung zum Nachbaraufzug in der Schachtgrube vorhanden?',
   ui='11.14', visible_when=yes('qa_mehrere_aufzuege'))
yn('qg_nachbar_abschaltung', 'Einrichtung zum automatischen Abschalten des Nachbaraufzugs bei '
   'Arbeiten in der Schachtgrube vorhanden?', ui='11.14a',
   visible_when=all_(yes('qa_mehrere_aufzuege'), no('qg_nachbar_abtrennung')))
yn('qg_nachbar_abschaltung_geprueft', 'Automatische Abschaltung in der Funktion geprüft, alle '
   'Nachbaranlagen erfasst und Wirkung bei Inspektions- und Rückholbetrieb bestätigt?', ui='11.14b',
   visible_when=yes('qg_nachbar_abschaltung'))
sel('qg_wasser', 'Wasser oder Feuchtigkeit in der Schachtgrube', ui='11.15',
    options=[('kein', 'Keine Feuchtigkeit erkennbar'),
             ('feuchte', 'Nur Feuchte oder Kondensat ohne Kontakt zu Bauteilen'),
             ('wasser', 'Stehendes Wasser in der Grube bzw. Wasser an elektrischen oder '
                        'sicherheitsrelevanten Bauteilen'),
             ('unklar', 'Umfang nicht beurteilbar')],
    help='Regelprüfung 20.09.2026: Aus der Ja/Nein-Frage „Wasser ODER Feuchtigkeit" geworden. Sie '
         'ordnete ausnahmslos Hoch mit Außerbetriebnahme an; feuchte Grubenwände und '
         'Kondensat sind in Altschächten aber der Regelfall und rechtfertigen keine '
         'Stilllegung. Maßgeblich ist der Kontakt zu Bauteilen: Stehendes Wasser an Puffern, '
         'Fangvorrichtung, Grubenschalter oder Leitungen bleibt Hoch – ebenso der nicht '
         'beurteilbare Umfang (fail-closed). Die Abgrenzung entspricht der bereits '
         'geschärften Frage 15.23a für den Bereich außerhalb der Grube.')
yn('qg_oel', 'Öl oder wassergefährdende Stoffe in der Grube ohne Auffangmöglichkeit?',
   ui='11.16')

# ---- Klärungen -------------------------------------------------------------
k('K-S01', 'Schachtgrube', 'Inspektionssteuerung Grube',
  'Fehlende Inspektionssteuerung in der Schachtgrube: Hoch (App S8) oder Mittel (Schindler M051)?',
  'Hoch (App)', 'Mittel (Schindler)', 'Abweichung App/Schindler.')
k('K-S02', 'Schachtgrube', 'Leiter im Fahrzeug',
  'Grubenleiter wird nur im Kundendienstfahrzeug mitgeführt: Mittel (App S3) – auch für '
  'die beauftragte Person des Betreibers, die kein Fahrzeug hat?', 'Mittel',
  'Hoch für Betreiber-Kontrollen', 'Eigene Nachfrage.')
k('K-S03', 'Schacht', 'Aufzugsfremde Leitungen fachgerecht',
  'Aufzugsfremde Leitungen vorhanden, aber fachgerecht verlegt und gekennzeichnet: '
  'Mittel (App S12) oder Niedrig?', 'Mittel', 'Niedrig', 'Eigene Nachfrage.')
k('K-S04', 'Schacht', 'Puffer bei > 1,0 m/s',
  'Energiespeichernde Puffer bei Nenngeschwindigkeit über 1,0 m/s: Mittel (App S9)?',
  'Mittel', 'Hoch', 'Eigene Nachfrage; EN 81-20 5.8.2.1 begrenzt auf 1,0 m/s.')
k('K-S05', 'Schacht', 'Teilumwehrter Schacht',
  'Teilumwehrter Schacht, nach aktuellen Vorgaben zulässig ausgeführt: Mittel (App S6) – '
  'oder Kein Risiko, wenn zulässig?', 'Mittel', 'Kein Risiko', 'Die App-Option ist gelb, obwohl „zulässig".')

# ---- Gefährdungen S --------------------------------------------------------
hz('MF-S01', 'Unzureichende Schachtbeleuchtung', GRP_BEL,
   [('qs_bel_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qs_bel_ausreichend', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qs_bel_vorhanden')}),
    ('qs_bel_altnorm', 'COMPENSATION', 'CONDITIONAL', {'required_when': no('qs_bel_ausreichend')}),
    ('qs_bel_splitterschutz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qs_bel_vorhanden')})],
   [r(no('qs_bel_vorhanden'), 'HIGH', mfrom=('N20-S1', 'Keine Beleuchtung'), evidence='HIGH_CONFIDENCE'),
    r(all_(no('qs_bel_ausreichend'), no('qs_bel_altnorm')), 'MEDIUM', mfrom=('N20-S1', 'Dunkle'),
      evidence='HIGH_CONFIDENCE', pb='B05 – Maßstab 50 lx auf dem Fahrkorbdach; Altnorm-Fall getrennt'),
    r(all_(no('qs_bel_ausreichend'), yes('qs_bel_altnorm')), 'LOW', mfrom=('N20-S1', 'Dunkle'),
      evidence='HIGH_CONFIDENCE',
      notes='TRBS 3121 Anh. 1 Nr. 8: Risiko niedrig, wenn die Schachtbeleuchtung TRA 200 bzw. EN 81-1/-2 entspricht.',
      pb='B05 – neu'),
    r(no('qs_bel_splitterschutz'), 'MEDIUM', mfrom=('N20-S1', 'Leuchten ohne'),
      sofort='Ungeschützte oder bruchgefährdete Leuchten spannungsfrei schalten bzw. außer '
             'Betrieb nehmen und gegen herabfallende Splitter sichern; Betreiber unterrichten',
      mittel='Leuchten mit Splitterschutz ausstatten und außerhalb des Fahrbereichs sowie der '
             'Arbeitsbereiche auf Fahrkorbdach und in der Grube anordnen',
      evidence='HIGH_CONFIDENCE', pb='H11 – Sofortmaßnahme ergänzt',
      notes='Regelprüfung 20.09.2026: Die Sofortmaßnahme traf einen anderen Sachverhalt als die Bedingung '
            '(beschädigte Leuchte statt fehlender Splitterschutz) und war für Prüfer und '
            'Betreiber nicht sofort ausführbar.')],
   sources=[en8120('5.2.1.4.1'), trbs3121('Anh. 1 Nr. 8')], factor=F_BELEUCHTUNG,
   persons=[WARTUNG], agg='MAXIMUM', bereich='S')

hz('MF-S02', 'Unzureichende Beleuchtung an den Schachtzugängen', GRP_BEL,
   [('qs_zugang_bel', 'TRIGGER', 'ALWAYS')],
   [r(no('qs_zugang_bel'), 'MEDIUM',
      sofort='Betreiber auf die Beleuchtung der Haltestellen hinweisen',
      mittel='Beleuchtung an den Schachtzugängen auf mind. 50 lx (Boden) herstellen',
      evidence='INFERRED')],
   sources=[en8120('5.3.7.1')], factor=F_BELEUCHTUNG, persons=[NUTZER], bereich='S')

hz('MF-S03', 'Unzureichende Schachtumwehrung oder Schachtwände', GRP_S,
   [('qs_vollumwehrt', 'TRIGGER', 'ALWAYS'),
    ('qs_teilumwehrt_zulaessig', 'COMPENSATION', 'CONDITIONAL', {'required_when': no('qs_vollumwehrt')}),
    ('qs_wand_fest', 'TRIGGER', 'ALWAYS'),
    ('qs_glas_vsg', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_glas_schacht')}),
    ('qa_glas_schacht', 'OPTIONAL', 'NEVER')],
   [r(no('qs_wand_fest'), 'HIGH', mfrom=('N20-S6', 'Schachtumwehrung durchbrochen'),
      evidence='HIGH_CONFIDENCE'),
    r(all_(no('qs_vollumwehrt'), no('qs_teilumwehrt_zulaessig')), 'HIGH',
      mfrom=('N20-S6', 'Schachtumwehrung durchbrochen'), evidence='INFERRED'),
    r(all_(no('qs_vollumwehrt'), yes('qs_teilumwehrt_zulaessig')), 'NO_RISK',
      evidence='HIGH_CONFIDENCE', klaerung='K-S05',
      notes='Entscheidung 02.09.2026: zulässig ausgeführte Teilumwehrung = kein Risiko.'),
    r(no('qs_glas_vsg'), 'MEDIUM', mfrom=('N20-S6', 'Verglasung'),
      mittel='Nachweis des Verbundsicherheitsglases (Scheibenkennzeichnung, Hersteller- bzw. '
             'Übereinstimmungsbescheinigung) beibringen; andernfalls Verglasung durch '
             'Verbundsicherheitsglas nach DIN EN 81-20 5.2.5 ersetzen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Gefordert ist der Werkstoffnachweis der Scheibe, nicht ein statischer '
            'Nachweis – „Statischen Nachweis erbringen" führte zur falschen Abhilfe.')],
   sources=[en8120('5.2.5'), en8120('5.2.5.2.3')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='S')

hz('MF-S04', 'Führungsschienen nicht aus Stahl', GRP_S,
   [('qs_schienen_stahl', 'TRIGGER', 'ALWAYS')],
   [r(no('qs_schienen_stahl'), 'MEDIUM',
      sofort='Führungsschienen, Verbindungen und Halterungen im Rahmen dieser Prüfung '
             'sichtprüfen; bei Verformung, Korrosion, Verschleiß oder erkennbar '
             'unzureichender Bremsfläche Anlage stilllegen; Betreiber unterrichten',
      mittel='Zustand der Führungsschienen in die wiederkehrende Wartung aufnehmen; bei '
             'Modernisierung Führungsschienen aus Stahl nach EN 81-20 5.7 vorsehen',
      evidence='INFERRED',
      notes='Regelprüfung 20.09.2026: „Zustand bei jeder Wartung prüfen" ist eine Dauerauflage und wirkt im '
            'Prüfzeitpunkt nicht; sie steht jetzt in der mittelfristigen Maßnahme.')],
   sources=[en8120('5.7.1')], factor=F_KINETISCH, persons=[NUTZER], bereich='S')

hz('MF-S05', 'Fehlende oder ungeprüfte Fangvorrichtung, Geschwindigkeitsbegrenzer oder '
   'Schlaffseilsicherung', GRP_SK,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': SEIL}),
    ('qs_fang', 'TRIGGER', 'ALWAYS'),
    ('qs_begrenzer', 'TRIGGER', 'ALWAYS'),
    ('qs_fang_geprueft', 'TRIGGER', 'CONDITIONAL', {'required_when': all_(yes('qs_fang'), yes('qs_begrenzer'))}),
    ('qs_spanngewicht_schalter', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qs_begrenzer')}),
    ('qs_fang_ersatzausloesung', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': all_(eq('qa_aufzugsart', 'seil_hydraulik'), no('qs_begrenzer'))}),
    ('qs_schlaffseil', 'TRIGGER', 'CONDITIONAL',
     {'required_when': in_('qa_aufzugsart', ['trommel', 'seil_hydraulik'])})],
   [r(no('qs_fang'), 'HIGH', mfrom=('N20-S10', 'Keine Fangvorrichtung'), evidence='HIGH_CONFIDENCE'),
    # Regelprüfung 20.09.2026: Am Normtext nachgeschlagen (DIN EN 81-20:2014, Tabelle 11 und
    # Tabelle 12; bestätigt durch EN 81-1:1998 9.8.3.1):
    #   Tabelle 11 (Treibscheiben-, TROMMEL- und Kettenaufzüge) nennt für den
    #   freien Fall des FAHRKORBS als Betätigungsmittel ausschließlich den
    #   Geschwindigkeitsbegrenzer (5.6.2.2.1). Die Alternative „bis 1 m/s durch
    #   Bruch der Tragmittel (5.6.2.2.2) oder Sicherheitsseil (5.6.2.2.3)" gilt
    #   dort NUR für das Gegengewicht bzw. Ausgleichsgewicht. Für Treibscheiben-
    #   UND Trommelaufzüge ist der fehlende Begrenzer also ein Hoch-Befund.
    #   Tabelle 12 lässt beim INDIREKT angetriebenen Hydraulikaufzug drei
    #   Kombinationen zu; zwei davon kommen ohne Begrenzer aus, verlangen dann
    #   aber Leitungsbruchventil (5.6.3) oder Drossel (5.6.4) ZUSAMMEN mit einer
    #   Fangvorrichtung, die durch Bruch der Tragmittel oder Sicherheitsseil
    #   ausgelöst wird. Nur dafür ist der Begrenzer entbehrlich – abgefragt über
    #   die neue Frage 10.8a.
    r(no('qs_begrenzer'), 'HIGH', mfrom=('N20-S10', 'Keine Fangvorrichtung'),
      applicability=in_('qa_aufzugsart', ['seil', 'trommel']),
      mittel='Geschwindigkeitsbegrenzer nachrüsten, der die Fangvorrichtung auslöst (DIN EN 81-20 5.6.2.2.1)',
      evidence='HIGH_CONFIDENCE', pb='B11 – Maßnahme zielte auf die Fangvorrichtung statt den Begrenzer',
      notes='Regelprüfung 20.09.2026: (vormals MF-S05-R2; die eingeschränkte Anwendbarkeit ist ein neuer Sachverhalt '
            'und bekommt nach der ID-Regel eine neue Regel-ID.) Frage 10.8 ist für alle drei '
            'Seil-Bauarten sichtbar, die Regel vergab aber ausnahmslos Hoch mit Stilllegung – '
            'beim indirekt angetriebenen Hydraulikaufzug auch dann, wenn die Anlage nach '
            'DIN EN 81-20 Tabelle 12 normgerecht mit Leitungsbruchventil oder Drossel plus '
            'Ersatzauslösung ausgeführt ist. Die Anwendbarkeit folgt jetzt Tabelle 11 '
            '(Treibscheibe und Trommel/Kette – dort ist der Begrenzer für den Fahrkorb '
            'zwingend); der Hydraulikfall steht in der folgenden Regel. Stufe, Bedingung und '
            'Maßnahmen bleiben.'),
    r(all_(no('qs_begrenzer'), no('qs_fang_ersatzausloesung')), 'HIGH',
      applicability=eq('qa_aufzugsart', 'seil_hydraulik'),
      sofort='Aufzug stilllegen',
      mittel='Zulässige Kombination nach DIN EN 81-20 Tabelle 12 herstellen – '
             'Geschwindigkeitsbegrenzer nachrüsten, der die Fangvorrichtung auslöst, oder '
             'Leitungsbruchventil bzw. Drossel zusammen mit einer durch Bruch der Tragmittel '
             'oder Sicherheitsseil ausgelösten Fangvorrichtung',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Neue Regel für den indirekt angetriebenen Hydraulikaufzug. Der fehlende '
            'Geschwindigkeitsbegrenzer ist dort erst dann ein Mangel, wenn auch die nach '
            'DIN EN 81-20 Tabelle 12 zulässige Ersatzkombination fehlt (10.8a = Nein). Ist '
            'sie vorhanden, entsteht kein Befund – die Anlage ist normgerecht. Fail-closed: '
            'bleibt 10.8a unbeantwortet, ist die Gefährdung unvollständig.'),
    r(no('qs_schlaffseil'), 'HIGH', mfrom=('N20-S10', 'Keine Schlaffseil'),
      evidence='HIGH_CONFIDENCE', sources=[en8120('5.5.5.3')],
      notes='Regelprüfung 20.09.2026: Gilt jetzt auch für den Seil-Hydraulikaufzug (indirekt) – die Sichtbarkeit von '
            '10.11 ist auf diese Bauart erweitert. DIN EN 81-20 5.5.5.3 b) verlangt die '
            'Schlaffseil-/Schlaffkettenüberwachung bei Ketten- und Trommelaufzügen sowie bei '
            'Hydraulikaufzügen, sobald eine Gefährdung durch Schlaffseil oder Schlaffkette '
            'besteht. Sie ist eine eigenständige elektrische Sicherheitseinrichtung und '
            'ausdrücklich KEIN Auslösemittel der Fangvorrichtung – ein früherer Entwurf dieser '
            'Regelprüfung hatte das verwechselt.'),
    r(no('qs_fang_geprueft'), 'MEDIUM', mfrom=('N20-S10', 'Prüfung von'), evidence='HIGH_CONFIDENCE'),
    r(no('qs_spanngewicht_schalter'), 'MEDIUM', mfrom=('N20-S10', 'Spanngewicht'),
      sofort='Begrenzerseil und Spanngewicht im Rahmen dieser Prüfung sichtprüfen; bei '
             'schlaffem, beschädigtem oder abgelaufenem Seil Anlage stilllegen; Betreiber '
             'unterrichten und Nachrüstung veranlassen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: „Spanngewicht bei Wartung sichtprüfen" ist eine Dauerauflage, keine '
            'Sofortmaßnahme.')],
   sources=[en8120('5.6.2'), en8120('5.6.2.2.1.6'), en8120('5.5.5.3')], factor=F_KINETISCH,
   persons=[NUTZER], agg='MAXIMUM', bereich='S')

hz('MF-S06', 'Aufzugsfremde Einrichtungen im Schacht', GRP_S,
   [('qs_fremd_frei', 'TRIGGER', 'ALWAYS'),
    ('qs_fremd_fachgerecht', 'COMPENSATION', 'CONDITIONAL', {'required_when': no('qs_fremd_frei')}),
    ('qs_fremd_behindert', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qs_fremd_frei')})],
   [r(yes('qs_fremd_behindert'), 'HIGH', prio=300, mfrom=('N20-S12', 'Aufzugsfremde Einrichtungen behindern'),
      evidence='HIGH_CONFIDENCE'),
    r(all_(no('qs_fremd_frei'), no('qs_fremd_fachgerecht')), 'HIGH', prio=200,
      mfrom=('N20-S12', 'Aufzugsfremde Einrichtungen behindern'), evidence='INFERRED'),
    r(no('qs_fremd_frei'), 'MEDIUM', prio=100, mfrom=('N20-S12', 'Aufzugsfremde Leitungen'),
      evidence='HIGH_CONFIDENCE', klaerung='K-S03')],
   sources=[en8120('5.2.1.2')], factor=F_STURZ, persons=[WARTUNG], bereich='S')

hz('MF-S07', 'Zugänge zum Schacht und zugehörige Schalteinrichtungen nicht frei und sicher '
   'begehbar', GRP_Z,
   [('qs_zugang_schacht_sicher', 'TRIGGER', 'ALWAYS'),
    ('qs_zugang_schalter_wirksam', 'TRIGGER', 'ALWAYS')],
   [r(no('qs_zugang_schalter_wirksam'), 'HIGH', prio=200,
      sofort='Anlage stilllegen, bis die Sicherheitseinrichtung der Schacht-/Inspektionstür '
             'wieder wirkt',
      mittel='Türkontakt/Verriegelung im Sicherheitskreis instand setzen bzw. nachrüsten und '
             'Wirksamkeit prüfen (DIN EN 81-20 5.3.9.1)',
      evidence='HIGH_CONFIDENCE',
      notes='Prüfbericht 20.09.2026: aus 10.13 herausgelöst – unwirksamer Türkontakt ist ein '
            'technischer Mangel am Sicherheitskreis, nicht ein zugestellter Verkehrsweg. '
            'Regelprüfung 20.09.2026: Maßnahme als technische Maßnahme geführt (vorher organisatorisch, was die '
            'TOP-Bewertung der Regel verfälschte). Eine festgestellte Überbrückung ist vor '
            'Wiederinbetriebnahme zu entfernen und die Wirksamkeit durch Funktionsprüfung '
            'zu belegen.'),
    r(no('qs_zugang_schacht_sicher'), 'MEDIUM', prio=100,
      sofort='Zugänge freiräumen, Hindernisse entfernen, Betreiber informieren',
      mittel='Bauliche Verbauungen und ortsfeste Einbauten vor Schacht- und Inspektionstüren '
             'sowie vor den zugehörigen Schalteinrichtungen zurückbauen, Freihaltefläche '
             'dauerhaft kennzeichnen bzw. abgrenzen (ASR A1.7, ASR A1.3); Freihaltung '
             'zusätzlich in der Betriebsanweisung festlegen und bei Betreiberkontrollen prüfen',
      evidence='INFERRED',
      notes='Blaupause Schindler M107 (f021 = Nein -> Hoch, DIRECT). Prüfbericht 20.09.2026: '
            'Hoch auf Mittel – ein zugestellter Zugang wird vor der Arbeit beseitigt; Hoch '
            'bleibt dem unwirksamen Sicherheitsschalter (10.13a) vorbehalten. '
            'Regelprüfung 20.09.2026: Frage 10.13 erfasst zwei Sachverhalte – „zugestellt" (Ordnungsmangel) und '
            '„verbaut" (bauliche Veränderung). Für den verbauten Zugang ist eine technische '
            'Maßnahme möglich und nach TOP vorrangig; die Mittelfristmaßnahme war rein '
            'organisatorisch und ließ die Ursache bestehen. Sie nennt jetzt beide Arten '
            'getrennt und ist als [TECH] geführt.')],
   sources=[en8120('5.2.2.1'), trbs3121('Anh. 1 Nr. 5')], factor=F_STURZ, persons=[BEAUFTRAGTE, WARTUNG],
   bereich='S')

# ---- Gefährdungen G --------------------------------------------------------
hz('MF-G01', 'Unzureichende Beleuchtung in der Schachtgrube', GRP_BEL,
   [('qg_bel_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qg_bel_50lux', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qg_bel_vorhanden')})],
   [r(no('qg_bel_vorhanden'), 'MEDIUM', mfrom=('N20-S1', 'Keine Beleuchtung'),
      sofort='Grube nur mit ausreichender, mitgeführter Handleuchte betreten; Not-Halt vor '
             'dem Abstieg betätigen; Betreiber unterrichten',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Hoch auf Mittel. Die Gefahr entsteht erst beim Abstieg und wird von der '
            'eigenen Sofortmaßnahme (Handleuchte) vollständig beherrscht – alle übrigen '
            'Hoch-Regeln der Schachtgrube verlangen Stilllegen oder Nichtbetreten.'),
    r(no('qg_bel_50lux'), 'LOW', mfrom=('N20-S1', 'Leuchten an ungeeigneter'),
      mittel='Beleuchtung ergänzen, ersetzen oder neu anordnen, bis mindestens 50 lx 1 m über '
             'der Grubensohle erreicht werden; Leuchten gegen Beschädigung schützen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Mittel auf Niedrig – Beleuchtung ist vorhanden, nur unzureichend; mit Mittel '
            'lag die Regel gleichauf mit dem völligen Fehlen. Die Maßnahme „Leuchten '
            'versetzen" traf nur einen der beiden von 11.2a erfassten Fälle.')],
   sources=[en8120('5.2.1.4.1'), trbs3121('Anh. 1 Nr. 8')], factor=F_BELEUCHTUNG, persons=[WARTUNG],
   agg='MAXIMUM', bereich='G')

hz('MF-G02', 'Unzureichender Schutzraum in der Schachtgrube', GRP_G,
   [('qg_schutzraum', 'TRIGGER', 'ALWAYS')],
   [r(eq('qg_schutzraum', 'nicht'), 'HIGH', mfrom=('N20-S7', 'Schutzraum in der Schachtgrube nicht'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qg_schutzraum', 'altnorm'), 'LOW',
      sofort='Zustand dokumentieren, Beschäftigte über den reduzierten Schutzraum unterweisen',
      mittel='Bei Modernisierung Schutzräume nach EN 81-20 herstellen oder Schutzeinrichtung für temporären Schutzraum vorsehen',
      evidence='INFERRED', klaerung='K-F05',
      notes='TRBS 3121 Anh. 1 Nr. 5: Risiko niedrig bei Schutzräumen nach TRA 200 oder EN 81-1/-2.'),
    r(eq('qg_schutzraum', 'reduziert'), 'NO_RISK', evidence='HIGH_CONFIDENCE', klaerung='K-F03',
      notes='Entscheidung 02.09.2026: reduzierte Grube mit wirksamer Zusatzeinrichtung = kein Risiko.')],
   sources=[en8120('5.2.5.8'), trbs3121('Anh. 1 Nr. 18')], factor=F_QUETSCH, persons=[WARTUNG],
   bereich='G')

hz('MF-G03', 'Fehlender Not-Halt oder fehlende Inspektionssteuerung in der Schachtgrube', GRP_SK,
   [('qg_nothalt', 'TRIGGER', 'ALWAYS'),
    ('qg_nothalt_aussen', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qg_nothalt')}),
    ('qg_nothalt_zwei', 'TRIGGER', 'CONDITIONAL',
     {'required_when': all_(yes('qg_nothalt'), gt('qa_grubentiefe', 1.6))}),
    ('qg_inspektion', 'TRIGGER', 'ALWAYS'),
    ('qa_grubentiefe', 'MODIFIER', 'NEVER')],
   [r(no('qg_nothalt'), 'HIGH', mfrom=('N20-S8', 'Kein Notbremsschalter'), evidence='HIGH_CONFIDENCE'),
    r(no('qg_inspektion'), 'MEDIUM', mfrom=('N20-S8', 'Keine Inspektionssteuerung'),
      evidence='HIGH_CONFIDENCE', klaerung='K-S01'),
    r(no('qg_nothalt_aussen'), 'MEDIUM', mfrom=('N20-S8', 'Notbremsschalter vorhanden, aber'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qg_nothalt_zwei'), 'MEDIUM', mfrom=('N20-S8', 'Bei einer Grubentiefe'),
      mittel='Zweite Halteinrichtung am Grubenboden nachrüsten (DIN EN 81-20, 5.2.1.5.1)',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Fundstelle korrigiert: 5.2.1.5.1 a) statt 5.4.8 – dieselbe Stelle, die die '
            'Hilfe zu 11.1 und die Quellen der Gefährdung nennen.')],
   sources=[en8120('5.2.1.5.1'), en8120('5.12.1.5.1.1')], factor=F_BEFEHL, persons=[WARTUNG],
   agg='MAXIMUM', bereich='G')

hz('MF-G04', 'Unsicherer Zugang zur Schachtgrube (Leiter, Grubenzugangstür)', GRP_Z,
   [('qg_zugangstuer', 'TRIGGER', 'ALWAYS'),
    ('qg_leiter', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qg_zugangstuer')}),
    ('qg_zugangstuer_schalter', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qg_zugangstuer')})],
   [r(all_(no('qg_zugangstuer'), eq('qg_leiter', 'keine')), 'HIGH', mfrom=('N20-S3', 'Keine Grubenleiter'),
      evidence='HIGH_CONFIDENCE',
      pb='Prüfbericht 16.09.2026 – Leiter nur bewertet, wenn der Zugang über eine Leiter erfolgt'),
    r(no('qg_zugangstuer_schalter'), 'HIGH',
      sofort='Grubenzugangstür verschlossen halten, Zutritt nur mit Freischaltung der Anlage',
      mittel='Elektrische Sicherheitseinrichtung (Türkontakt im Sicherheitskreis) an der '
             'Grubenzugangstür nachrüsten', evidence='INFERRED',
      notes='Blaupause Schindler M008 (f069 = Ja, f070 = Nein -> Hoch, DIRECT).'),
    r(all_(no('qg_zugangstuer'), eq('qg_leiter', 'mobil_schacht')), 'LOW',
      sofort='Mobile Leiter vor jedem Abstieg auf Eignung, Unversehrtheit und sicheren Stand '
             'prüfen; Not-Halt vorher betätigen',
      mittel='Fest installierte Grubenleiter nach DIN EN 81-20 5.2.2.4 nachrüsten',
      evidence='INFERRED',
      notes='Prüfbericht 20.09.2026: Die Option blieb ohne Regel und damit ohne Stufe. Eine im '
            'Schacht deponierte mobile Leiter ist verfügbar, aber keine fest angebrachte '
            'Steigeinrichtung (TRBS 3121 Anh. 1 Nr. 6).'),
    r(all_(no('qg_zugangstuer'), eq('qg_leiter', 'schwer')), 'MEDIUM', mfrom=('N20-S3', 'Grubenleiter schwer'),
      evidence='HIGH_CONFIDENCE', pb='Prüfbericht 16.09.2026 – nur bei Zugang über Leiter'),
    r(all_(no('qg_zugangstuer'), eq('qg_leiter', 'kunde')), 'MEDIUM', mfrom=('N20-S3', 'Grubenleiter ist beim Kunden'),
      sofort='Leiter vor dem Abstieg holen, auf Eignung, Unversehrtheit und sicheren Stand '
             'prüfen, Not-Halt vorher betätigen; ohne geeignete Leiter nicht einsteigen',
      evidence='HIGH_CONFIDENCE', pb='Prüfbericht 16.09.2026 – nur bei Zugang über Leiter',
      notes='Regelprüfung 20.09.2026: „Auf Eignung, Unversehrtheit, Vollständigkeit achten" war eine Ermahnung ohne '
            'Handlung und ohne Folge für den Fall, dass die beim Kunden deponierte Leiter '
            'untauglich oder nicht auffindbar ist.'),
    r(all_(no('qg_zugangstuer'), eq('qg_leiter', 'fahrzeug')), 'HIGH', mfrom=('N20-S3', 'Grubenleiter wird'),
      evidence='HIGH_CONFIDENCE', klaerung='K-S02', pb='Prüfbericht 16.09.2026 – nur bei Zugang über Leiter')],
   sources=[en8120('5.2.2.4'), en8120('5.2.3.3'), trbs3121('Anh. 1 Nr. 6')], factor=F_ABSTURZ,
   persons=[WARTUNG, BEAUFTRAGTE], agg='MAXIMUM', bereich='G')

hz('MF-G05', 'Keine Selbstbefreiung aus der Schachtgrube und kein Notruf in der Grube', GRP_NOT,
   [('qg_selbstbefreiung', 'TRIGGER', 'ALWAYS'),
    ('qg_notruf', 'TRIGGER', 'ALWAYS')],
   [r(all_(no('qg_selbstbefreiung'), no('qg_notruf')), 'HIGH', prio=300,
      mfrom=('N20-S13', 'Keine Selbstbefreiung'), evidence='HIGH_CONFIDENCE'),
    r(no('qg_selbstbefreiung'), 'MEDIUM', prio=200, mfrom=('N20-S13', 'Selbstbefreiung nur'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qg_notruf'), 'MEDIUM', prio=100, mfrom=('N20-K12', 'Keine Notrufverbindung vom FK-Dach'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.3.9.3.5'), en8120('5.12.3.2'), trbs3121('Anh. 1 Nr. 7')], factor=F_NOTFALL,
   persons=[WARTUNG], bereich='G')

hz('MF-G06', 'Fehlende, beschädigte oder ungeeignete Puffer', GRP_G,
   [('qg_puffer', 'TRIGGER', 'ALWAYS'),
    ('qg_puffer_zustand', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qg_puffer')}),
    ('qg_puffer_art', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qg_puffer')}),
    ('qg_puffer_oelstand', 'TRIGGER', 'CONDITIONAL', {'required_when': eq('qg_puffer_art', 'verzehrend')}),
    ('qg_puffer_kennz', 'TRIGGER', 'CONDITIONAL', {'required_when': eq('qg_puffer_art', 'verzehrend')}),
    ('qa_nenngeschwindigkeit', 'MODIFIER', 'NEVER')],
   [r(no('qg_puffer'), 'HIGH', mfrom=('N20-S9', 'Puffer fehlen'), evidence='HIGH_CONFIDENCE'),
    r(eq('qg_puffer_zustand', 'defekt'), 'HIGH', mfrom=('N20-S9', 'Puffer fehlen'),
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Bedingung auf den Funktionsverlust eingegrenzt (11.10a ist jetzt eine '
            'Auswahlfrage). Hoch samt Stilllegung bleibt dem gerissenen oder losen Puffer und '
            'dem hydraulischen Puffer ohne Öl oder ohne Rückstellung vorbehalten; bloßer '
            'Alterungsverschleiß bei erhaltener Funktion führte vorher ebenfalls zur '
            'Stilllegung der gesamten Anlage – ein unverhältnismäßiges und damit falsches '
            'Bewertungsergebnis.'),
    r(eq('qg_puffer_zustand', 'verschleiss'), 'MEDIUM', prio=100,
      sofort='Betreiber unterrichten, Pufferzustand bei jeder Wartung dokumentiert überwachen',
      mittel='Puffer bei der nächsten Wartung ersetzen (DIN EN 81-20 5.8.1)',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Neue Regel für den Verschleißfall. Verschleiß bei erhaltener Funktion ist eine '
            'wirksame, aber unvollständige Schutzmaßnahme und damit Mittel – nicht Hoch.'),
    r(all_(eq('qg_puffer_art', 'speichernd'), gt('qa_nenngeschwindigkeit', 1.0)), 'HIGH',
      mfrom=('N20-S9', 'Energiespeichernde'), evidence='HIGH_CONFIDENCE', klaerung='K-S04'),
    r(no('qg_puffer_oelstand'), 'MEDIUM', mfrom=('N20-S9', 'Ölstand'),
      sofort='Betreiber unterrichten und Ölstandsprüfung über die Wartungsfirma veranlassen; '
             'bei erkennbarem Ölaustritt oder nicht zurückgestelltem Puffer Anlage stilllegen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Bedingung auf den nicht prüfbaren Ölstand eingegrenzt; die fehlende '
            'Kennzeichnung steht jetzt in einer eigenen Regel mit Stufe Niedrig. Die '
            'Sofortmaßnahme „Zustand sichtprüfen" war keine Maßnahme, sondern der Prüfschritt '
            'selbst – sie wirkte nichts und nannte keine Konsequenz. Stufe Mittel und '
            'Mittelfristmaßnahme bleiben.'),
    r(no('qg_puffer_kennz'), 'LOW',
      sofort='Puffer provisorisch kennzeichnen; Angaben beim Hersteller oder '
             'Wartungsunternehmen anfordern',
      mittel='Dauerhafte Kennzeichnung der hydraulischen Puffer anbringen (Typ, Ölsorte bzw. '
             'Füllmenge, zulässiger Ölstand) und in die Wartungsunterlagen aufnehmen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Neue Regel. Die fehlende Kennzeichnung war mit dem nicht prüfbaren Ölstand in '
            'einer Frage gebündelt und wurde mit Mittel überbewertet: Sie ist ein Mangel ohne '
            'unmittelbaren Gefährdungsbeitrag.')],
   sources=[en8120('5.8.1.1'), en8120('5.8.2.1')], factor=F_STOSS, persons=[NUTZER, WARTUNG],
   agg='MAXIMUM', bereich='G')

hz('MF-G07', 'Fehlende oder unzulängliche Abtrennung und Sicherung des Gegengewichts', GRP_S,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': GG}),
    ('qa_gegengewicht', 'APPLICABILITY', 'NEVER'),
    ('qg_gg_abtrennung', 'TRIGGER', 'ALWAYS'),
    ('qg_gg_abtrennung_hoehe_mm', 'DOCUMENTATION', 'NEVER'),
    ('qg_gg_fuellung', 'TRIGGER', 'ALWAYS'),
    ('qg_gg_fang', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_raum_unter_schacht')}),
    ('qa_raum_unter_schacht', 'MODIFIER', 'NEVER')],
   [r(eq('qg_gg_abtrennung', 'keine'), 'HIGH', mfrom=('N20-S11', 'Keine Abtrennung'),
      mittel='Abtrennung der Gegengewichtsfahrbahn von höchstens 0,30 m bis mindestens 2,0 m über der '
             'Schachtgrubensohle in der Breite des Gegengewichts herstellen',
      evidence='HIGH_CONFIDENCE',
      pb='B03 – Maß nach TRBS 3121 Anh. 1 Nr. 2 (2,0 m über Grubensohle); 2,50 m über unterster Haltestelle gilt für Nachbaraufzüge (Nr. 3)'),
    r(no('qg_gg_fuellung'), 'HIGH', mfrom=('N20-S11', 'Gegengewichtsfüllung'), evidence='HIGH_CONFIDENCE'),
    r(no('qg_gg_fang'), 'HIGH', mfrom=('N20-S11', 'Betretbarer Raum'), evidence='HIGH_CONFIDENCE'),
    r(eq('qg_gg_abtrennung', 'mangelhaft'), 'MEDIUM', mfrom=('N20-S11', 'Abtrennung vorhanden'),
      sofort='Vor dem Betreten der Grube Not-Halt betätigen bzw. Anlage freischalten und gegen '
             'Wiedereinschalten sichern; Gefahrstelle am Gegengewicht kennzeichnen',
      evidence='HIGH_CONFIDENCE', pb='B03 – organisatorische Maßnahme nach TRBS 3121 Anh. 1 Nr. 2',
      notes='Regelprüfung 20.09.2026: Ein Warnhinweis schützt niemanden, der die Grube betreten muss, und „sichere '
            'Position einnehmen" ist ein Appell zur Vorsicht. Gesichert wird jetzt vor dem '
            'Betreten.')],
   sources=[en8120('5.2.5.5.1'), en8120('5.2.5.5.2'), trbs3121('Anh. 1 Nr. 2')], factor=F_BEWEGT,
   persons=[WARTUNG], agg='MAXIMUM', bereich='G')

hz('MF-G08', 'Fehlende Abtrennung zum Nachbaraufzug in der Schachtgrube', GRP_S,
   [('qa_mehrere_aufzuege', 'APPLICABILITY', 'NEVER'),
    ('qg_nachbar_abtrennung', 'TRIGGER', 'ALWAYS'),
    ('qg_nachbar_abschaltung', 'COMPENSATION', 'CONDITIONAL', {'required_when': no('qg_nachbar_abtrennung')}),
    ('qg_nachbar_abschaltung_geprueft', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': yes('qg_nachbar_abschaltung')})],
   [r(all_(no('qg_nachbar_abtrennung'), yes('qg_nachbar_abschaltung'), no('qg_nachbar_abschaltung_geprueft')),
      'HIGH', prio=210,
      sofort='Nachbaraufzug zusätzlich von Hand abschalten und gegen Wiedereinschalten sichern',
      mittel='Funktion der automatischen Abschaltung für alle Nachbaranlagen prüfen und dokumentieren',
      evidence='INFERRED',
      notes='Prüfbericht 20.09.2026: fail-closed – ohne Funktionsnachweis ist die automatische '
            'Abschaltung keine wirksame Kompensation und senkt die Stufe der fehlenden '
            'Abtrennung nicht (vorher Mittel).',
      pb='Prüfbericht 16.09.2026 – Abschaltung ohne Funktionsnachweis'),
    r(all_(no('qg_nachbar_abtrennung'), yes('qg_nachbar_abschaltung'), yes('qg_nachbar_abschaltung_geprueft')),
      'NO_RISK', prio=200,
      evidence='HIGH_CONFIDENCE',
      notes='TRBS 3121 Anh. 1 Nr. 3 b): automatische Abschaltung des Nachbaraufzugs ist gleichwertige Alternative.',
      pb='H03 – neu: Alternative automatische Abschaltung'),
    r(no('qg_nachbar_abtrennung'), 'HIGH', mfrom=('N20-S2.2', 'Keine Absperrung'),
      sofort='Vor Betreten der Schachtgrube den Nachbaraufzug abschalten und gegen Wiedereinschalten sichern',
      mittel='Abtrennung von höchstens 0,30 m über dem Grubenboden bis 2,50 m über dem Niveau der untersten '
             'Haltestelle nachrüsten oder automatische Abschaltung des Nachbaraufzugs vorsehen',
      evidence='HIGH_CONFIDENCE', pb='H03 – Maßnahme benennt den Nachbaraufzug und die Alternativen')],
   sources=[en8120('5.2.5.5.2.1'), trbs3121('Anh. 1 Nr. 3')], factor=F_BEWEGT, persons=[WARTUNG],
   bereich='G')
