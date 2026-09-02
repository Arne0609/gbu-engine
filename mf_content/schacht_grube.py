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
yn('qs_bel_ausreichend', 'Schachtbeleuchtung ausreichend (mind. 20 Lux, auch auf dem '
   'Fahrkorbdach)?', ui='10.1a', visible_when=yes('qs_bel_vorhanden'))
yn('qs_bel_splitterschutz', 'Leuchten im Schacht mit Splitterschutz und an geeigneter Stelle?',
   ui='10.1b', visible_when=yes('qs_bel_vorhanden'))
yn('qs_zugang_bel', 'Beleuchtung an den Schachtzugängen (Haltestellen) mind. 75 Lux?',
   ui='10.2')
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
yn('qs_schlaffseil', 'Schlaffseil-/Schlaffkettensicherung vorhanden?', ui='10.11',
   visible_when=eq('qa_aufzugsart', 'trommel'))
yn('qs_fremd_frei', 'Schacht frei von aufzugsfremden Einrichtungen?', ui='10.12')
yn('qs_fremd_fachgerecht', 'Aufzugsfremde Leitungen fachgerecht verlegt und gekennzeichnet?',
   ui='10.12a', visible_when=no('qs_fremd_frei'))
yn('qs_fremd_behindert', 'Behindern aufzugsfremde Einrichtungen Arbeiten oder Rettungswege '
   'im Schacht?', ui='10.12b', visible_when=no('qs_fremd_frei'))
yn('qs_zugang_schacht_sicher', 'Zugänge zum Schacht (Schachttüren, Inspektionstüren) und '
   'die zugehörigen Schalteinrichtungen frei und sicher begehbar?', ui='10.13')

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
sel('qg_leiter', 'Grubenleiter', ui='11.6',
    options=[('fest', 'Fest installierte Grubenleiter'),
             ('mobil_schacht', 'Mobile Leiter im Schacht deponiert'),
             ('schwer', 'Grubenleiter vorhanden, aber schwer erreichbar'),
             ('kunde', 'Leiter beim Kunden deponiert'),
             ('fahrzeug', 'Leiter wird im Kundendienstfahrzeug mitgeführt'),
             ('keine', 'Keine Grubenleiter')])
yn('qg_zugangstuer', 'Separate Grubenzugangstür vorhanden?', ui='11.7')
yn('qg_zugangstuer_schalter', 'Elektrische Sicherheitseinrichtung an der Grubenzugangstür?',
   ui='11.7a', visible_when=yes('qg_zugangstuer'))
yn('qg_selbstbefreiung', 'Selbstbefreiung aus der Grube über die Schachttür möglich '
   '(Verschluss innerhalb 1,80 m Höhe / 0,80 m horizontal)?', ui='11.8')
yn('qg_notruf', 'Notrufeinrichtung in der Schachtgrube vorhanden?', ui='11.9')
yn('qg_puffer', 'Puffer für Fahrkorb und Gegengewicht vorhanden?', ui='11.10')
yn('qg_puffer_zustand', 'Puffer unbeschädigt und nicht verschlissen?', ui='11.10a',
   visible_when=yes('qg_puffer'))
sel('qg_puffer_art', 'Bauart der Puffer', ui='11.10b',
    options=[('speichernd', 'Energiespeichernd (Feder / Polyurethan)'),
             ('verzehrend', 'Energieverzehrend (hydraulisch)')],
    visible_when=yes('qg_puffer'))
yn('qg_puffer_oelstand', 'Ölstand hydraulischer Puffer prüfbar und Kennzeichnung vorhanden?',
   ui='11.10c', visible_when=eq('qg_puffer_art', 'verzehrend'))
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
yn('qg_wasser', 'Wasser oder Feuchtigkeit in der Schachtgrube?', ui='11.15')
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
    ('qs_bel_splitterschutz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qs_bel_vorhanden')})],
   [r(no('qs_bel_vorhanden'), 'HIGH', mfrom=('N20-S1', 'Keine Beleuchtung'), evidence='HIGH_CONFIDENCE'),
    r(no('qs_bel_ausreichend'), 'MEDIUM', mfrom=('N20-S1', 'Dunkle'), evidence='HIGH_CONFIDENCE'),
    r(no('qs_bel_splitterschutz'), 'MEDIUM', mfrom=('N20-S1', 'Leuchten ohne'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.1.4.1'), trbs3121('Anh. 1 Nr. 8')], factor=F_BELEUCHTUNG,
   persons=[WARTUNG], agg='MAXIMUM', bereich='S')

hz('MF-S02', 'Unzureichende Beleuchtung an den Schachtzugängen', GRP_BEL,
   [('qs_zugang_bel', 'TRIGGER', 'ALWAYS')],
   [r(no('qs_zugang_bel'), 'MEDIUM',
      sofort='Betreiber auf die Beleuchtung der Haltestellen hinweisen',
      mittel='Beleuchtung an den Schachtzugängen auf mind. 75 Lux (Boden) herstellen',
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
    r(no('qs_glas_vsg'), 'MEDIUM', mfrom=('N20-S6', 'Verglasung'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.5'), en8120('5.2.5.2.3')], factor=F_ABSTURZ_SCHACHT,
   persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='S')

hz('MF-S04', 'Führungsschienen nicht aus Stahl', GRP_S,
   [('qs_schienen_stahl', 'TRIGGER', 'ALWAYS')],
   [r(no('qs_schienen_stahl'), 'MEDIUM',
      sofort='Zustand der Führungsschienen bei jeder Wartung prüfen',
      mittel='Bei Modernisierung Führungsschienen aus Stahl nach EN 81-20 5.7 vorsehen',
      evidence='INFERRED')],
   sources=[en8120('5.7.1')], factor=F_KINETISCH, persons=[NUTZER], bereich='S')

hz('MF-S05', 'Fehlende oder ungeprüfte Fangvorrichtung, Geschwindigkeitsbegrenzer oder '
   'Schlaffseilsicherung', GRP_SK,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': SEIL}),
    ('qs_fang', 'TRIGGER', 'ALWAYS'),
    ('qs_begrenzer', 'TRIGGER', 'ALWAYS'),
    ('qs_fang_geprueft', 'TRIGGER', 'CONDITIONAL', {'required_when': all_(yes('qs_fang'), yes('qs_begrenzer'))}),
    ('qs_spanngewicht_schalter', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qs_begrenzer')}),
    ('qs_schlaffseil', 'TRIGGER', 'CONDITIONAL', {'required_when': eq('qa_aufzugsart', 'trommel')})],
   [r(no('qs_fang'), 'HIGH', mfrom=('N20-S10', 'Keine Fangvorrichtung'), evidence='HIGH_CONFIDENCE'),
    r(no('qs_begrenzer'), 'HIGH', mfrom=('N20-S10', 'Keine Fangvorrichtung'), evidence='HIGH_CONFIDENCE'),
    r(no('qs_schlaffseil'), 'HIGH', mfrom=('N20-S10', 'Keine Schlaffseil'), evidence='HIGH_CONFIDENCE'),
    r(no('qs_fang_geprueft'), 'MEDIUM', mfrom=('N20-S10', 'Prüfung von'), evidence='HIGH_CONFIDENCE'),
    r(no('qs_spanngewicht_schalter'), 'MEDIUM', mfrom=('N20-S10', 'Spanngewicht'), evidence='HIGH_CONFIDENCE')],
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
   [('qs_zugang_schacht_sicher', 'TRIGGER', 'ALWAYS')],
   [r(no('qs_zugang_schacht_sicher'), 'HIGH',
      sofort='Zugänge freiräumen, Hindernisse entfernen, Betreiber informieren',
      mittel='Freihaltung der Schachtzugänge und Schalteinrichtungen in der Betriebsanweisung '
             'festlegen und bei Betreiberkontrollen prüfen',
      evidence='INFERRED', notes='Blaupause Schindler M107 (f021 = Nein -> Hoch, DIRECT).')],
   sources=[en8120('5.2.2.1'), trbs3121('Anh. 1 Nr. 5')], factor=F_STURZ, persons=[BEAUFTRAGTE, WARTUNG],
   bereich='S')

# ---- Gefährdungen G --------------------------------------------------------
hz('MF-G01', 'Unzureichende Beleuchtung in der Schachtgrube', GRP_BEL,
   [('qg_bel_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qg_bel_50lux', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qg_bel_vorhanden')})],
   [r(no('qg_bel_vorhanden'), 'HIGH', mfrom=('N20-S1', 'Keine Beleuchtung'), evidence='HIGH_CONFIDENCE'),
    r(no('qg_bel_50lux'), 'MEDIUM', mfrom=('N20-S1', 'Leuchten an ungeeigneter'), evidence='HIGH_CONFIDENCE')],
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
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.1.5.1'), en8120('5.12.1.5.1.1')], factor=F_BEFEHL, persons=[WARTUNG],
   agg='MAXIMUM', bereich='G')

hz('MF-G04', 'Unsicherer Zugang zur Schachtgrube (Leiter, Grubenzugangstür)', GRP_Z,
   [('qg_leiter', 'TRIGGER', 'ALWAYS'),
    ('qg_zugangstuer', 'TRIGGER', 'ALWAYS'),
    ('qg_zugangstuer_schalter', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qg_zugangstuer')})],
   [r(eq('qg_leiter', 'keine'), 'HIGH', mfrom=('N20-S3', 'Keine Grubenleiter'), evidence='HIGH_CONFIDENCE'),
    r(no('qg_zugangstuer_schalter'), 'HIGH',
      sofort='Grubenzugangstür verschlossen halten, Zutritt nur mit Freischaltung der Anlage',
      mittel='Elektrische Sicherheitseinrichtung (Türkontakt im Sicherheitskreis) an der '
             'Grubenzugangstür nachrüsten', evidence='INFERRED',
      notes='Blaupause Schindler M008 (f069 = Ja, f070 = Nein -> Hoch, DIRECT).'),
    r(eq('qg_leiter', 'schwer'), 'MEDIUM', mfrom=('N20-S3', 'Grubenleiter schwer'), evidence='HIGH_CONFIDENCE'),
    r(eq('qg_leiter', 'kunde'), 'MEDIUM', mfrom=('N20-S3', 'Grubenleiter ist beim Kunden'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qg_leiter', 'fahrzeug'), 'HIGH', mfrom=('N20-S3', 'Grubenleiter wird'),
      evidence='HIGH_CONFIDENCE', klaerung='K-S02')],
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
    ('qa_nenngeschwindigkeit', 'MODIFIER', 'NEVER')],
   [r(no('qg_puffer'), 'HIGH', mfrom=('N20-S9', 'Puffer fehlen'), evidence='HIGH_CONFIDENCE'),
    r(no('qg_puffer_zustand'), 'HIGH', mfrom=('N20-S9', 'Puffer fehlen'), evidence='HIGH_CONFIDENCE'),
    r(all_(eq('qg_puffer_art', 'speichernd'), gt('qa_nenngeschwindigkeit', 1.0)), 'HIGH',
      mfrom=('N20-S9', 'Energiespeichernde'), evidence='HIGH_CONFIDENCE', klaerung='K-S04'),
    r(no('qg_puffer_oelstand'), 'MEDIUM', mfrom=('N20-S9', 'Ölstand'), evidence='HIGH_CONFIDENCE')],
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
   [r(eq('qg_gg_abtrennung', 'keine'), 'HIGH', mfrom=('N20-S11', 'Keine Abtrennung'), evidence='HIGH_CONFIDENCE'),
    r(no('qg_gg_fuellung'), 'HIGH', mfrom=('N20-S11', 'Gegengewichtsfüllung'), evidence='HIGH_CONFIDENCE'),
    r(no('qg_gg_fang'), 'HIGH', mfrom=('N20-S11', 'Betretbarer Raum'), evidence='HIGH_CONFIDENCE'),
    r(eq('qg_gg_abtrennung', 'mangelhaft'), 'MEDIUM', mfrom=('N20-S11', 'Abtrennung vorhanden'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.5.5.1'), en8120('5.2.5.5.2'), trbs3121('Anh. 1 Nr. 2')], factor=F_BEWEGT,
   persons=[WARTUNG], agg='MAXIMUM', bereich='G')

hz('MF-G08', 'Fehlende Abtrennung zum Nachbaraufzug in der Schachtgrube', GRP_S,
   [('qa_mehrere_aufzuege', 'APPLICABILITY', 'NEVER'),
    ('qg_nachbar_abtrennung', 'TRIGGER', 'ALWAYS')],
   [r(no('qg_nachbar_abtrennung'), 'HIGH', mfrom=('N20-S2.2', 'Keine Absperrung'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.5.5.2.1'), trbs3121('Anh. 1 Nr. 3')], factor=F_BEWEGT, persons=[WARTUNG],
   bereich='G')
