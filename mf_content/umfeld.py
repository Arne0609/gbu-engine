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
yn('qu_ex_moeglich', 'Kann sich im Bereich der Anlage ein explosionsfähiges Gemisch bilden '
   '(Gase, Dämpfe, Stäube)?', ui='15.25')
yn('qu_ex_bewertet', 'Explosionsschutz für die Aufzugsanlage bewertet und dokumentiert '
   '(Explosionsschutzdokument)?', ui='15.25a', visible_when=yes('qu_ex_moeglich'))
yn('qu_ex_umgesetzt', 'Festgelegte Ex-Schutzmaßnahmen an der Aufzugsanlage umgesetzt und auf '
   'Wirksamkeit geprüft (geeignete Betriebsmittel, Prüfung vor Inbetriebnahme/wiederkehrend)?',
   ui='15.25b', visible_when=yes('qu_ex_bewertet'))
yn('qu_temperatur', 'Unzulässige Temperaturen im Triebwerksraum oder Schacht möglich '
   '(Überhitzung über 40 °C, Frost)?', ui='15.23')
yn('qu_feuchte_sicherheitsteile', 'Feuchtigkeit oder Kondensat an sicherheitsrelevanten '
   'Bauteilen (Steuerung, Bremse, Türverriegelung)?', ui='15.23a')
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
yn('qu_evak_in_gbu', 'Evakuierungs-/Sonderfunktion des Aufzugs in dieser Gefährdungsbeurteilung '
   'berücksichtigt?', ui='15.8c', visible_when=yes('qa_bma_vorhanden'))
yn('qu_brandschutz_behindert', 'Behindert eine Brandschutzeinrichtung (Brandschutztür, '
   'Abschottung) den Aufzugsbetrieb oder die Personenrettung?', ui='15.8d')
sel('qu_entrauchung', 'Zustand der Schachtentrauchung / RWA / Lüftungsöffnung', ui='15.9a',
    options=[('ok', 'Funktion geprüft, Öffnungen frei'),
             ('unklar', 'Funktion unklar, blockiert oder defekt'),
             ('veraendert', 'Öffnungen verschlossen, verändert oder unzureichend'),
             ('kein_nachweis', 'Kein Nachweis über Prüfung')],
    visible_when=yes('qa_entrauchung_vorhanden'))
yn('qu_sprinkler_bewertet', 'Wechselwirkung der Löschanlage mit der Aufzugsanlage '
   '(Wasserbeaufschlagung, Abschaltung) bewertet?', ui='15.10a',
   visible_when=yes('qa_sprinkler_vorhanden'))
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
    'evak': ('Evakuierungsfunktion bis zur Bewertung nicht nutzen; Feuerwehr informieren',
             'Evakuierungsbetrieb nach DIN EN 81-76 bzw. Brandschutzkonzept in diese GBU aufnehmen'),
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


def _ortshazard(code, title, qs, result, mfrom_, extra_q=(), extra_rules=(), factor=F_GEFAHRSTOFF,
                persons=(WARTUNG, BEAUFTRAGTE), group=GRP_U, sources=(), massn=None):
    hqs = [(x, 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_maschinenraum')})
           if x.startswith('qm_') else (x, 'TRIGGER', 'ALWAYS') for x in qs] + list(extra_q)
    so, mi = MU[massn] if massn else (None, None)
    rules = [r(yes(x), result, mfrom=mfrom_, sofort=so, mittel=mi, evidence='INFERRED',
               klaerung='K-U01', pb=_PB_U if massn else None) for x in qs]
    rules += list(extra_rules)
    hz(code, title, group, hqs, rules, sources=sources, factor=factor, persons=list(persons),
       agg='ANY', mode='STANDARD', bereich='U')

_ortshazard('MF-U01', 'Asbesthaltige oder andere schädliche Baustoffe im Bereich der Anlage',
            ASBEST, 'HIGH', ('E26-G5', 'Asbest'),
            extra_q=[('qu_asbest_unbekannt', 'TRIGGER', 'ALWAYS')],
            extra_rules=[r(yes('qu_asbest_unbekannt'), 'MEDIUM', sofort=MU['asbest_unbekannt'][0],
                           mittel=MU['asbest_unbekannt'][1], evidence='HIGH_CONFIDENCE',
                           pb='H06 – Unsicherheit ist kein bestätigter Befund: Mittel mit Erkundung statt Hoch mit Stillsetzung')],
            sources=[law('GefStoffV', '§ 6'), trbs('TRGS 519')], massn='asbest')

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

hz('MF-U05', 'Transport von Gefahrstoffen mit der Aufzugsanlage', GRP_U,
   [('qu_transport_chem', 'TRIGGER', 'ALWAYS'),
    ('qu_transport_bio', 'TRIGGER', 'ALWAYS'),
    ('qu_transport_brennbar', 'TRIGGER', 'ALWAYS'),
    ('qu_transport_radioaktiv', 'TRIGGER', 'ALWAYS')],
   [r(yes('qu_transport_chem'), 'MEDIUM',
      sofort='Transportregeln (Behälter, Begleitung, Nutzung durch Dritte) mit dem Betreiber festlegen',
      mittel='Lüftung des Fahrkorbs und Verhalten bei Freisetzung in der Betriebsanweisung regeln',
      evidence='INFERRED'),
    r(yes('qu_transport_bio'), 'MEDIUM',
      sofort='Transport nur in dichten, gekennzeichneten Behältern; Fahrkorb nach Kontamination reinigen',
      mittel='Reinigungs- und Desinfektionsplan für den Fahrkorb festlegen', evidence='INFERRED'),
    r(yes('qu_transport_brennbar'), 'MEDIUM',
      sofort='Transportmengen begrenzen, Zündquellen im Fahrkorb ausschließen',
      mittel='Explosionsschutz-/Brandschutzbewertung für den Transport dokumentieren',
      evidence='INFERRED'),
    r(yes('qu_transport_radioaktiv'), 'MEDIUM',
      sofort='Strahlenschutzbeauftragten einbinden, Transport nur nach Strahlenschutzanweisung',
      mittel='Regelung des Transports radioaktiver Stoffe in der Betriebsanweisung', evidence='INFERRED')],
   sources=[law('GefStoffV'), law('StrlSchV'), law('BioStoffV')], factor=F_GEFAHRSTOFF,
   persons=[NUTZER, WARTUNG], agg='MAXIMUM', bereich='U')

hz('MF-U06', 'Explosionsfähiges Gemisch kann durch die Aufzugsanlage gezündet werden', GRP_U,
   [('qu_ex_moeglich', 'TRIGGER', 'ALWAYS'),
    ('qu_ex_bewertet', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes('qu_ex_moeglich')}),
    ('qu_ex_umgesetzt', 'COMPENSATION', 'CONDITIONAL', {'required_when': yes('qu_ex_bewertet')})],
   [r(all_(yes('qu_ex_moeglich'), yes('qu_ex_bewertet'), no('qu_ex_umgesetzt')), 'HIGH', prio=210,
      sofort='Keine Arbeiten mit Zündquellen ohne Freigabe des Betreibers (Erlaubnisschein)',
      mittel='Festgelegte Ex-Schutzmaßnahmen umsetzen und ihre Wirksamkeit vor der weiteren Nutzung prüfen lassen',
      evidence='HIGH_CONFIDENCE', pb='Prüfbericht 16.09.2026 – Dokumentation allein ist keine Schutzmaßnahme (§ 6 GefStoffV, § 4 BetrSichV)'),
    r(all_(yes('qu_ex_moeglich'), yes('qu_ex_bewertet'), yes('qu_ex_umgesetzt')), 'MEDIUM', prio=200,
      sofort='Festgelegte Ex-Schutzmaßnahmen einhalten, Zündquellen an der Anlage prüfen',
      mittel='Explosionsschutzdokument bei Änderungen an Anlage oder Nutzung fortschreiben',
      evidence='INFERRED', klaerung='K-U03'),
    r(yes('qu_ex_moeglich'), 'HIGH', prio=100,
      sofort='Keine Arbeiten mit Zündquellen ohne Freigabe des Betreibers (Erlaubnisschein); '
             'Betreiber auf die fehlende Bewertung hinweisen',
      mittel='Explosionsschutzbewertung für die Aufzugsanlage erstellen lassen (Explosionsschutzdokument, '
             'Zoneneinteilung, geeignete Betriebsmittel)',
      evidence='HIGH_CONFIDENCE', klaerung='K-U03', pb=_PB_U)],
   sources=[law('GefStoffV', '§ 6 Abs. 9'), trbs('TRBS 2152'), trbs('TRGS 720')],
   factor=F_BRAND, persons=[NUTZER, WARTUNG], bereich='U')

hz('MF-U07', 'Umgebungsbedingungen: Temperatur, Feuchtigkeit, Wasser, Korrosion', GRP_U,
   [('qu_temperatur', 'TRIGGER', 'ALWAYS'),
    ('qu_feuchte_sicherheitsteile', 'TRIGGER', 'ALWAYS'),
    ('qu_korrosion', 'TRIGGER', 'ALWAYS'),
    ('qg_wasser', 'TRIGGER', 'ALWAYS'),
    ('qg_oel', 'TRIGGER', 'ALWAYS')],
   [r(yes('qg_wasser'), 'HIGH', sofort=MU['wasser'][0], mittel=MU['wasser'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(yes('qu_feuchte_sicherheitsteile'), 'HIGH', sofort=MU['wasser'][0], mittel=MU['wasser'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
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

hz('MF-U09', 'Brandmeldeanlage, Brandfall- und Evakuierungssteuerung nicht abgestimmt', GRP_BRAND,
   [('qa_bma_vorhanden', 'APPLICABILITY', 'NEVER'),
    ('qu_bma_abgestimmt', 'TRIGGER', 'ALWAYS'),
    ('qu_bma_geprueft', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qu_bma_abgestimmt')}),
    ('qu_evak_in_gbu', 'TRIGGER', 'ALWAYS'),
    ('qu_brandschutz_behindert', 'TRIGGER', 'ALWAYS')],
   [r(no('qu_bma_abgestimmt'), 'MEDIUM', sofort=MU['bma_abstimmung'][0], mittel=MU['bma_abstimmung'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(no('qu_bma_geprueft'), 'HIGH', sofort=MU['bma_pruefung'][0], mittel=MU['bma_pruefung'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(no('qu_evak_in_gbu'), 'HIGH', sofort=MU['evak'][0], mittel=MU['evak'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(yes('qu_brandschutz_behindert'), 'HIGH', sofort=MU['brandschutz_behindert'][0],
      mittel=MU['brandschutz_behindert'][1], evidence='HIGH_CONFIDENCE', pb=_PB_U)],
   sources=[trbs('TRBS 1201 Teil 4', 'Anhang 4'), trbs3121('Anhang 4'), en('DIN EN 81-73')],
   factor=F_BRAND, persons=[NUTZER, FEUERWEHR], agg='MAXIMUM', bereich='U')

hz('MF-U10', 'Schachtentrauchung, Lüftung und RWA unklar oder verändert', GRP_BRAND,
   [('qa_entrauchung_vorhanden', 'APPLICABILITY', 'NEVER'),
    ('qu_entrauchung', 'TRIGGER', 'ALWAYS')],
   [r(eq('qu_entrauchung', 'unklar'), 'HIGH', sofort=MU['entrauchung_unklar'][0],
      mittel=MU['entrauchung_unklar'][1], evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(eq('qu_entrauchung', 'veraendert'), 'MEDIUM', sofort=MU['entrauchung_veraendert'][0],
      mittel=MU['entrauchung_veraendert'][1], evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(eq('qu_entrauchung', 'kein_nachweis'), 'MEDIUM', sofort=MU['entrauchung_nachweis'][0],
      mittel=MU['entrauchung_nachweis'][1], evidence='HIGH_CONFIDENCE', pb=_PB_U)],
   sources=[trbs('TRBS 1201 Teil 4', 'Anhang 4'), en8120('5.2.1.4.1')], factor=F_BRAND,
   persons=[NUTZER, FEUERWEHR], bereich='U')

hz('MF-U11', 'Löschanlage / Sprinkler ohne Bewertung der Wechselwirkung mit dem Aufzug', GRP_BRAND,
   [('qa_sprinkler_vorhanden', 'APPLICABILITY', 'NEVER'),
    ('qu_sprinkler_bewertet', 'TRIGGER', 'ALWAYS')],
   [r(no('qu_sprinkler_bewertet'), 'HIGH', sofort=MU['sprinkler'][0], mittel=MU['sprinkler'][1],
      evidence='HIGH_CONFIDENCE', pb=_PB_U)],
   sources=[trbs('TRBS 1201 Teil 4', 'Anhang 4'), src('OTHER', 'VdS CEA 4001')], factor=F_ELEKTRISCH,
   persons=[NUTZER, FEUERWEHR], bereich='U')

hz('MF-U12', 'Fremdgewerke und Reinigungspersonal ohne Zugangs- und Schutzkonzept', GRP_U,
   [('qu_wartung_gefaehrlicher_zugang', 'TRIGGER', 'ALWAYS'),
    ('qu_fremd_zugangskonzept', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': yes('qu_wartung_gefaehrlicher_zugang')})],
   [r(all_(yes('qu_wartung_gefaehrlicher_zugang'), no('qu_fremd_zugangskonzept')), 'HIGH',
      sofort=MU['fremd_zugang'][0], mittel=MU['fremd_zugang'][1], evidence='HIGH_CONFIDENCE', pb=_PB_U),
    r(all_(yes('qu_wartung_gefaehrlicher_zugang'), yes('qu_fremd_zugangskonzept')), 'LOW',
      sofort='Zugangskonzept bei Änderungen der Gewerke fortschreiben',
      mittel='Wirksamkeit des Zugangskonzepts regelmäßig prüfen (Unterweisungsnachweise)',
      evidence='INFERRED')],
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
    ('qu_laerm', 'DOCUMENTATION', 'NEVER',
     {'notes': 'Entscheidung 02.09.2026 (K-U04): nur Dokumentation, keine Stufe.'}),
    ('qu_unfaelle', 'DOCUMENTATION', 'NEVER',
     {'notes': 'Entscheidung 02.09.2026 (K-U04): nur Dokumentation, keine Stufe.'}),
    ('qu_umfeld_kritisch', 'DOCUMENTATION', 'NEVER')],
   [r(yes('qu_abgase'), 'MEDIUM',
      sofort='Lüftung des Aufstellbereichs prüfen, Betreiber informieren',
      mittel='Lüftung / Absaugung im Aufstellbereich sicherstellen; Fahrkorblüftung prüfen',
      evidence='INFERRED')],
   sources=[law('LärmVibrationsArbSchV'), src('OTHER', 'ASR A3.6'), law('BetrSichV', '§ 3 Abs. 7')],
   factor=F_UMGEBUNG, persons=[WARTUNG, BEAUFTRAGTE], bereich='U')
