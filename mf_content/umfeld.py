# -*- coding: utf-8 -*-
"""U – Umfeld, Gebäude und Nutzung (Blaupause: Schindler Kundenbefragung
M087–M111 mit dem Ortsmatrix-Aufbau Zugang/Triebwerksraum/Schacht/Grube;
Inhalte aus der Ergänzung 2026 G1–G8)."""
from .common import *

GRP_BRAND = 'Brandschutz und Gebäudeschnittstelle'
GRP_U = 'Umfeld und Gefahrstoffe'
GRP_G = 'Schachtgrube'

# ---- Fragen: Ortsmatrix (Mangeltyp x Ort) ----------------------------------
# Jede Zeile wird im Fragebogen unter ihrem Ort erhoben (Z, M, S, G), die
# Gefährdung fasst die vier Orte zusammen (Aggregation ANY).
def ortsblock(stem, text, ui_z, ui_m, ui_s, ui_g):
    q('qz_%s' % stem, text % 'im Zugangsbereich zum Triebwerksraum', 'YES_NO', ui=ui_z)
    q('qm_%s' % stem, text % 'im Triebwerks-/Maschinenraum', 'YES_NO', ui=ui_m,
      visible_when=yes('qa_maschinenraum'))
    q('qs_%s' % stem, text % 'im Schacht / am Fahrkorb', 'YES_NO', ui=ui_s)
    q('qg_%s' % stem, text % 'in der Schachtgrube', 'YES_NO', ui=ui_g)
    return ['qz_%s' % stem, 'qm_%s' % stem, 'qs_%s' % stem, 'qg_%s' % stem]

ASBEST = ortsblock('asbest', 'Asbesthaltige oder andere schädliche Baustoffe %s '
                   '(Bremsbeläge, Dichtungen, Brandschutzplatten, Isolierungen)?',
                   '5.60', '5.61', '10.20', '11.20')
SCHMUTZ = ortsblock('verschmutzung', 'Erhebliche Verschmutzungen (Taubenkot, Unrat, '
                    'Schimmel, Ablagerungen) %s?', '5.62', '5.63', '10.21', '11.21')
BRENNBAR = ortsblock('brennbar_lager', 'Lagerung brennbarer oder leicht entzündlicher '
                     'Stoffe %s?', '5.64', '5.65', '10.22', '11.22')

# Regelprüfung 20.09.2026: Zustandsfrage je Fundort. Bisher gab JEDER Fund Hoch, unabhängig vom
# Zustand des Materials – auch eine unbeschädigte Asbestzement-Brandschutzplatte,
# die ohne Bearbeitung keine Fasern freisetzt. Das ist nach dem Stufenmaßstab
# „Gefahr erst bei zusätzlichem Ereignis", also Mittel; dass die Regel selbst
# keine Stilllegung, sondern nur ein Bearbeitungsverbot anordnete, bestätigte
# das. Fail-closed: „nicht beurteilbar" bleibt Hoch, sonst wäre die neue Regel
# schwächer als die alte. Die Frage ist Pflicht, sobald am Ort ein Fund
# gemeldet ist – bleibt sie unbeantwortet, ist die Gefährdung unvollständig.
_ZUSTAND = [
    ('fest', 'Fest gebunden und unbeschädigt (z. B. Asbestzementplatte, Dichtung, '
             'Brandschutzplatte ohne Bruchstellen)'),
    ('beschaedigt', 'Schwach gebunden, beschädigt oder abriebbelastet (Bruchstellen, '
                    'Abrieb, Staubablagerungen)'),
    ('unklar', 'Zustand nicht beurteilbar'),
]
_ZUSTAND_HILFE = (
    'Bewertet wird der Zustand, nicht die Menge. Fest gebunden und unbeschädigt heißt: '
    'keine Bruch-, Bohr- oder Schleifstellen, keine Abplatzungen, keine Staubablagerungen '
    'mit Abriebanteil. Im Zweifel „Zustand nicht beurteilbar" wählen – das ergibt '
    'dieselbe Einstufung wie ein beschädigter Fund. Die Zuordnung ersetzt keine '
    'Probenahme.')

sel('qz_asbest_zustand', 'Zustand des Fundes im Zugangsbereich zum Triebwerksraum',
    ui='5.60a', visible_when=yes('qz_asbest'), options=_ZUSTAND, help=_ZUSTAND_HILFE)
sel('qm_asbest_zustand', 'Zustand des Fundes im Triebwerks-/Maschinenraum', ui='5.61a',
    visible_when=yes('qm_asbest'),
    options=_ZUSTAND + [('bremsbelag', 'Asbesthaltige Bremsbeläge oder '
                                       'Bremsstaubablagerungen an Maschine oder Bremse')],
    help=_ZUSTAND_HILFE + ' Für den Triebwerksraum gibt es eine vierte Option: '
         'Asbesthaltige Bremsbeläge und Bremsstaub werden im bestimmungsgemäßen Betrieb '
         'bei jedem Halt abgerieben – die Freisetzung erfolgt ohne weiteres Zutun. Dieser '
         'Fall bleibt Hoch, unabhängig vom Zustand des übrigen Materials.')
sel('qs_asbest_zustand', 'Zustand des Fundes im Schacht / am Fahrkorb', ui='10.20a',
    visible_when=yes('qs_asbest'), options=_ZUSTAND,
    help=_ZUSTAND_HILFE + ' Im Fahrgastbereich wirkt kein Bearbeitungsverbot und der '
         'Personenkreis ist unkontrolliert – beschädigte oder abriebbelastete Verkleidungen '
         'im Fahrkorb bleiben deshalb Hoch.')
sel('qg_asbest_zustand', 'Zustand des Fundes in der Schachtgrube', ui='11.20a',
    visible_when=yes('qg_asbest'), options=_ZUSTAND,
    help=_ZUSTAND_HILFE + ' Ablagerungen und Staub mit Abriebanteil in der Grube gehören '
         'zu „schwach gebunden, beschädigt oder abriebbelastet" – Feuchte und Ablagerungen '
         'setzen beschädigtes Material dort eher frei.')

yn('qu_asbest_unbekannt', 'Ist die Asbest-/Schadstoffsituation der Anlage unbekannt '
   '(Baujahr vor 1995, keine Unterlagen, keine Beprobung)?', ui='15.11')
yn('qu_gefahrstoff_chem_lager', 'Chemische Gefahrstoffe in unmittelbarer Nähe der Anlage '
   'gelagert?', ui='15.28')
yn('qu_gefahrstoff_bio_lager', 'Biologische Arbeitsstoffe (Labor, Klinik, Entsorgung) in '
   'unmittelbarer Nähe der Anlage?', ui='15.29')
yn('qu_transport_chem', 'Transport chemischer Gefahrstoffe mit dem Aufzug?', ui='15.32')
yn('qu_transport_bio', 'Transport biologischer Arbeitsstoffe / infektiöser Stoffe mit dem '
   'Aufzug?', ui='15.33')
yn('qu_transport_brennbar', 'Transport brennbarer oder leicht entzündlicher Stoffe mit dem '
   'Aufzug?', ui='15.34')
yn('qu_transport_radioaktiv', 'Transport radioaktiver Stoffe mit dem Aufzug?', ui='15.35')
# Regelprüfung 20.09.2026: Kompensationsfragen zu 15.32 bis 15.35. Bisher bewertete MF-U05 eine
# NUTZUNGSART, keinen Mangel: Sobald Gefahrstoffe transportiert werden, entstand
# ein Mittel-Befund, der auch bei vorbildlicher Regelung nie wieder auf „Kein
# Risiko" fiel – in Kliniken, Laboren und Werkstätten also dauerhaft. Der Katalog
# kennt das richtige Muster bereits (MF-U06, MF-U12): Kompensationsfrage, Pflicht
# nur wenn die Transportfrage Ja ist, sonst entstünde eine Regellücke.
# Zielstufe bei erfüllter Kompensation ist NIEDRIG, nicht Kein Risiko: Der
# Transport bleibt auch geregelt ein Restrisiko mit Fortschreibungs- und
# Unterweisungspflicht (GefStoffV § 14); „Kein Risiko" ließe die Maßnahmen aus
# dem Bericht verschwinden.
yn('qu_transport_chem_geregelt',
   'Transport chemischer Gefahrstoffe verbindlich geregelt und unterwiesen (Behälter, '
   'Mengenbegrenzung, Mitfahrverbot Dritter, Verhalten bei Freisetzung)?', ui='15.32a',
   visible_when=yes('qu_transport_chem'),
   help='Ja nur, wenn die Regelung schriftlich vorliegt (Betriebsanweisung nach GefStoffV '
        '§ 14) UND die Beteiligten darin unterwiesen sind. Eine bloß mündliche Übung genügt '
        'nicht. Im Zweifel Nein.')
yn('qu_transport_bio_geregelt',
   'Transport biologischer Arbeitsstoffe verbindlich geregelt und unterwiesen (dichte, '
   'gekennzeichnete Transportbehälter festgelegt UND Reinigungs-/Desinfektionsverfahren '
   'für den Fahrkorb nach Kontamination festgelegt)?', ui='15.33a',
   visible_when=yes('qu_transport_bio'),
   help='Beide Punkte müssen erfüllt sein – Behälter allein genügen nicht, weil die '
        'Kontamination des Fahrkorbs der eigentliche Expositionspfad für das '
        'Wartungspersonal ist. Im Zweifel Nein.')
yn('qu_transport_brennbar_geregelt',
   'Transport brennbarer oder leicht entzündlicher Stoffe verbindlich geregelt und '
   'unterwiesen (Mengenbegrenzung, Behälter, Zündquellenverbot im Fahrkorb, Verhalten bei '
   'Freisetzung)?', ui='15.34a',
   visible_when=yes('qu_transport_brennbar'),
   help='Die Bewertung einer möglichen explosionsfähigen Atmosphäre gehört nicht hierher, '
        'sondern unter 15.25 (MF-U06) – dort ist der Transportfall als Anlass zu '
        'berücksichtigen. Im Zweifel Nein.')
yn('qu_transport_radioaktiv_geregelt',
   'Strahlenschutzanweisung liegt vor UND erfasst den Transport mit dem Aufzug (Behälter, '
   'Begleitung, Verhalten bei Kontamination)?', ui='15.35a',
   visible_when=yes('qu_transport_radioaktiv'),
   help='Eine allgemeine Strahlenschutzanweisung genügt nicht – sie muss den Aufzugstransport '
        'ausdrücklich erfassen und fortgeschrieben werden, und das Wartungspersonal ist über '
        'das Verhalten bei beschädigten Versandstücken zu unterweisen. Im Zweifel Nein.')
yn('qu_ex_moeglich', 'Kann sich im Bereich der Anlage ein explosionsfähiges Gemisch bilden '
   '(Gase, Dämpfe, Stäube)?', ui='15.25',
   help='Regelprüfung 20.09.2026: Auch der regelmäßige Transport von Lösemitteln oder Gasflaschen mit dem Aufzug '
        '(15.34) ist hier zu berücksichtigen – er kann im Fahrkorb selbst eine '
        'explosionsfähige Atmosphäre erzeugen. Die Explosionsschutzbewertung gehört dann in '
        'diese Gefährdung, nicht in MF-U05.')
yn('qu_ex_bewertet', 'Explosionsschutz für die Aufzugsanlage bewertet und dokumentiert '
   '(Explosionsschutzdokument)?', ui='15.25a', visible_when=yes('qu_ex_moeglich'))
yn('qu_ex_umgesetzt', 'Festgelegte Ex-Schutzmaßnahmen an der Aufzugsanlage umgesetzt und auf '
   'Wirksamkeit geprüft (geeignete Betriebsmittel, Prüfung vor Inbetriebnahme/wiederkehrend)?',
   ui='15.25b', visible_when=yes('qu_ex_bewertet'))
yn('qu_temperatur', 'Unzulässige Temperaturen im Triebwerksraum oder Schacht möglich '
   '(Überhitzung über 40 °C, Frost)?', ui='15.23')
yn('qu_feuchte_sicherheitsteile', 'Feuchtigkeit oder Kondensat an sicherheitsrelevanten '
   'Bauteilen außerhalb der Schachtgrube (Steuerung, Bremse, Türverriegelung)?', ui='15.23a',
   help='Wasser und Feuchtigkeit IN der Schachtgrube werden unter 11.15 erfasst – hier nur '
        'Triebwerksraum, Schacht und Fahrkorb (Prüfbericht 20.09.2026: Abgrenzung geschärft, '
        'beide Fragen führten zuvor zur selben Stufe mit derselben Maßnahme).')
yn('qu_korrosion', 'Massive Korrosion, Betonabplatzungen oder andere bauliche Schäden am '
   'Schacht oder Triebwerksraum?', ui='15.23b')
yn('qu_bauliche_aenderung', 'Bauliche Änderungen am Schacht / Triebwerksraum ohne statische '
   'und sicherheitstechnische Bewertung?', ui='15.26')
yn('qu_verkleidung', 'Nachträgliche Verkleidungen oder Änderungen, die den Sicherheitszustand '
   'verschlechtern (Schutzräume, Lüftung, Zugänge)?', ui='15.26a')
yn('qu_bma_abgestimmt', 'Schnittstelle Brandmeldeanlage – Aufzug bekannt und abgestimmt '
   '(Brandfallsteuerung, Rückholung, Evakuierung)?', ui='15.8a',
   visible_when=yes('qa_bma_vorhanden'))
yn('qu_bma_geprueft', 'Funktion der Schnittstelle BMA – Aufzug geprüft (Nachweis)?',
   ui='15.8b', visible_when=yes('qu_bma_abgestimmt'))
yn('qu_evak_in_gbu', 'Evakuierungs-/Sonderfunktion des Aufzugs im Brandschutzkonzept und in '
   'der Betriebsanweisung beschrieben (wer den Aufzug im Brandfall wie benutzen darf)?',
   ui='15.8c', visible_when=yes('qa_bma_vorhanden'),
   help='Prüfbericht 20.09.2026: Die Frage lautete bisher „… in dieser Gefährdungsbeurteilung '
        'berücksichtigt?" und bewertete damit das eigene Dokument. Gefragt ist jetzt die '
        'Festlegung des Betreibers, die vor Ort prüfbar ist.')
sel('qu_brandschutz_behindert', 'Behindert eine Brandschutzeinrichtung (Brandschutztür, '
    'Abschottung) den Aufzugsbetrieb oder die Personenrettung?', ui='15.8d',
    options=[('nein', 'Keine Behinderung'),
             ('rettung', 'Zugang zur Anlage, Notentriegelung, Schachttür oder Rettungsweg '
                         'behindert – oder nicht sicher beurteilbar'),
             ('betrieb', 'Nur der Aufzugsbetrieb behindert, Rettungszugang und Rettungsweg '
                         'nachweislich frei')],
    help='Regelprüfung 20.09.2026: Aus der Ja/Nein-Frage geworden. Sie bündelte die behinderte '
         'Personenrettung (unmittelbare Gefahr bei Einschluss – Hoch) mit der reinen '
         'Betriebsbehinderung (etwa eine Abschottung, die den Zugang verengt, oder eine '
         'Brandschutztür, die gegen die Schachttür schlägt) und bewertete beides mit Hoch. '
         'Fail-closed: Der nicht sicher beurteilbare Fall gehört ausdrücklich zur Option '
         '„Rettung behindert", damit keine Absenkung durch Unsicherheit entsteht.')
sel('qu_entrauchung', 'Zustand der Schachtentrauchung / RWA / Lüftungsöffnung', ui='15.9a',
    options=[('ok', 'Funktion geprüft, Öffnungen frei'),
             ('gestoert', 'Entrauchung / RWA blockiert oder defekt'),
             ('veraendert', 'Öffnungen verschlossen, verändert oder unzureichend'),
             ('kein_nachweis', 'Funktion unklar oder kein Nachweis über Prüfung')],
    visible_when=yes('qa_entrauchung_vorhanden'),
    help='Regelprüfung 20.09.2026: Die frühere Option „Funktion unklar, blockiert oder defekt" ist '
         'geteilt. „Unklar" beschreibt keinen festgestellten Mangel, sondern eine fehlende '
         'Feststellung – eine RWA-Auslösung ist ohne Auslöseversuch vor Ort oft nicht '
         'beurteilbar. Ein Prüfer, der ehrlich „unklar" wählte, erzeugte damit zwingend Hoch; '
         'das drängte zum Ausweichen auf „kein Nachweis". „Unklar" steht jetzt bei '
         '„kein Nachweis", der festgestellte Defekt bei „blockiert oder defekt".')
yn('qu_sprinkler_abschaltung', 'Ist sichergestellt, dass die Energieversorgung des Aufzugs '
   'vor Wasserbeaufschlagung abgeschaltet wird (Auslösekontakt der Löschanlage bzw. '
   'Abschaltung vorhanden)?', ui='15.10a', visible_when=yes('qa_sprinkler_vorhanden'),
   help='Regelprüfung 20.09.2026: Die Frage lautete „Wechselwirkung … bewertet?" und bewertete damit '
        'einen Dokumentationszustand – derselbe Fehlertyp, der bei 15.8c bereits korrigiert '
        'wurde. Gefragt ist jetzt der vor Ort prüfbare Sachverhalt. Im Zweifel Nein.')
yn('qu_sprinkler_geprueft', 'Wirksamkeit der Abschaltung geprüft und dokumentiert?',
   ui='15.10b', visible_when=yes('qu_sprinkler_abschaltung'),
   help='Regelprüfung 20.09.2026: Nachweis der Wirk-Prinzip-Prüfung. Getrennt von 15.10a, damit der '
        'fehlende Nachweis nicht dieselbe Stufe bekommt wie die fehlende Abschaltung.')
yn('qu_wartung_gefaehrlicher_zugang', 'Müssen Fremdgewerke (Lüftung, Elektro, Reinigung) '
   'für ihre Arbeiten in den Aufzugsbereich (Schacht, Triebwerksraum) eindringen?', ui='15.36')
yn('qu_fremd_zugangskonzept', 'Zugangs- und Schutzkonzept für Fremdgewerke / '
   'Reinigungspersonal vorhanden?', ui='15.36a',
   visible_when=yes('qu_wartung_gefaehrlicher_zugang'))
yn('qu_nachweise_fremdgewerke', 'Prüfnachweise der angrenzenden Gewerke (BMA, RWA, '
   'Ersatzstrom, Löschanlage) verfügbar?', ui='15.37')
yn('qu_zustaendigkeit', 'Zuständigkeiten zwischen den Gewerken für Maßnahmen an den '
   'Schnittstellen geregelt?', ui='15.38')
yn('qu_verkehrswege', 'Grenzt der Aufzugszugang unmittelbar an Fahrwege oder Verkehrsflächen '
   '(Tiefgarage, Anlieferung, Flurförderzeuge)?', ui='15.27')
yn('qu_abgase', 'Abgase oder Emissionen im Aufstellbereich (Tiefgarage, Werkstatt, '
   'Notstromaggregat)?', ui='15.24')
yn('qu_abgase_lueftung', 'Wirksame Lüftung oder Absaugung des Aufstellbereichs vorhanden und '
   'nachgewiesen (Garagenverordnung, ASR A3.6)?', ui='15.24a',
   visible_when=yes('qu_abgase'),
   help='Regelprüfung 20.09.2026: Kompensationsfrage. Die Regel löste bisher allein daraus aus, dass '
        'der Aufstellbereich eine Tiefgarage, Werkstatt oder ein Notstromaggregat-Raum ist – '
        'also auch dann, wenn die geforderte maschinelle Lüftung wirksam vorhanden und der '
        'Soll-Zustand erfüllt ist. Ja nur mit Nachweis (Abnahme, wiederkehrende Prüfung); im '
        'Zweifel Nein.')
yn('qu_laerm', 'Erhöhte Lärmbelastung im Triebwerksraum oder am Aufzug (über 85 dB(A))?',
   ui='15.22')
sel('qu_unfaelle', 'Unfälle oder gefährliche Ereignisse an der Anlage in den letzten Jahren',
    ui='15.30',
    options=[('keine', 'Keine bekannt'),
             ('sachschaden', 'Ereignisse mit Sachschaden'),
             ('personenschaden', 'Unfälle mit Personenschaden')])
yn('qu_umfeld_kritisch', 'Kritisches soziales Umfeld (Vandalismus, Missbrauch der Anlage)?',
   ui='15.4')

# ---- Klärungen -------------------------------------------------------------
k('K-U01', 'Umfeld', 'Ortsfragen Pflicht oder optional',
  'Sollen die vier Ortsfragen (Zugang / Triebwerksraum / Schacht / Grube) je Mangeltyp '
  'alle beantwortet sein, bevor die Gefährdung bewertet wird (Pflicht -> sonst Unvollständig)?',
  'Ja, alle Pflicht (ehrlicher Stand)', 'Nein, eine Ja-Antwort genügt, Rest optional '
  '(Schindler-Verhalten M087/M090/M103)', 'Bewusste Abweichung vom Original.')
k('K-U02', 'Umfeld', 'Gefahrstofflagerung',
  'Chemische / biologische Gefahrstoffe in der Nähe gelagert: Niedrig (Schindler M101/M102) – '
  'oder Mittel wie bei brennbaren Stoffen?', 'Niedrig', 'Mittel', 'Nur aus Schindler ableitbar; '
  'die Ergänzung 2026 (G5) kennt nur Hoch für „unbekannt/unbewertet".')
k('K-U03', 'Umfeld', 'Explosionsfähiges Gemisch',
  'Explosionsfähiges Gemisch möglich, Explosionsschutz bewertet: Mittel? Nicht bewertet: Hoch?',
  'Mittel / Hoch', 'Immer Mittel (Schindler M092)', 'Ergänzung 2026 G5 sagt Hoch für „ohne Bewertung".')
k('K-U04', 'Umfeld', 'Lärm und Unfallhistorie',
  'Lärm (Niedrig), Unfälle mit Sachschaden (Niedrig) und mit Personenschaden (Hoch) sind '
  'aus der Schindler-Kundenbefragung übernommen – sinnvoll für die eigene GBU?', 'Übernehmen',
  'Nur dokumentieren, keine Stufe', 'Im App-Katalog nicht enthalten.')
k('K-U05', 'Umfeld', 'Angrenzende Verkehrswege',
  'Aufzugszugang an Fahrwegen: Mittel nur bei Nutzung durch Personen mit eingeschränkter '
  'Mobilität (Schindler M106) – oder immer Mittel?', 'Immer Mittel, Hoch mit PmeM-Nutzung',
  'Nur mit PmeM-Nutzung', 'Eigene Verschärfung.')

# ---- Gefährdungen ----------------------------------------------------------
# Gefährdungsspezifische Maßnahmen statt der generischen Schnittstellen-Texte
# aus der Ergänzung 2026 (Prüfbericht 15.09.2026, H07).
MU = {
    'asbest': ('Keine Tätigkeiten, die das Material beschädigen (Bohren, Schleifen, Stemmen); '
               'Fundstelle kennzeichnen und Betreiber schriftlich informieren',
               'Fundstelle durch Sachkundige nach TRGS 519 bewerten und sanieren lassen; '
               'Tätigkeiten bis dahin nur nach TRGS 519'),
    'asbest_unbekannt': ('Vor Tätigkeiten, die Baustoffe beschädigen können, Schadstoffsituation klären; '
                         'bis dahin solche Tätigkeiten unterlassen',
                         'Schadstofferkundung (Probenahme) durch Sachkundige veranlassen und das Ergebnis '
                         'in dieser Gefährdungsbeurteilung nachtragen'),
    'schmutz': ('Bereich nur mit geeigneter Schutzausrüstung (Handschuhe, bei Taubenkot/Schimmel '
                'Atemschutz FFP3) betreten; Betreiber zur Reinigung auffordern',
                'Reinigung veranlassen (bei Taubenkot/Schimmel durch Fachfirma) und Ursache abstellen '
                '(Abdichtung, Taubenabwehr)'),
    'brennbar': ('Brennbare Stoffe aus dem Aufzugsbereich entfernen lassen; keine Zündquellen',
                 'Lagerverbot für brennbare Stoffe im Aufzugsbereich in der Betriebsanweisung festlegen '
                 'und bei der Betreiberkontrolle prüfen'),
    'wasser': ('Anlage bei Wasser in der Grube oder an Sicherheitsbauteilen außer Betrieb nehmen; '
               'Ursache mit dem Betreiber klären',
               'Wassereintritt beseitigen (Abdichtung, Pumpensumpf) und betroffene Bauteile prüfen lassen'),
    'korrosion': ('Tragende und sicherheitsrelevante Bauteile auf Tragfähigkeit prüfen; bei Zweifel '
                  'Anlage außer Betrieb nehmen',
                  'Bauliche Schäden durch Fachbetrieb instand setzen und Standsicherheit nachweisen lassen'),
    'temperatur': ('Raumtemperatur messen; bei Überschreitung Betrieb nach Herstellervorgaben einschränken',
                   'Lüftung/Kühlung bzw. Frostschutz im Triebwerksraum oder Schacht herstellen'),
    'oel': ('Austretendes Öl binden und entsorgen; Leckage suchen',
            'Leckage beseitigen und Auffangwanne bzw. Ölabscheider vorsehen'),
    'bau_aenderung': ('Betreiber auffordern, Umfang und Bewertung der baulichen Änderung vorzulegen; '
                      'bei Zweifel an der Standsicherheit Anlage außer Betrieb nehmen',
                      'Statische und sicherheitstechnische Bewertung der Änderung durch Fachplaner und ZÜS '
                      'veranlassen'),
    'verkleidung': ('Auswirkung der Verkleidung auf Schutzräume, Lüftung und Zugänge prüfen',
                    'Verkleidung zurückbauen oder Zustand durch die ZÜS bewerten lassen'),
    'bma_abstimmung': ('Brandfallsteuerung mit dem Betreiber und dem Brandschutzbeauftragten abstimmen',
                       'Ansteuerung aus der BMA gemäß Brandschutzkonzept herstellen und dokumentieren'),
    'bma_pruefung': ('Funktionsprüfung der Schnittstelle BMA – Aufzug kurzfristig veranlassen',
                     'Wirk-Prinzip-Prüfung nach Prüfverordnung des Landes in den Prüfplan aufnehmen'),
    # Regelprüfung 20.09.2026: Beide Maßnahmen neu gefasst. Die alte Sofortmaßnahme lief bei der
    # Mehrzahl der Anlagen ins Leere (ein Aufzug ohne Evakuierungs- oder
    # Feuerwehrfunktion hat keine „Evakuierungsfunktion", die man nicht nutzen
    # könnte), und die Mittelfristmaßnahme bewertete mit „in diese GBU
    # aufnehmen" wieder das eigene Dokument – genau der Fehler, wegen dessen
    # die Frage geändert wurde. Die Fundstelle DIN EN 81-76 ist als CEN/TS
    # 81-76 bzw. DIN EN 81-72 berichtigt.
    'evak': ('Betreiber unterrichten; bis zur Festlegung gilt der Aufzug im Brandfall als nicht '
             'benutzbar – Vorhandensein und Lesbarkeit des Verbotszeichens „Im Brandfall Aufzug '
             'nicht benutzen" (ASR A1.3 / ISO 7010 P020) an allen Haltestellen prüfen; nur bei '
             'Anlagen mit Evakuierungs- oder Feuerwehrfunktion zusätzlich Feuerwehr bzw. '
             'Brandschutzbeauftragten informieren',
             'Festlegung im Brandschutzkonzept und in der Betriebsanweisung treffen lassen '
             '(Benutzungsverbot im Brandfall bzw. – bei Evakuierungs- oder Feuerwehraufzügen – '
             'Evakuierungsbetrieb nach CEN/TS 81-76 bzw. DIN EN 81-72) mit Angabe, wer den '
             'Aufzug wie benutzen darf; fehlende Kennzeichnung nachrüsten'),
    'brandschutz_behindert': ('Behinderung sofort beseitigen lassen (Tür, Abschottung); Betreiber informieren',
                              'Brandschutzeinrichtung und Aufzug so abstimmen, dass sich beide nicht behindern'),
    'entrauchung_unklar': ('Funktion der Entrauchung/RWA kurzfristig prüfen lassen; Feuerwehr informieren',
                           'Entrauchung instand setzen und Prüfnachweis vorlegen lassen'),
    'entrauchung_veraendert': ('Veränderte Öffnung dem Betreiber melden',
                               'Öffnungsquerschnitt nach Brandschutzkonzept wiederherstellen'),
    'entrauchung_nachweis': ('Prüfnachweis beim Betreiber anfordern',
                             'Wiederkehrende Prüfung der Entrauchung in den Prüfplan aufnehmen'),
    'sprinkler': ('Betreiber auf die fehlende Bewertung hinweisen; Wasserschutz der Steuerung prüfen',
                  'Wechselwirkung Löschanlage – Aufzug (Abschaltung vor Wasserbeaufschlagung) bewerten '
                  'und umsetzen lassen'),
    'fremd_zugang': ('Fremdgewerke erst nach Einweisung und Freischaltung der Anlage in den Schacht oder '
                     'Triebwerksraum lassen',
                     'Zugangs- und Schutzkonzept für Fremdgewerke erstellen (Anmeldung, Freischaltung, '
                     'Aufsicht durch Aufzugsfachpersonal)'),
    'nachweise': ('Fehlende Prüfnachweise beim Betreiber anfordern',
                  'Übersicht der aufzugsexternen Sicherheitseinrichtungen mit Prüffristen führen '
                  '(TRBS 3121 Abschnitt 3.2 Nr. 5)'),
    'zustaendigkeit': ('Ansprechpartner je Gewerk beim Betreiber erfragen',
                       'Zuständigkeiten an den Schnittstellen schriftlich festlegen'),
}

_PB_U = 'H07 – gefährdungsspezifische Maßnahmen statt generischer Schnittstellen-Texte'


# Ortsangabe je Frage der Ortsmatrix. Prüfbericht 20.09.2026: Die vier Regeln
# einer Ortsgefährdung trugen bisher denselben Maßnahmentext – bei der
# Aggregation ANY erscheinen im Bericht bis zu vier identische Zeilen, ohne dass
# erkennbar wäre, WO zu reinigen, zu räumen oder zu sanieren ist.
ORT = {'qz_': 'Zugangsbereich zum Triebwerksraum', 'qm_': 'Triebwerks-/Maschinenraum',
       'qs_': 'Schacht / Fahrkorb', 'qg_': 'Schachtgrube'}


def _ort(code):
    return ORT.get(code[:3], '')


def _ortshazard(code, title, qs, result, mfrom_, extra_q=(), extra_rules=(), factor=F_GEFAHRSTOFF,
                persons=(WARTUNG, BEAUFTRAGTE), group=GRP_U, sources=(), massn=None):
    hqs = [(x, 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_maschinenraum')})
           if x.startswith('qm_') else (x, 'TRIGGER', 'ALWAYS') for x in qs] + list(extra_q)
    so, mi = MU[massn] if massn else (None, None)
    rules = [r(yes(x), result, mfrom=mfrom_,
               sofort=('%s: %s' % (_ort(x), so)) if so else None,
               mittel=('%s: %s' % (_ort(x), mi)) if mi else None,
               evidence='INFERRED',
               klaerung='K-U01', pb=_PB_U if massn else None) for x in qs]
    rules += list(extra_rules)
    hz(code, title, group, hqs, rules, sources=sources, factor=factor, persons=list(persons),
       agg='ANY', mode='STANDARD', bereich='U')

# Regelprüfung 20.09.2026: MF-U01 wird nicht mehr über _ortshazard gebaut, weil die Stufe jetzt am
# Zustand des Fundes hängt und nicht mehr allein am Fund. Je Ort zwei Regeln:
# fest gebunden und unbeschädigt -> Mittel, beschädigt oder nicht beurteilbar
# -> Hoch. Im Triebwerksraum kommt der Bremsbelag-Fall mit eigener Priorität
# und eigener Sofortmaßnahme hinzu.
_ASB_SO, _ASB_MI = MU['asbest']

def _asbest_regeln():
    aus = []
    for x in ASBEST:
        ort = _ort(x)
        zst = x + '_zustand'
        if x.startswith('qm_'):
            aus.append(r(all_(yes(x), eq(zst, 'bremsbelag')), 'HIGH', prio=300,
                         mfrom=('E26-G5', 'Asbest'),
                         sofort='%s: Keine trockene Reinigung, kein Ausblasen; Bremsstaub nur '
                                'mit Staubsauger der Staubklasse H aufnehmen. Keine Tätigkeiten '
                                'an Bremse oder Belägen; Fundstelle kennzeichnen und Betreiber '
                                'schriftlich informieren' % ort,
                         mittel='%s: Asbesthaltige Bremsbeläge durch Sachkundige nach TRGS 519 '
                                'austauschen und den Raum fachgerecht reinigen lassen; '
                                'Tätigkeiten bis dahin nur nach TRGS 519' % ort,
                         evidence='HIGH_CONFIDENCE', klaerung='K-U01',
                     pb='Regelprüfung 20.09.2026 – Zustandsabstufung neu, Klärung K-U01 deckt den '
                        'geänderten Inhalt nicht mehr',
                         notes='Regelprüfung 20.09.2026: Asbesthaltige Bremsbeläge und Bremsstaub werden im '
                               'bestimmungsgemäßen Betrieb bei jedem Halt abgerieben – die '
                               'Freisetzung erfolgt ohne weiteres Zutun. Dieser Fall bleibt '
                               'Hoch, unabhängig vom Zustand des übrigen Materials, und '
                               'bekommt eine eigene Sofortmaßnahme (Staubklasse H).'))
        zusatz = ''
        if x.startswith('qs_'):
            zusatz = ('; Fahrkorb bis zur Bewertung außer Betrieb nehmen oder beschädigte '
                      'Verkleidung staubdicht sichern')
        elif x.startswith('qg_'):
            zusatz = ('; Grube nicht trocken kehren oder ausblasen, Reinigung nur nass oder '
                      'mit Sauger der Staubklasse H, bis die Beprobung vorliegt')
        aus.append(r(all_(yes(x), in_(zst, ['beschaedigt', 'unklar'])), 'HIGH', prio=200,
                     mfrom=('E26-G5', 'Asbest'),
                     sofort='%s: %s%s' % (ort, _ASB_SO, zusatz),
                     mittel='%s: Fundstelle durch Sachkundige nach der für den festgestellten '
                            'Stoff einschlägigen TRGS (TRGS 519 Asbest, TRGS 521 künstliche '
                            'Mineralfasern, TRGS 524 Arbeiten in kontaminierten Bereichen) '
                            'bewerten und sanieren lassen; Tätigkeiten bis dahin nur nach '
                            'dieser TRGS' % ort,
                     evidence='HIGH_CONFIDENCE', klaerung='K-U01',
                     pb='Regelprüfung 20.09.2026 – Zustandsabstufung neu, Klärung K-U01 deckt den '
                        'geänderten Inhalt nicht mehr',
                     notes='Regelprüfung 20.09.2026: Hoch bleibt für beschädigtes, schwach gebundenes oder '
                           'abriebbelastetes Material – und ausdrücklich auch für den nicht '
                           'beurteilbaren Zustand (fail-closed: die Abstufung darf nicht '
                           'dazu führen, dass ein ungeprüfter Fund günstiger bewertet wird '
                           'als vorher). Der Maßnahmentext nennt nicht mehr nur die TRGS 519, '
                           'sondern die für den festgestellten Stoff einschlägige TRGS; auf '
                           'die Asbest-Richtlinie wird bewusst nicht verwiesen, sie ist in '
                           'mehreren Ländern zurückgezogen.'))
        aus.append(r(all_(yes(x), eq(zst, 'fest')), 'MEDIUM', prio=100,
                     mfrom=('E26-G5', 'Asbest'),
                     sofort='%s: %s' % (ort, _ASB_SO),
                     mittel='%s: Fund in das Gebäudeschadstoffkataster aufnehmen und dauerhaft '
                            'kennzeichnen; Zustandsbewertung und wiederkehrende Zustands'
                            'kontrolle durch Sachkundige veranlassen; bei Tätigkeiten am '
                            'Material die einschlägige TRGS (519/521/524) anwenden' % ort,
                     evidence='HIGH_CONFIDENCE', klaerung='K-U01',
                     pb='Regelprüfung 20.09.2026 – Zustandsabstufung neu, Klärung K-U01 deckt den '
                        'geänderten Inhalt nicht mehr',
                     notes='Regelprüfung 20.09.2026: Hoch auf Mittel für den fest gebundenen, unbeschädigten Fund: '
                           'Er setzt ohne Bearbeitung keine Fasern frei, die Gefahr entsteht '
                           'erst bei einem zusätzlichen Ereignis. Die Maßnahmen bleiben auf '
                           'Mittel-Niveau (Bearbeitungsverbot, Kennzeichnung, Kataster, '
                           'wiederkehrende Zustandskontrolle) – eine Stilllegung ordnete auch '
                           'die alte Hoch-Regel nicht an.'))
    return aus

hz('MF-U01', 'Asbesthaltige oder andere schädliche Baustoffe im Bereich der Anlage', GRP_U,
   [(x, 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_maschinenraum')})
    if x.startswith('qm_') else (x, 'TRIGGER', 'ALWAYS') for x in ASBEST]
   + [(x + '_zustand', 'TRIGGER', 'CONDITIONAL', {'required_when': yes(x)}) for x in ASBEST]
   + [('qu_asbest_unbekannt', 'TRIGGER', 'ALWAYS')],
   _asbest_regeln()
   + [r(yes('qu_asbest_unbekannt'), 'MEDIUM', sofort=MU['asbest_unbekannt'][0],
        mittel=MU['asbest_unbekannt'][1], evidence='HIGH_CONFIDENCE',
        pb='H06 – Unsicherheit ist kein bestätigter Befund: Mittel mit Erkundung statt Hoch mit Stillsetzung')],
   sources=[law('GefStoffV', '§ 6'), trbs('TRGS 519'), trbs('TRGS 521'), trbs('TRGS 524')],
   factor=F_GEFAHRSTOFF, persons=[WARTUNG, BEAUFTRAGTE, NUTZER], agg='ANY', bereich='U')

_ortshazard('MF-U02', 'Erhebliche Verschmutzungen im Bereich der Anlage', SCHMUTZ, 'MEDIUM',
            ('E26-G5', 'Kontaminierter'),
            factor=F_GEFAHRSTOFF, sources=[law('BioStoffV'), trbs3121('Anh. 1 Nr. 5')], massn='schmutz')

_ortshazard('MF-U03', 'Lagerung brennbarer oder leicht entzündlicher Stoffe im Bereich der Anlage',
            BRENNBAR, 'MEDIUM', ('E26-G5', 'Kontaminierter'),
            factor=F_BRAND, persons=(NUTZER, WARTUNG, BEAUFTRAGTE),
            sources=[law('BetrSichV', '§ 3'), trbs('TRGS 800')], massn='brennbar')

hz('MF-U04', 'Chemische oder biologische Gefahrstoffe in unmittelbarer Nähe der Anlage gelagert',
   GRP_U,
   [('qu_gefahrstoff_chem_lager', 'TRIGGER', 'ALWAYS'),
    ('qu_gefahrstoff_bio_lager', 'TRIGGER', 'ALWAYS')],
   [r(yes('qu_gefahrstoff_chem_lager'), 'MEDIUM',
      sofort='Lagerung mit dem Betreiber klären, Sicherheitsdatenblätter einsehen',
      mittel='Gefahrstofflagerung aus dem Aufzugsbereich verlegen oder in die Betriebsanweisung aufnehmen',
      evidence='INFERRED', klaerung='K-U02'),
    r(yes('qu_gefahrstoff_bio_lager'), 'MEDIUM',
      sofort='Hygiene-/Schutzmaßnahmen für Wartungspersonal mit dem Betreiber abstimmen',
      mittel='Umgang mit biologischen Arbeitsstoffen im Aufzugsbereich in der Betriebsanweisung regeln',
      evidence='INFERRED', klaerung='K-U02')],
   sources=[law('GefStoffV'), law('BioStoffV')], factor=F_GEFAHRSTOFF, persons=[WARTUNG, BEAUFTRAGTE],
   agg='MAXIMUM', bereich='U')

# Regelprüfung 20.09.2026: Je Stoffgruppe eine Kompensationsregel. Ohne verbindliche Regelung bleibt
# es bei Mittel (Bedingung, Stufe und Maßnahmen wie bisher); mit Regelung
# Niedrig statt Kein Risiko – die Fortschreibung und die Unterweisung bleiben
# geschuldet und sollen im Bericht stehen. Bleibt die Kompensationsfrage
# unbeantwortet, obwohl transportiert wird, ist die Gefährdung unvollständig.
_U05 = [
    ('chem', 'qu_transport_chem',
     'Transportregeln (Behälter, Begleitung, Nutzung durch Dritte) mit dem Betreiber festlegen',
     'Lüftung des Fahrkorbs und Verhalten bei Freisetzung in der Betriebsanweisung regeln',
     'Betriebsanweisung für den Transport chemischer Gefahrstoffe bei Änderung von Stoffen '
     'oder Mengen fortschreiben und die Unterweisung wiederholen (GefStoffV § 14)'),
    ('bio', 'qu_transport_bio',
     'Transport nur in dichten, gekennzeichneten Behältern; Fahrkorb nach Kontamination reinigen',
     'Reinigungs- und Desinfektionsplan für den Fahrkorb festlegen',
     'Wirksamkeit des Reinigungs- und Desinfektionsplans kontrollieren und ihn bei geänderten '
     'Stoffen fortschreiben; Unterweisung wiederholen'),
    ('brennbar', 'qu_transport_brennbar',
     'Transportmengen begrenzen, Zündquellen im Fahrkorb ausschließen',
     'Mengenbegrenzung, Behälter, Lüftung des Fahrkorbs und Verhalten bei Freisetzung in der '
     'Betriebsanweisung regeln; die Bewertung einer explosionsfähigen Atmosphäre gehört '
     'unter 15.25 (MF-U06)',
     'Mengenbegrenzung und Zündquellenverbot bei der Betreiberkontrolle stichprobenartig '
     'prüfen; Bewertung nach 15.25 (MF-U06) bei geänderter Nutzung wiederholen'),
    ('radioaktiv', 'qu_transport_radioaktiv',
     'Strahlenschutzbeauftragten einbinden, Transport nur nach Strahlenschutzanweisung',
     'Regelung des Transports radioaktiver Stoffe in der Betriebsanweisung',
     'Strahlenschutzanweisung fortschreiben und das Wartungspersonal über das Verhalten bei '
     'beschädigten Versandstücken unterweisen'),
]

hz('MF-U05', 'Transport von Gefahrstoffen mit der Aufzugsanlage', GRP_U,
   [(qc, 'TRIGGER', 'ALWAYS') for _s, qc, _a, _b2, _c in _U05]
   + [(qc + '_geregelt', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes(qc)})
      for _s, qc, _a, _b2, _c in _U05],
   [x for _s, qc, so, mi, erh in _U05 for x in (
       r(all_(yes(qc), no(qc + '_geregelt')), 'MEDIUM', prio=100,
         sofort=so, mittel=mi, evidence='INFERRED',
         notes='Regelprüfung 20.09.2026: Bedingung um die Kompensation ergänzt. Vorher bewertete die Regel die '
               'Nutzungsart und nicht den Mangel: Sobald transportiert wurde, entstand ein '
               'Mittel-Befund, der auch bei vorbildlicher Regelung nie wieder verschwand. '
               'Stufe und Maßnahmen bleiben für den ungeregelten Fall unverändert.'),
       r(all_(yes(qc), yes(qc + '_geregelt')), 'LOW', prio=200,
         sofort='Vorhandene Regelung anwenden; Abweichungen dem Betreiber melden',
         mittel=erh, evidence='INFERRED',
         notes='Regelprüfung 20.09.2026: Neue Kompensationsregel. Zielstufe ist ausdrücklich Niedrig und nicht Kein '
               'Risiko: Der Transport bleibt auch geregelt ein Restrisiko mit Fortschreibungs- '
               'und Unterweisungspflicht; bei Kein Risiko verschwänden diese Maßnahmen aus dem '
               'Bericht.'))],
   sources=[law('GefStoffV', '§ 14'), law('StrlSchV'), law('BioStoffV')], factor=F_GEFAHRSTOFF,
   persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='U')

hz('MF-U06', 'Explosionsfähiges Gemisch kann durch die Aufzugsanlage gezündet werden', GRP_U,
   [('qu_ex_moeglich', 'TRIGGER', 'ALWAYS'),
    ('qu_ex_bewertet', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes('qu_ex_moeglich')}),
    ('qu_ex_umgesetzt', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes('qu_ex_bewertet')})],
   [r(all_(yes('qu_ex_moeglich'), yes('qu_ex_bewertet'), no('qu_ex_umgesetzt')), 'HIGH', prio=210,
      sofort='Betrieb der Anlage im betroffenen Bereich bis zur Umsetzung der festgelegten '
             'Schutzmaßnahmen einstellen oder nur nach schriftlicher Freigaberegelung des '
             'Betreibers zulassen, Betreiber unverzüglich schriftlich unterrichten; daneben '
             'keine Arbeiten mit Zündquellen ohne Erlaubnisschein',
      mittel='Festgelegte Ex-Schutzmaßnahmen umsetzen und ihre Wirksamkeit vor der weiteren Nutzung prüfen lassen',
      evidence='HIGH_CONFIDENCE', pb='Prüfbericht 16.09.2026 – Dokumentation allein ist keine Schutzmaßnahme (§ 6 GefStoffV, § 4 BetrSichV)',
      notes='Regelprüfung 20.09.2026: Sofortmaßnahme ergänzt. Sie deckte nur die Zündquelle „Fremdarbeit" ab, '
            'während die Gefährdung darin besteht, dass die Aufzugsanlage selbst im Ex-Bereich '
            'betrieben wird und ungeeignete Betriebsmittel enthält – bei Stufe Hoch blieb die '
            'Gefahr damit unbeantwortet. Bedingung, Stufe und Priorität bleiben.'),
    r(all_(yes('qu_ex_moeglich'), yes('qu_ex_bewertet'), yes('qu_ex_umgesetzt')), 'MEDIUM', prio=200,
      sofort='Festgelegte Ex-Schutzmaßnahmen einhalten, Zündquellen an der Anlage prüfen',
      mittel='Explosionsschutzdokument bei Änderungen an Anlage oder Nutzung fortschreiben',
      evidence='INFERRED', klaerung='K-U03'),
    r(yes('qu_ex_moeglich'), 'HIGH', prio=100,
      sofort='Betreiber unverzüglich schriftlich unterrichten; bis zur Vorlage der '
             'Explosionsschutzbewertung den Betrieb der Anlage im möglicherweise '
             'explosionsgefährdeten Bereich mit dem Betreiber verbindlich regeln '
             '(Einschränkung, Freigaberegelung oder Außerbetriebnahme); Erlaubnisscheinverfahren '
             'für Arbeiten mit Zündquellen beibehalten',
      mittel='Explosionsschutzbewertung für die Aufzugsanlage erstellen lassen (Explosionsschutzdokument, '
             'Zoneneinteilung, geeignete Betriebsmittel)',
      evidence='HIGH_CONFIDENCE', klaerung='K-U03', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Sofortmaßnahme erweitert wie bei R4, aber abgestuft: Anders als dort ist bei '
            'fehlendem Explosionsschutzdokument nicht erwiesen, dass der Aufzug in einer Zone '
            'liegt – deshalb „mit dem Betreiber verbindlich regeln" statt Betriebseinstellung. '
            'Die bisherige Fassung ließ die Anlage als mögliche Zündquelle im unbewerteten '
            'Bereich weiterlaufen. Stufe und Priorität bleiben.')],
   sources=[law('GefStoffV', '§ 6 Abs. 9'), trbs('TRBS 2152'), trbs('TRGS 720')],
   factor=F_BRAND, persons=[NUTZER, WARTUNG], bereich='U')

hz('MF-U07', 'Umgebungsbedingungen: Temperatur, Feuchtigkeit, Wasser, Korrosion', GRP_U,
   [('qu_temperatur', 'TRIGGER', 'ALWAYS'),
    ('qu_feuchte_sicherheitsteile', 'TRIGGER', 'ALWAYS'),
    ('qu_korrosion', 'TRIGGER', 'ALWAYS'),
    ('qg_wasser', 'TRIGGER', 'ALWAYS'),
    ('qg_oel', 'TRIGGER', 'ALWAYS')],
   [r(in_('qg_wasser', ['wasser', 'unklar']), 'HIGH',
      sofort=MU['wasser'][0], mittel=MU['wasser'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Bedingung auf stehendes Wasser bzw. Wasser an elektrischen oder '
            'sicherheitsrelevanten Bauteilen eingegrenzt – und ausdrücklich auch auf den '
            'nicht beurteilbaren Umfang (fail-closed). Frage 11.15 lautete „Wasser ODER '
            'Feuchtigkeit" und führte ausnahmslos zu Hoch mit Außerbetriebnahme; feuchte '
            'Grubenwände und Kondensat sind in Altschächten der Regelfall und rechtfertigen '
            'keine Stilllegung. Bei 15.23a war die Bedingung bereits auf sicherheitsrelevante '
            'Bauteile geschärft – die Asymmetrie ist damit behoben. Stufe und Maßnahmen '
            'bleiben für den echten Wasserfall unverändert.'),
    r(eq('qg_wasser', 'feuchte'), 'MEDIUM', prio=90,
      sofort='Betroffene Bauteile auf Feuchteschäden und Korrosion sichtprüfen; Betreiber '
             'unterrichten',
      mittel='Ursache der Feuchte beseitigen – Abdichtung prüfen, Belüftung bzw. Beheizung '
             'der Grube herstellen; Zustand der Bauteile bei der wiederkehrenden Prüfung '
             'erneut bewerten',
      evidence='INFERRED',
      notes='Regelprüfung 20.09.2026: Neue Regel für die bloße Feuchte bzw. Kondensat ohne Bauteilkontakt. Sie ist '
            'nicht folgenlos – Korrosion an tragenden und sicherheitsrelevanten Teilen '
            'entsteht daraus –, rechtfertigt aber keine Stilllegung.'),
    r(yes('qu_feuchte_sicherheitsteile'), 'HIGH',
      sofort='Anlage bei Feuchtigkeit oder Wasser an Steuerung, Bremse oder Türverriegelung '
             'außer Betrieb nehmen; Ursache mit dem Betreiber klären',
      mittel='Ursache nach Befund beseitigen – bei Wassereintritt abdichten, bei Kondensat '
             'Belüftung bzw. Beheizung von Triebwerksraum oder Schacht herstellen und die '
             'Schutzart der betroffenen Betriebsmittel anheben; betroffene Sicherheitsbauteile '
             'prüfen und bei Korrosionsspuren austauschen lassen',
      evidence='HIGH_CONFIDENCE', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Beide Maßnahmen von MU[\'wasser\'] gelöst. Sie stammten unverändert aus dem '
            'Wasser-Textblock der Schachtgrube und passten nicht zu der 2026 geschärften '
            'Bedingung, die ausdrücklich den Bereich AUSSERHALB der Grube und den Fall '
            'Kondensat erfasst: Die Sofortmaßnahme nannte einen Bereich, den 15.23a gerade '
            'ausschließt, und für Kondensat an der Steuerung liegt die Ursache in Lüftung, '
            'Beheizung und Schutzart, nicht im Wassereintritt. Bedingung und Stufe Hoch '
            'bleiben – Feuchte an Bremse oder Türverriegelung kann eine Einrichtung im '
            'Sicherheitskreis zum Versagen bringen.'),
    r(yes('qu_korrosion'), 'HIGH', sofort=MU['korrosion'][0], mittel=MU['korrosion'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(yes('qu_temperatur'), 'MEDIUM', sofort=MU['temperatur'][0], mittel=MU['temperatur'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(yes('qg_oel'), 'MEDIUM', sofort=MU['oel'][0], mittel=MU['oel'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U)],
   sources=[en8120('5.2.1.2'), en8120('5.2.6.1'), trbs('TRBS 1201 Teil 4', 'Anhang 4')],
   factor=F_UMGEBUNG, persons=[WARTUNG, NUTZER], agg='MAXIMUM', bereich='U')

hz('MF-U08', 'Bauliche Änderungen ohne Bewertung, Statik und baulicher Zustand', GRP_BRAND,
   [('qu_bauliche_aenderung', 'TRIGGER', 'ALWAYS'),
    ('qu_verkleidung', 'TRIGGER', 'ALWAYS')],
   [r(yes('qu_bauliche_aenderung'), 'HIGH', sofort=MU['bau_aenderung'][0], mittel=MU['bau_aenderung'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(yes('qu_verkleidung'), 'MEDIUM', sofort=MU['verkleidung'][0], mittel=MU['verkleidung'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U)],
   sources=[trbs('TRBS 1201 Teil 4', 'Anhang 4'), trbs3121('Anhang 4')], factor=F_LAST,
   persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='U')

hz('MF-U09', 'Brandmeldeanlage, Brandfall- und Evakuierungssteuerung nicht abgestimmt; '
   'Brandschutzeinrichtung behindert Betrieb oder Rettung', GRP_BRAND,
   [('qa_bma_vorhanden', 'APPLICABILITY', 'NEVER',
     {'applicable_when': any_(yes('qa_bma_vorhanden'),
                              in_('qu_brandschutz_behindert', ['rettung', 'betrieb'])),
      'notes': 'Prüfbericht 20.09.2026: 15.8d wird immer gefragt, wurde ohne Brandmeldeanlage '
               'aber nie bewertet – die Gefährdung ist jetzt auch allein darüber anwendbar.'}),
    ('qu_bma_abgestimmt', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_bma_vorhanden')}),
    ('qu_bma_geprueft', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qu_bma_abgestimmt')}),
    ('qu_evak_in_gbu', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_bma_vorhanden')}),
    ('qu_brandschutz_behindert', 'TRIGGER', 'ALWAYS')],
   [r(no('qu_bma_abgestimmt'), 'MEDIUM', sofort=MU['bma_abstimmung'][0], mittel=MU['bma_abstimmung'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(no('qu_bma_geprueft'), 'MEDIUM', sofort=MU['bma_pruefung'][0], mittel=MU['bma_pruefung'][1],
      evidence='HIGH_CONFIDENCE',
      notes='Prüfbericht 20.09.2026: Hoch auf Mittel. Der fehlende Nachweis der Wirk-Prinzip-'
            'Prüfung ist ein Dokumentationsmangel der Gebäudeseite; die Funktionsprüfung der '
            'Aufzugs-Brandfallsteuerung (8.21a) ist ebenfalls Mittel – beide Stufen sind jetzt '
            'gleich.', pb=_PB_U),
    r(no('qu_evak_in_gbu'), 'MEDIUM', sofort=MU['evak'][0], mittel=MU['evak'][1],
      evidence='HIGH_CONFIDENCE',
      notes='Prüfbericht 20.09.2026: Hoch auf Mittel, nachdem die Frage auf die Festlegung des '
            'Betreibers (Brandschutzkonzept, Betriebsanweisung) umgestellt wurde. '
            'Regelprüfung 20.09.2026: Stufe Mittel bleibt, beide Maßnahmen neu gefasst (siehe MU[\'evak\']): Der '
            'sicherheitsrelevante Kern ist die fehlende Festlegung und Kennzeichnung des '
            'Benutzungsverbots im Brandfall, nicht eine Evakuierungsfunktion, die die meisten '
            'Anlagen gar nicht haben.', pb=_PB_U),
    r(eq('qu_brandschutz_behindert', 'rettung'), 'HIGH',
      sofort='Betreiber unterrichten; Zugang zu Triebwerksraum, Notentriegelung und '
             'Schachttür freiräumen bzw. sichern; ist die Personenrettung weiter behindert, '
             'Anlage bis zur Beseitigung außer Betrieb nehmen',
      mittel='Brandschutzeinrichtung und Aufzug baulich bzw. technisch entflechten '
             '(Türfeststellanlage, geänderter Anschlag, Revisionsöffnung in der Abschottung) '
             'und das Ergebnis im Brandschutzkonzept fortschreiben',
      evidence='HIGH_CONFIDENCE', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Bedingung auf die behinderte Personenrettung eingegrenzt – der nicht sicher '
            'beurteilbare Fall gehört ausdrücklich dazu (fail-closed). Die Regel bündelte '
            'vorher zwei Sachverhalte sehr unterschiedlicher Schwere. Außerdem kehrte die '
            'Maßnahmenlogik das TOP-Prinzip um: sofort wurde technisch beseitigt, '
            'mittelfristig blieb es bei einer vagen organisatorischen „Abstimmung", obwohl '
            'die Ursachenbeseitigung baulich-technisch ist.'),
    r(eq('qu_brandschutz_behindert', 'betrieb'), 'MEDIUM',
      sofort='Betreiber unterrichten; Behinderung des Aufzugsbetriebs dokumentieren und '
             'Freihaltung des Rettungszugangs bei jeder Begehung prüfen',
      mittel='Brandschutzeinrichtung und Aufzug baulich bzw. technisch entflechten '
             '(Türfeststellanlage, geänderter Anschlag) und das Ergebnis im '
             'Brandschutzkonzept fortschreiben',
      evidence='INFERRED', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Neue Regel für die reine Betriebsbehinderung bei nachweislich freiem '
            'Rettungszugang. Das ist kein unmittelbares Lebensrisiko und wurde mit Hoch '
            'überbewertet.')],
   sources=[trbs('TRBS 1201 Teil 4', 'Anhang 4'), trbs3121('Anhang 4'), en('DIN EN 81-73')],
   factor=F_BRAND, persons=[NUTZER, FEUERWEHR], agg='MAXIMUM', bereich='U')

hz('MF-U10', 'Schachtentrauchung, Lüftung und RWA unklar oder verändert', GRP_BRAND,
   [('qa_entrauchung_vorhanden', 'APPLICABILITY', 'NEVER'),
    ('qu_entrauchung', 'TRIGGER', 'ALWAYS')],
   [r(in_('qu_entrauchung', ['gestoert', 'veraendert']), 'MEDIUM',
      sofort='Betreiber unterrichten und Funktionsprüfung durch die Fachfirma des Gewerks '
             'veranlassen',
      mittel='Entrauchung instand setzen bzw. Öffnungsquerschnitt nach Brandschutzkonzept '
             'wiederherstellen und Prüfnachweis vorlegen lassen',
      evidence='HIGH_CONFIDENCE', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Die frühere Hoch-Regel für „blockiert oder defekt" und die Mittel-Regel für '
            '„verschlossen oder verändert" sind zusammengefasst: Physikalisch ist das '
            'derselbe Zustand, die Abstufung Hoch/Mittel trennte nur die Ursache (Defekt '
            'gegenüber baulicher Veränderung), nicht das Risiko. Die Gefahr setzt in beiden '
            'Fällen das Brandereignis voraus – nach dem Stufenmaßstab Mittel, konsistent zu '
            'MF-U09-R1/R2. Eine Anhebung auf Hoch käme nur über die zusätzliche Feststellung '
            'in Betracht, dass die Entrauchung nach Brandschutzkonzept zwingend gefordert und '
            'vollständig unwirksam ist. Normbezug ist die Landesbauordnung bzw. das '
            'Brandschutzkonzept, nicht DIN EN 81-20 5.2.1.4.1 (Beleuchtung).'),
    r(eq('qu_entrauchung', 'kein_nachweis'), 'MEDIUM', sofort=MU['entrauchung_nachweis'][0],
      mittel=MU['entrauchung_nachweis'][1], evidence='HIGH_CONFIDENCE', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Bedingung um den Fall „Funktion unklar" erweitert (Option geteilt). Stufe '
            'Mittel unverändert.')],
   sources=[trbs('TRBS 1201 Teil 4', 'Anhang 4'), law('Landesbauordnung')], factor=F_BRAND,
   persons=[NUTZER, FEUERWEHR], bereich='U')

hz('MF-U11', 'Löschanlage / Sprinkler ohne Bewertung der Wechselwirkung mit dem Aufzug', GRP_BRAND,
   [('qa_sprinkler_vorhanden', 'APPLICABILITY', 'NEVER'),
    ('qu_sprinkler_abschaltung', 'TRIGGER', 'ALWAYS'),
    ('qu_sprinkler_geprueft', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qu_sprinkler_abschaltung')})],
   [r(no('qu_sprinkler_abschaltung'), 'HIGH',
      sofort='Betreiber unterrichten; bis zur Klärung Steuerung gegen Wasserbeaufschlagung '
             'schützen oder Anlage stilllegen',
      mittel='Abschaltung der Aufzugsenergie bei Auslösung der Löschanlage herstellen und '
             'die Schutzart der Steuerung sicherstellen',
      evidence='HIGH_CONFIDENCE', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Bedingung auf den prüfbaren Sachverhalt umgestellt: Bewertet wurde vorher ein '
            'Dokumentationszustand („Wechselwirkung bewertet?"), vergeben wurde dafür Hoch. '
            'Das ist derselbe Fehlertyp, der bei 15.8c bereits korrigiert wurde – die '
            'fehlende Bewertung ist kein unmittelbares Lebensrisiko, das Risiko entsteht erst '
            'bei Auslösung der Löschanlage. Hoch ist jetzt der Feststellung vorbehalten, dass '
            'die Abschaltung vor Wasserbeaufschlagung tatsächlich fehlt. Die '
            'Mittelfristmaßnahme ist technisch gefasst (vorher „bewerten und umsetzen lassen" '
            '[ORGA], obwohl die Ursachenbeseitigung technisch ist).'),
    r(no('qu_sprinkler_geprueft'), 'MEDIUM',
      sofort='Nachweis der Wirksamkeitsprüfung beim Betreiber anfordern',
      mittel='Wirk-Prinzip-Prüfung der Abschaltung in den Prüfplan nach BetrSichV § 3 '
             'aufnehmen und dokumentieren',
      evidence='HIGH_CONFIDENCE', pb=_PB_U,
      notes='Regelprüfung 20.09.2026: Neue Regel für den fehlenden Nachweis (neue Frage 15.10b). Beide Fragen sind '
            'Pflicht, damit die Nichtbeantwortung INCOMPLETE ergibt und nicht Kein Risiko.')],
   sources=[trbs('TRBS 1201 Teil 4', 'Anhang 4'), src('OTHER', 'VdS CEA 4001')], factor=F_ELEKTRISCH,
   persons=[NUTZER, FEUERWEHR], bereich='U')

hz('MF-U12', 'Fremdgewerke und Reinigungspersonal ohne Zugangs- und Schutzkonzept', GRP_U,
   [('qu_wartung_gefaehrlicher_zugang', 'TRIGGER', 'ALWAYS'),
    ('qu_fremd_zugangskonzept', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': yes('qu_wartung_gefaehrlicher_zugang')})],
   # Regelprüfung 20.09.2026: Die frühere Regel R2 ([15.36]=Ja UND [15.36a]=Ja -> Niedrig) ist
   # ersatzlos entfallen: Sie vergab „Niedrig", obwohl die Kompensation erfüllt
   # war. Der Stufenmaßstab setzt für Niedrig einen Mangel voraus; hier liegt
   # keiner vor (Soll-Zustand erfüllt). Folge war ein Dauerbefund bei jeder
   # Anlage mit Fremdgewerken und vorhandenem Konzept, der bei MAXIMUM die
   # Kein-Risiko-Regel verdrängte. Ihre beiden Maßnahmen waren ohnehin
   # Erhaltungsmaßnahmen – sie stehen jetzt in der Auffangregel. Ein echter
   # Befund entsteht erst, wenn das Konzept unwirksam oder nicht unterwiesen
   # ist; dafür wäre eine eigene Frage nötig (Gruppe B der Regelprüfung).
   [r(all_(yes('qu_wartung_gefaehrlicher_zugang'), no('qu_fremd_zugangskonzept')), 'HIGH',
      sofort=MU['fremd_zugang'][0], mittel=MU['fremd_zugang'][1], evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(answered('qu_wartung_gefaehrlicher_zugang'), 'NO_RISK', prio=1,
      sofort='Zustand erhalten; bei der wiederkehrenden Prüfung und der Betreiberkontrolle '
             'erneut prüfen – Zugangs- und Schutzkonzept bei Änderungen der Gewerke '
             'fortschreiben, Unterweisungsnachweise stichprobenartig prüfen',
      evidence='HIGH_CONFIDENCE',
      notes='Kein Risiko: keine Mangelregel trifft zu, alle Pflichtfragen beantwortet. '
            'Regelprüfung 20.09.2026: Erhaltungstext um die Fortschreibung des Zugangskonzepts ergänzt, die vorher '
            'in der entfallenen Niedrig-Regel R2 stand.')],
   sources=[trbs3121('3.4.2'), dguv('DGUV Information 209-085')], factor=F_BEWEGT,
   persons=[FREMDFIRMEN, REINIGUNG], agg='MAXIMUM', bereich='U')

hz('MF-U13', 'Fehlende Prüfnachweise und unklare Zuständigkeiten an den Gewerkeschnittstellen',
   GRP_BRAND,
   [('qu_nachweise_fremdgewerke', 'TRIGGER', 'ALWAYS'),
    ('qu_zustaendigkeit', 'TRIGGER', 'ALWAYS')],
   [r(no('qu_nachweise_fremdgewerke'), 'MEDIUM', sofort=MU['nachweise'][0], mittel=MU['nachweise'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(no('qu_zustaendigkeit'), 'MEDIUM', sofort=MU['zustaendigkeit'][0], mittel=MU['zustaendigkeit'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U)],
   sources=[trbs('TRBS 1201 Teil 4', 'Anhang 4'), law('BetrSichV', '§ 13')], factor=F_ORGA,
   persons=[BETREIBER], agg='MAXIMUM', bereich='U')

hz('MF-U14', 'Aufzugszugang grenzt an Fahrwege / Verkehrsflächen', GRP_U,
   [('qu_verkehrswege', 'TRIGGER', 'ALWAYS'),
    ('qa_nutzung_pmem', 'MODIFIER', 'NEVER')],
   [r(all_(yes('qu_verkehrswege'), yes('qa_nutzung_pmem')), 'HIGH', prio=200,
      sofort='Wartebereich vor dem Aufzug gegen den Fahrverkehr abgrenzen (Markierung, Absperrung)',
      mittel='Bauliche Trennung von Fußgänger- und Fahrbereich am Aufzugszugang',
      evidence='HYPOTHESIS', klaerung='K-U05'),
    r(yes('qu_verkehrswege'), 'MEDIUM', prio=100,
      sofort='Wartebereich vor dem Aufzug markieren, Betreiber informieren',
      mittel='Bauliche oder organisatorische Trennung von Fußgänger- und Fahrbereich',
      evidence='INFERRED', klaerung='K-U05')],
   sources=[src('OTHER', 'ASR A1.8'), trbs3121('Anh. 1 Nr. 5')], factor=F_STOSS, persons=[NUTZER],
   bereich='U')

hz('MF-U15', 'Abgase und Emissionen im Aufstellbereich (Lärm und Ereignishistorie dokumentiert)', GRP_U,
   [('qu_abgase', 'TRIGGER', 'ALWAYS'),
    ('qu_abgase_lueftung', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes('qu_abgase')}),
    ('qu_laerm', 'DOCUMENTATION', 'NEVER',
     {'notes': 'Entscheidung 02.09.2026 (K-U04): nur Dokumentation, keine Stufe.'}),
    ('qu_unfaelle', 'DOCUMENTATION', 'NEVER',
     {'notes': 'Entscheidung 02.09.2026 (K-U04): nur Dokumentation, keine Stufe.'}),
    ('qu_umfeld_kritisch', 'DOCUMENTATION', 'NEVER')],
   [r(all_(yes('qu_abgase'), yes('qu_abgase_lueftung')), 'NO_RISK', prio=150,
      sofort='Zustand erhalten; Wirksamkeit der Lüftung bei der Betreiberkontrolle erneut prüfen',
      evidence='INFERRED',
      notes='Regelprüfung 20.09.2026: Neue Kompensationsregel. Bei NONE-Aggregation ist die katalogtypische Form '
            'die Kompensationsregel, nicht die Einengung der Bedingung – R1 bleibt deshalb '
            'unverändert und greift, solange die Kompensation nicht erfüllt ist.'),
    r(yes('qu_abgase'), 'MEDIUM', prio=100,
      sofort='Lüftung des Aufstellbereichs prüfen, Betreiber informieren',
      mittel='Lüftung und Absaugung im Aufstellbereich technisch sicherstellen bzw. instand '
             'setzen; Fahrkorb- und Triebwerksraumlüftung prüfen',
      evidence='INFERRED',
      notes='Regelprüfung 20.09.2026: Bedingung und Stufe bleiben – für den echten Mangelfall (Emissionen ohne '
            'wirksame Lüftung) ist Mittel richtig, weil die Gesundheitsgefahr expositions- '
            'und dauerabhängig ist. Ohne Kompensationsfrage entstand aber bei einem großen '
            'Teil der Anlagen ein Dauerbefund Mittel ohne Mangel. Die Mittelfristmaßnahme ist '
            'außerdem als [TECH] gefasst – Lüftung und Absaugung sind technische Maßnahmen, '
            'die Kennzeichnung als [ORGA] war falsch.')],
   sources=[law('LärmVibrationsArbSchV'), src('OTHER', 'ASR A3.6'), law('BetrSichV', '§ 3 Abs. 7')],
   factor=F_UMGEBUNG, persons=[WARTUNG, BEAUFTRAGTE], bereich='U')
