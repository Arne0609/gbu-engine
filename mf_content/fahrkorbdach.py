# -*- coding: utf-8 -*-
"""F – Fahrkorbdach und Schachtkopf (Blaupause: Schindler M009, M023, M028,
M030, M031, M034, M045, M049, M050; Inhalte aus App-Kategorien F1–F3, F5–F9)."""
from .common import *

GRP_F = 'Fahrkorbdach und Schachtkopf'
GRP_NOT = 'Notruf und Personenbefreiung'
GRP_BEL = 'Beleuchtung'
GRP_SK = 'Sicherheitskomponenten'

# ---- Fragen ----------------------------------------------------------------
# Schwellenfragen 9.1/9.3: erhebung.py (SCHWELLEN) stellt sie im Seed auf Bereichsauswahl um;
# Regeln hier weiter als Zahlvergleich schreiben (stabile Regel-IDs).
num('qf_spalt_mm', 'Größter horizontaler Abstand zwischen Fahrkorbdachkante und '
    'Schachtwand [mm]', min=0, max=3000, ui='9.1')
yn('qf_gelaender', 'Geländer auf dem Fahrkorbdach vorhanden?', ui='9.2',
   visible_when=gt('qf_spalt_mm', 300))
num('qf_gelaender_hoehe_mm', 'Geländerhöhe [mm]', min=0, max=2000, ui='9.3', visible_when=yes('qf_gelaender'))
yn('qf_fussleiste', 'Fußleiste (mind. 100 mm) am Rand des Fahrkorbdachs vorhanden?', ui='9.4')
yn('qf_einzugstellen', 'Einzugstellen im Schachtkopf / auf dem Fahrkorbdach vorhanden '
   '(Umlenkrollen, Heberrolle, Seilrollen)?', ui='9.5')
sel('qf_einzug_abdeckung', 'Abdeckung der Einzugstellen', ui='9.5a',
    options=[('komplett', 'Komplett abgedeckt'),
             ('teilweise', 'Teilweise abgedeckt'),
             ('offen', 'Einzugstellen offen')],
    visible_when=yes('qf_einzugstellen'))
sel('qf_nachbar_trennung', 'Abtrennung zum Nachbaraufzug / Nachbar-Gegengewicht im '
    'Bereich des Fahrkorbdachs', ui='9.6',
    options=[('abgedeckt', 'Gefahrstellen komplett abgedeckt'),
             ('engmaschig', 'Engmaschiges Trenngitter'),
             ('abstand', 'Ausreichende Abstände (kein Erreichen möglich)'),
             ('teilweise', 'Teilweise Abdeckungen'),
             ('grobmaschig', 'Grobmaschiges Trenngitter oder Spanndrähte'),
             ('fehlt', 'Keine Abdeckung / kein Trenngitter')],
    visible_when=yes('qa_mehrere_aufzuege'))
yn('qf_nachbar_abschaltung', 'Einrichtung zum automatischen Abschalten des Nachbaraufzugs bei '
   'Arbeiten im Fahrschacht vorhanden?', ui='9.6a',
   visible_when=in_('qf_nachbar_trennung', ['fehlt', 'teilweise', 'grobmaschig']))
yn('qf_nachbar_abschaltung_geprueft', 'Automatische Abschaltung in der Funktion geprüft, alle '
   'Nachbaranlagen erfasst und Wirkung bei Inspektionsbetrieb bestätigt?', ui='9.6b',
   visible_when=yes('qf_nachbar_abschaltung'))
sel('qf_schutzraum', 'Schutzraum im Schachtkopf', ui='9.7',
    options=[('normgerecht', 'Schutzraum nach EN 81-20 vorhanden (Abmessungen eingehalten)'),
             ('altnorm', 'Schutzraum nach TRA 200 / EN 81-1/-2 (kleiner als EN 81-20)'),
             ('reduziert', 'Reduzierter Schachtkopf mit wirksamer Zusatzeinrichtung und '
                           'Betriebsanweisung'),
             ('nicht', 'Schutzraum nicht gegeben (z. B. nachträgliche Einbauten)')])
yn('qf_kopffreiheit_gekennz', 'Warnkennzeichnung zur reduzierten Kopffreiheit vorhanden?',
   ui='9.7a', visible_when=eq('qf_schutzraum', 'reduziert'))
yn('qf_inspektion', 'Inspektionssteuerung auf dem Fahrkorbdach vorhanden?', ui='9.8')
yn('qf_inspektion_schutz', 'Inspektionssteuerung gegen unbeabsichtigtes Betätigen geschützt?',
   ui='9.8a', visible_when=yes('qf_inspektion'))
yn('qf_inspektion_erreichbar', 'Inspektionssteuerung vom Zugang aus gut erreichbar?',
   ui='9.8b', visible_when=yes('qf_inspektion'))
yn('qf_inspektion_geschw', 'Inspektionsgeschwindigkeit max. 0,63 m/s?', ui='9.8c',
   visible_when=yes('qf_inspektion'))
yn('qf_nothalt', 'Notbremsschalter (Not-Halt) auf dem Fahrkorbdach vorhanden?', ui='9.9')
yn('qf_nothalt_erreichbar', 'Not-Halt vom Zugang aus erreichbar?', ui='9.9a',
   visible_when=yes('qf_nothalt'))
yn('qf_nothalt_wirksam', 'Not-Halt wirksam (Funktion geprüft)?', ui='9.9b',
   visible_when=yes('qf_nothalt'))
yn('qf_dach_tragfaehig', 'Fahrkorbdach tragfähig (200 kg auf 0,30 m × 0,30 m)?', ui='9.10')
yn('qf_klappe', 'Klappe / Notausstieg im Fahrkorbdach vorhanden?', ui='9.11')
yn('qf_klappe_ueberwacht', 'Klappe elektrisch überwacht (Sicherheitskreis)?', ui='9.11a',
   visible_when=yes('qf_klappe'))
yn('qf_notbeleuchtung', 'Notbeleuchtung auf dem Fahrkorbdach (mind. 5 Lux, 1 h) vorhanden?',
   ui='9.12')
yn('qf_notruf_dach', 'Eindeutig erkennbarer Auslöser für den (Fern-)Notruf auf dem '
   'Fahrkorbdach vorhanden?', ui='9.13')

# ---- Klärungen -------------------------------------------------------------
k('K-F01', 'Fahrkorbdach', 'Geländerhöhe bei großem Spalt',
  'Spalt > 850 mm und Geländer unter 1.100 mm: Hoch (eigene Regel) – App F1 nennt nur '
  '„Geländerhöhe 70 cm bei Spalt > 50 ≤ 85 cm = Mittel"?', 'Hoch', 'Mittel',
  'Lücke im App-Katalog; nach EN 81-20 5.4.7.4 ist ab 850 mm ein Geländer 1.100 mm gefordert.')
k('K-F02', 'Fahrkorbdach', 'Absturz gesamt',
  'Schindler bewertet die Absturzsicherung auf dem Fahrkorbdach (M028) im Worst Case nur '
  'mit Niedrig, der App-Katalog mit Hoch. Bleibt es bei Hoch?', 'Hoch (App F1)',
  'Niedrig (Schindler M028)', 'Deutliche Abweichung.')
k('K-F03', 'Fahrkorbdach', 'Reduzierter Schachtkopf',
  'Reduzierter Schachtkopf mit wirksamer Zusatzeinrichtung: Mittel (App F8) oder Kein '
  'Risiko (App F5 „Flacher Schachtkopf, aber Schutzraum durch temporäre Maßnahme gegeben")?',
  'Mittel', 'Kein Risiko', 'Die App-Kategorien F5 und F8 widersprechen sich.')
k('K-F04', 'Fahrkorbdach', 'Notbeleuchtung auf dem Dach',
  'Fehlende Notbeleuchtung auf dem Fahrkorbdach: Mittel (eigener Vorschlag) oder Hoch '
  '(Schindler M023 gemeinsam mit Fahrkorb)?', 'Mittel', 'Hoch',
  'Im App-Katalog nicht als eigene Option enthalten.')

k('K-F05', 'Fahrkorbdach', 'Schutzraum nach Altnorm (TRBS-Matrix)',
  'Neue Option „Schutzraum nach TRA 200 / EN 81-1/-2 (kleiner als EN 81-20)" für Schachtkopf und '
  'Grube: TRBS 3121 Anh. 1 Nr. 5 nennt das Risiko dafür niedrig. Umgesetzt: Niedrig statt Kein Risiko.',
  'Niedrig (TRBS-explizit)', 'Kein Risiko / Option nicht aufnehmen', 'Neu aus der TRBS-Risikomatrix vom 02.09.2026.')
# ---- Gefährdungen ----------------------------------------------------------
hz('MF-F01', 'Fehlende oder unzureichende Absturzsicherung auf dem Fahrkorbdach', GRP_F,
   [('qf_spalt_mm', 'TRIGGER', 'ALWAYS'),
    ('qf_gelaender', 'COMPENSATION', 'CONDITIONAL', {'required_when': gt('qf_spalt_mm', 300)}),
    ('qf_gelaender_hoehe_mm', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes('qf_gelaender')}),
    ('qf_fussleiste', 'TRIGGER', 'ALWAYS')],
   [r(all_(gt('qf_spalt_mm', 300), no('qf_gelaender')), 'HIGH',
      mfrom=('N20-F1', 'Kein oder Geländer'), evidence='HIGH_CONFIDENCE', klaerung='K-F02'),
    r(all_(gt('qf_spalt_mm', 300), yes('qf_gelaender'), lt('qf_gelaender_hoehe_mm', 700)), 'HIGH',
      mfrom=('N20-F1', 'Kein oder Geländer'), evidence='HIGH_CONFIDENCE'),
    r(all_(gt('qf_spalt_mm', 850), yes('qf_gelaender'), lt('qf_gelaender_hoehe_mm', 1100)), 'HIGH',
      mfrom=('N20-F1', 'Kein oder Geländer'), evidence='HYPOTHESIS', klaerung='K-F01'),
    r(all_(gt('qf_spalt_mm', 500), lte('qf_spalt_mm', 850), yes('qf_gelaender'),
           lt('qf_gelaender_hoehe_mm', 1100)), 'MEDIUM',
      mfrom=('N20-F1', 'Geländerhöhe 70 cm bei'), evidence='HIGH_CONFIDENCE',
      notes='Prüfbericht 20.09.2026: auf 501–850 mm begrenzt; darüber gilt MF-F01-R3 (Hoch), '
            'beide Regeln trafen bisher gemeinsam zu.'),
    r(all_(no('qf_fussleiste'), gt('qf_spalt_mm', 300)), 'MEDIUM',
      mfrom=('N20-F1', 'Fußleiste'),
      sofort='Dachrand kennzeichnen, keine losen Teile und Werkzeuge im Randbereich '
             'ablegen; auf dem Dach nur innerhalb der Umwehrung arbeiten; Betreiber '
             'unterrichten',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Die Frage 9.4 wird immer gestellt, die Regel griff dadurch auch bei einem '
            'Spalt bis 300 mm, wo weder EN 81-20 noch EN 81-1 eine Umwehrung und damit auch '
            'keine Fußleiste fordern. Bedingung an denselben Spalt gebunden wie die '
            'Umwehrung selbst. Sofortmaßnahme: „Mit dem Fuß nicht über den Rand treten" war '
            'eine Ermahnung, keine Maßnahme.')],
   sources=[en8120('5.4.7.3'), en8120('5.4.7.4'), trbs3121('Anh. 1 Nr. 15')],
   factor=F_ABSTURZ_SCHACHT, persons=[WARTUNG], agg='MAXIMUM', bereich='F')

hz('MF-F02', 'Einzugsgefahr an Rollen im Schachtkopf / auf dem Fahrkorbdach', GRP_F,
   [('qf_einzugstellen', 'TRIGGER', 'ALWAYS'),
    ('qf_einzug_abdeckung', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qf_einzugstellen')})],
   [r(eq('qf_einzug_abdeckung', 'offen'), 'HIGH', mfrom=('N20-F2', 'Einzugsstellen offen'),
      sofort='Arbeiten im Bereich der Einzugstellen nur bei stillgesetzter und gegen Wiederanlauf '
             'gesicherter Anlage; keine Fahrt mit Personen auf dem Fahrkorbdach',
      evidence='HIGH_CONFIDENCE', pb='B11 – Sofortmaßnahme wirksam gemacht'),
    r(eq('qf_einzug_abdeckung', 'teilweise'), 'MEDIUM', mfrom=('N20-F2', 'Teilweise'),
      sofort='Offene Einzugstellen vor Arbeiten ermitteln; dort nur bei stillgesetzter Anlage arbeiten',
      evidence='HIGH_CONFIDENCE', pb='B11 – Sofortmaßnahme wirksam gemacht')],
   sources=[en8120('5.5.7'), trbs3121('Anh. 1 Nr. 20')], factor=F_ROTIEREND, persons=[WARTUNG],
   agg='MAXIMUM', bereich='F')

hz('MF-F03', 'Gefährdung durch Nachbaraufzug oder dessen Gegengewicht (Fahrkorbdach)', GRP_F,
   [('qa_mehrere_aufzuege', 'APPLICABILITY', 'NEVER'),
    ('qf_nachbar_trennung', 'TRIGGER', 'ALWAYS'),
    ('qf_nachbar_abschaltung', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': in_('qf_nachbar_trennung', ['fehlt', 'teilweise', 'grobmaschig'])}),
    ('qf_nachbar_abschaltung_geprueft', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': yes('qf_nachbar_abschaltung')})],
   [r(all_(eq('qf_nachbar_trennung', 'fehlt'),
           yes('qf_nachbar_abschaltung'), no('qf_nachbar_abschaltung_geprueft')), 'HIGH', prio=212,
      sofort='Nachbaraufzug zusätzlich von Hand abschalten und gegen Wiedereinschalten sichern',
      mittel='Trenngitter über die volle Schachthöhe nachrüsten oder Abstand über 0,5 m zu '
             'beweglichen Teilen des Nachbaraufzugs herstellen; alternativ Funktion der '
             'automatischen Abschaltung für alle Nachbaranlagen nachweisen und dokumentieren',
      evidence='INFERRED',
      notes='Prüfbericht 20.09.2026: fail-closed – ohne Funktionsnachweis senkt die automatische '
            'Abschaltung die Stufe nicht (vorher Mittel trotz fehlender Abtrennung). '
            'Regelprüfung 20.09.2026: Die Regel verdrängt mit P212 die Grundregel R4 und damit deren technische '
            'Maßnahme; die Ursache – gar keine Abtrennung – muss in der Maßnahme stehen '
            'bleiben (TOP-Prinzip).',
      pb='Prüfbericht 16.09.2026 – Abschaltung ohne Funktionsnachweis'),
    r(all_(in_('qf_nachbar_trennung', ['teilweise', 'grobmaschig']),
           yes('qf_nachbar_abschaltung'), no('qf_nachbar_abschaltung_geprueft')), 'MEDIUM', prio=210,
      sofort='Nachbaraufzug zusätzlich von Hand abschalten und gegen Wiedereinschalten sichern',
      mittel='Abdeckung vervollständigen bzw. engmaschiges Trenngitter nachrüsten; alternativ '
             'Funktion der automatischen Abschaltung für alle Nachbaranlagen nachweisen und '
             'dokumentieren',
      evidence='INFERRED',
      notes='Teilabdeckung bzw. grobmaschiges Gitter: die Grundstufe bleibt Mittel, der fehlende '
            'Funktionsnachweis senkt sie aber nicht. Regelprüfung 20.09.2026: Die Regel verdrängt mit P210 die '
            'Grundregeln R5/R6 und damit deren technische Maßnahme – die unzureichende '
            'Abtrennung muss benannt bleiben (TOP-Prinzip).',
      pb='Prüfbericht 16.09.2026 – Abschaltung ohne Funktionsnachweis'),
    r(all_(in_('qf_nachbar_trennung', ['fehlt', 'teilweise', 'grobmaschig']),
           yes('qf_nachbar_abschaltung'), yes('qf_nachbar_abschaltung_geprueft')), 'NO_RISK', prio=200,
      evidence='HIGH_CONFIDENCE',
      notes='TRBS 3121 Anh. 1 Nr. 4 c): automatische Abschaltung des Nachbaraufzugs ist gleichwertige Alternative.',
      pb='H03 – neu: Alternative automatische Abschaltung'),
    r(eq('qf_nachbar_trennung', 'fehlt'), 'HIGH', mfrom=('N20-F3', 'Fehlendes Trenngitter'),
      sofort='Vor Arbeiten auf dem Fahrkorbdach den Nachbaraufzug abschalten und gegen '
             'Wiedereinschalten sichern',
      mittel='Trenngitter über die volle Schachthöhe nachrüsten, Umwehrung mit mehr als 0,5 m Abstand '
             'zu beweglichen Teilen herstellen oder automatische Abschaltung des Nachbaraufzugs vorsehen',
      evidence='HIGH_CONFIDENCE', pb='H03 – Maßnahme benennt den Nachbaraufzug und die Alternativen'),
    r(eq('qf_nachbar_trennung', 'teilweise'), 'MEDIUM', mfrom=('N20-F3', 'Teilweise'),
      sofort='Vor Arbeiten im Bereich der offenen Stellen den Nachbaraufzug abschalten und sichern',
      evidence='HIGH_CONFIDENCE', pb='H03 – Sofortmaßnahme benennt den Nachbaraufzug'),
    r(eq('qf_nachbar_trennung', 'grobmaschig'), 'MEDIUM', mfrom=('N20-F3', 'Grobmaschiges'),
      sofort='Vor Arbeiten im Bereich des Trenngitters den Nachbaraufzug abschalten und sichern',
      evidence='HIGH_CONFIDENCE', pb='H03 – Sofortmaßnahme benennt den Nachbaraufzug')],
   sources=[en8120('5.2.5.5.2.2'), trbs3121('Anh. 1 Nr. 4')], factor=F_BEWEGT, persons=[WARTUNG],
   bereich='F')

hz('MF-F04', 'Unzureichender Schutzraum / Kopffreiheit im Schachtkopf', GRP_F,
   [('qf_schutzraum', 'TRIGGER', 'ALWAYS'),
    ('qf_kopffreiheit_gekennz', 'TRIGGER', 'CONDITIONAL', {'required_when': eq('qf_schutzraum', 'reduziert')})],
   [r(eq('qf_schutzraum', 'nicht'), 'HIGH', mfrom=('N20-F8', 'Schutzraum nicht mehr'),
      evidence='HIGH_CONFIDENCE'),
    r(all_(eq('qf_schutzraum', 'reduziert'), no('qf_kopffreiheit_gekennz')), 'MEDIUM',
      mfrom=('N20-F8', 'Kopffreiheit'), evidence='HIGH_CONFIDENCE',
      pb='H15 – Hoch auf Mittel: Schutzeinrichtung wirkt, es fehlt die Kennzeichnung'),
    r(eq('qf_schutzraum', 'altnorm'), 'LOW',
      sofort='Zustand dokumentieren, Beschäftigte über den reduzierten Schutzraum unterweisen',
      mittel='Bei Modernisierung Schutzräume nach EN 81-20 herstellen oder Schutzeinrichtung für temporären Schutzraum vorsehen',
      evidence='INFERRED', klaerung='K-F05',
      notes='TRBS 3121 Anh. 1 Nr. 5: Risiko niedrig bei Schutzräumen nach TRA 200 oder EN 81-1/-2.'),
    r(eq('qf_schutzraum', 'reduziert'), 'NO_RISK', evidence='HIGH_CONFIDENCE', klaerung='K-F03',
      notes='Entscheidung 02.09.2026: reduzierter Schachtkopf mit wirksamer Zusatzeinrichtung = kein Risiko (App F5).')],
   sources=[en8120('5.2.5.7'), en8120('5.2.5.8'), trbs3121('Anh. 1 Nr. 18')],
   factor=F_QUETSCH, persons=[WARTUNG], agg='MAXIMUM', bereich='F')

hz('MF-F05', 'Fehlende oder unzulängliche Inspektionssteuerung auf dem Fahrkorbdach', GRP_SK,
   [('qf_inspektion', 'TRIGGER', 'ALWAYS'),
    ('qf_inspektion_schutz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qf_inspektion')}),
    ('qf_inspektion_erreichbar', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qf_inspektion')}),
    ('qf_inspektion_geschw', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qf_inspektion')})],
   [r(no('qf_inspektion'), 'HIGH', mfrom=('N20-F6', 'Keine Inspektionssteuerung'),
      sofort='Fahrkorbdach nur nach Freischalten der Anlage und Sichern gegen '
             'Wiedereinschalten betreten; keine Fahrt mit Personen auf dem Fahrkorbdach; '
             'Betreiber unterrichten; keine Alleinarbeit (DGUV Information 209-053)',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Ohne Inspektionssteuerung fährt der Aufzug im Normalbetrieb mit '
            'Nenngeschwindigkeit, während Personen auf dem Dach stehen. Das Verbot der '
            'Alleinarbeit und ein Literaturhinweis verhindern diese Fahrt nicht – die '
            'Sofortmaßnahme setzt jetzt am Freischalten an.'),
    r(no('qf_inspektion_geschw'), 'HIGH', mfrom=('N20-F5', 'Inspektionsgeschwindigkeit'),
      sofort='Keine Inspektionsfahrten mit Personen auf dem Fahrkorbdach bis zur Begrenzung der '
             'Geschwindigkeit; Arbeiten nur bei stillgesetzter Anlage',
      evidence='HIGH_CONFIDENCE', pb='B11 – „nur abwärts" ist keine wirksame Maßnahme'),
    r(no('qf_inspektion_schutz'), 'MEDIUM', mfrom=('N20-F6', 'Kein Schutz'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qf_inspektion_erreichbar'), 'MEDIUM', mfrom=('N20-F6', 'Inspektionssteuerung vorhanden, aber'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.12.1.5.1.1'), en8120('5.12.1.5.2')], factor=F_BEFEHL, persons=[WARTUNG],
   agg='MAXIMUM', bereich='F')

hz('MF-F06', 'Fehlender oder unwirksamer Not-Halt auf dem Fahrkorbdach', GRP_SK,
   [('qf_nothalt', 'TRIGGER', 'ALWAYS'),
    ('qf_nothalt_erreichbar', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qf_nothalt')}),
    ('qf_nothalt_wirksam', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qf_nothalt')})],
   [r(no('qf_nothalt'), 'HIGH', mfrom=('N20-F7', 'Kein Notbremsschalter'), evidence='HIGH_CONFIDENCE'),
    r(no('qf_nothalt_wirksam'), 'HIGH', mfrom=('N20-F7', 'Notbremsschalter ohne'), evidence='HIGH_CONFIDENCE'),
    r(no('qf_nothalt_erreichbar'), 'MEDIUM', mfrom=('N20-F7', 'Notbremsschalter vorhanden, aber'),
      sofort='Fahrkorbdach erst betreten, nachdem die Anlage stillgesetzt und gegen '
             'Wiedereinschalten gesichert ist; Lage des Not-Halt vor dem Betreten '
             'feststellen und den Beschäftigten bekannt machen; Betreiber unterrichten',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: „Position vor dem Betreten prüfen" benennt keine Handlung, die die '
            'Gefährdung begrenzt.')],
   sources=[en8120('5.4.8'), en8120('5.12.1.11')], factor=F_BEFEHL, persons=[WARTUNG],
   agg='MAXIMUM', bereich='F')

hz('MF-F07', 'Nicht tragfähiges Fahrkorbdach oder unüberwachte Dachklappe', GRP_F,
   [('qf_dach_tragfaehig', 'TRIGGER', 'ALWAYS'),
    ('qf_klappe', 'TRIGGER', 'ALWAYS'),
    ('qf_klappe_ueberwacht', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qf_klappe')}),
    ('qa_norm_inverkehrbringen', 'DOCUMENTATION', 'NEVER')],
   [r(no('qf_dach_tragfaehig'), 'HIGH', mfrom=('N20-F9', 'Fahrkorbdach nicht tragfähig'),
      sofort='Fahrkorbdach nicht betreten, bis die Tragfähigkeit hergestellt oder nachgewiesen ist; '
             'Warnhinweis am Zugang anbringen',
      mittel='Tragfähiges Fahrkorbdach herstellen (200 kg auf 0,30 m × 0,30 m, DIN EN 81-20 5.4.7.1) '
             'und nachweisen',
      evidence='HIGH_CONFIDENCE', pb='B11 – widersprüchliche Sofortmaßnahme bereinigt'),
    r(no('qf_klappe_ueberwacht'), 'MEDIUM', mfrom=('N20-F9', 'Klappe im Fahrkorbdach'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.4.7.1'), en8120('5.4.6.2')], factor=F_ABSTURZ_SCHACHT, persons=[WARTUNG],
   agg='MAXIMUM', bereich='F')

hz('MF-F08', 'Fehlende Notbeleuchtung auf dem Fahrkorbdach', GRP_BEL,
   [('qf_notbeleuchtung', 'TRIGGER', 'ALWAYS')],
   [r(no('qf_notbeleuchtung'), 'HIGH',
      sofort='Handleuchte für Arbeiten auf dem Fahrkorbdach mitführen',
      mittel='Notbeleuchtung (mind. 5 Lux, 1 h) auf dem Fahrkorbdach nachrüsten',
      evidence='HYPOTHESIS', klaerung='K-F04')],
   sources=[en8120('5.4.10.4')], factor=F_BELEUCHTUNG, persons=[WARTUNG], bereich='F')

hz('MF-F09', 'Fehlender Notruf auf dem Fahrkorbdach', GRP_NOT,
   [('qf_notruf_dach', 'TRIGGER', 'ALWAYS')],
   [r(no('qf_notruf_dach'), 'MEDIUM', mfrom=('N20-K12', 'Keine Notrufverbindung vom FK-Dach'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.12.3.2'), trbs3121('Anh. 1 Nr. 7')], factor=F_NOTFALL, persons=[WARTUNG],
   bereich='F')
