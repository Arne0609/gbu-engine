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
GRP_SK = 'Sicherheitskomponenten'

MR = yes('qa_maschinenraum')
SEIL = in_('qa_aufzugsart', ['seil', 'trommel', 'seil_hydraulik'])
HYDR = in_('qa_aufzugsart', ['hydraulik', 'seil_hydraulik'])
# Treibscheiben- und Trommelantrieb: elektromechanische Betriebsbremse und
# Antriebswelle. Ein indirekter Hydraulikaufzug hängt zwar am Seil, hat aber
# keinen Treibscheibenantrieb (zweite Prüfung 16.09.2026, Punkt 5).
TREIB = in_('qa_aufzugsart', ['seil', 'trommel'])

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
   ui='5.34', visible_when=no('qm_beruehrungssicher'),
   help='Die Kennzeichnung ersetzt den Berührungsschutz nicht (Entscheidung 02.09.2026, K-K10); '
        'sie fehlt, ist das ein eigener – geringer – Mangel.')
yn('qm_dguv_v3', 'Nachweis der elektrischen Prüfung der AUFZUGSANLAGE nach DGUV Vorschrift 3 '
   'vorhanden (Steuerung, Antrieb, Leitungen der Anlage; Prüfplakette / Protokoll aktuell)?',
   ui='5.35',
   help='Nur die Aufzugsanlage selbst. Die bauseitige ortsfeste Installation des Raumes '
        '(Steckdosen, Raumbeleuchtung, Zuleitung) wird unter 5.37 erfasst '
        '(Prüfbericht 20.09.2026: Abgrenzung geschärft).')
yn('qm_bauseitig_ok', 'Bauseitige Elektroinstallation im Raum (Steckdosen, Schalter, '
   'Leitungen) unbeschädigt?', ui='5.36')
yn('qm_ortsfest_geprueft', 'Prüfung der BAUSEITIGEN ortsfesten elektrischen Anlage des Raumes '
   'nachgewiesen (Zuleitung, Steckdosen, Raumbeleuchtung)?', ui='5.37',
   help='Bauseitige Installation, nicht die Aufzugsanlage (die steht unter 5.35). Zuständig '
        'ist der Betreiber bzw. das Elektrogewerk des Gebäudes.')
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
   'Antrieb vorhanden?', ui='5.44', visible_when=MR,
   help='Gemeint ist das Flächenmaß nach DIN EN 81-20 5.2.6.3.2. Ist der Zugang zu Handrad '
        'bzw. Bremslüftung dadurch vollständig versperrt, ist die Notbetriebseinrichtung '
        'nicht bedienbar – dann ist zusätzlich 5.53 mit Nein zu beantworten; erst darüber '
        '(MF-M15) entsteht die Einstufung Hoch.')
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
   ui='6.2', visible_when=TREIB)
yn('qm_bremse_ueberwacht', 'Bremse elektrisch überwacht (Bremskontrollschalter)?',
   ui='6.2a', visible_when=yes('qm_zweikreisbremse'))
yn('qm_motorschutz', 'Schutz gegen Überhitzen des Antriebsmotors vorhanden?', ui='6.3')
yn('qm_schuetze_unabhaengig', 'Zwei unabhängige Fahrschütze / Abschaltwege vorhanden?',
   ui='6.4', visible_when=not_(HYDR))
yn('qm_steuerung_selbstueberw', 'Bei nur einem Schütz: selbstüberwachende Steuerung '
   'mit Baumusterprüfung?', ui='6.4a', visible_when=no('qm_schuetze_unabhaengig'))
yn('qm_laufzeit', 'Motor-Laufzeitüberwachung vorhanden?', ui='6.5')
yn('qm_phasenumkehr', 'Schutz gegen Phasenumkehr / Phasenausfall vorhanden?', ui='6.6',
   visible_when=nin('qa_antrieb', ['geregelt', 'hydraulisch']))

yn('qm_absperrventil', 'Absperrventil am Hydraulikaggregat vorhanden?', ui='6.10',
   visible_when=HYDR)
yn('qm_absperrventil_zugang', 'Absperrventil gut zugänglich (ohne Hilfsmittel, ohne '
   'Umbauten erreichbar und bedienbar)?', ui='6.10a',
   visible_when=yes('qm_absperrventil'),
   help='Regelprüfung 20.09.2026: Aus der früheren Doppelfrage „gekennzeichnet UND gut zugänglich" '
        'herausgelöst. Ein nicht zugängliches Ventil verhindert das sichere Absperren bei '
        'Arbeiten (Mittel, technische Abhilfe); die bloß fehlende Kennzeichnung ist ein '
        'Mangel ohne unmittelbaren Gefährdungsbeitrag und steht unter 6.10b (Niedrig).')
yn('qm_absperrventil_gekennz', 'Absperrventil dauerhaft gekennzeichnet (Funktion, '
   'Wirkrichtung)?', ui='6.10b', visible_when=yes('qm_absperrventil'),
   help='Regelprüfung 20.09.2026: Aus 6.10a herausgelöst; eigener Befund mit Stufe Niedrig.')
yn('qm_rohrbruch', 'Rohrbruchsicherungsventil (Leitungsbruchventil) vorhanden?', ui='6.11',
   visible_when=HYDR)
# Regelprüfung 20.09.2026: Zusatzfrage zu 6.11. DIN EN 81-20 Tabelle 12 lässt gegen freien Fall bzw.
# Abwärtsbewegung mit überhöhter Geschwindigkeit mehrere Kombinationen zu: beim
# DIREKT angetriebenen Aufzug Fangvorrichtung mit Geschwindigkeitsbegrenzer ODER
# Leitungsbruchventil (5.6.3) ODER Drossel (5.6.4); beim INDIREKT angetriebenen
# Aufzug zusätzlich Leitungsbruchventil bzw. Drossel zusammen mit einer durch
# Bruch der Tragmittel oder Sicherheitsseil ausgelösten Fangvorrichtung (die
# Auslösung selbst wird unter 10.8/10.8a erhoben). Die bisherige Regel vergab
# Hoch allein aus dem fehlenden Leitungsbruchventil und traf damit auch
# normkonforme Anlagen mit zulässiger Drossel.
sel('qm_absturzsicherung_alt', 'Zulässige Absturzsicherung statt Leitungsbruchventil',
    ui='6.11a', visible_when=all_(HYDR, no('qm_rohrbruch')),
    options=[('drossel', 'Drossel oder Drosselrückschlagventil (DIN EN 81-20 5.6.4)'),
             ('fang', 'Fangvorrichtung, eingerückt durch Geschwindigkeitsbegrenzer '
                      '(DIN EN 81-20 5.6.2.1 mit 5.6.2.2.1)'),
             ('keine', 'Keine dieser Einrichtungen vorhanden')],
    help='Regelprüfung 20.09.2026: Nur zu beantworten, wenn kein Leitungsbruchventil vorhanden ist. '
         'Maßgeblich ist DIN EN 81-20 Tabelle 12. Beim indirekt angetriebenen Aufzug genügt '
         'die Drossel allein nicht – sie muss mit einer Fangvorrichtung kombiniert sein, die '
         'durch Bruch der Tragmittel oder ein Sicherheitsseil ausgelöst wird; das wird unter '
         '10.8 und 10.8a erhoben. Im Zweifel „Keine dieser Einrichtungen vorhanden".')
yn('qm_kav', 'Einrichtung gegen Absinken (Kolbenabsinkverhinderung / '
   'Nachholsteuerung) vorhanden?', ui='6.12', visible_when=HYDR)
yn('qm_absinkt', 'Sinkt der Fahrkorb im Stillstand merklich ab?', ui='6.13',
   visible_when=HYDR)

# Ergaenzung 04.09.2026 (Lueckenschluss EN 81-80 Nr. 57): Notendschalter,
# EN 81-20 5.12.2. Bei Hydraulikaufzuegen nur am oberen Ende des Fahrwegs.
sel('qm_notendschalter', 'Notendschalter (Endbegrenzung hinter den Endhaltestellen)',
    ui='6.14',
    options=[('geprueft', 'Vorhanden, Wirksamkeit vor Pufferberührung nachgewiesen'),
             ('ungeprueft', 'Vorhanden, Wirksamkeit nicht nachgewiesen'),
             ('fehlt', 'Nicht vorhanden oder unwirksam (überbrückt, verstellt)')],
    help='EN 81-20 5.12.2.1: bei Treibscheiben-, Trommel- und Kettenaufzügen am oberen und '
         'unteren Ende des Fahrwegs, bei Hydraulikaufzügen nur am oberen Ende. Sie müssen '
         'wirksam werden, bevor Fahrkorb oder Gegengewicht die Puffer berühren.')
yn('qm_notendschalter_getrennt', 'Getrennte Betätigungseinrichtungen für das '
   'betriebsmäßige Anhalten und für die Notendschalter?', ui='6.14a',
   help='EN 81-20 5.12.2.2.1.',
   visible_when=nin('qm_notendschalter', ['fehlt']))
yn('qm_notendschalter_verbindung_ueberwacht', 'Bei mittelbarer Betätigung (Seil, Riemen, '
   'Kette): Bruch oder Schlaffwerden hält das Triebwerk über eine elektrische '
   'Sicherheitseinrichtung an?', ui='6.14b',
   help='EN 81-20 5.12.2.2.3 b) und 5.12.2.2.4 b). Bei direkter Betätigung durch den '
        'Fahrkorb mit „Ja" beantworten.',
   visible_when=nin('qm_notendschalter', ['fehlt']))

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
   'eingewiesen?', ui='5.53b', visible_when=yes('qd_beauftragte_person'),
   help='Setzt eine benannte beauftragte Person voraus (E1). Fehlt sie ganz, ist das der Befund '
        'von MF-D05 – die Einweisung wird dann nicht zusätzlich bemängelt '
        '(Prüfbericht 20.09.2026).')

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
   [r(no('qm_bel_vorhanden'), 'MEDIUM',
      sofort='Betreten des Raumes ohne ausreichende Beleuchtung untersagen; ortsveränderliche '
             'Leuchte (Handlampe/Akkustrahler) dauerhaft im Zugangsbereich bereitstellen, '
             'Betreiber unterrichten',
      mittel='Geeignete Leuchten nachrüsten (mind. 200 lx an den Arbeitsflächen nach DIN EN '
             '81-20 5.2.1.4.2 / ASR A3.4)',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Hoch auf Mittel. Die Gefahr entsteht erst beim Betreten und wird von einer '
            'mitgeführten Leuchte vollständig beherrscht; eine Hoch-Regel, deren eigene '
            'Sofortmaßnahme „Handlampe benutzen" lautet, widerspricht dem Stufenmaßstab '
            '(Hoch verlangt Absperren/Stilllegen). Sofortmaßnahme auf ein Betretungsverbot '
            'mit bereitgestellter Leuchte umgestellt [ORGA], Zielwert 200 lx ergänzt.'),
    r(no('qm_bel_200lux'), 'MEDIUM', mfrom=('N20-M3', 'Dunkle Schiffsarmaturen'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_bel_geeignet'), 'MEDIUM', mfrom=('N20-M3', 'Leuchten an ungeeigneter'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_bel_splitterschutz'), 'MEDIUM', mfrom=('N20-M3', 'Leuchten ohne Splitterschutz'),
      sofort='Ungeschützte Leuchtmittel im Kopfbereich provisorisch sichern '
             '(Splitterschutzschlauch/-folie) oder betroffene Leuchte außer Betrieb nehmen und '
             'Handlampe verwenden; Betreiber unterrichten',
      evidence='HIGH_CONFIDENCE', pb='H11 – Sofortmaßnahme ergänzt',
      notes='Regelprüfung 20.09.2026: Stufe Mittel bleibt. Die bisherige Sofortmaßnahme „Beschädigte Leuchten sofort '
            'ersetzen" passte nicht zur Bedingung – die Regel feuert bei FEHLENDEM '
            'Splitterschutz, nicht bei beschädigten Leuchten – und war technisch statt '
            'organisatorisch.')],
   sources=[en8120('5.2.1.4.2'), trbs3121('Anh. 1 Nr. 8'),
            law('ArbStättV', 'Anh. 3.4'), src('OTHER', 'ASR A3.4')],
   factor=F_BELEUCHTUNG, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M02', 'Unzureichender Schutz gegen elektrischen Schlag (offene Schalttafel, '
   'offene Kontakte, fehlende Berührungssicherheit)', GRP_EL,
   [('qm_beruehrungssicher', 'TRIGGER', 'ALWAYS'),
    ('qm_offene_schalttafel', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qm_beruehrungssicher')}),
    ('qm_offene_schalter', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qm_beruehrungssicher')}),
    ('qm_schaltschrank_unsicher', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qm_beruehrungssicher')}),
    ('qm_kennz_kontakte', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qm_beruehrungssicher')}),
    ('qm_dguv_v3', 'TRIGGER', 'ALWAYS')],
   [r(yes('qm_offene_schalttafel'), 'HIGH', mfrom=('N20-M1', 'Offene Schalttafel'),
      sofort='Triebwerksraum verschlossen halten, Zutritt nur für Elektrofachkräfte bzw. '
             'elektrotechnisch unterwiesene Personen; beim Betreten Hauptschalter ausschalten '
             '– Achtung: die Einspeisung vor dem Hauptschalter (Zuleitung, Vorsicherung, '
             'Beleuchtungs- und Notrufkreis) bleibt unter Spannung',
      mittel='Berührungsschutz herstellen (Abdeckungen, geschlossener Schaltschrank); sofern '
             'nicht möglich, Steuerung erneuern',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Stufe Hoch bleibt. Die bisherige Sofortmaßnahme „Bei Betreten des '
            'Maschinenraumes ausschalten" war nur teilwirksam: Der Hauptschalter trennt die '
            'Einspeisung vor ihm gerade nicht, an einer offenen Schalttafel bleiben '
            'spannungsführende Teile berührbar. Mittelfristmaßnahme vom reinen '
            'Steuerungstausch auf den Berührungsschutz aufgeweitet.'),
    r(yes('qm_offene_schalter'), 'HIGH', mfrom=('N20-M1', 'Offene Kontakte'),
      evidence='HIGH_CONFIDENCE'),
    r(yes('qm_schaltschrank_unsicher'), 'MEDIUM', mfrom=('N20-M1', 'Unsichere Teile'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_beruehrungssicher'), 'MEDIUM', mfrom=('N20-M1', 'Nur teilweise'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_dguv_v3'), 'MEDIUM', mfrom=('N20-M1', 'Kein Nachweis'),
      mittel='Prüfung der Aufzugsanlage nach DGUV Vorschrift 3 unverzüglich beauftragen, '
             'Prüfprotokoll und Plakette dokumentieren, Prüffrist in den Prüfplan nach '
             'BetrSichV § 3 aufnehmen',
      evidence='HIGH_CONFIDENCE', klaerung='K-M01',
      notes='Regelprüfung 20.09.2026: Mittelfristmaßnahme neu gefasst. „Bei Notwendigkeit DGUV V3 Prüfung '
            'beauftragen" stellte die Prüfung ins Ermessen, obwohl der fehlende Nachweis die '
            'Notwendigkeit gerade begründet; der Vorbehalt ist gestrichen. Die Beauftragung '
            'einer Prüfung ist organisatorisch, nicht technisch [ORGA]. Stufe Mittel bleibt.'),
    r(no('qm_kennz_kontakte'), 'LOW',
      sofort='Offene Kontakte provisorisch mit Warnzeichen W012 kennzeichnen',
      mittel='Dauerhafte Warnkennzeichnung anbringen; sie ersetzt den Berührungsschutz nicht',
      evidence='INFERRED',
      notes='Prüfbericht 20.09.2026: bisher optionale Frage ohne Regelwirkung. Eigener geringer '
            'Mangel, ausdrücklich KEINE Kompensation (Entscheidung K-K10).')],
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
   [r(no('qm_freiflaeche'), 'MEDIUM', mfrom=('N20-M6', 'Freifläche'),
      mittel='Einbauten und Lagerflächen verlagern, Freifläche dauerhaft herstellen und am '
             'Boden markieren; Freihaltung zusätzlich organisatorisch sicherstellen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Hoch auf Mittel. Ein Mangel, den die eigene Sofortmaßnahme durch Freiräumen '
            'binnen Minuten beseitigt, ist keine unmittelbare Gefahr; die Unterschreitung '
            'bedeutet erschwerten, nicht unmöglichen Notbetrieb, und Hoch stand unplausibel '
            'neben R3 (Lagerung = Mittel), obwohl die Lagerung regelmäßig die Ursache ist. '
            'Der Hoch-Fall (Notbetriebseinrichtung nicht bedienbar) ist über 5.53 / MF-M15-R1 '
            'abgebildet – Hilfe zu 5.44 entsprechend ergänzt. Mittelfristmaßnahme technisch '
            'gefasst (TOP: T vor O).'),
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
      mittel='Rutschhemmenden Bodenbelag bzw. rutschhemmende Beschichtung herstellen '
             '(Bewertungsgruppe nach ASR A1.5 / DGUV-Regelwerk); Reinigung zusätzlich in den '
             'Wartungsplan aufnehmen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: TOP-Verstoß behoben. Frage 5.48 bündelt „rutschhemmend" (baulich) und '
            '„sauber" (organisatorisch), die einzige Mittelfristmaßnahme war aber rein '
            'organisatorisch: Bei baulich glattem Boden beseitigt der Wartungsplan die '
            'Ursache nicht. Eine Aufteilung der Frage ist nicht erforderlich, die ergänzte '
            'technische Maßnahme deckt beide Fälle. Stufe Mittel bleibt.'),
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
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': TREIB}),
    ('qm_zweikreisbremse', 'TRIGGER', 'ALWAYS'),
    ('qm_bremse_ueberwacht', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_zweikreisbremse')}),
    ('qk_ucm_sr_modul', 'MODIFIER', 'CONDITIONAL', {'required_when': no('qm_bremse_ueberwacht')})],
   [r(no('qm_zweikreisbremse'), 'HIGH', mfrom=('N20-M10', 'Einkreisbremse'), evidence='HIGH_CONFIDENCE'),
    r(all_(no('qm_bremse_ueberwacht'), yes('qk_ucm_sr_modul')), 'MEDIUM',
      mfrom=('N20-K4.2', 'Zweikreisbremse vorhanden'), evidence='HIGH_CONFIDENCE', klaerung='K-M09',
      sofort='Türüberbrückung (Nachregulieren bzw. Voraböffnen mit offener Tür) sofort außer '
             'Betrieb setzen – Betrieb nur mit geschlossener Tür – und Wirksamkeit beider '
             'Bremskreise prüfen; Betreiber unterrichten',
      pb='H11 – Sofortmaßnahme ergänzt',
      notes='Entscheidung 02.09.2026: ohne Türüberbrückung (SR-Modul) kein Risiko. '
            'Regelprüfung 20.09.2026: Sofortmaßnahme ersetzt – „bei jeder Wartung prüfen" ist eine wiederkehrende '
            'organisatorische Maßnahme und wirkt nicht sofort. Die Gefahr entsteht gerade '
            'durch das aktive SR-Modul, das sich sofort abschalten lässt.')],
   sources=[en8120('5.9.2.2.2'), trbs3121('Anh. 1 Nr. 16')], factor=F_UEBERLAST,
   persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M09', 'Fehlender Schutz des Antriebsmotors gegen Überhitzen', GRP_ANT,
   [('qm_motorschutz', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_motorschutz'), 'MEDIUM', mfrom=('N20-M10', 'Kein Schutz gegen Überhitzen'),
      evidence='HIGH_CONFIDENCE', klaerung='K-M03')],
   sources=[en8120('5.10.4.3')], factor=F_BRAND, persons=[NUTZER, WARTUNG], bereich='M')

hz('MF-M10', 'Fehlende unabhängige Fahrschütze / Abschaltwege', GRP_EL,
   [('qa_aufzugsart', 'APPLICABILITY', 'NEVER', {'applicable_when': not_(HYDR),
     'notes': 'Prüfbericht 20.09.2026: Anwendbarkeit an der Aufzugsart (3.1) statt am frei '
              'wählbaren Antriebsfeld (6.1) – widersprüchliche Eingaben wirkten sonst hier.'}),
    ('qm_schuetze_unabhaengig', 'TRIGGER', 'ALWAYS'),
    ('qm_steuerung_selbstueberw', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': no('qm_schuetze_unabhaengig')})],
   [r(all_(no('qm_schuetze_unabhaengig'), yes('qm_steuerung_selbstueberw')), 'NO_RISK', prio=200,
      evidence='HIGH_CONFIDENCE', klaerung='K-M04',
      notes='App M5: „Nur ein Fahrschütz, jedoch selbst überwachende Steuerung" = grün'),
    r(no('qm_schuetze_unabhaengig'), 'HIGH', prio=100, mfrom=('N20-M5', 'Fehlende unabhängige'),
      sofort='Abschaltfunktion des Fahrschützes bei jeder Wartung prüfen; bei Auffälligkeit (Schütz '
             'fällt nicht ab) Anlage sofort außer Betrieb nehmen',
      mittel='Zweites, unabhängiges Fahrschütz bzw. redundante Abschaltung nachrüsten oder Steuerung erneuern',
      evidence='HIGH_CONFIDENCE', pb='B11 – „bei Arbeiten ausschalten" schützt die Nutzer nicht')],
   sources=[en8120('5.9.2.5'), trbs3121('Anh. 1 Nr. 16')], factor=F_UEBERLAST,
   persons=[NUTZER], bereich='M')

hz('MF-M11', 'Fehlende Laufzeitüberwachung des Antriebs', GRP_EL,
   [('qm_laufzeit', 'TRIGGER', 'ALWAYS')],
   [r(no('qm_laufzeit'), 'MEDIUM', mfrom=('N20-M10', 'Laufzeitüberwachung'),
      sofort='Thermischen Motorschutz (Thermistor, Motorschutzschalter) auf Vorhandensein und '
             'Funktion prüfen; bei blockierter Anlage oder Anzeichen von Überhitzung (Geruch, '
             'Verfärbung, heißes Öl) Hauptschalter ausschalten, Anlage stilllegen und '
             'Betreiber unterrichten',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Sofortmaßnahme konkretisiert. „Anlage bei Auffälligkeiten stilllegen" nennt '
            'weder Auslöser noch Handlung und liegt nahe am unzulässigen „Vorsicht walten '
            'lassen". Stufe Mittel bleibt: Brand entsteht erst, wenn zusätzlich eine '
            'Blockade oder ein Seilrutsch auftritt und der Motorschutz versagt.')],
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
    ('qm_absperrventil_zugang', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_absperrventil')}),
    ('qm_absperrventil_gekennz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_absperrventil')}),
    ('qm_rohrbruch', 'TRIGGER', 'ALWAYS'),
    ('qm_absturzsicherung_alt', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': no('qm_rohrbruch')}),
    ('qm_kav', 'TRIGGER', 'ALWAYS'),
    ('qm_absinkt', 'TRIGGER', 'ALWAYS')],
   [r(all_(no('qm_rohrbruch'), in_('qm_absturzsicherung_alt', ['drossel', 'fang'])),
      'NO_RISK', prio=150,
      sofort='Zustand erhalten; Wirksamkeit der Absturzsicherung bei der wiederkehrenden '
             'Prüfung erneut belegen',
      evidence='HIGH_CONFIDENCE', sources=[en8120('5.6.1.3')],
      notes='Regelprüfung 20.09.2026: Ausdrückliche Kein-Risiko-Regel für die nach DIN EN 81-20 Tabelle 12 '
            'zulässigen Alternativen zum Leitungsbruchventil. Sie steht hier, damit der '
            'Bericht den normgerechten Zustand benennt und nicht nur die Auffangregel greift; '
            'ohne sie fielen beide Antwortwerte durch die Abdeckungsprüfung '
            '(mf_optionen.ts).'),
    r(all_(no('qm_rohrbruch'), eq('qm_absturzsicherung_alt', 'keine')), 'HIGH',
      mfrom=('N20-M11', 'Kein Rohrbruch'),
      sofort='Aufzug sofort außer Betrieb nehmen und gegen Benutzung sichern, bis eine '
             'zulässige Absturzsicherung nachgewiesen ist; Betreiber unterrichten',
      evidence='HIGH_CONFIDENCE', sources=[en8120('5.6.1.3'), en8120('5.6.3'), en8120('5.6.4')],
      notes='Regelprüfung 20.09.2026: Bedingung um die zulässigen Alternativen erweitert (neue Frage 6.11a). Die '
            'Regel vergab Hoch auch für Anlagen, die nach DIN EN 81-20 Tabelle 12 normgerecht '
            'statt eines Leitungsbruchventils eine Drossel bzw. ein Drosselrückschlagventil '
            'oder eine über den Geschwindigkeitsbegrenzer eingerückte Fangvorrichtung haben. '
            'Die Stufe Hoch ist beim tatsächlich fehlenden Absturzschutz richtig und '
            'altersunabhängig. Die Sofortmaßnahme trug außerdem nicht: Ein Leitungsbruchventil '
            'schützt gegen den plötzlichen Leitungsbruch, den man durch „Absinkverhalten '
            'überwachen" nicht beherrscht, und „nur eingeschränkt betreiben" ist unbestimmt.'),
    r(all_(yes('qm_absinkt'), no('qm_kav')), 'HIGH', mfrom=('N20-M11', 'Fahrkorb sinkt'),
      evidence='HIGH_CONFIDENCE'),
    r(all_(yes('qm_absinkt'), yes('qm_kav')), 'MEDIUM',
      sofort='Vor Arbeiten am Hydrauliksystem Fahrkorb auf dem Puffer absetzen oder gegen '
             'Absinken sichern; Absinkverhalten und Bündigkeit überwachen',
      mittel='Wirksamkeit der Kolbenabsinkverhinderung / Nachholsteuerung prüfen lassen, '
             'Leckage (Dichtungen, Ventile, Leitungen) suchen und beseitigen',
      evidence='INFERRED',
      notes='Prüfbericht 20.09.2026: bisherige Lücke – ein merkliches Absinken TROTZ vorhandener '
            'Einrichtung fiel auf „Kein Risiko". Die Einrichtung ist dann unwirksam.'),
    r(no('qm_kav'), 'MEDIUM', mfrom=('N20-K5', 'Keine Kolbenabsinkverhinderung'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_absperrventil'), 'MEDIUM',
      sofort='Arbeiten am Hydrauliksystem nur mit abgesetztem, gegen Bewegung gesichertem Fahrkorb',
      mittel='Absperrventil zwischen Zylinder und Rückschlagventil nachrüsten, gut zugänglich und gekennzeichnet',
      evidence='INFERRED', pb='B12 – fehlendes Ventil wird nachgerüstet, nicht nur gekennzeichnet'),
    r(no('qm_absperrventil_zugang'), 'MEDIUM', mfrom=('N20-M11', 'Absperrventil vorhanden'),
      sofort='Arbeiten am Hydrauliksystem nur mit abgesetztem, gegen Bewegung gesichertem '
             'Fahrkorb, bis das Ventil ohne Hilfsmittel bedienbar ist',
      mittel='Absperrventil zugänglich anordnen (verlegen, Einbauten entfernen, '
             'Bedienzugang schaffen)',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Bedingung auf die Zugänglichkeit eingegrenzt (6.10a und 6.10b sind getrennt). '
            'Die Frage bündelte zwei verschiedene Mängel und bewertete beide mit Mittel, was '
            'den Kennzeichnungsmangel überzeichnete. Außerdem ist „Ventil zugänglich anordnen" '
            'eine technische Maßnahme – die Kennzeichnung als einzige Mittelfristmaßnahme '
            'verstieß beim Zugänglichkeitsmangel gegen das TOP-Prinzip.'),
    r(no('qm_absperrventil_gekennz'), 'LOW',
      sofort='Absperrventil provisorisch kennzeichnen (Funktion und Wirkrichtung)',
      mittel='Dauerhafte Kennzeichnung des Absperrventils anbringen und in die '
             'Wartungsunterlagen aufnehmen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Neue Regel. Die fehlende Kennzeichnung war mit der Zugänglichkeit in einer '
            'Frage gebündelt und wurde mit Mittel überbewertet: Sie ist ein Mangel ohne '
            'unmittelbaren Gefährdungsbeitrag.')],
   sources=[en8120('5.6.1.3'), en8120('5.6.7'), trbs3121('Anh. 1 Nr. 17')],
   factor=F_UEBERLAST, persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M14', 'Fehlende oder unzureichende Hebezeuge / Anschlagpunkte im Triebwerksraum',
   GRP_MR,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qm_anschlagpunkte', 'TRIGGER', 'ALWAYS'),
    ('qm_tragfaehigkeit', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_anschlagpunkte')}),
    ('qm_anschlag_geprueft', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_anschlagpunkte')})],
   [r(no('qm_anschlagpunkte'), 'MEDIUM', mfrom=('N20-M12', 'Keine Anschlagpunkte'),
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Hoch auf Mittel. Die Gefahr entsteht erst, wenn tatsächlich schwere Teile '
            'gehoben werden und eine improvisierte Anschlagstelle versagt – ein zusätzliches '
            'Ereignis. Bedingung und beide Maßnahmen bleiben. Der Rang des Mangels hängt am '
            'Errichtungsregelwerk (1.28): Bei EN 81-1/-2 (1999–2016) und EN 81-20 ist das '
            'Fehlen von Anschlagpunkten ein Konformitätsmangel, bei TRA-Anlagen (vor 1999) '
            'Nachrüstbedarf nach Stand der Technik (EN 81-80). Fundstellen am Normtext '
            'nachgeschlagen: DIN EN 81-20 5.2.1.7 „Hebezeuge" (Anschlagpunkte mit Angabe der '
            'Tragfähigkeit in den Aufstellungsorten für Triebwerk und Steuerung, bei Bedarf '
            'auch im Schachtkopf) und EN 81-1:1998 6.3.7 „Hebezeuge für Aufzugsteile" '
            '(metallische Anschlagpunkte oder Haken mit Angabe der Tragfähigkeit an der Decke '
            'des Triebwerksraums oder an Trägern); die Tragfähigkeitsangabe selbst verlangt '
            'EN 81-1:1998 15.4.5.'),
    r(no('qm_tragfaehigkeit'), 'MEDIUM', mfrom=('N20-M12', 'Anschlagpunkte vorhanden'),
      evidence='HIGH_CONFIDENCE', sources=[en8120('5.2.1.7')],
      notes='Regelprüfung 20.09.2026: Normbezug am Normtext bestätigt – DIN EN 81-20 5.2.1.7 '
            'verlangt die Angabe der Tragfähigkeit am Anschlagpunkt, EN 81-1:1998 15.4.5 in '
            'Verbindung mit 6.3.7 ebenso.'),
    r(no('qm_anschlag_geprueft'), 'LOW', mfrom=('N20-M12', 'Prüfung der Anschlagpunkte'),
      evidence='HIGH_CONFIDENCE', sources=[law('BetrSichV', '§ 10')],
      notes='Regelprüfung 20.09.2026: Mittel auf Niedrig. Der fehlende Prüfnachweis ist ein Dokumentationsmangel '
            'ohne unmittelbaren Gefährdungsbeitrag – der Anschlagpunkt ist vorhanden und '
            'gekennzeichnet; mit Mittel stand er auf einer Stufe mit der fehlenden '
            'Tragfähigkeitsangabe, die einen echten Überlastbeitrag hat. Normbezug ist die '
            'Prüfpflicht nach BetrSichV § 10, nicht EN 81-20 5.2.1.7. Maßnahmen bleiben.')],
   sources=[en8120('5.2.1.7')], factor=F_LAST, persons=[WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M15', 'Fehlende oder unzureichende Einrichtung für Notbetrieb und Personenbefreiung',
   GRP_NOT,
   [('qm_notbetrieb', 'TRIGGER', 'ALWAYS'),
    ('qm_notbetrieb_gekennz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qm_notbetrieb')}),
    ('qm_personal_eingewiesen', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qd_beauftragte_person')}),
    ('qd_beauftragte_person', 'MODIFIER', 'NEVER',
     {'notes': 'Ohne benannte beauftragte Person greift MF-D05; die Einweisung wird dann hier '
               'nicht zusätzlich bemängelt.'})],
   [r(no('qm_notbetrieb'), 'HIGH', mfrom=('N20-M13', 'Keine Einrichtung'), evidence='HIGH_CONFIDENCE'),
    r(no('qm_notbetrieb_gekennz'), 'MEDIUM', mfrom=('N20-M13', 'Notbetriebseinrichtung vorhanden'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_personal_eingewiesen'), 'MEDIUM',
      sofort='Personenbefreiung bis zur Einweisung nur durch das Wartungsunternehmen',
      mittel='Beauftragte Personen anlagenbezogen in die Personenbefreiung einweisen und '
             'dokumentieren (BetrSichV Anh. 1 Nr. 4.1)', evidence='INFERRED')],
   sources=[en8120('5.9.2.3'), law('BetrSichV', 'Anh. 1 Nr. 4.1'), trbs3121('3.7.3')],
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
      sofort='Prüfnachweis der bauseitigen Installation beim Betreiber anfordern',
      mittel='Wiederkehrende Prüfung der bauseitigen ortsfesten Anlage (Zuleitung, Steckdosen, '
             'Raumbeleuchtung) nach DGUV Vorschrift 3 durch den Betreiber veranlassen',
      evidence='HIGH_CONFIDENCE',
      notes='Prüfbericht 20.09.2026: Abgrenzung zu 5.35 (Aufzugsanlage) geschärft.')],
   sources=[en8120('5.10.1.1'), src('OTHER', 'DIN VDE 0100-410'), dguv('DGUV Vorschrift 3')],
   factor=F_ELEKTRISCH, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='M')

hz('MF-M17', 'Fehlende Kennzeichnung elektrischer Einrichtungen, Stromlaufplan, '
   'Beschilderung und Betriebsanleitung', GRP_DOC,
   [('qm_kennz_elektrisch', 'TRIGGER', 'ALWAYS'),
    ('qm_stromlaufplan', 'TRIGGER', 'ALWAYS'),
    ('qm_beschilderung', 'TRIGGER', 'ALWAYS'),
    ('qm_betriebsanleitung', 'TRIGGER', 'ALWAYS')],
   # Regelprüfung 20.09.2026: Die frühere Regel R1 (Kennzeichnung fehlt UND Stromlaufplan fehlt -> Hoch)
   # ist ersatzlos entfallen: Sie hatte keine eigene Maßnahme, sondern wiederholte
   # die von R3 wörtlich, und hob in dieser Antwortkombination nur die Stufe an.
   # Über MAXIMUM greifen dort ohnehin R2 und R3 mit je eigener Maßnahme = Mittel.
   # Eine Häufung von Dokumentationsmängeln gehört in den Berichtstext, nicht in
   # eine Stufenanhebung auf Hoch.
   [r(no('qm_kennz_elektrisch'), 'MEDIUM', mfrom=('N20-M15', 'Keine Kennzeichnung'),
      evidence='HIGH_CONFIDENCE'),
    r(in_('qm_stromlaufplan', ['unrichtig', 'fehlt']), 'MEDIUM',
      mfrom=('N20-M5', 'Fehlender oder unrichtiger Stromlaufplan'),
      sofort='Vor Arbeiten an Steuerung und Antrieb Anlage freischalten und gegen '
             'Wiedereinschalten sichern; Schaltunterlagen bei Betreiber bzw. '
             'Wartungsunternehmen anfordern',
      mittel='Stromlaufplan und Schaltunterlagen anlagenbezogen beschaffen oder neu erstellen '
             'lassen und im Triebwerksraum hinterlegen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Beide Maßnahmen ersetzt. „Arbeiten an der Elektrik nur durch Elektrofachkraft" '
            'wiederholte nur die ohnehin geltende Rechtslage (DGUV V3) und war damit keine '
            'zusätzliche Schutzmaßnahme; die Mittelfristmaßnahme enthielt eine aus der '
            'entfallenen R1 übernommene DGUV-V3-Prüfung, die mit der Ursache „fehlender '
            'Stromlaufplan" nichts zu tun hat und die Zuständigkeit (5.35/5.37) verwischt. '
            'Bedingung und Stufe bleiben. Die Beschaffung der Schaltunterlagen bleibt '
            'organisatorisch [ORGA] – der Prüfentwurf hatte sie als [TECH] vorgeschlagen; '
            'ein Dokument ist keine technische Schutzmaßnahme.'),
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
   [r(eq('qm_sprechverbindung', 'keine'), 'MEDIUM', mfrom=('N20-K18', 'Keine Sprechverbindung'),
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Hoch auf Mittel. Die fehlende Sprechverbindung gefährdet das Wartungspersonal '
            'erst, wenn zusätzlich im Schacht gearbeitet wird und jemand unabgestimmt handelt; '
            'der eigentliche Schutz ist die Stoppeinrichtung, nicht die Sprechstelle. Dass die '
            'Regel selbst eine vollwertige organisatorische Kompensation nennt, bestätigt das. '
            'Zudem stellt die Norm die Anforderung unterhalb 30 m Förderhöhe gar nicht. '
            'Bedingung und beide Maßnahmen bleiben; die Anwendbarkeit über die Option '
            '„Verständigung ohne Hilfsmittel möglich" bleibt ebenfalls – eine Kopplung an '
            '> 30 m würde Anlagen unter 30 m ohne jede Verständigungsmöglichkeit '
            'herausfallen lassen (fail-open).'),
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
   [r(no('qm_rollenraum_nothalt'), 'HIGH',
      sofort='Arbeiten im Rollenraum nur bei freigeschalteter und gegen Wiedereinschalten gesicherter Anlage',
      mittel='Notbremsschalter (Stoppeinrichtung) im Rollenraum nachrüsten (DIN EN 81-20 5.12.1.11)',
      evidence='INFERRED', notes='Blaupause Schindler M049 (f132 Rollenraum).',
      pb='B13 – Maßnahme auf den Rollenraum bezogen')],
   sources=[en8120('5.2.6.4.5'), en8120('5.12.1.11')], factor=F_BEFEHL, persons=[WARTUNG], bereich='M')


hz('MF-M21', 'Fehlende oder unwirksame Notendschalter', GRP_SK,
   [('qm_notendschalter', 'TRIGGER', 'ALWAYS'),
    ('qm_notendschalter_getrennt', 'MODIFIER', 'CONDITIONAL',
     {'required_when': nin('qm_notendschalter', ['fehlt'])}),
    ('qm_notendschalter_verbindung_ueberwacht', 'MODIFIER', 'CONDITIONAL',
     {'required_when': nin('qm_notendschalter', ['fehlt'])})],
   [r(eq('qm_notendschalter', 'fehlt'), 'HIGH', prio=300,
      sofort='Anlage bis zur Instandsetzung stillsetzen; Überbrückungen entfernen',
      mittel='Notendschalter nach EN 81-20 5.12.2 einbauen und Wirksamkeit vor '
             'Pufferberührung nachweisen',
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_notendschalter_verbindung_ueberwacht'), 'HIGH', prio=250,
      sofort='Zustand von Seil, Riemen oder Kette der Notendschalter-Betätigung prüfen',
      mittel='Bruch und Schlaffwerden der Verbindung über eine elektrische '
             'Sicherheitseinrichtung überwachen (EN 81-20 5.12.2.2.3 b)',
      evidence='HIGH_CONFIDENCE'),
    r(no('qm_notendschalter_getrennt'), 'MEDIUM', prio=200,
      sofort='Betriebsmäßiges Anhalten und Notendschalter bei der Prüfung getrennt '
             'nachweisen',
      mittel='Getrennte Betätigungseinrichtungen herstellen (EN 81-20 5.12.2.2.1)',
      evidence='HIGH_CONFIDENCE'),
    r(eq('qm_notendschalter', 'ungeprueft'), 'MEDIUM', prio=100,
      sofort='Wirksamkeit der Notendschalter bei der nächsten Prüfung feststellen',
      mittel='Funktionsprüfung der Notendschalter in den Wartungsplan aufnehmen und '
             'dokumentieren',
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.12.2.1'), en8120('5.12.2.2.1'), en8120('5.12.2.2.3'),
            en8120('5.12.2.2.4')],
   factor=F_STOSS, persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='M',
   description='Notendschalter begrenzen den Fahrweg hinter den Endhaltestellen und müssen '
   'ansprechen, bevor Fahrkorb oder Gegengewicht die Puffer berühren (EN 81-20 5.12.2). '
   'Ergänzt EN 81-80 Nr. 57.')
