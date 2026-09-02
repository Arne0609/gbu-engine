# -*- coding: utf-8 -*-
"""M – Triebwerks-/Maschinenraum und Steuerung (Blaupause: Schindler M005, M006,
M015–M018, M020, M033, M042, M047, M048, M055, M056, M058, M071, M110, M112,
M116; Inhalte aus App-Kategorien M1–M3, M5–M15, K5, K18)."""
from .common import *

GRP_BEL = 'Beleuchtung'
GRP_EL = 'Steuerung und Elektrik'
GRP_MR = 'Triebwerksraum – Ausstattung'
GRP_ANT = 'Antrieb, Bremse und Hydraulik'
GRP_NOT = 'Notruf und Personenbefreiung'
GRP_DOC = 'Beschilderung und Unterlagen'

MR = yes('qa_maschinenraum')
SEIL = in_('qa_aufzugsart', ['seil', 'trommel', 'seil_hydraulik'])
HYDR = in_('qa_aufzugsart', ['hydraulik', 'seil_hydraulik'])

# ---- Fragen ----------------------------------------------------------------
yn('qm_bel_vorhanden', 'Beleuchtung im Triebwerks-/Maschinenraum vorhanden?', ui='5.20',
   visible_when=MR)
yn('qm_bel_200lux', 'Beleuchtungsstärke an den Arbeitsflächen (Antrieb, Steuerschrank) '
   'mind. 200 Lux, Leuchten funktionsfähig?', ui='5.21', visible_when=yes('qm_bel_vorhanden'))
yn('qm_bel_geeignet', 'Leuchten an geeigneter Stelle (Arbeitsflächen nicht abgeschattet)?',
   ui='5.22', visible_when=yes('qm_bel_vorhanden'))
yn('qm_bel_splitterschutz', 'Leuchten im Kopfbereich mit Splitterschutz / bruchsicher?',
   ui='5.23', visible_when=yes('qm_bel_vorhanden'))

yn('qm_beruehrungssicher', 'Alle spannungsführenden Teile berührungssicher '
   '(Abdeckungen vorhanden, Schaltschrank geschlossen)?', ui='5.30')
yn('qm_offene_schalttafel', 'Offene Schalttafel ohne Schaltschrank vorhanden?', ui='5.31',
   visible_when=no('qm_beruehrungssicher'))
yn('qm_offene_schalter', 'Offene Kontakte oder Schalter an Maschine, Kopierwerk oder '
   'Begrenzer?', ui='5.32', visible_when=no('qm_beruehrungssicher'))
yn('qm_schaltschrank_unsicher', 'Nicht berührungssichere Bauteile im Schaltschrank '
   '(bei geöffneter Tür erreichbar)?', ui='5.33', visible_when=no('qm_beruehrungssicher'))
yn('qm_kennz_kontakte', 'Warnkennzeichnung für offene elektrische Kontakte vorhanden?',
   ui='5.34', visible_when=no('qm_beruehrungssicher'))
yn('qm_dguv_v3', 'Nachweis der elektrischen Prüfung nach DGUV Vorschrift 3 vorhanden '
   '(Prüfplakette / Protokoll aktuell)?', ui='5.35')
yn('qm_bauseitig_ok', 'Bauseitige Elektroinstallation im Raum (Steckdosen, Schalter, '
   'Leitungen) unbeschädigt?', ui='5.36')
yn('qm_ortsfest_geprueft', 'Prüfung der ortsfesten elektrischen Anlage nachgewiesen?',
   ui='5.37')
yn('qm_potenzialausgleich', 'Hauptpotenzialausgleich an der Aufzugskonstruktion '
   'vorhanden?', ui='5.38')

yn('qm_einzug_treibscheibe', 'Einzugsschutz an Treibscheibe, Umlenkrollen und '
   'Kopierwerk vorhanden?', ui='5.40', visible_when=SEIL)
yn('qm_einzug_begrenzer', 'Einzugsschutz am Geschwindigkeitsbegrenzer vorhanden?',
   ui='5.41', visible_when=SEIL)
sel('qm_einzug_grad', 'Abdeckung der Einzugstellen insgesamt', ui='5.42',
    options=[('komplett', 'Komplett abgedeckt'),
             ('teilweise', 'Teilweise abgedeckt'),
             ('offen', 'Einzugstellen offen')], visible_when=SEIL)

yn('qm_hoehe_180', 'Lichte Höhe im Gehbereich mind. 1,80 m?', ui='5.43', visible_when=MR)
yn('qm_freiflaeche', 'Freifläche für Notbetrieb/Handrad mind. 0,50 m × 0,60 m vor dem '
   'Antrieb vorhanden?', ui='5.44', visible_when=MR)
yn('qm_lagerung', 'Bewegungsflächen durch Lagerung eingeengt?', ui='5.45', visible_when=MR)

yn('qm_niveau', 'Niveauunterschiede über 0,50 m im Raum vorhanden?', ui='5.46',
   visible_when=MR)
yn('qm_niveau_gesichert', 'Niveauunterschied durch Treppe oder Leiter überwindbar?',
   ui='5.46a', visible_when=yes('qm_niveau'))
yn('qm_podest_absturz', 'Podest mit Absturzhöhe über 1,00 m ohne Geländer?', ui='5.46b',
   visible_when=yes('qm_niveau'))
yn('qm_bodenoeffnung', 'Ungesicherte Bodenöffnung oder Vertiefung im Raum?', ui='5.47',
   visible_when=MR)

yn('qm_boden_rutschhemmend', 'Boden rutschhemmend und sauber?', ui='5.48', visible_when=MR)
yn('qm_boden_oelfest', 'Boden ölfest gestrichen und unbeschädigt?', ui='5.49',
   visible_when=MR)
yn('qm_oel_ausgetreten', 'Ausgetretenes Öl / Hydrauliköl ohne Auffangmöglichkeit?',
   ui='5.50')

yn('qm_hauptschalter', 'Hauptschalter vorhanden und Wirkung nachvollziehbar?', ui='5.51')
yn('qm_hauptschalter_abschliessbar', 'Hauptschalter abschließbar?', ui='5.51a',
   visible_when=yes('qm_hauptschalter'))
yn('qm_hauptschalter_gekennz', 'Hauptschalter eindeutig gekennzeichnet?', ui='5.51b',
   visible_when=yes('qm_hauptschalter'))

yn('qm_zweikreisbremse', 'Zweikreisbremse (redundante Betriebsbremse) vorhanden?',
   ui='6.2', visible_when=SEIL)
yn('qm_bremse_ueberwacht', 'Bremse elektrisch überwacht (Bremskontrollschalter)?',
   ui='6.2a', visible_when=yes('qm_zweikreisbremse'))
yn('qm_motorschutz', 'Schutz gegen Überhitzen des Antriebsmotors vorhanden?', ui='6.3')
yn('qm_schuetze_unabhaengig', 'Zwei unabhängige Fahrschütze / Abschaltwege vorhanden?',
   ui='6.4', visible_when=neq('qa_antrieb', 'hydraulisch'))
yn('qm_steuerung_selbstueberw', 'Bei nur einem Schütz: selbstüberwachende Steuerung '
   'mit Baumusterprüfung?', ui='6.4a', visible_when=no('qm_schuetze_unabhaengig'))
yn('qm_laufzeit', 'Motor-Laufzeitüberwachung vorhanden?', ui='6.5')
yn('qm_phasenumkehr', 'Schutz gegen Phasenumkehr / Phasenausfall vorhanden?', ui='6.6',
   visible_when=nin('qa_antrieb', ['geregelt', 'hydraulisch']))

yn('qm_absperrventil', 'Absperrventil am Hydraulikaggregat vorhanden?', ui='6.10',
   visible_when=HYDR)
yn('qm_absperrventil_gekennz', 'Absperrventil gekennzeichnet und gut zugänglich?',
   ui='6.10a', visible_when=yes('qm_absperrventil'))
yn('qm_rohrbruch', 'Rohrbruchsicherungsventil vorhanden?', ui='6.11', visible_when=HYDR)
yn('qm_kav', 'Einrichtung gegen Absinken (Kolbenabsinkverhinderung / '
   'Nachholsteuerung) vorhanden?', ui='6.12', visible_when=HYDR)
yn('qm_absinkt', 'Sinkt der Fahrkorb im Stillstand merklich ab?', ui='6.13',
   visible_when=HYDR)

yn('qm_anschlagpunkte', 'Anschlagpunkte / Hebezeuge zum Anheben schwerer Teile '
   'vorhanden?', ui='5.52', visible_when=MR)
yn('qm_tragfaehigkeit', 'Tragfähigkeit der Anschlagpunkte angegeben?', ui='5.52a',
   visible_when=yes('qm_anschlagpunkte'))
yn('qm_anschlag_geprueft', 'Prüfung der Anschlagpunkte dokumentiert?', ui='5.52b',
   visible_when=yes('qm_anschlagpunkte'))

yn('qm_notbetrieb', 'Einrichtung für Notbetrieb / Personenbefreiung vorhanden '
   '(Handrad, Bremslüfthebel, Evakuierungseinheit, Notablass)?', ui='5.53')
yn('qm_notbetrieb_gekennz', 'Notbetriebseinrichtung gekennzeichnet (Fahrtrichtung, '
   'Bündigmarken)?', ui='5.53a', visible_when=yes('qm_notbetrieb'))
yn('qm_personal_eingewiesen', 'Beauftragte Personen in die Personenbefreiung '
   'eingewiesen?', ui='5.53b')

yn('qm_kennz_elektrisch', 'Elektrische Einrichtungen gekennzeichnet (Zuordnung im '
   'Notfall möglich)?', ui='5.54')
sel('qm_stromlaufplan', 'Stromlaufplan / Schaltunterlagen', ui='5.55',
    options=[('aktuell', 'Vorhanden und aktuell'),
             ('unrichtig', 'Vorhanden, aber unrichtig oder unvollständig'),
             ('fehlt', 'Nicht vorhanden')])
yn('qm_beschilderung', 'Beschilderung vollständig (Schutzraum, Notablass, '
   'Entriegelungsschlüssel, Verhalten bei Personenbefreiung)?', ui='5.56')
sel('qm_betriebsanleitung', 'Betriebs-/Bedienungsanleitung der Anlage', ui='5.57',
    options=[('aktuell', 'Vorhanden und aktuell'),
             ('veraltet', 'Vorhanden, aber nicht aktuell oder unvollständig'),
             ('fehlt', 'Nicht vorhanden')])

sel('qm_sprechverbindung', 'Sprechverbindung zwischen Fahrkorb und '
    'Triebwerksraum/Steuerung', ui='5.58',
    options=[('ok', 'Vorhanden und funktionsfähig'),
             ('eingeschraenkt', 'Vorhanden, Verständigung nur eingeschränkt'),
             ('keine', 'Keine Sprechverbindung'),
             ('nicht_noetig', 'Verständigung ohne Hilfsmittel möglich (kurze Wege)')],
    visible_when=MR)

yn('qm_rollenraum_nothalt', 'Notbremsschalter im zusätzlichen Rollenraum vorhanden?',
   ui='5.24', visible_when=yes('qa_rollenraum'))

yn('qm_fremd_frei', 'Triebwerksraum frei von aufzugsfremden Einrichtungen '
   '(Lager, Leitungen, Geräte Dritter)?', ui='5.59', visible_when=MR)

# ---- Klärungen -------------------------------------------------------------
k('K-M01', 'Triebwerksraum', 'DGUV-V3-Nachweis',
  'Fehlender Nachweis der Prüfung nach DGUV Vorschrift 3: Hoch (wie App M1) oder '
  'Mittel (organisatorischer Mangel, kein unmittelbarer Schaden)?',
  'Hoch (App-Katalog M1)', 'Mittel', 'Rein organisatorischer Befund mit Stufe Hoch.')
k('K-M02', 'Triebwerksraum', 'Hauptschalter nicht abschließbar',
  'Hauptschalter vorhanden, aber nicht abschließbar: Mittel (App M9) oder Hoch (App M5)?',
  'Mittel (M9 ist die neuere Kategorie)', 'Hoch (M5)',
  'Die beiden App-Kategorien M5 und M9 widersprechen sich.')
k('K-M03', 'Antrieb', 'Motorschutz',
  'Fehlender Schutz gegen Überhitzen des Antriebs: Hoch (App M10) oder Mittel '
  '(Schindler M006)?', 'Hoch (App)', 'Mittel (Schindler)', 'Abweichung App/Schindler.')
k('K-M04', 'Antrieb', 'Ein Fahrschütz mit selbstüberwachender Steuerung',
  'Nur ein Fahrschütz, aber selbstüberwachende Steuerung mit Baumusterprüfung: '
  'Kein Risiko (App M5) oder Mittel (App M10)?', 'Kein Risiko', 'Mittel',
  'Die App-Kategorien M5 und M10 widersprechen sich.')
k('K-M05', 'Antrieb', 'Phasenumkehrschutz bei geregelten Antrieben',
  'Darf der Phasenumkehrschutz bei Frequenzumrichter-Antrieben als „nicht zutreffend" '
  'gelten (Schutz ist im Umrichter enthalten)?', 'Ja, nicht zutreffend', 'Nein, immer prüfen',
  'Eigene Annahme; im App-Katalog nicht geregelt.')
k('K-M06', 'Elektrik', 'Potenzialausgleich',
  'Fehlender Hauptpotenzialausgleich: Hoch (App M14) oder Mittel (Schindler M110)?',
  'Hoch (App)', 'Mittel (Schindler)', 'Abweichung App/Schindler.')
k('K-M07', 'Personenbefreiung', 'Notbefreiungsanleitung',
  'Fehlende oder veraltete Notbefreiungsanleitung: Mittel (App M13) oder Hoch '
  '(Schindler M116)?', 'Hoch, wenn sie fehlt; Mittel, wenn nur veraltet', 'Immer Mittel',
  'Abweichung App/Schindler; hier als abgestufte Regel vorgeschlagen.')
k('K-M08', 'Elektrik', 'Ohne Maschinenraum',
  'Bei maschinenraumlosen Anlagen: Gelten die Fragen zu Berührungssicherheit, '
  'Hauptschalter, Kennzeichnung und Stromlaufplan unverändert für den Steuerschrank?',
  'Ja (so umgesetzt: nur raumbezogene Gefährdungen entfallen)', 'Eigener Fragensatz',
  'Eigene Annahme.')
k('K-M09', 'Antrieb', 'Zweikreisbremse ohne Überwachung',
  'Zweikreisbremse vorhanden, aber kein Bremskontrollschalter: Mittel (App K4.2) – '
  'auch wenn kein SR-Modul / keine Nachregulierung mit offener Tür vorhanden ist?',
  'Mittel', 'Kein Risiko ohne Türüberbrückung', 'Eigene Nachfrage.')

# ---- Gefährdungen ----------------------------------------------------------
hz('MF-M01', 'Unzureichende Beleuchtung im Triebwerks-/Maschinenraum', GRP_BEL,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_bel_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qm_bel_200lux', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_bel_vorhanden')}),
    ('qm_bel_geeignet', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_bel_vorhanden')}),
    ('qm_bel_splitterschutz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_bel_vorhanden')})],
   [r(no('qm_bel_vorhanden'), 'HIGH', mfrom=('N20-M3', 'Keine Beleuchtung'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_bel_200lux'), 'MEDIUM', mfrom=('N20-M3', 'Dunkle Schiffsarmaturen'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_bel_geeignet'), 'MEDIUM', mfrom=('N20-M3', 'Leuchten an ungeeigneter'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_bel_splitterschutz'), 'MEDIUM', mfrom=('N20-M3', 'Leuchten ohne Splitterschutz'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.1.4.2'), trbs3121('Anh. 1 Nr. 8')],
   factor=F_BELEUCHTUNG, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M02', 'Unzureichender Schutz gegen elektrischen Schlag (offene Schalttafel, '
   'offene Kontakte, fehlende Berührungssicherheit)', GRP_EL,
   [('qm_beruehrungssicher', 'TRIGGER', 'ALWAYS'),
    ('qm_offene_schalttafel', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qm_beruehrungssicher')}),
    ('qm_offene_schalter', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qm_beruehrungssicher')}),
    ('qm_schaltschrank_unsicher', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qm_beruehrungssicher')}),
    ('qm_kennz_kontakte', 'OPTIONAL', 'NEVER'),
    ('qm_dguv_v3', 'TRIGGER', 'ALWAYS')],
   [r(yes('qm_offene_schalttafel'), 'HIGH', mfrom=('N20-M1', 'Offene Schalttafel'),
      evidence='HIGH_CONFIDENCE'),
    r(yes('qm_offene_schalter'), 'HIGH', mfrom=('N20-M1', 'Offene Kontakte'),
      evidence='HIGH_CONFIDENCE'),
    r(yes('qm_schaltschrank_unsicher'), 'MEDIUM', mfrom=('N20-M1', 'Unsichere Teile'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_beruehrungssicher'), 'MEDIUM', mfrom=('N20-M1', 'Nur teilweise'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_dguv_v3'), 'MEDIUM', mfrom=('N20-M1', 'Kein Nachweis'),
      evidence='HIGH_CONFIDENCE', klaerung='K-M01')],
   sources=[en8120('5.10.1.2'), trbs3121('Anh. 1 Nr. 21'), dguv('DGUV Vorschrift 3')],
   factor=F_ELEKTRISCH, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='M',
   klaerung='K-M08')

hz('MF-M03', 'Fehlender oder unzureichender Schutz an drehenden Teilen '
   '(Treibscheibe, Umlenkrollen, Begrenzer)', GRP_MR,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': SEIL}),
    ('qm_einzug_treibscheibe', 'TRIGGER', 'ALWAYS'),
    ('qm_einzug_begrenzer', 'TRIGGER', 'ALWAYS'),
    ('qm_einzug_grad', 'TRIGGER', 'ALWAYS')],
   [r(eq('qm_einzug_grad', 'offen'), 'HIGH', mfrom=('N20-M2', 'Einzugsstellen offen'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_einzug_treibscheibe'), 'HIGH', mfrom=('N20-M2', 'Einzugsstellen offen'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qm_einzug_grad', 'teilweise'), 'MEDIUM', mfrom=('N20-M2', 'Teilweise abgedeckte'),
      evidence='HIGH_CONFIDENCE'),
    r(all_(yes('qm_einzug_treibscheibe'), no('qm_einzug_begrenzer')), 'MEDIUM',
      mfrom=('N20-M2', 'Treibscheibe ist abgedeckt'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.9.3.1'), trbs3121('Anh. 1 Nr. 20')],
   factor=F_ROTIEREND, persons=[WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M04', 'Unzureichende Raumhöhe, Bewegungs- und Freiflächen im Triebwerksraum',
   GRP_MR,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_hoehe_180', 'TRIGGER', 'ALWAYS'),
    ('qm_freiflaeche', 'TRIGGER', 'ALWAYS'),
    ('qm_lagerung', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_freiflaeche'), 'HIGH', mfrom=('N20-M6', 'Freifläche'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_hoehe_180'), 'MEDIUM', mfrom=('N20-M6', 'Lichte Höhe'),
      sofort='Niedrige Stellen kennzeichnen (Warnmarkierung, Polsterung), Beschäftigte unterweisen',
      mittel='Lichte Höhe von 1,80 m im Gehbereich herstellen (Umbau, Verlegung von Einbauten)',
      evidence='HIGH_CONFIDENCE'),
    r(yes('qm_lagerung'), 'MEDIUM', mfrom=('N20-M6', 'Bewegungsflächen'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.6.3.2')], factor=F_ERGONOMIE, persons=[BEAUFTRAGTE, WARTUNG],
   agg='MAXIMUM', bereich='M')

hz('MF-M05', 'Unterschiedliche Ebenen, Podeste und Bodenöffnungen im Triebwerksraum '
   'ungesichert', GRP_MR,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_niveau', 'TRIGGER', 'ALWAYS'),
    ('qm_niveau_gesichert', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes('qm_niveau')}),
    ('qm_podest_absturz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_niveau')}),
    ('qm_bodenoeffnung', 'TRIGGER', 'ALWAYS')],
   [r(all_(yes('qm_niveau'), no('qm_niveau_gesichert')), 'MEDIUM',
      mfrom=('N20-M7', 'Niveauunterschied'), evidence='HIGH_CONFIDENCE'),
    r(yes('qm_podest_absturz'), 'HIGH', mfrom=('N20-M7', 'Podest ohne'), evidence='HIGH_CONFIDENCE'),
    r(yes('qm_bodenoeffnung'), 'HIGH', mfrom=('N20-M7', 'Bodenöffnung'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.6.3.2.4')], factor=F_ABSTURZ, persons=[BEAUFTRAGTE, WARTUNG],
   agg='MAXIMUM', bereich='M')

hz('MF-M06', 'Rutschiger, verschmutzter oder ölverunreinigter Boden im Triebwerksraum',
   GRP_MR,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_boden_rutschhemmend', 'TRIGGER', 'ALWAYS'),
    ('qm_boden_oelfest', 'TRIGGER', 'ALWAYS'),
    ('qm_oel_ausgetreten', 'TRIGGER', 'ALWAYS')],
   [r(yes('qm_oel_ausgetreten'), 'HIGH', mfrom=('N20-M8', 'Ausgetretenes'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_boden_rutschhemmend'), 'MEDIUM', mfrom=('N20-M8', 'Boden verschmutzt'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_boden_oelfest'), 'MEDIUM', mfrom=('N20-M8', 'Ölfester Anstrich'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.1.9')], factor=F_STURZ, persons=[BEAUFTRAGTE, WARTUNG],
   agg='MAXIMUM', bereich='M')

hz('MF-M07', 'Fehlender, nicht abschließbarer oder nicht gekennzeichneter Hauptschalter',
   GRP_EL,
   [('qm_hauptschalter', 'TRIGGER', 'ALWAYS'),
    ('qm_hauptschalter_abschliessbar', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_hauptschalter')}),
    ('qm_hauptschalter_gekennz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_hauptschalter')})],
   [r(no('qm_hauptschalter'), 'HIGH', mfrom=('N20-M9', 'Kein Hauptschalter'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_hauptschalter_abschliessbar'), 'HIGH', mfrom=('N20-M5', 'Kein abschließbarer'),
      evidence='HIGH_CONFIDENCE', klaerung='K-M02'),
    r(no('qm_hauptschalter_gekennz'), 'MEDIUM', mfrom=('N20-M9', 'Hauptschalter nicht eindeutig'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.10.5.1'), dguv('DGUV Vorschrift 3')], factor=F_ELEKTRISCH,
   persons=[WARTUNG], agg='MAXIMUM', bereich='M', klaerung='K-M08')

hz('MF-M08', 'Unzureichende elektromechanische Bremse (Einkreisbremse, keine Überwachung)',
   GRP_ANT,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': SEIL}),
    ('qm_zweikreisbremse', 'TRIGGER', 'ALWAYS'),
    ('qm_bremse_ueberwacht', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_zweikreisbremse')}),
    ('qk_ucm_sr_modul', 'MODIFIER', 'CONDITIONAL', {'required_when': no('qm_bremse_ueberwacht')})],
   [r(no('qm_zweikreisbremse'), 'HIGH', mfrom=('N20-M10', 'Einkreisbremse'), evidence='HIGH_CONFIDENCE'),
    r(all_(no('qm_bremse_ueberwacht'), yes('qk_ucm_sr_modul')), 'MEDIUM',
      mfrom=('N20-K4.2', 'Zweikreisbremse vorhanden'), evidence='HIGH_CONFIDENCE', klaerung='K-M09',
      notes='Entscheidung 02.09.2026: ohne Türüberbrückung (SR-Modul) kein Risiko.')],
   sources=[en8120('5.9.2.2.2'), trbs3121('Anh. 1 Nr. 16')], factor=F_UEBERLAST,
   persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M09', 'Fehlender Schutz des Antriebsmotors gegen Überhitzen', GRP_ANT,
   [('qm_motorschutz', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_motorschutz'), 'MEDIUM', mfrom=('N20-M10', 'Kein Schutz gegen Überhitzen'),
      evidence='HIGH_CONFIDENCE', klaerung='K-M03')],
   sources=[en8120('5.10.4.3')], factor=F_BRAND, persons=[NUTZER, WARTUNG], bereich='M')

hz('MF-M10', 'Fehlende unabhängige Fahrschütze / Abschaltwege', GRP_EL,
   [('qa_antrieb', 'APPLICABILITY', 'NEVER', {'applicable_when': neq('qa_antrieb', 'hydraulisch')}),
    ('qm_schuetze_unabhaengig', 'TRIGGER', 'ALWAYS'),
    ('qm_steuerung_selbstueberw', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': no('qm_schuetze_unabhaengig')})],
   [r(all_(no('qm_schuetze_unabhaengig'), yes('qm_steuerung_selbstueberw')), 'NO_RISK', prio=200,
      evidence='HIGH_CONFIDENCE', klaerung='K-M04',
      notes='App M5: „Nur ein Fahrschütz, jedoch selbst überwachende Steuerung" = grün'),
    r(no('qm_schuetze_unabhaengig'), 'HIGH', prio=100, mfrom=('N20-M5', 'Fehlende unabhängige'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.9.2.5'), trbs3121('Anh. 1 Nr. 16')], factor=F_UEBERLAST,
   persons=[NUTZER], bereich='M')

hz('MF-M11', 'Fehlende Laufzeitüberwachung des Antriebs', GRP_EL,
   [('qm_laufzeit', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_laufzeit'), 'MEDIUM', mfrom=('N20-M10', 'Laufzeitüberwachung'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.9.2.6.2')], factor=F_BRAND, persons=[NUTZER], bereich='M')

hz('MF-M12', 'Fehlender Schutz gegen Phasenumkehr / Phasenausfall', GRP_EL,
   [('qa_antrieb', 'APPLICABILITY', 'NEVER',
     {'applicable_when': nin('qa_antrieb', ['geregelt', 'hydraulisch'])}),
    ('qm_phasenumkehr', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_phasenumkehr'), 'MEDIUM',
      sofort='Anlage auf richtige Drehrichtung prüfen, Hinweis an Betreiber',
      mittel='Phasenfolge-/Phasenausfallrelais nachrüsten',
      evidence='INFERRED', klaerung='K-M05')],
   sources=[en8120('5.10.7')], factor=F_UEBERLAST, persons=[NUTZER], bereich='M')

hz('MF-M13', 'Unzureichende Hydraulikeinrichtungen (Absperrventil, Rohrbruchsicherung, '
   'Absinken)', GRP_ANT,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': HYDR}),
    ('qm_absperrventil', 'TRIGGER', 'ALWAYS'),
    ('qm_absperrventil_gekennz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_absperrventil')}),
    ('qm_rohrbruch', 'TRIGGER', 'ALWAYS'),
    ('qm_kav', 'TRIGGER', 'ALWAYS'),
    ('qm_absinkt', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_rohrbruch'), 'HIGH', mfrom=('N20-M11', 'Kein Rohrbruch'), evidence='HIGH_CONFIDENCE'),
    r(all_(yes('qm_absinkt'), no('qm_kav')), 'HIGH', mfrom=('N20-M11', 'Fahrkorb sinkt'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_kav'), 'MEDIUM', mfrom=('N20-K5', 'Keine Kolbenabsinkverhinderung'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_absperrventil'), 'MEDIUM', mfrom=('N20-M11', 'Absperrventil vorhanden'),
      evidence='INFERRED'),
    r(no('qm_absperrventil_gekennz'), 'MEDIUM', mfrom=('N20-M11', 'Absperrventil vorhanden'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.6.1.3'), en8120('5.6.7'), trbs3121('Anh. 1 Nr. 17')],
   factor=F_UEBERLAST, persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M14', 'Fehlende oder unzureichende Hebezeuge / Anschlagpunkte im Triebwerksraum',
   GRP_MR,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_anschlagpunkte', 'TRIGGER', 'ALWAYS'),
    ('qm_tragfaehigkeit', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_anschlagpunkte')}),
    ('qm_anschlag_geprueft', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_anschlagpunkte')})],
   [r(no('qm_anschlagpunkte'), 'HIGH', mfrom=('N20-M12', 'Keine Anschlagpunkte'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_tragfaehigkeit'), 'MEDIUM', mfrom=('N20-M12', 'Anschlagpunkte vorhanden'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_anschlag_geprueft'), 'MEDIUM', mfrom=('N20-M12', 'Prüfung der Anschlagpunkte'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.1.7')], factor=F_LAST, persons=[WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M15', 'Fehlende oder unzureichende Einrichtung für Notbetrieb und Personenbefreiung',
   GRP_NOT,
   [('qm_notbetrieb', 'TRIGGER', 'ALWAYS'),
    ('qm_notbetrieb_gekennz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_notbetrieb')}),
    ('qm_personal_eingewiesen', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_notbetrieb'), 'HIGH', mfrom=('N20-M13', 'Keine Einrichtung'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_notbetrieb_gekennz'), 'MEDIUM', mfrom=('N20-M13', 'Notbetriebseinrichtung vorhanden'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_personal_eingewiesen'), 'MEDIUM',
      sofort='Personenbefreiung bis zur Einweisung nur durch das Wartungsunternehmen',
      mittel='Beauftragte Personen anlagenbezogen in die Personenbefreiung einweisen und '
             'dokumentieren (BetrSichV Anh. 1 Nr. 4.1)', evidence='INFERRED')],
   sources=[en8120('5.9.2.3'), law('BetrSichV', 'Anh. 1 Nr. 4.1'), trbs3121('4.4')],
   factor=F_NOTFALL, persons=[NUTZER, BEAUFTRAGTE], agg='MAXIMUM', bereich='M')

hz('MF-M16', 'Fehlender Potenzialausgleich / mangelhafte bauseitige Elektroinstallation',
   GRP_EL,
   [('qm_potenzialausgleich', 'TRIGGER', 'ALWAYS'),
    ('qm_bauseitig_ok', 'TRIGGER', 'ALWAYS'),
    ('qm_ortsfest_geprueft', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_potenzialausgleich'), 'MEDIUM', mfrom=('N20-M14', 'Hauptpotenzialausgleich'),
      sofort='Elektrofachkraft mit der Prüfung der Schutzmaßnahme beauftragen',
      mittel='Hauptpotenzialausgleich an Führungsschienen, Maschinenrahmen und Schaltschrank herstellen (DIN VDE 0100-410)',
      evidence='HIGH_CONFIDENCE', klaerung='K-M06'),
    r(no('qm_bauseitig_ok'), 'HIGH', mfrom=('N20-M14', 'Defekte bauseitige'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_ortsfest_geprueft'), 'MEDIUM', mfrom=('N20-M14', 'Prüfung der ortsfesten'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.10.1.1'), src('OTHER', 'DIN VDE 0100-410'), dguv('DGUV Vorschrift 3')],
   factor=F_ELEKTRISCH, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M17', 'Fehlende Kennzeichnung elektrischer Einrichtungen, Stromlaufplan, '
   'Beschilderung und Betriebsanleitung', GRP_DOC,
   [('qm_kennz_elektrisch', 'TRIGGER', 'ALWAYS'),
    ('qm_stromlaufplan', 'TRIGGER', 'ALWAYS'),
    ('qm_beschilderung', 'TRIGGER', 'ALWAYS'),
    ('qm_betriebsanleitung', 'TRIGGER', 'ALWAYS')],
   [r(all_(no('qm_kennz_elektrisch'), eq('qm_stromlaufplan', 'fehlt')), 'HIGH',
      mfrom=('N20-M5', 'Mangelhafte Kennzeichnung elektrischer Einrichtungen, keine'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_kennz_elektrisch'), 'MEDIUM', mfrom=('N20-M15', 'Keine Kennzeichnung'),
      evidence='HIGH_CONFIDENCE'),
    r(in_('qm_stromlaufplan', ['unrichtig', 'fehlt']), 'MEDIUM',
      mfrom=('N20-M5', 'Fehlender oder unrichtiger Stromlaufplan'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_beschilderung'), 'MEDIUM', mfrom=('N20-M15', 'Einzelne Kennzeichnungen'),
      evidence='HIGH_CONFIDENCE'),
    r(in_('qm_betriebsanleitung', ['veraltet', 'fehlt']), 'MEDIUM',
      mfrom=('N20-M15', 'Betriebsanleitung vorhanden'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('7'), en8120('5.10.1.3'), law('BetrSichV', '§ 12')],
   factor=F_ORGA, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='M', klaerung='K-M08')

hz('MF-M18', 'Fehlende oder unzulängliche Sprechverbindung zwischen Fahrkorb und '
   'Triebwerksraum', GRP_NOT,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_sprechverbindung', 'APPLICABILITY', 'NEVER',
     {'applicable_when': neq('qm_sprechverbindung', 'nicht_noetig')}),
    ('qm_sprechverbindung', 'TRIGGER', 'ALWAYS')],
   [r(eq('qm_sprechverbindung', 'keine'), 'HIGH', mfrom=('N20-K18', 'Keine Sprechverbindung'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qm_sprechverbindung', 'eingeschraenkt'), 'MEDIUM', mfrom=('N20-K18', 'Sprechverbindung vorhanden'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.12.3')], factor=F_NOTFALL, persons=[WARTUNG, BEAUFTRAGTE], bereich='M')

hz('MF-M19', 'Aufzugsfremde Einrichtungen im Triebwerksraum', GRP_MR,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_fremd_frei', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_fremd_frei'), 'MEDIUM',
      sofort='Fremdnutzung mit dem Betreiber klären, Zugang nur für Aufzugspersonal',
      mittel='Aufzugsfremde Einrichtungen entfernen; Raum ausschließlich für den Aufzug nutzen',
      evidence='INFERRED')],
   sources=[en8120('5.2.1.2'), en8120('5.2.6.1')], factor=F_STURZ, persons=[WARTUNG], bereich='M')

hz('MF-M20', 'Fehlender Not-Halt im zusätzlichen Rollenraum', GRP_EL,
   [('qa_rollenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_rollenraum_nothalt', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_rollenraum_nothalt'), 'HIGH', mfrom=('N20-F7', 'Kein Notbremsschalter'),
      evidence='INFERRED', notes='Blaupause Schindler M049 (f132 Rollenraum).')],
   sources=[en8120('5.2.6.4.5'), en8120('5.12.1.11')], factor=F_BEFEHL, persons=[WARTUNG], bereich='M')
