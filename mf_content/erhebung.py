# -*- coding: utf-8 -*-
"""Erhebung kürzen: Fragengruppen, Nachweis-Vorbelegung, Stammdaten, Phasen.

Umsetzung des Kürzungs- und Synergievorschlags vom 16.09.2026 (Projektdoku
„GBU 4.0 – Fragenkatalog kürzen“). Grundsatz: Die Bewertung ändert sich nicht.
Fragen, Gefährdungen und Regeln bleiben bestehen (stabile Regel-IDs, laufende
Freigabe); gekürzt wird die ERHEBUNG – also das, was der Prüfer sieht und
anklickt. Vier Mechanismen, alle rein beschreibend im Seed, ausgewertet in der
App:

1. FRAGENGRUPPEN (`question_groups`, Frage.group)
   Mehrere Fragen werden als EINE Karte gezeigt. Zwei Arten:
     * checklist – alle Positionen sind Ja/Nein-Fragen; die Karte zeigt die
       AUFFÄLLIGKEIT als Ankreuzfeld („Not-Halt fehlt“). Angekreuzt setzt den
       auffälligen Wert (`value`). Bestätigt der Prüfer die Karte („keine
       weiteren Auffälligkeiten“), erhalten alle nicht angekreuzten, sichtbaren
       Positionen den unauffälligen Wert (`clear`) mit Herkunft `sammel` –
       dieselbe Mechanik wie die Sammelantwort je Ortsbereich, nur je Karte und
       mit sichtbaren Positionen. Positionen mit `implies` setzen beim Ankreuzen
       zusätzlich die Elternfrage (z. B. „Verkehrsweg rutschig“ setzt „Verkehrsweg
       sicher“ auf Nein), damit die Position sichtbar und die Regel scharf ist.
     * card – gemischte Karte: Auswahl- und Zahlenfragen werden nativ gezeigt
       (`mode: native`), Ja/Nein-Positionen als Ankreuzfeld wie oben.
   Sichtbarkeit: eine Position erscheint nur, wenn ihre `visible_when`-Regel
   erfüllt ist; eine Karte ohne sichtbare Position wird nicht gezeigt. Zeilen
   (`row`) gliedern große Karten nach Ort (Beleuchtung, Not-Halt).
   Für die Engine ändert sich nichts: Antworten sind weiterhin Antworten auf die
   Einzelfragen; `best_case` je Frage bleibt die Wahrheit für `clear`.

2. NACHWEIS-VORBELEGUNG (`nachweise`)
   Was die ZÜS in der letzten Hauptprüfung nach TRBS 1201-4 3.3 (2) geprüft hat,
   wird aus dem Prüfbericht vorbelegt und nur bestätigt oder korrigiert. Frei-
   geschaltet durch die neue Frage D05 (`qd_zues_bericht` = ohne offene
   sicherheitsrelevante Mängel). Die App setzt die Antworten mit Herkunft
   `nachweis` (mit Datum des Prüfberichts) – GESPEICHERT, anders als die
   Baujahr-Annahme, weil an ein konkretes Dokument gebunden. Handantwort löscht
   die Herkunft; ein Mangel im Prüfbericht lässt die Frage offen.
   Grenze: Die ZÜS prüft Zustand und Funktion gegen die Errichtungsgrundlage,
   sie belegt nicht, dass eine Einrichtung vorhanden ist, die bei Errichtung
   nicht gefordert war. Deshalb `min_baujahr`: 1999 = nur Anlagen ab
   Aufzugsrichtlinie; None = auch bei Anlagen vor 1999 tragfähig (Einrichtung
   schon nach TRA 200 (Mai 1992) gefordert oder geprüfter Zustand).
   Rangfolge in der App: erhobene Antwort > Baujahr-Annahme > Nachweis.

3. STAMMDATEN (`Frage.source = anlagenstamm`, `Frage.stamm_key`)
   Anlagenmerkmale werden im Anlagenstamm gepflegt und im Fragebogen nur
   angezeigt (Herkunft `stamm`); Korrektur im Fragebogen schreibt zurück.

4. PHASEN (`category_phases`, `category_order`)
   stamm = aus dem Anlagenstamm; vorab = vor dem Ortstermin beantwortbar
   (Unterlagen, Organisation, Umfeld – Betreiber-Vorabbogen); vor_ort = Begehung
   in Begehungsreihenfolge.

Außerdem (Strukturänderungen ohne Regelwirkung):
   * STREICHEN – vier Fragen ohne Regelbezug entfallen (2.2, 8.4, 8.11, 11.11a);
     8.4 wird im Cyber-Fragebogen erhoben.
   * VERSCHIEBEN – fünf Unterlagen-/Organisationsfragen wandern in den D-Block.
   * D05 – neue Steuerfrage für die Nachweis-Vorbelegung (Gefährdung MF-D04,
     Rolle DOCUMENTATION, keine Regel).
   * SCHWELLEN – sechs Zahlenfragen, bei denen nur die Regelgrenzen wirken,
     werden Bereichs- oder Ja/Nein-Fragen mit genau diesen Grenzen; jede
     Regel-, Sichtbarkeits- und Pflichtbedingung wird mechanisch umgeschrieben
     (GT 20 -> IN [über 20 mm]). Unerwartete Vergleiche brechen den Generator
     ab. Der Messwert bleibt als optionales Zahlenfeld ohne Regelwirkung
     erfassbar (Entscheidung E6).

Aufruf aus gen_mf_catalog.build():
   erhebung.vorbereiten(seed)   # vor set_best_case: streichen, verschieben, D05
   erhebung.anreichern(seed)    # nach set_best_case: Gruppen, Nachweise, Stamm, Phasen
und aus check(): errors += erhebung.pruefen(seed).
"""
from collections import OrderedDict
import json as _json

# Baujahrgrenzen und Ausdruckshelfer der Regelsprache – für Nachweis-Einträge
# mit Zusatzbedingung (Prüfbericht 20.09.2026 B05: Schutzraum je Regelwerk).
from .common import BJ_AUFZUGSRICHTLINIE, BJ_EN8120, lt

# ---------------------------------------------------------------------------
# Strukturänderungen
# ---------------------------------------------------------------------------
STREICHEN = OrderedDict([
    ('qa_oeffentlich', 'Öffentlich zugänglich – ohne Regelwirkung; Nutzerkreis (A11) und Barrierefreiheit decken den Bedarf.'),
    ('qk_notruf_en8128', 'EN-81-28-Merkmale – nur Dokumentation; wird im Cyber-Fragebogen (Notrufkomponente) erhoben.'),
    ('qk_nachregulierung', 'Nachregulierung – ohne Regelwirkung; die Stufenbildung (8.10) ist der Befund.'),
    ('qg_gg_abtrennung_hoehe_mm', 'Höhe der Gegengewichtsabtrennung – ohne Regelwirkung; Bewertung über 11.11.'),
])

# Frage -> Erhebungsbereich (Buchstabe). Unterlagen und Organisation gehören in
# den D-Block, damit sie vor dem Ortstermin beantwortet werden können.
VERSCHIEBEN = OrderedDict([
    ('qm_stromlaufplan', 'D'),
    ('qm_betriebsanleitung', 'D'),
    ('qm_personal_eingewiesen', 'D'),
    ('qt_dreikant_hinterlegt', 'D'),
    ('qu_unfaelle', 'D'),
    ('qa_nutzung_flurfoerderzeug', 'U'),   # Nutzung, kein Anlagenmerkmal: zu Verkehrsflächen (U12)
    ('qt_nur_eingewiesene', 'A'),          # Nutzerkreis (A11), nicht Türen
])

D05 = {
    'code': 'qd_zues_bericht', 'type': 'SELECT', 'domain': 'GBU',
    'text': 'Letzte ZÜS-Hauptprüfung: Prüfbericht liegt vor und ohne offene sicherheitsrelevante Mängel?',
    'ui_number': '3.7',
    'options': [
        {'value': 'ohne_maengel', 'label': 'Ja – Prüfbericht liegt vor, keine offenen sicherheitsrelevanten Mängel'},
        {'value': 'mit_maengeln', 'label': 'Prüfbericht liegt vor, aber mit offenen sicherheitsrelevanten Mängeln'},
        {'value': 'nicht_vorhanden', 'label': 'Nein – kein Prüfbericht verfügbar / unbekannt'},
    ],
    'help_text': ('Steuerfrage ohne eigene Bewertung. Bei „Ja“ werden die im Prüfbericht geprüften '
                  'Einrichtungen (Verriegelungen, Fangvorrichtung, Begrenzer, Puffer, Bremse, Notruf-Funktion, '
                  'Beleuchtung, Haltegenauigkeit, elektrische Anlage) als unauffällig vorbelegt – Herkunft '
                  '„Nachweis“ mit Datum des Prüfberichts, bereichsweise zu bestätigen. Grundlage: TRBS 1201 Teil 4 '
                  '3.3 (2) Nr. 1–31; die Prüfberichte gehören nach TRBS 3121 3.2 zu den Unterlagen des Betreibers. '
                  'Ein im Prüfbericht gemeldeter Mangel setzt die betroffene Frage nicht auf „unauffällig“.'),
}
# Seit 20.09.2026 legt mf_content/sonderfunktion_doku.py die Frage selbst an und
# bewertet sie in MF-D04 (Prüfbericht mit offenen Mängeln). vorbereiten() legt sie
# nur noch an, wenn sie fehlt – der Wortlaut hier bleibt die einzige Quelle.
D05_HAZARD = 'MF-D04'   # Prüfplakette / Prüffrist

# Zahlenfrage -> Schwellenfrage. bands: (wert, label) in absteigender Güte;
# ops: (operator, schwelle) -> Liste der Optionswerte, die die Bedingung erfüllen.
SCHWELLEN = OrderedDict([
    ('qk_stufe_mm', {
        'type': 'SELECT', 'text': 'Größte Stufenbildung / Haltegenauigkeit an den Haltestellen',
        'help': 'Regelgrenzen 10 mm und 20 mm (DIN EN 81-20 5.12.1.1.4: Anhaltegenauigkeit ± 10 mm). Vorbelegung aus dem ZÜS-Prüfbericht (Hauptprüfung Nr. 5, Haltegenauigkeit in allen Etagen). Messwert optional im Feld daneben.',
        'bands': [('bis_10', '≤ 10 mm'), ('11_20', '11–20 mm'), ('ueber_20', 'über 20 mm')],
        'ops': {('GT', 20): ['ueber_20'], ('GT', 10): ['11_20', 'ueber_20']},
        'wert': ('qk_stufe_mm_wert', 'Stufenbildung gemessen [mm]')}),
    ('qk_schuerze_mm', {
        'type': 'SELECT', 'text': 'Fahrkorbtürschürze',
        'help': 'Regelgrenzen 300 mm und 750 mm (DIN EN 81-20 5.4.5.2: vertikaler Teil mindestens 0,75 m; TRA 200 Nr. 245.1: 0,75 m, Güteraufzüge 0,3 m). Messwert optional im Feld daneben.',
        'bands': [('ab_750', '≥ 750 mm'), ('300_749', '300–749 mm'), ('unter_300', 'unter 300 mm oder keine Schürze')],
        'ops': {('LT', 300): ['unter_300'], ('LT', 750): ['300_749', 'unter_300']},
        'wert': ('qk_schuerze_mm_wert', 'Schürzenlänge gemessen [mm]')}),
    ('qk_abstand_schwelle_mm', {
        'type': 'YES_NO', 'text': 'Abstand Fahrkorbschwelle – Schachtwand über 150 mm?',
        'help': 'Regelgrenze 150 mm (DIN EN 81-20 5.2.5.3.1: höchstens 0,15 m über die gesamte Schachthöhe). Nur bei Ja oder Unsicherheit messen; Messwert optional im Feld daneben.',
        'ops': {('GT', 150): True},
        'wert': ('qk_abstand_schwelle_mm_wert', 'Abstand gemessen [mm]')}),
    ('qf_spalt_mm', {
        'type': 'SELECT', 'text': 'Größter horizontaler Abstand Fahrkorbdachkante – Schachtwand',
        'help': 'Regelgrenzen 300, 500 und 850 mm: Geländer ab 0,30 m (DIN EN 81-20 5.4.7.2 b)); Höhe 0,70 m bis 0,50 m Abstand, 1,10 m darüber (5.4.7.4 b)); nach EN 81-1 8.13.3.2 lag die Grenze bei 0,85 m. Messwert optional im Feld daneben.',
        'bands': [('bis_300', '≤ 300 mm'), ('301_500', '301–500 mm'), ('501_850', '501–850 mm'), ('ueber_850', 'über 850 mm')],
        'ops': {('GT', 300): ['301_500', '501_850', 'ueber_850'], ('GT', 500): ['501_850', 'ueber_850'],
                ('GT', 850): ['ueber_850'], ('LTE', 850): ['bis_300', '301_500', '501_850']},
        'wert': ('qf_spalt_mm_wert', 'Abstand gemessen [mm]')}),
    ('qf_gelaender_hoehe_mm', {
        'type': 'SELECT', 'text': 'Geländerhöhe auf dem Fahrkorbdach',
        'help': 'Regelgrenzen 700 mm und 1 100 mm (DIN EN 81-20 5.4.7.4 b); EN 81-1 8.13.3.2).',
        'bands': [('ab_1100', '≥ 1 100 mm'), ('700_1099', '700–1 099 mm'), ('unter_700', 'unter 700 mm')],
        'ops': {('LT', 700): ['unter_700'], ('LT', 1100): ['700_1099', 'unter_700']}}),
    ('qa_grubentiefe', {
        'type': 'YES_NO', 'text': 'Schachtgrubentiefe über 1,60 m?',
        'help': 'Regelgrenze 1,60 m (DIN EN 81-20 5.2.1.5.1 a): bei Grubentiefe über 1,60 m zwei Notbremsschalter). Aus dem Anlagenstamm (Grubentiefe [m]).',
        'ops': {('GT', 1.6): True}}),
])

# ---------------------------------------------------------------------------
# Phasen und Reihenfolge der Erhebungsbereiche
# ---------------------------------------------------------------------------
PHASEN = OrderedDict([
    ('A', 'stamm'), ('D', 'vorab'), ('U', 'vorab'),
    ('Z', 'vor_ort'), ('M', 'vor_ort'), ('F', 'vor_ort'), ('S', 'vor_ort'),
    ('G', 'vor_ort'), ('T', 'vor_ort'), ('K', 'vor_ort'), ('SF', 'vor_ort'),
])
# Begehungsweg: Zugang -> Triebwerksraum -> Fahrkorbdach/Schachtkopf -> Schacht
# -> Grube -> Türen -> Fahrkorb -> Sonderfunktionen. Stamm und Vorab davor.
REIHENFOLGE = ['A', 'D', 'U', 'Z', 'M', 'F', 'S', 'G', 'T', 'K', 'SF']

# ---------------------------------------------------------------------------
# Nie per Sammelantwort (17.09.2026): Fragen, deren Antwort keine Sichtprüfung
# ist, sondern eine Bauart-, Ausstattungs- oder Prüfaussage. Die Simulation
# fände hier zwar einen „nie schlechteren" Wert, aber ein Sammelhaken würde
# eine Tatsache behaupten, die niemand festgestellt hat. Sie bleiben
# Einzelfragen (und sind zugleich die Kandidaten für den Anlagenstamm).
KEIN_SAMMEL = OrderedDict([
    ('qg_puffer_art', 'Bauart der Puffer – Eigenschaft der Anlage, keine Feststellung.'),
    ('qk_notruf_art', 'Art der Notrufeinrichtung – Ausstattung der Anlage.'),
    ('qk_notbeleuchtung', 'Art der Notbeleuchtung – Ausstattung der Anlage.'),
    ('qf_schutzraum', 'Schutzraum im Schachtkopf – Abmessung nach Errichtungsgrundlage.'),
    ('qm_notendschalter', 'Wirksamkeit vor Pufferberührung ist eine Prüfaussage, kein Augenschein.'),
    ('qz_zugang_befreiung', 'Erreichbarkeit für die Personenbefreiung ist eine organisatorische Zusage.'),
])

# ---------------------------------------------------------------------------
# Reine Dokumentationsfragen (17.09.2026, Arne): Sie kommen in keiner Regel vor,
# steuern weder Sichtbarkeit noch Annahmen oder Nachweise und sind in keiner
# Gefaehrdung Pflichtfrage. Sie bleiben im Fragebogen stehen, zaehlen aber wie
# die optionalen Messfelder nicht im Fortschritt und halten keine Karte offen.
DOKU_OPTIONAL = OrderedDict([
    ('qu_unfaelle', 'Unfallhistorie – Dokumentation nach Klärung vom 02.09.2026, ohne Regel.'),
    ('qd_gbu_vorhanden', 'Hinweis auf eine vorhandene Beurteilung des Betreibers, ohne Regel.'),
])

# ---------------------------------------------------------------------------
# Sammelantwort im Umfeld (U) – 17.09.2026, Arne: „U – Umfeld, Gebäude und
# Nutzung soll mit einem Klick komplett auf Sammelantwort gesetzt werden
# können.“ gen_mf_catalog.set_best_case() leitet den unauffälligen Wert aus
# den Befundregeln ab (Bereich U ist dort seitdem SAMMELBEREICH, Auswahlfragen
# eingeschlossen). Reine Dokumentationsfragen kommen in keiner Befundregel
# vor – für sie steht der unauffällige Wert hier, mit Begründung.
# ---------------------------------------------------------------------------
SAMMEL_DOKU = OrderedDict([
    ('qu_laerm', (False, 'Lärm ist laut Klärung vom 02.09.2026 nur Dokumentation; '
                         'unauffällig = keine erhöhte Lärmbelastung.')),
    ('qu_umfeld_kritisch', (False, 'Kritisches soziales Umfeld ist nur Dokumentation; '
                                   'unauffällig = nein.')),
])
# Was danach im Umfeld ohne best_case bleibt, ist gewollt: Stammfragen (aus
# dem Anlagenstamm) und Folgefragen, die erst nach einer angekreuzten
# Auffälligkeit sichtbar werden (Ex-Schutz umgesetzt?, Zugangskonzept?).

# ---------------------------------------------------------------------------
# Stammdaten: Frage -> Schlüssel im Anlagenstamm der App
# ---------------------------------------------------------------------------
STAMM = OrderedDict([
    # Schlüssel = Feld-ID im Anlagenstamm der App (lib/data/stammdaten_katalog.dart);
    # Felder ohne Vorbild dort werden in der App ergänzt (Gruppe „Anlagenmerkmale“).
    ('qa_aufzugsart', 'aufzugsart'),
    ('qa_antrieb', 'antrieb'),
    ('qa_nenngeschwindigkeit', 'nenngeschwindigkeit_vkn'),
    ('qa_gegengewicht', 'gegengewicht'),
    ('qa_maschinenraum', 'maschinenraum_vorhanden'),
    ('qa_rollenraum', 'rollenraum'),
    ('qa_mehrere_aufzuege', 'mehrere_aufzuege_im_schacht'),
    ('qa_raum_unter_schacht', 'raum_unter_schacht'),
    ('qa_glas_schachttueren', 'glas_schachttueren'),
    ('qa_glas_fahrkorbtueren', 'glas_fahrkorbtueren'),
    ('qa_glas_schacht', 'glas_schacht'),
    ('qa_nutzungsart', 'ausfuehrungsart'),
    ('qa_nutzung_pmem', 'nutzung_eingeschraenkte_mobilitaet'),
    ('qa_barrierefrei_gefordert', 'barrierefrei_gefordert'),
    ('qa_nutzung_kinder', 'nutzung_durch_kinder'),
    ('qa_nutzung_flurfoerderzeug', 'nutzung_flurfoerderzeug'),
    ('qa_baujahr', 'baujahr'),
    ('qa_norm_inverkehrbringen', 'regelwerk_inverkehrbringen'),
    ('qa_bma_vorhanden', 'bma_vorhanden'),
    ('qa_bfs_gefordert', 'brandfallsteuerung_gefordert'),
    ('qa_entrauchung_vorhanden', 'entrauchung_vorhanden'),
    ('qa_sprinkler_vorhanden', 'loeschanlage_vorhanden'),
    ('qa_feuerwehraufzug', 'hinweis_feuerwehraufzug'),
    ('qa_ucm_a3', 'ucm_a3'),
    ('qa_lagerung_statisch_bestimmt', 'antriebswelle_ohne_dreipunktlagerung'),
    ('qa_grubentiefe', 'grubentiefe_ueber_160'),
])
# Bewusst KEINE Stammdaten: qa_fahrkorbtuer (Pflichtfrage, nie annehmen; sofort sichtbar).

# ---------------------------------------------------------------------------
# Nachweis-Vorbelegung aus dem ZÜS-Prüfbericht
#   (frage, wert, min_baujahr, TRBS-1201-4-Prüfpunkt, Begründung)
# ---------------------------------------------------------------------------
_HP = 'TRBS 1201 Teil 4, 3.3 (2) Nr. %s'

# ---------------------------------------------------------------------------
# Prüfpunkte der Hauptprüfung ohne Frage im Katalog (Entscheidung Arne,
# 17.09.2026: „überlassen wird der Wartung/ZÜS")
#
# TRBS 1201 Teil 4, 3.3 (2) zählt 31 Prüfpunkte auf. Die folgenden haben
# bewusst keine Entsprechung im MF-Katalog: Sie betreffen den technischen
# Zustand von Tragmitteln und Antrieb, der über die Wartung und die
# wiederkehrende Prüfung der ZÜS abgedeckt wird. Die Gefährdungsbeurteilung
# fragt stattdessen die Schutzeinrichtungen ab, die bei deren Versagen wirken:
# Fangvorrichtung (Nr. 21), Geschwindigkeitsbegrenzer (Nr. 12),
# Schlaffseilsicherung (Nr. 11), Führungen (Nr. 13).
#
# Wer den Katalog erweitert, prüfe zuerst hier: Diese Punkte sind entschieden,
# nicht übersehen.
ZUES_PRUEFPUNKTE = 31
OHNE_KATALOGFRAGE = OrderedDict([
    ('15', 'Seilführung und Seilendbefestigungen – Wartung und ZÜS-Hauptprüfung'),
    ('16', 'Seilrollen und Umlenkrollen – Wartung und ZÜS-Hauptprüfung'),
    ('17', 'Treibscheibe und Treibfähigkeit – Wartung und ZÜS-Hauptprüfung'),
    ('24', 'Gegengewichtsausgleich (Massenausgleich) – Wartung und ZÜS-Hauptprüfung'),
    ('25', 'Aufsetzvorrichtung – Wartung und ZÜS-Hauptprüfung'),
    ('28', 'Sicherheitsrelevante MSR-Einrichtungen, funktionale Sicherheit, '
           'Software-Stand und Parameter – im Cyber-Fragebogen (CY)'),
])
# ---------------------------------------------------------------------------
# Prüfpunkte der Hauptprüfung, die es im Katalog GIBT, die aber bewusst KEINE
# Vorbelegung tragen (Prüfbericht 20.09.2026). Unterschied zu OHNE_KATALOGFRAGE:
# dort fehlt die Frage, hier fehlt die Tragfähigkeit des Nachweises.
NICHT_VORBELEGBAR = OrderedDict([
    ('1', 'Sicherer und ungehinderter Zugang (5.4 Durchgangsmaße): Der Prüfbericht belegt den '
          'ungehinderten Zugang, nicht die Einhaltung der EN-81-20-Maße an einer Altanlage.'),
    ('22', 'Schutz gegen unkontrolliert aufwärtsfahrenden Fahrkorb (8.28): Der Prüfbericht '
           'belegt die Wirksamkeit, nicht die Bauart (aktiv/passiv) – genau die entscheidet '
           'aber über die Kompensation in MF-K14.'),
    ('29', 'Zusammenwirken aufzugsexterner Sicherheitseinrichtungen (8.21 Brandfallsteuerung): '
           'Der Prüfbericht bewertet eine VORHANDENE Brandfallsteuerung; ob überhaupt eine '
           'gefordert und vorhanden ist, sagt er nicht.'),
])
NACHWEISE = [
    # --- auch bei Anlagen vor 1999 tragfähig (Einrichtung nach TRA 200 gefordert oder geprüfter Zustand)
    # Prüfpunkt 1 und 7 nachgetragen am 17.09.2026 (Auswertung der bis dahin
    # ungenutzten Prüfpunkte 1, 7, 15, 16, 17, 24, 25, 28):
    # 20.09.2026 gestrichen (Prüfbericht): Prüfpunkt 1 belegt den ungehinderten Zugang,
    # nicht die Einhaltung der EN-81-20-Durchgangsmaße an einer Altanlage.
    #   ('qz_weg_eng', False, None, '1', …)
    ('qt_glas_einzugsschutz', True, 2017, '7', 'Funktionsfähigkeit der Schutzeinrichtungen gegen Quetschen, Scheren und Einziehen von Händen in der Hauptprüfung geprüft; der Schutz gegen Einziehen von Kinderhänden ist erst mit DIN EN 81-20 gefordert – bei Altanlagen ist er Nachrüstbedarf und kein Prüfmangel (Prüfbericht 20.09.2026)'),
    ('qz_bel_vorhanden', True, None, '6', 'Funktionsfähigkeit der Beleuchtung der Zugänge in der Hauptprüfung geprüft'),
    ('qm_bel_vorhanden', True, None, '6', 'Funktionsfähigkeit der Beleuchtung im Triebwerksraum in der Hauptprüfung geprüft'),
    ('qs_bel_vorhanden', True, None, '6', 'Funktionsfähigkeit der Schachtbeleuchtung in der Hauptprüfung geprüft'),
    ('qg_bel_vorhanden', True, None, '6', 'Funktionsfähigkeit der Grubenbeleuchtung in der Hauptprüfung geprüft'),
    ('qm_einzug_begrenzer', True, None, '18', 'Schutz vor drehenden Teilen, Quetschen und Scheren in der Hauptprüfung sichtgeprüft'),
    ('qf_nothalt', True, None, '8', 'Sicherheitsrelevante Bedienelemente (Notbremsschalter) in der Hauptprüfung geprüft; TRA 200 Nr. 260.51'),
    ('qf_nothalt_wirksam', True, None, '8', 'Funktionsfähigkeit des Not-Halts in der Hauptprüfung geprüft'),
    ('qf_inspektion', True, None, '10', 'Funktionsfähigkeit der Inspektionssteuerung in der Hauptprüfung geprüft; TRA 200 Nr. 266.1'),
    ('qg_nothalt', True, None, '8', 'Notbremsschalter in der Grube in der Hauptprüfung geprüft; TRA 200 Nr. 260.51'),
    ('qm_beruehrungssicher', True, None, '27', 'Elektrische Anlage mindestens im Umfang des Anhangs 1 in der Hauptprüfung geprüft'),
    ('qm_potenzialausgleich', True, None, '27', 'Anhang 1 (Potenzialausgleich und Schutzleiter) in der Hauptprüfung geprüft'),
    ('qm_rohrbruch', True, None, '20', 'Funktionsfähigkeit des Leitungsbruchventils / der Rohrbruchsicherung in der Hauptprüfung geprüft (Nr. 20 f); TRA 200 Nr. 253'),
    ('qm_notbetrieb', True, None, '4', 'Maßnahmen und Hilfsmittel zur Personenbefreiung in der Hauptprüfung auf Eignung und Funktion geprüft; TRA 200 Nr. 228'),
    ('qt_verriegelung_elektrisch', True, None, '9', 'Funktionsfähigkeit der Türverschlüsse und ihrer elektrischen Sicherheitseinrichtungen in der Hauptprüfung geprüft; TRA 200 Nr. 212'),
    ('qk_notbeleuchtung', 'netzersatz', None, '6', 'Notbeleuchtung im Fahrkorb in der Hauptprüfung geprüft; TRA 200 Nr. 260.53 (Hilfsstromquelle für Notruf und Beleuchtung)'),
    # 20.09.2026 gestrichen (Prüfbericht): Prüfpunkt 29 prüft das Zusammenwirken einer
    # VORHANDENEN Brandfallsteuerung. Dass überhaupt eine vorhanden ist, sagt der
    # Prüfbericht nicht – das ist eine Anforderung des Brandschutzkonzepts.
    #   ('qk_bfs_vorhanden', True, None, '29', …)
    ('qs_fang', True, None, '21', 'Fangvorrichtung in der Hauptprüfung geprüft; TRA 200 Nr. 250 ff.'),
    ('qs_begrenzer', True, None, '12', 'Geschwindigkeitsbegrenzer in der Hauptprüfung geprüft; TRA 200 Nr. 250 ff.'),
    ('qs_fang_geprueft', True, None, '21', 'Prüfung von Fangvorrichtung und Begrenzer ist Teil der Hauptprüfung (Prüfbericht = Dokumentation)'),
    ('qg_puffer', True, None, '14', 'Funktionsfähigkeit der Puffer in der Hauptprüfung geprüft; TRA 200 Nr. 255'),
    ('qg_puffer_zustand', 'ok', None, '14', 'Puffer in der Hauptprüfung funktionsgeprüft'),
    ('qd_notbefreiungsanleitung', 'aktuell', None, '3', 'Notfallplan und Notbefreiungsanleitung in der Hauptprüfung auf Übereinstimmung mit der BetrSichV geprüft'),
    ('qk_stufe_mm', 'bis_10', None, '5', 'Haltegenauigkeit in allen Etagen in der Hauptprüfung geprüft (Zustand zum Prüfzeitpunkt)'),
    ('qk_notruf_vorhanden', True, None, '2', 'Funktionsfähigkeit der Notrufeinrichtung in der Hauptprüfung geprüft (nicht: Organisation der besetzten Stelle); TRA 200 Nr. 260.521 forderte die Notrufeinrichtung im Fahrkorb bei Personen- und Lastenaufzügen'),
    # --- nur ab 1999 (Errichtung nach EN 81-1/2; zusätzlich greift die Baujahr-Annahme)
    ('qt_selbstschliessend', True, 1999, '9', 'Funktionsfähigkeit der Schachttüren in der Hauptprüfung geprüft; TRA 200 Nr. 212 forderte kein Selbstschließen handbetätigter Türen – daher erst ab 1999'),
    ('qt_fehlschliess', True, 1999, '9', 'Türverschlüsse in der Hauptprüfung geprüft'),
    ('qs_schienen_stahl', True, 1999, '13', 'Führungen in der Hauptprüfung sichtgeprüft; TRA 200 Nr. 204.1 ließ auch andere zähe Metalle zu – daher erst ab 1999'),
    ('qs_spanngewicht_schalter', True, 1999, '12', 'Geschwindigkeitsbegrenzer einschließlich Spanngewicht in der Hauptprüfung geprüft'),
    ('qs_schlaffseil', True, 1999, '11', 'Tragmittel und Gewichtsausgleich in der Hauptprüfung geprüft'),
    ('qm_zweikreisbremse', True, 1999, '19', 'Bremsen einschließlich redundanter Funktionen in der Hauptprüfung geprüft'),
    ('qm_bremse_ueberwacht', True, 1999, '19', 'Bremsfunktion in der Hauptprüfung geprüft'),
    ('qm_schuetze_unabhaengig', True, 1999, '27', 'Sicherheitsstromkreise in der Hauptprüfung geprüft'),
    ('qm_motorschutz', True, 1999, '27', 'Elektrische Anlage in der Hauptprüfung geprüft'),
    ('qm_laufzeit', True, 1999, '27', 'Elektrische Anlage in der Hauptprüfung geprüft'),
    ('qm_phasenumkehr', True, 1999, '27', 'Elektrische Anlage in der Hauptprüfung geprüft'),
    ('qm_kav', True, 1999, '20', 'Hydrauliksystem einschließlich Nachregulierung in der Hauptprüfung geprüft (Nr. 20 e)'),
    ('qm_anschlagpunkte', True, 1999, 'Anh. 4 Nr. 4.1', 'Kennzeichnung der Traglast von Anschlagpunkten (Anhang 4 Nr. 4.1, ZÜS-SV); TRA 200 forderte keine Anschlagpunkte – daher erst ab 1999'),
    ('qm_anschlag_geprueft', True, 1999, 'Anh. 4 Nr. 4.1', 'Anschlagpunkte durch die ZÜS-SV geprüft (Anhang 4 Nr. 4.1)'),
    ('qk_ueberlast', True, 1999, '30', 'Überlastkontrolle als technische Schutzmaßnahme in der Hauptprüfung geprüft'),
    ('qk_ueberlast_geprueft', True, 1999, '30', 'Funktionsprüfung in der Hauptprüfung'),
    ('qa_ucm_a3', True, 2012, '23', 'Schutzeinrichtung gegen unbeabsichtigte Bewegung des Fahrkorbs in der Hauptprüfung geprüft'),
    # 20.09.2026 (Prüfbericht): Der Prüfbericht belegt, dass eine Schutzeinrichtung wirkt –
    # nicht, ob sie aktiv (SAFÜ/Notbremse) oder passiv ausgeführt ist. Die Unterscheidung
    # ist für die Kompensation in MF-K14 entscheidend und bleibt zu erheben.
    #   ('qk_schutz_aufwaerts', 'aktiv', 1999, '22', …)
    # Prüfbericht 20.09.2026 B05: „normgerecht" heißt im Katalog „nach EN 81-20".
    # Anlagen von 1999 bis 2016 sind nach EN 81-1/-2 errichtet; ihr Schutzraum ist
    # „altnorm" (MF-F04-R3 / MF-G02-R2: Niedrig). Eine Vorbelegung mit „normgerecht"
    # widerspräche der eigenen Regel – deshalb zwei Einträge je Frage, getrennt durch
    # das Baujahr. Der sechste Eintrag ist die Zusatzbedingung.
    ('qf_schutzraum', 'normgerecht', BJ_EN8120, '26', 'Schutzräume: Vorrichtungen zur Herstellung temporärer Schutzräume in der Hauptprüfung geprüft; Abmessungen nach DIN EN 81-20 (Baujahr ab 2017)'),
    ('qf_schutzraum', 'altnorm', BJ_AUFZUGSRICHTLINIE, '26', 'Schutzräume: Vorrichtungen zur Herstellung temporärer Schutzräume in der Hauptprüfung geprüft; bei fester Kopffreiheit Bestandsangabe nach DIN EN 81-1/-2 (Baujahr 1999 bis 2016)', lt('qa_baujahr', BJ_EN8120)),
    ('qg_schutzraum', 'normgerecht', BJ_EN8120, '26', 'Schutzräume: Vorrichtungen zur Herstellung temporärer Schutzräume in der Hauptprüfung geprüft; Abmessungen nach DIN EN 81-20 (Baujahr ab 2017)'),
    ('qg_schutzraum', 'altnorm', BJ_AUFZUGSRICHTLINIE, '26', 'Schutzräume: Vorrichtungen zur Herstellung temporärer Schutzräume in der Hauptprüfung geprüft; bei fester Grubentiefe Bestandsangabe nach DIN EN 81-1/-2 (Baujahr 1999 bis 2016)', lt('qa_baujahr', BJ_EN8120)),
    ('qm_stromlaufplan', 'aktuell', 1999, '31', 'Ordnungsprüfung (Nr. 31): technische Unterlagen'),
]

# ---------------------------------------------------------------------------
# Fragengruppen
#   g(id, bereich, titel, items, ui=None, help=None, kind=None)
#   item: (frage, label, value)            -> Ankreuzfeld (Ja/Nein-Frage)
#         (frage, label, value, row)       -> mit Zeile (Ort)
#         (frage,)  bzw. (frage, None)     -> native (Auswahl/Zahl oder Ja/Nein ohne Auffälligkeitslogik)
#         (frage, None, None, row)         -> native mit Zeile
#   value = der AUFFÄLLIGE Wert (angekreuzt); clear = Gegenteil (bestätigt, nicht angekreuzt).
# ---------------------------------------------------------------------------
GRUPPEN = []


def g(gid, bereich, titel, items, ui=None, help=None, kind=None):
    assert not any(x['id'] == gid for x in GRUPPEN), 'doppelte Gruppe ' + gid
    its = []
    for t in items:
        code = t[0]
        label = t[1] if len(t) > 1 else None
        value = t[2] if len(t) > 2 else None
        row = t[3] if len(t) > 3 else None
        it = {'question': code, 'mode': 'check' if label is not None else 'native'}
        if label is not None:
            it['label'] = label
            it['value'] = value
        if row:
            it['row'] = row
        its.append(it)
    d = {'id': gid, 'bereich': bereich, 'title': titel, 'items': its}
    if ui: d['ui_number'] = ui
    if help: d['help'] = help
    if kind: d['kind'] = kind
    GRUPPEN.append(d)
    return gid



# ---- A Anlagenmerkmale (Mehrfachauswahl-Karten; Werte aus dem Anlagenstamm) ----
g('A09', 'A', 'Glas an', [
    ('qa_glas_schachttueren', 'Schachttüren', True),
    ('qa_glas_fahrkorbtueren', 'Fahrkorbtüren', True),
    ('qa_glas_schacht', 'Schacht oder Schachtgerüst', True)], ui='4.1',
  help='Mehrfachauswahl; nichts angekreuzt = kein Glas.')
g('A11', 'A', 'Nutzerkreis', [
    ('qa_nutzung_pmem', 'Personen mit eingeschränkter Mobilität zu erwarten', True),
    ('qa_barrierefrei_gefordert', 'Barrierefreie Ausführung gefordert (Baugenehmigung, Nutzungskonzept, öffentlich)', True),
    ('qa_nutzung_kinder', 'Unbeaufsichtigte Kinder zu erwarten (Schule, Kita, Wohnanlage)', True),
    ('qt_nur_eingewiesene', 'Ohne Fahrkorbtür: ausschließlich eingewiesene Personen (Lastenaufzug)', True)], ui='4.9')
g('A14', 'A', 'Gebäudeseitige Einrichtungen mit Schnittstelle zum Aufzug', [
    ('qa_bma_vorhanden', 'Brandmeldeanlage (BMA) im Gebäude', True),
    ('qa_bfs_gefordert', 'Brandfallsteuerung nach Brandschutzkonzept gefordert', True),
    ('qa_entrauchung_vorhanden', 'Schachtentrauchung / RWA / Lüftungsöffnung', True),
    ('qa_sprinkler_vorhanden', 'Löschanlage / Sprinkler im Schacht oder Triebwerksraum', True),
    ('qa_feuerwehraufzug', 'Feuerwehr- oder Evakuierungsaufzug (EN 81-72 / EN 81-73)', True)], ui='15.6',
  help='Mehrfachauswahl; nichts angekreuzt = keine Schnittstelle. Schaltet die Fragen zu Brandfallsteuerung, BMA, Entrauchung, Löschanlage und Sonderfunktionen.')

# ---- Ortsbezogene Sammelkarten (je Begehungsort eine Karte; Regeln unverändert) ----
# Beleuchtung: 13 Einzelfragen -> 4 Karten (Zuwege, Triebwerksraum, Schacht/Haltestellen, Grube)
g('BZ1', 'Z', 'Beleuchtung der Zuwege zum Triebwerksraum', [
    ('qz_bel_vorhanden', 'Keine Beleuchtung', False),
    ('qz_bel_ausreichend', 'Unzureichend (unter 50 lx, Leuchten an ungeeigneter Stelle, nicht funktionsfähig)', False),
    ('qz_bel_defekt', 'Defekte Leuchten oder Leuchtkörper', True)], ui='5.1',
  help='Sollwert DIN EN 81-20:2020-06 5.2.2.2: Zugangswege 50 lx.')
g('BM1', 'M', 'Beleuchtung im Triebwerks-/Maschinenraum', [
    ('qm_bel_vorhanden', 'Keine Beleuchtung', False),
    ('qm_bel_200lux', 'Unter 200 lx an den Arbeitsflächen (Antrieb, Steuerschrank)', False),
    ('qm_bel_geeignet', 'Arbeitsflächen abgeschattet / Leuchten ungünstig', False),
    ('qm_bel_splitterschutz', 'Leuchten im Kopfbereich ohne Splitterschutz', False)], ui='5.20',
  help='Sollwert DIN EN 81-20:2020-06 5.2.1.4.2: 200 lx am Boden, wo Personen arbeiten.')
g('BS1', 'S', 'Schachtbeleuchtung und Beleuchtung der Haltestellen', [
    ('qs_bel_vorhanden', 'Keine Schachtbeleuchtung', False),
    ('qs_bel_ausreichend', 'Unzureichend (unter 50 lx 1 m über dem Fahrkorbdach, unter 20 lx sonst)', False),
    ('qs_bel_altnorm',),
    ('qs_bel_splitterschutz', 'Leuchten ohne Splitterschutz / an ungeeigneter Stelle', False),
    ('qs_zugang_bel', 'Beleuchtung an den Haltestellen (Schachtzugängen) unzureichend', False)], ui='10.1',
  help='Sollwerte DIN EN 81-20:2020-06: Schacht 50 lx 1 m über dem Fahrkorbdach, 20 lx sonst '
       '(5.2.1.4.1); Haltestellen 50 lx am Boden (5.3.7.1) – derselbe Wert wie in Frage 10.2 '
       '(Entscheidung Arne 20.09.2026, Prüfbericht B42).')
g('BG1', 'G', 'Beleuchtung der Schachtgrube', [
    ('qg_bel_vorhanden', 'Keine Beleuchtung', False),
    ('qg_bel_50lux', 'Unter 50 lx / Leuchten ungeeignet angeordnet', False)], ui='11.2',
  help='Sollwert DIN EN 81-20:2020-06 5.2.1.4.1 b): 50 lx 1 m über dem Grubenboden.')
# Umgebung je Ort: Schadstoffe, Verschmutzung, brennbare Stoffe, Fremdeinrichtungen (17 Fragen -> 4 Karten + 1)
g('UZ1', 'Z', 'Zugangsbereich – Umgebung und Lagerung', [
    ('qz_asbest', 'Asbest-/Schadstoffverdacht (Bremsbeläge, Dichtungen, Brandschutzverkleidungen)', True),
    ('qz_asbest_zustand',),
    ('qz_verschmutzung', 'Erhebliche Verschmutzung (Taubenkot, Unrat, Schimmel, Ablagerungen)', True),
    ('qz_brennbar_lager', 'Lagerung brennbarer oder leicht entzündlicher Stoffe', True)], ui='5.60')
g('UM1', 'M', 'Triebwerksraum – Umgebung, Lagerung und Fremdeinrichtungen', [
    ('qm_asbest', 'Asbest-/Schadstoffverdacht (Bremsbeläge, Dichtungen, Brandschutzverkleidungen)', True),
    ('qm_asbest_zustand',),
    ('qm_verschmutzung', 'Erhebliche Verschmutzung (Taubenkot, Unrat, Schimmel, Ablagerungen)', True),
    ('qm_brennbar_lager', 'Lagerung brennbarer oder leicht entzündlicher Stoffe', True),
    ('qm_fremd_frei', 'Aufzugsfremde Einrichtungen (Lager, Leitungen, Geräte Dritter)', False)], ui='5.59')
g('US1', 'S', 'Schacht und Fahrkorb – Umgebung und Fremdeinrichtungen', [
    ('qs_asbest', 'Asbest-/Schadstoffverdacht (Bremsbeläge, Dichtungen, Brandschutzverkleidungen)', True),
    ('qs_asbest_zustand',),
    ('qs_verschmutzung', 'Erhebliche Verschmutzung (Taubenkot, Unrat, Schimmel, Ablagerungen)', True),
    ('qs_brennbar_lager', 'Lagerung brennbarer oder leicht entzündlicher Stoffe', True),
    ('qs_fremd_frei', 'Aufzugsfremde Einrichtungen im Schacht', False),
    ('qs_fremd_fachgerecht', 'Fremde Leitungen nicht fachgerecht verlegt / nicht gekennzeichnet', False),
    ('qs_fremd_behindert', 'Fremde Einrichtungen behindern Arbeiten oder Rettungswege', True)], ui='10.12')
g('UG1', 'G', 'Schachtgrube – Umgebung und Lagerung', [
    ('qg_asbest', 'Asbest-/Schadstoffverdacht (Bremsbeläge, Dichtungen)', True),
    ('qg_asbest_zustand',),
    ('qg_verschmutzung', 'Erhebliche Verschmutzung (Taubenkot, Unrat, Schimmel, Ablagerungen)', True),
    ('qg_brennbar_lager', 'Lagerung brennbarer oder leicht entzündlicher Stoffe', True)], ui='11.20')
# Einzugstellen
g('BM6', 'M', 'Einzugstellen im Triebwerksraum (Treibscheibe, Umlenkrollen, Kopierwerk, Begrenzer)', [
    ('qm_einzug_treibscheibe', 'Treibscheibe, Umlenkrollen, Kopierwerk ohne Einzugsschutz', False),
    ('qm_einzug_begrenzer', 'Geschwindigkeitsbegrenzer ohne Einzugsschutz', False),
    ('qm_einzug_grad',)], ui='5.40')
g('BF6', 'F', 'Einzugstellen im Schachtkopf / auf dem Fahrkorbdach', [
    ('qf_einzugstellen',),
    ('qf_einzug_abdeckung',)], ui='9.5')
# Not-Halt und Inspektionssteuerung: 12 Fragen -> 2 Karten (+ Rollenraum-Einzelfrage)
g('BF7', 'F', 'Not-Halt und Inspektionssteuerung auf dem Fahrkorbdach', [
    ('qf_nothalt', 'Not-Halt fehlt', False),
    ('qf_nothalt_erreichbar', 'Not-Halt vom Zugang aus nicht erreichbar', False),
    ('qf_nothalt_wirksam', 'Not-Halt nicht wirksam', False),
    ('qf_inspektion', 'Inspektionssteuerung fehlt', False),
    ('qf_inspektion_schutz', 'Inspektionssteuerung nicht gegen unbeabsichtigtes Betätigen geschützt', False),
    ('qf_inspektion_erreichbar', 'Inspektionssteuerung vom Zugang aus schlecht erreichbar', False),
    ('qf_inspektion_geschw', 'Inspektionsgeschwindigkeit über 0,63 m/s', False)], ui='9.8')
g('BG7', 'G', 'Not-Halt und Inspektionssteuerung in der Schachtgrube', [
    ('qg_nothalt', 'Not-Halt fehlt', False),
    ('qg_nothalt_aussen', 'Not-Halt von der Schachttür aus nicht erreichbar', False),
    ('qg_nothalt_zwei', 'Zweiter Not-Halt am Grubenboden fehlt (Grubentiefe über 1,60 m)', False),
    ('qg_inspektion', 'Inspektionssteuerung fehlt', False)], ui='11.4')
# Notruf, Notbeleuchtung, Selbstbefreiung
g('BF8', 'F', 'Notbeleuchtung und Notruf auf dem Fahrkorbdach', [
    ('qf_notbeleuchtung', 'Notbeleuchtung fehlt (mind. 5 lx, 1 h)', False),
    ('qf_notruf_dach', 'Kein eindeutig erkennbarer Auslöser für den (Fern-)Notruf', False)], ui='9.12')
g('BG8', 'G', 'Notruf und Selbstbefreiung in der Schachtgrube', [
    ('qg_selbstbefreiung', 'Selbstbefreiung über die Schachttür nicht möglich', False),
    ('qg_notruf', 'Notrufeinrichtung fehlt', False)], ui='11.8')
# Nachbaraufzug
g('BF9', 'F', 'Nachbaraufzug im gemeinsamen Schacht (Fahrkorbdach)', [
    ('qf_nachbar_trennung',),
    ('qf_nachbar_abschaltung',),
    ('qf_nachbar_abschaltung_geprueft',)], ui='9.6')
g('BG9', 'G', 'Nachbaraufzug im gemeinsamen Schacht (Schachtgrube)', [
    ('qg_nachbar_abtrennung', 'Abtrennung zum Nachbaraufzug fehlt', False),
    ('qg_nachbar_abschaltung',),
    ('qg_nachbar_abschaltung_geprueft',)], ui='11.14')

# ---- Z Zugang --------------------------------------------------------------------
g('Z01', 'Z', 'Verkehrsweg zum Triebwerks-/Steuerungsraum', [
    ('qz_weg_sicher', 'Verkehrsweg nicht sicher / nicht frei', False),
    ('qz_weg_rutschig', 'Rutschig, glatt oder verschmutzt', True),
    ('qz_weg_stolper', 'Stolperstellen', True),
    ('qz_weg_eng', 'Enge oder niedrige Durchgänge (unter 0,60 m breit / 2,00 m hoch)', True)], ui='5.3')
g('Z02', 'Z', 'Aufstieg zum Triebwerksraum', [
    ('qz_aufstieg',),
    ('qz_aufstieg_bruch', 'Bruch- oder Kippgefahr am Aufstieg', True)], ui='5.5')
g('Z03', 'Z', 'Absturzkanten und Überstiege auf dem Zugangsweg', [
    ('qz_absturzkante', 'Zugang über Dachfläche, Dachkante, Empore oder andere Absturzkante', True),
    ('qz_absturz_gesichert', 'Absturzkante nicht durch Geländer / Umwehrung gesichert', False),
    ('qz_absturz_gekennzeichnet',),
    ('qz_uebersteigen', 'Treppenauge, Brüstung oder Fenster muss überstiegen werden', True)], ui='5.7')
g('Z05', 'Z', 'Zugang zur Anlage: fremde Räume, Transport und Erreichbarkeit für die Personenbefreiung', [
    ('qz_durch_fremde',),
    ('qz_material_erschwert', 'Transport von Material und Werkzeug erschwert (Leiter, Dachluke, enge Wendeltreppe)', True),
    ('qz_zugang_befreiung',)], ui='5.10')
g('Z06', 'Z', 'Zugangstür zum Triebwerks-/Maschinenraum', [
    ('qz_tuer_vorhanden', 'Keine Zugangstür', False),
    ('qz_tuer_abschliessbar', 'Nicht abschließbar', False),
    ('qz_tuer_zustand', 'Beschädigt oder schwergängig', False),
    ('qz_tuer_mass', 'Durchgangsmaß zu klein (unter 2,00 m hoch / 0,60 m breit)', False),
    ('qz_von_innen',),
    ('qz_schaltschrank_abschliessbar', 'Ohne Triebwerksraum: Steuerschrank nicht abschließbar', False)],
  ui='5.12')
g('Z07', 'Z', 'Flucht- und Rettungsweg vom Triebwerks-/Steuerungsraum', [
    ('qz_flucht_frei', 'Nicht frei oder nicht benutzbar', False),
    ('qz_flucht_gekennz', 'Nicht gekennzeichnet oder nicht beleuchtet', False),
    ('qz_flucht_eingeengt', 'Durch Lagerung eingeengt', True)], ui='5.13')

# ---- M Triebwerksraum und Steuerung ----------------------------------------------
g('M01', 'M', 'Elektrische Sicherheit im Triebwerks-/Maschinenraum', [
    ('qm_beruehrungssicher', 'Spannungsführende Teile nicht berührungssicher', False),
    ('qm_offene_schalttafel', 'Offene Schalttafel ohne Schaltschrank', True),
    ('qm_offene_schalter', 'Offene Kontakte oder Schalter an Maschine, Kopierwerk oder Begrenzer', True),
    ('qm_schaltschrank_unsicher', 'Nicht berührungssichere Bauteile im Schaltschrank (bei geöffneter Tür erreichbar)', True),
    ('qm_kennz_kontakte', 'Keine Warnkennzeichnung für offene elektrische Kontakte', False),
    ('qm_bauseitig_ok', 'Bauseitige Elektroinstallation im Raum beschädigt oder unvollständig (Steckdosen, Schalter, Leitungen)', False),
    ('qm_potenzialausgleich', 'Kein Hauptpotenzialausgleich an der Aufzugskonstruktion', False)], ui='5.30')
g('M02', 'M', 'Prüfnachweise der elektrischen Anlage', [
    ('qm_dguv_v3', 'Kein Nachweis der Prüfung nach DGUV Vorschrift 3', False),
    ('qm_ortsfest_geprueft', 'Prüfung der ortsfesten elektrischen Anlage nicht nachgewiesen', False)], ui='5.35')
g('M05', 'M', 'Raum und Freiflächen', [
    ('qm_hoehe_180', 'Lichte Höhe im Gehbereich unter 1,80 m', False),
    ('qm_freiflaeche', 'Freifläche für Notbetrieb / Handrad vor dem Antrieb fehlt (0,50 m × 0,60 m)', False),
    ('qm_lagerung', 'Bewegungsflächen durch Lagerung eingeengt', True)], ui='5.43')
g('M06', 'M', 'Ebenen, Podeste und Bodenöffnungen', [
    ('qm_niveau', 'Niveauunterschiede über 0,50 m im Raum', True),
    ('qm_niveau_gesichert', 'Niveauunterschied nicht über Treppe oder Leiter überwindbar', False),
    ('qm_podest_absturz', 'Podest mit Absturzhöhe über 1,00 m ohne Geländer', True),
    ('qm_bodenoeffnung', 'Ungesicherte Bodenöffnung oder Vertiefung', True)], ui='5.46')
g('M07', 'M', 'Boden im Triebwerksraum', [
    ('qm_boden_rutschhemmend', 'Boden nicht rutschhemmend oder verschmutzt', False),
    ('qm_boden_oelfest', 'Boden nicht ölfest gestrichen oder beschädigt', False),
    ('qm_oel_ausgetreten', 'Ausgetretenes Öl / Hydrauliköl ohne Auffangmöglichkeit', True)], ui='5.48')
g('M08', 'M', 'Hauptschalter', [
    ('qm_hauptschalter', 'Hauptschalter fehlt oder Wirkung nicht nachvollziehbar', False),
    ('qm_hauptschalter_abschliessbar', 'Nicht abschließbar', False),
    ('qm_hauptschalter_gekennz', 'Nicht eindeutig gekennzeichnet', False)], ui='5.51')
g('M09', 'M', 'Betriebsbremse', [
    ('qm_zweikreisbremse', 'Keine Zweikreisbremse (redundante Betriebsbremse)', False),
    ('qm_bremse_ueberwacht', 'Bremse nicht elektrisch überwacht (Bremskontrollschalter)', False)], ui='6.2')
g('M10', 'M', 'Schutzeinrichtungen der Steuerung (nach Unterlagen / Prüfbericht)', [
    ('qm_schuetze_unabhaengig', 'Nur ein Fahrschütz / ein Abschaltweg', False),
    ('qm_steuerung_selbstueberw',),
    ('qm_motorschutz', 'Kein Schutz gegen Überhitzen des Antriebsmotors', False),
    ('qm_laufzeit', 'Keine Motor-Laufzeitüberwachung', False),
    ('qm_phasenumkehr', 'Kein Schutz gegen Phasenumkehr / Phasenausfall', False)], ui='6.3')
g('M12', 'M', 'Hydraulik: Absinken des Fahrkorbs und Rohrbruchsicherung', [
    ('qm_kav', 'Keine Einrichtung gegen Absinken (Kolbenabsinkverhinderung / Nachholsteuerung)', False),
    ('qm_absinkt', 'Fahrkorb sinkt im Stillstand merklich ab', True),
    ('qm_rohrbruch', 'Kein Rohrbruchsicherungsventil vorhanden', False),
    ('qm_absturzsicherung_alt',)], ui='6.12')
g('M13', 'M', 'Hydraulik: Absperrventil am Aggregat', [
    ('qm_absperrventil', 'Absperrventil fehlt', False),
    ('qm_absperrventil_zugang', 'Absperrventil schlecht zugänglich', False),
    ('qm_absperrventil_gekennz', 'Absperrventil nicht gekennzeichnet', False)], ui='6.10')
g('M14', 'M', 'Anschlagpunkte / Hebezeuge zum Anheben schwerer Teile', [
    ('qm_anschlagpunkte', 'Keine Anschlagpunkte / Hebezeuge', False),
    ('qm_tragfaehigkeit', 'Tragfähigkeit nicht angegeben', False),
    ('qm_anschlag_geprueft', 'Prüfung nicht dokumentiert', False)], ui='5.52')
g('M15', 'M', 'Einrichtung für Notbetrieb / Personenbefreiung', [
    ('qm_notbetrieb', 'Keine Einrichtung für Notbetrieb / Personenbefreiung (Handrad, Bremslüfthebel, Evakuierungseinheit, Notablass)', False),
    ('qm_notbetrieb_gekennz', 'Nicht gekennzeichnet (Fahrtrichtung, Bündigmarken)', False)], ui='5.53')
g('M17', 'M', 'Notendschalter (Endbegrenzung hinter den Endhaltestellen)', [
    ('qm_notendschalter',),
    ('qm_notendschalter_getrennt', 'Keine getrennten Betätigungseinrichtungen für betriebsmäßiges Anhalten und Notendschalter', False),
    ('qm_notendschalter_verbindung_ueberwacht', 'Bei mittelbarer Betätigung (Seil, Riemen, Kette): Bruch oder Schlaffwerden führt nicht zum Stillsetzen', False)], ui='6.14')
g('M16', 'M', 'Kennzeichnung und Beschilderung', [
    ('qm_kennz_elektrisch', 'Elektrische Einrichtungen nicht gekennzeichnet (Zuordnung im Notfall nicht möglich)', False),
    ('qm_beschilderung', 'Beschilderung unvollständig (Schutzraum, Notablass, Entriegelungsschlüssel, Verhalten)', False)], ui='5.54')

# ---- T Türen -----------------------------------------------------------------------
g('T01', 'T', 'Schachttürverriegelung und Fläche unterhalb der Schwelle', [
    ('qt_verriegelung_elektrisch', 'Verriegelung nicht vom Sicherheitskreis elektrisch überwacht', False),
    ('qt_fehlschliess', 'Keine Fehlschließsicherung / Nachschließeinrichtung', False),
    ('qt_flaeche_unter_schwelle',)], ui='7.1')
g('T10', 'T', 'Türblätter der Schiebetüren: Rückhaltung und Führung', [
    ('qt_rueckhaltung_tuerblatt', 'Keine Rückhalteeinrichtungen an den horizontal bewegten Schacht-Schiebetüren', False),
    ('qt_fuehrung_tuerblatt_ok', 'Führungselemente, Hänger oder Befestigungen der Türblätter beschädigt / ausgeschlagen', False)], ui='7.13')
g('T02', 'T', 'Selbstschließende Schachttüren', [
    ('qt_selbstschliessend', 'Schachttüren nicht selbstschließend (Feder oder Gewicht)', False),
    ('qt_schliesst_nach_notentriegelung', 'Schließt nach einer Notentriegelung nicht selbsttätig', False)], ui='7.3')
g('T03', 'T', 'Notentriegelung der Schachttüren', [
    ('qt_notentriegelung_alle', 'Notentriegelung nicht an allen Schachttüren', False),
    ('qt_notentriegelung_hoehe', 'Notentriegelung nicht erreichbar (über 2,00 m im Türblatt / 2,70 m im Rahmen)', False)], ui='7.5')
g('T04', 'T', 'Glas in Schacht- und Fahrkorbtüren', [
    ('qt_glas_normgerecht', 'Glas nicht normgerecht (kein VSG) oder beschädigt', False),
    ('qt_glas_beschaedigt', 'Glaseinsatz beschädigt, lose oder nicht sicher befestigt', True),
    ('qt_glas_drahtglas', 'Drahtglas (Gitterglas) verbaut', True)], ui='7.8')
g('T05', 'T', 'Glas-Schiebetüren: Schutz gegen Einziehen von Kinderhänden', [
    ('qt_glas_schiebetuer',),
    ('qt_glas_flaeche_gross', 'Glasflächen größer als ein Sichtfenster nach DIN EN 81-20 5.3.7.2.1 a) (Breite über 150 mm)', True),
    ('qt_glas_einzugsschutz', 'Kein Schutz gegen Einziehen von Kinderhänden (Sensorleiste, Abstand, Reibungsarmut)', False)], ui='7.9a')
g('T08', 'T', 'Schließkantensicherung der Fahrkorbtür / Schutz ohne Fahrkorbtür', [
    ('qt_fk_tuer_automatisch',),
    ('qt_schliesskante',),
    ('qt_lichtgitter_ohne_tuer',),
    ('qt_scherengitter',)], ui='8.8')

# ---- K Fahrkorb --------------------------------------------------------------------
g('K01', 'K', 'Notrufeinrichtung im Fahrkorb', [
    ('qk_notruf_vorhanden', 'Keine Notrufeinrichtung', False),
    ('qk_notruf_art',),
    ('qk_notruf_24h', 'Notruf nicht auf eine rund um die Uhr besetzte Stelle aufgeschaltet', False)], ui='8.1')
g('K15', 'K', 'Beleuchtung und Notbeleuchtung im Fahrkorb', [
    ('qk_beleuchtung',),
    ('qk_bel_zwei_lampen', 'Weniger als zwei parallel geschaltete Lampen im Fahrkorb', False),
    ('qk_bel_staendig', 'Fahrkorb nicht ständig beleuchtet (außer Parken mit geschlossenen Türen)', False),
    ('qk_notbeleuchtung',)], ui='8.29')
g('K07', 'K', 'Fahrkorb: Nennlast, Nutzfläche und Lüftung', [
    ('qk_nennlast_gekennz', 'Nennlast und zulässige Personenzahl nicht gekennzeichnet', False),
    ('qk_nutzflaeche_ok', 'Nutzfläche passt nicht zur Nennlast (Tabelle EN 81-20 5.4.2)', False),
    ('qk_lueftung',)], ui='8.16')
g('K08', 'K', 'Überlastkontrolle', [
    ('qk_ueberlast', 'Keine Überlastkontrolle / Lastmessung', False),
    ('qk_ueberlast_geprueft', 'Funktion nicht nachweislich geprüft', False)], ui='8.18')
g('K11', 'K', 'Brandfall: Steuerung und Hinweisschilder', [
    ('qk_bfs_vorhanden', 'Keine Brandfallsteuerung', False),
    ('qk_bfs_ausloesung',),
    ('qk_bfs_geprueft', 'Funktion nicht regelmäßig geprüft (kein Nachweis)', False),
    ('qk_hinweis_brandfall', 'Hinweisschild „Aufzug im Brandfall nicht benutzen" fehlt an mindestens einer Haltestelle', False)], ui='8.21')
g('K12', 'K', 'Barrierefreie Ausführung', [
    ('qk_en8170', 'Nicht nach DIN EN 81-70 barrierefrei ausgeführt', False),
    ('qk_bedienelemente', 'Bedienelemente nicht in erreichbarer Höhe / nicht ertastbar', False),
    ('qk_rollstuhl_mass', 'Fahrkorb für Rollstuhlnutzung zu klein (unter 1,00 m × 1,25 m)', False)], ui='8.22')
g('K14', 'K', 'Zustand der Fahrkorbausstattung, Vandalismus und soziales Umfeld', [
    ('qk_ausstattung',),
    ('qk_vandalismus_wiederholt', 'Wiederholte Vandalismusschäden', True),
    ('qk_en8171', 'Nicht vandalismussicher nach DIN EN 81-71 ausgeführt', False)], ui='8.26')

g('K04', 'K', 'Stufenbildung / Haltegenauigkeit', [
    ('qk_stufe_mm',),
    ('qk_stufe_mm_wert',)], ui='8.10')
g('K05', 'K', 'Fahrkorbtürschürze', [
    ('qk_schuerze_mm',),
    ('qk_schuerze_mm_wert',),
    ('qk_befreiung_nur_fachkundig',)], ui='8.12')
g('K06', 'K', 'Abstand Fahrkorbschwelle – Schachtwand', [
    ('qk_abstand_schwelle_mm',),
    ('qk_abstand_schwelle_mm_wert',),
    ('qk_fk_tuer_verriegelt',),
    ('qk_schachttuer_zusatzverriegelung',)], ui='8.14')

# ---- F Fahrkorbdach und Schachtkopf ----------------------------------------------
g('F01', 'F', 'Abstand Fahrkorbdachkante – Schachtwand', [
    ('qf_spalt_mm',),
    ('qf_spalt_mm_wert',)], ui='9.1')
g('F01a', 'F', 'Fahrkorbdach als Standfläche: Geländer, Fußleiste, Tragfähigkeit', [
    ('qf_gelaender', 'Kein Geländer auf dem Fahrkorbdach', False),
    ('qf_gelaender_hoehe_mm',),
    ('qf_fussleiste', 'Keine Fußleiste (mind. 100 mm) am Rand des Fahrkorbdachs', False),
    ('qf_dach_tragfaehig', 'Fahrkorbdach nicht tragfähig (200 kg auf 0,30 m × 0,30 m)', False)], ui='9.2')
g('F07', 'F', 'Schutzraum im Schachtkopf', [
    ('qf_schutzraum',),
    ('qf_kopffreiheit_gekennz', 'Keine Warnkennzeichnung zur reduzierten Kopffreiheit', False)], ui='9.7')
g('F05', 'F', 'Klappe / Notausstieg im Fahrkorbdach', [
    ('qf_klappe',),
    ('qf_klappe_ueberwacht', 'Klappe nicht elektrisch überwacht (Sicherheitskreis)', False)], ui='9.11')

# ---- S Schacht -----------------------------------------------------------------------
g('S01', 'S', 'Schachtumwehrung und Zugänge zum Schacht', [
    ('qs_vollumwehrt', 'Schacht nicht vollständig umwehrt (Wände, Decke, Boden)', False),
    ('qs_teilumwehrt_zulaessig', 'Teilumwehrung nicht nach EN 81-20 5.2.5.2.3 ausgeführt (Höhen, Abstände)', False),
    ('qs_zugang_schacht_sicher', 'Zugänge zum Schacht zugestellt oder nicht sicher erreichbar', False),
    ('qs_zugang_schalter_wirksam', 'Sicherheitseinrichtung der Schacht-/Inspektionstüren fehlt oder ist unwirksam', False)], ui='10.3')
g('S02', 'S', 'Schachtwände, Verglasung und Führungsschienen', [
    ('qs_wand_fest', 'Schachtwände nicht ausreichend fest / Durchbrüche', False),
    ('qs_glas_vsg', 'Kein VSG-Nachweis für die Schachtverglasung', False),
    ('qs_schienen_stahl', 'Führungsschienen für Fahrkorb und Gegengewicht nicht aus Stahl', False)], ui='10.4')
g('S04', 'S', 'Fangvorrichtung, Geschwindigkeitsbegrenzer und Schlaffseilsicherung', [
    ('qs_fang', 'Fangvorrichtung am Fahrkorb fehlt', False),
    ('qs_begrenzer', 'Geschwindigkeitsbegrenzer fehlt', False),
    ('qs_fang_ersatzausloesung', 'Zulässige Ersatzauslösung der Fangvorrichtung fehlt '
     '(indirekt angetriebener Hydraulikaufzug ohne Geschwindigkeitsbegrenzer)', False),
    ('qs_fang_geprueft', 'Prüfung von Fangvorrichtung und Begrenzer nicht dokumentiert', False),
    ('qs_spanngewicht_schalter', 'Spanngewicht des Begrenzerseils ohne Schlaffseilschalter', False),
    ('qs_schlaffseil', 'Schlaffseil-/Schlaffkettensicherung fehlt', False)], ui='10.7')

# ---- G Schachtgrube ---------------------------------------------------------------
g('G02', 'G', 'Zugang zur Schachtgrube', [
    ('qg_zugangstuer',),
    ('qg_leiter',),
    ('qg_zugangstuer_schalter', 'Grubenzugangstür ohne elektrische Sicherheitseinrichtung', False)], ui='11.6')
g('G03', 'G', 'Puffer', [
    ('qg_puffer', 'Puffer für Fahrkorb und Gegengewicht fehlen', False),
    ('qg_puffer_zustand',),
    ('qg_puffer_art',),
    ('qg_puffer_oelstand', 'Ölstand hydraulischer Puffer nicht prüfbar', False),
    ('qg_puffer_kennz', 'Kennzeichnung der hydraulischen Puffer fehlt', False)], ui='11.10')
g('G04', 'G', 'Gegengewicht in der Grube', [
    ('qg_gg_abtrennung',),
    ('qg_gg_fuellung', 'Gegengewichtsfüllung nicht gegen Herausfallen gesichert (Rahmen)', False),
    ('qg_gg_fang', 'Keine Fangvorrichtung am Gegengewicht / kein durchgehendes Fundament bei betretbarem Raum unter der Grube', False)], ui='11.11')
g('G07', 'G', 'Wasser, Feuchtigkeit und wassergefährdende Stoffe in der Grube', [
    ('qg_wasser',),
    ('qg_oel', 'Öl oder wassergefährdende Stoffe ohne Auffangmöglichkeit', True)], ui='11.15')

# ---- U Umfeld -----------------------------------------------------------------------
g('U01', 'U', 'Gefahrstoffe und Schadstoffsituation der Anlage', [
    ('qu_gefahrstoff_chem_lager', 'Chemische Gefahrstoffe in unmittelbarer Nähe gelagert', True),
    ('qu_gefahrstoff_bio_lager', 'Biologische Arbeitsstoffe in unmittelbarer Nähe gelagert (Labor, Klinik, Entsorgung)', True),
    ('qu_asbest_unbekannt', 'Asbest-/Schadstoffsituation der Anlage unbekannt (Baujahr vor 1995, keine Unterlagen, keine Beprobung)', True)], ui='15.28')
g('U02', 'U', 'Transport gefährlicher Stoffe mit dem Aufzug', [
    ('qu_transport_chem', 'Chemische Gefahrstoffe', True),
    ('qu_transport_chem_geregelt', 'Transport chemischer Gefahrstoffe nicht verbindlich geregelt', False),
    ('qu_transport_bio', 'Biologische Arbeitsstoffe / infektiöse Stoffe', True),
    ('qu_transport_bio_geregelt', 'Transport biologischer Arbeitsstoffe nicht verbindlich geregelt', False),
    ('qu_transport_brennbar', 'Brennbare oder leicht entzündliche Stoffe', True),
    ('qu_transport_brennbar_geregelt', 'Transport brennbarer Stoffe nicht verbindlich geregelt', False),
    ('qu_transport_radioaktiv', 'Radioaktive Stoffe', True),
    ('qu_transport_radioaktiv_geregelt', 'Strahlenschutzanweisung erfasst den Aufzugstransport nicht', False)],
  ui='15.32')
g('U03', 'U', 'Explosionsfähige Atmosphäre im Bereich der Anlage', [
    ('qu_ex_moeglich', 'Explosionsfähiges Gemisch im Bereich der Anlage möglich (Gase, Dämpfe, Stäube)', True),
    ('qu_ex_bewertet',),
    ('qu_ex_umgesetzt',)], ui='15.25')
g('U04', 'U', 'Umgebungsbedingungen', [
    ('qu_temperatur', 'Unzulässige Temperaturen im Triebwerksraum oder Schacht möglich', True),
    ('qu_feuchte_sicherheitsteile', 'Feuchtigkeit oder Kondensat an sicherheitsrelevanten Bauteilen (außerhalb der Grube)', True),
    ('qu_korrosion', 'Massive Korrosion, Betonabplatzungen oder andere bauliche Schäden', True)], ui='15.23')
g('U05', 'U', 'Bauliche Änderungen', [
    ('qu_bauliche_aenderung', 'Bauliche Änderungen am Schacht / Triebwerksraum ohne statische und sicherheitstechnische Bewertung', True),
    ('qu_verkleidung', 'Nachträgliche Verkleidungen oder Änderungen, die den Sicherheitszustand verschleiern', True)], ui='15.26')
g('U06', 'U', 'Brandschutzeinrichtungen des Gebäudes und ihre Schnittstellen zum Aufzug', [
    ('qu_bma_abgestimmt', 'Schnittstelle BMA – Aufzug nicht bekannt / nicht abgestimmt', False, 'Brandmeldeanlage'),
    ('qu_bma_geprueft', 'Funktion der Schnittstelle nicht geprüft (kein Nachweis)', False, 'Brandmeldeanlage'),
    ('qu_evak_in_gbu', 'Evakuierungs-/Sonderfunktion nicht im Brandschutzkonzept und in der Betriebsanweisung beschrieben', False, 'Brandmeldeanlage'),
    ('qu_brandschutz_behindert', None, None, 'Bauliche Brandschutzeinrichtungen'),
    ('qu_entrauchung', None, None, 'Entrauchung / RWA'),
    ('qu_sprinkler_abschaltung', 'Abschaltung der Aufzugsenergie vor Wasserbeaufschlagung nicht sichergestellt', False, 'Löschanlage'),
    ('qu_sprinkler_geprueft', 'Wirksamkeit der Abschaltung nicht geprüft und dokumentiert', False, 'Löschanlage')], ui='15.8a')
g('U10', 'U', 'Fremdgewerke und Reinigungspersonal im Aufzugsbereich', [
    ('qu_wartung_gefaehrlicher_zugang', 'Fremdgewerke (Lüftung, Elektro, Reinigung) müssen für ihre Arbeiten in Aufzugsbereiche', True),
    ('qu_fremd_zugangskonzept', 'Kein Zugangs- und Schutzkonzept für Fremdgewerke / Reinigungspersonal', False)], ui='15.36')
g('U11', 'U', 'Prüfnachweise und Zuständigkeiten der angrenzenden Gewerke', [
    ('qu_nachweise_fremdgewerke', 'Prüfnachweise der angrenzenden Gewerke (BMA, RWA, Ersatzstrom, Löschanlage) nicht verfügbar', False),
    ('qu_zustaendigkeit', 'Zuständigkeiten zwischen den Gewerken nicht geregelt', False)], ui='15.37')
g('U12', 'U', 'Verkehrsflächen und Flurförderzeuge', [
    ('qu_verkehrswege', 'Aufzugszugang grenzt unmittelbar an Fahrwege oder Verkehrsflächen (Tiefgarage, Anlieferung)', True),
    ('qa_nutzung_flurfoerderzeug', 'Beladung mit Flurförderzeugen oder Transportwagen', True)], ui='15.27')
g('U13', 'U', 'Emissionen, Lärm und soziales Umfeld', [
    ('qu_abgase', 'Abgase oder Emissionen (Tiefgarage, Werkstatt, Notstromaggregat)', True),
    ('qu_abgase_lueftung', 'Keine wirksame Lüftung/Absaugung des Aufstellbereichs nachgewiesen', False),
    ('qu_laerm', 'Erhöhte Lärmbelastung (über 85 dB(A))', True),
    ('qu_umfeld_kritisch', 'Kritisches soziales Umfeld (Vandalismus, Missbrauch der Anlage)', True)], ui='15.24')

# ---- SF Sonderfunktionen ----------------------------------------------------------
g('SF01', 'SF', 'Feuerwehr- / Evakuierungsaufzug: fehlende Nachweise und Abstimmungen', [
    ('qsf_unterlagen', 'Anforderungen und Unterlagen (EN 81-72, Brandschutzkonzept) fehlen', False),
    ('qsf_bma', 'Brandmeldeanlage und Feuerwehraufzugsfunktion nicht aufeinander abgestimmt', False),
    ('qsf_druckbelueftung', 'Druckbelüftungs-/Rauchschutzanlagen fehlen oder ungeprüft', False),
    ('qsf_loeschwasser', 'Löschwasser-/Pumpeneinrichtungen mit Schnittstelle zum Aufzug nicht berücksichtigt', False),
    ('qsf_ersatzstrom', 'Sicherheits-/Ersatzstromversorgung fehlt oder ungeprüft', False),
    ('qsf_ersatzstrom_test', 'Funktion unter Ersatzstrombedingungen nicht geprüft', False),
    ('qsf_nachweise', 'Erforderliche Prüfnachweise der Fremdgewerke nicht verfügbar', False),
    ('qsf_feuerwehr_doku', 'Schnittstellen zur Feuerwehr / Brandschutzdienststelle nicht dokumentiert', False),
    ('qsf_organisation', 'Betreiberorganisation nicht auf den Sonderbetrieb abgestimmt', False),
    ('qsf_cyber', 'Cyber-Auswirkungen auf die Feuerwehrfunktionen nicht gesondert betrachtet', False)], ui='16.1')

# ---- D Unterlagen und Betreiberorganisation ------------------------------------
g('D03', 'D', 'Instandhaltung und Wartungsunterlagen', [
    ('qd_wartungsunterlagen', 'Wartungsunterlagen / Prüfbuch fehlen oder nicht aktuell', False),
    ('qd_regelmaessige_wartung', 'Keine regelmäßige Instandhaltung durch ein Fachunternehmen (Wartungsvertrag)', False)], ui='3.9')
g('D04', 'D', 'Wiederkehrende Prüfung (ZÜS)', [
    ('qd_pruefplakette', 'Prüfplakette fehlt oder unleserlich', False),
    ('qd_pruefung_ueberfaellig', 'Prüffrist der wiederkehrenden Prüfung überschritten', True),
    ('qd_zues_bericht',)], ui='3.6')
g('D06', 'D', 'Beauftragte Person (Aufzugswärter)', [
    ('qd_beauftragte_person', 'Keine beauftragte Person schriftlich benannt', False),
    ('qd_unterweisung', 'Unterweisung nicht dokumentiert', False),
    ('qm_personal_eingewiesen', 'Nicht in die Personenbefreiung eingewiesen', False)], ui='E1')
g('D07', 'D', 'Betriebsanweisung, Zutritt und Entriegelungsschlüssel', [
    ('qd_betriebsanweisung', 'Betriebsanweisung fehlt oder nicht ausgehängt', False),
    ('qd_zugang_mr_geregelt', 'Zutritt zum Triebwerksraum / Steuerschrank organisatorisch nicht geregelt', False),
    ('qt_dreikant_hinterlegt', 'Passender Entriegelungsschlüssel (Dreikant) nicht vor Ort hinterlegt', False)], ui='E3')
g('D08', 'D', 'Technische Unterlagen', [
    ('qm_stromlaufplan',),
    ('qm_betriebsanleitung',)], ui='5.55')


# ---------------------------------------------------------------------------
# Anwendung auf den Seed
# ---------------------------------------------------------------------------
def _cats():
    from .common import CATS
    return CATS


def _leaves(expr, out):
    if not expr:
        return out
    if 'all' in expr:
        for e in expr['all']: _leaves(e, out)
    elif 'any' in expr:
        for e in expr['any']: _leaves(e, out)
    elif 'not' in expr:
        pass  # negierte Zweige liefern keine eindeutige Elternantwort
    else:
        out.append(expr)
    return out


def _rewrite(expr, code, spec, errors, where):
    """Ersetzt Vergleiche auf die Zahlenfrage <code> durch Optionsvergleiche."""
    if not expr:
        return expr
    if 'all' in expr:
        return {'all': [_rewrite(e, code, spec, errors, where) for e in expr['all']]}
    if 'any' in expr:
        return {'any': [_rewrite(e, code, spec, errors, where) for e in expr['any']]}
    if 'not' in expr:
        return {'not': _rewrite(expr['not'], code, spec, errors, where)}
    if expr.get('question') != code:
        return expr
    op = expr.get('operator')
    if op in ('ANSWERED', 'NOT_ANSWERED'):
        return expr
    key = (op, expr.get('value'))
    ziel = spec['ops'].get(key)
    if ziel is None:
        errors.append('%s: Vergleich %s %s %r auf %s ohne Entsprechung in SCHWELLEN' % (where, code, op, expr.get('value'), code))
        return expr
    if spec['type'] == 'YES_NO':
        return {'question': code, 'operator': 'EQ', 'value': ziel}
    return {'question': code, 'operator': 'IN', 'value': list(ziel)}


def schwellen(seed, errors):
    """Zahlenfragen in Schwellenfragen umschreiben (Fragen, Regeln, Sichtbarkeit, Pflicht)."""
    qmap = {q['code']: q for q in seed['questions']}
    hmap = {}
    for h in seed['hazards']:
        for hq in h.get('questions', []):
            hmap.setdefault(hq['question'], []).append(h)
    neue = []
    for code, spec in SCHWELLEN.items():
        q = qmap.get(code)
        if q is None:
            continue
        if q['type'] != 'NUMBER':
            continue  # bereits umgestellt
        mn, mx = q.get('min'), q.get('max')
        q['type'] = spec['type']; q['text'] = spec['text']; q['help_text'] = spec['help']
        q.pop('min', None); q.pop('max', None); q.pop('options', None)
        if spec['type'] == 'SELECT':
            q['options'] = [{'value': v, 'label': l} for v, l in spec['bands']]
        for r in seed['rules']:
            r['condition'] = _rewrite(r['condition'], code, spec, errors, r['code'])
            if r.get('applicability'):
                r['applicability'] = _rewrite(r['applicability'], code, spec, errors, r['code'] + '/applicability')
        for h in seed['hazards']:
            for hq in h.get('questions', []):
                for key in ('required_when', 'applicable_when'):
                    if hq.get(key):
                        hq[key] = _rewrite(hq[key], code, spec, errors, '%s/%s/%s' % (h['code'], hq['question'], key))
        for q2 in seed['questions']:
            if q2.get('visible_when'):
                q2['visible_when'] = _rewrite(q2['visible_when'], code, spec, errors, q2['code'] + '/visible_when')
        for a in seed.get('assumptions', []):
            a['when'] = _rewrite(a['when'], code, spec, errors, 'Annahme ' + a['question'])
        # optionales Messwertfeld ohne Regelwirkung, an derselben Gefährdung
        if spec.get('wert'):
            wcode, wtext = spec['wert']
            if wcode not in qmap:
                w = {'code': wcode, 'type': 'NUMBER', 'domain': 'GBU', 'text': wtext,
                     'category': q['category'], 'min': mn if mn is not None else 0,
                     'max': mx if mx is not None else 5000, 'optional': True,
                     'help_text': 'Dokumentation des Messwerts; die Bewertung nimmt die Bereichsauswahl.'}
                if q.get('ui_number'): w['ui_number'] = q['ui_number'] + 'm'
                if q.get('visible_when'): w['visible_when'] = q['visible_when']
                neue.append((q, w))
                for h in hmap.get(code, []):
                    h['questions'].append({'question': wcode, 'role': 'DOCUMENTATION', 'required_mode': 'NEVER',
                                           'notes': 'Optionaler Messwert zur Schwellenfrage (Kürzung 17.09.2026).'})
    for q, w in neue:
        seed['questions'].insert(seed['questions'].index(q) + 1, w)
    return seed


def vorbereiten(seed):
    """Vor set_best_case: streichen, verschieben, D05 einfügen, Schwellenfragen."""
    cats = _cats()
    errors = []
    schwellen(seed, errors)
    if errors:
        raise SystemExit('\n'.join('FEHLER ' + e for e in errors))
    weg = set(STREICHEN)
    seed['questions'] = [q for q in seed['questions'] if q['code'] not in weg]
    for h in seed['hazards']:
        h['questions'] = [hq for hq in h.get('questions', []) if hq['question'] not in weg]
    if 'assumptions' in seed:
        seed['assumptions'] = [a for a in seed['assumptions'] if a['question'] not in weg]
    for q in seed['questions']:
        z = VERSCHIEBEN.get(q['code'])
        if z:
            q['category'] = cats[z]
    if not any(q['code'] == D05['code'] for q in seed['questions']):
        d = dict(D05); d['category'] = cats['D']
        seed['questions'].append(d)
        for h in seed['hazards']:
            if h['code'] == D05_HAZARD and not any(x['question'] == D05['code'] for x in h['questions']):
                h['questions'].append({'question': D05['code'], 'role': 'DOCUMENTATION', 'required_mode': 'NEVER',
                                       'notes': 'Steuerfrage für die Nachweis-Vorbelegung (Kürzung 17.09.2026).'})
    # Reihenfolge: Erhebungsbereiche nach REIHENFOLGE, innerhalb Definitionsreihenfolge
    order = {cats[c]: i for i, c in enumerate(REIHENFOLGE)}
    idx = {id(q): i for i, q in enumerate(seed['questions'])}
    seed['questions'].sort(key=lambda q: (order.get(q['category'], 99), idx[id(q)]))
    return seed


def anreichern(seed):
    """Nach set_best_case: Gruppen, Nachweise, Stammdaten, Phasen."""
    cats = _cats()
    qmap = {q['code']: q for q in seed['questions']}
    # Stammdaten – nie per Sammelantwort (der Stamm ist die Anlage selbst)
    for code, key in STAMM.items():
        if code in qmap:
            qmap[code]['source'] = 'anlagenstamm'
            qmap[code]['stamm_key'] = key
            qmap[code].pop('best_case', None)
    # Sammelantwort im Umfeld: Dokumentationsfragen ohne Befundregel
    for code, (wert, _grund) in SAMMEL_DOKU.items():
        q = qmap.get(code)
        if q is not None and q['type'] == 'YES_NO' and q.get('best_case') is None:
            q['best_case'] = wert
    # Reine Dokumentationsfragen halten nichts auf
    for code in DOKU_OPTIONAL:
        if code in qmap:
            qmap[code]['optional'] = True
    # Messwerte nie per Sammelantwort (Entscheidung Arne, 17.09.2026): Die
    # Schwellenfragen und ihre optionalen Messfelder beantwortet der Prüfer
    # bewusst – „≤ 10 mm" ist ein Messergebnis, keine Sichtprüfung.
    for code, spec in SCHWELLEN.items():
        for c in (code, (spec.get('wert') or (None,))[0]):
            if c and c in qmap:
                qmap[c].pop('best_case', None)
    for code in KEIN_SAMMEL:
        if code in qmap:
            qmap[code].pop('best_case', None)
    # Phasen
    seed['category_phases'] = {cats[c]: p for c, p in PHASEN.items()}
    seed['category_order'] = [cats[c] for c in REIHENFOLGE]
    # Gruppen
    groups = []
    for grp in GRUPPEN:
        items = []
        members = {it['question'] for it in grp['items']}
        for it in grp['items']:
            q = qmap.get(it['question'])
            if q is None:
                continue
            d = {'question': it['question'], 'mode': it['mode']}
            if it.get('row'): d['row'] = it['row']
            if it['mode'] == 'check':
                d['label'] = it['label']
                d['value'] = it['value']
                d['clear'] = (not it['value']) if isinstance(it['value'], bool) else None
                # Elternantwort, die die Position sichtbar macht (nur innerhalb der Gruppe, nur EQ)
                implies = []
                for lf in _leaves(q.get('visible_when'), []):
                    if lf.get('operator') == 'EQ' and lf['question'] in members and lf['question'] != it['question']:
                        implies.append({'question': lf['question'], 'value': lf['value']})
                if implies: d['implies'] = implies
            items.append(d)
            q['group'] = grp['id']
        if not items:
            continue
        kind = grp.get('kind') or ('checklist' if all(i['mode'] == 'check' for i in items) else 'card')
        gd = {'id': grp['id'], 'title': grp['title'], 'category': cats[grp['bereich']], 'kind': kind, 'items': items}
        if grp.get('ui_number'): gd['ui_number'] = grp['ui_number']
        if grp.get('help'): gd['help'] = grp['help']
        groups.append(gd)
    seed['question_groups'] = groups
    # Nachweise
    nachweise = []
    for eintrag in NACHWEISE:
        code, wert, min_bj, nr, grund = eintrag[:5]
        zusatz = eintrag[5] if len(eintrag) > 5 else None
        q = qmap.get(code)
        if q is None or q['type'] == 'NUMBER':
            continue
        wann = {'question': D05['code'], 'operator': 'EQ', 'value': 'ohne_maengel'}
        if zusatz:
            wann = {'all': [wann, zusatz]}
        d = {'question': code, 'value': wert,
             'when': wann,
             'min_baujahr': min_bj, 'reason': grund,
             'source': (_HP % nr) if not nr.startswith('Anh') else 'TRBS 1201 Teil 4, ' + nr}
        nachweise.append(d)
    seed['nachweise'] = nachweise
    return seed


def pruefen(seed):
    """Fachliche Konsistenz; liefert (errors, warnings)."""
    errors, warnings = [], []
    qmap = {q['code']: q for q in seed['questions']}
    applicability = {hq['question'] for h in seed['hazards'] for hq in h.get('questions', []) if hq['role'] == 'APPLICABILITY'}
    for code in STREICHEN:
        if code in qmap:
            errors.append('erhebung: %s sollte gestrichen sein' % code)
    for code in VERSCHIEBEN:
        if code not in qmap:
            warnings.append('erhebung: zu verschiebende Frage %s nicht im Katalog' % code)
    regelfragen = set()
    for r in seed['rules']:
        for lf in _leaves(r['condition'], []) + _leaves(r.get('applicability'), []):
            regelfragen.add(lf['question'])
    steuert = set()
    for q in seed['questions']:
        for lf in _leaves(q.get('visible_when'), []):
            steuert.add(lf['question'])
    for a in seed.get('assumptions', []):
        for lf in _leaves(a.get('when'), []):
            steuert.add(lf['question'])
    for lf in _leaves(seed.get('assumptions_void_when'), []):
        steuert.add(lf['question'])
    for n in seed.get('nachweise', []):
        for lf in _leaves(n.get('when'), []):
            steuert.add(lf['question'])
    for h in seed['hazards']:
        for x in h.get('questions', []):
            if x.get('required_mode') in ('ALWAYS', 'CONDITIONAL'):
                steuert.add(x['question'])
            for k in ('applicable_when', 'required_when'):
                for lf in _leaves(x.get(k), []):
                    steuert.add(lf['question'])
    genutzt = {e[3] for e in NACHWEISE if e[3].isdigit()}
    fehlt = ({str(i) for i in range(1, ZUES_PRUEFPUNKTE + 1)} - genutzt
             - set(OHNE_KATALOGFRAGE) - set(NICHT_VORBELEGBAR))
    if fehlt:
        warnings.append('erhebung: Prüfpunkte der Hauptprüfung weder genutzt noch in '
                        'OHNE_KATALOGFRAGE / NICHT_VORBELEGBAR begründet: %s'
                        % ', '.join(sorted(fehlt, key=int)))
    doppelt = (genutzt & set(OHNE_KATALOGFRAGE)) | (genutzt & set(NICHT_VORBELEGBAR))
    if doppelt:
        errors.append('erhebung: Prüfpunkt %s ist als „ohne Katalogfrage" bzw. „nicht '
                      'vorbelegbar" begründet, wird aber für eine Vorbelegung genutzt'
                      % ', '.join(sorted(doppelt, key=int)))
    for code in KEIN_SAMMEL:
        if code not in qmap:
            warnings.append('erhebung: KEIN_SAMMEL %s nicht im Katalog' % code)
        elif qmap[code].get('best_case') is not None:
            errors.append('erhebung: %s darf keinen unauffälligen Wert tragen' % code)
    for code in DOKU_OPTIONAL:
        if code not in qmap:
            warnings.append('erhebung: DOKU_OPTIONAL %s nicht im Katalog' % code)
        elif code in regelfragen or code in steuert:
            errors.append('erhebung: %s ist nicht nur Dokumentation (Regel, Sichtbarkeit, '
                          'Annahme, Nachweis oder Pflichtfrage) und darf nicht optional sein' % code)
    for code, (wert, _grund) in SAMMEL_DOKU.items():
        q = qmap.get(code)
        if q is None:
            warnings.append('erhebung: SAMMEL_DOKU %s nicht im Katalog' % code)
        elif q['type'] != 'YES_NO' or not isinstance(wert, bool):
            errors.append('erhebung: SAMMEL_DOKU %s muss Ja/Nein sein' % code)
    for code in STAMM:
        if code not in qmap:
            warnings.append('erhebung: Stammdaten-Frage %s nicht im Katalog' % code)
    seen = set()
    for grp in seed.get('question_groups', []):
        for it in grp['items']:
            q = qmap.get(it['question'])
            if q is None:
                errors.append('Gruppe %s: unbekannte Frage %s' % (grp['id'], it['question'])); continue
            if it['question'] in seen:
                errors.append('Gruppe %s: Frage %s in mehreren Gruppen' % (grp['id'], it['question']))
            seen.add(it['question'])
            if q['category'] != grp['category']:
                errors.append('Gruppe %s: Frage %s liegt im Bereich „%s“, Gruppe in „%s“' % (grp['id'], it['question'], q['category'][:2], grp['category'][:2]))
            if it['mode'] == 'check':
                if q['type'] != 'YES_NO':
                    errors.append('Gruppe %s: Ankreuzposition %s ist keine Ja/Nein-Frage' % (grp['id'], it['question']))
                elif not isinstance(it.get('value'), bool):
                    errors.append('Gruppe %s: Position %s ohne auffälligen Wert' % (grp['id'], it['question']))
                elif q.get('best_case') is not None and it['value'] == q['best_case']:
                    errors.append('Gruppe %s: Position %s – auffälliger Wert %r widerspricht best_case %r' % (grp['id'], it['question'], it['value'], q['best_case']))
                if it['question'] in applicability and grp['category'][0] != 'A':
                    warnings.append('Gruppe %s: Position %s ist APPLICABILITY-Frage' % (grp['id'], it['question']))
    for grp in GRUPPEN:
        for it in grp['items']:
            if it['question'] not in qmap:
                warnings.append('Gruppe %s: Frage %s nicht im Katalog (übersprungen)' % (grp['id'], it['question']))
    # Mehrere Vorbelegungen je Frage sind zulässig, solange ihre Freischalt-
    # bedingungen sich unterscheiden (Prüfbericht 20.09.2026 B05: Schutzraum
    # „normgerecht" ab 2017, „altnorm" davor). Gleiche Bedingung = echte Dopplung.
    gesehen = {}
    for n in seed.get('nachweise', []):
        code = n['question']
        kennung = _json.dumps(n['when'], sort_keys=True, ensure_ascii=False)
        if kennung in gesehen.get(code, set()):
            errors.append('Nachweis %s: doppelt (gleiche Freischaltbedingung)' % code)
        gesehen.setdefault(code, set()).add(kennung)
        q = qmap.get(code)
        if q is None:
            errors.append('Nachweis %s: unbekannte Frage' % code); continue
        if code in applicability:
            errors.append('Nachweis %s: APPLICABILITY-Frage darf nicht vorbelegt werden' % code)
        if q['type'] == 'YES_NO':
            if not isinstance(n['value'], bool):
                errors.append('Nachweis %s: Wert muss Ja/Nein sein' % code)
            elif q.get('best_case') is not None and n['value'] != q['best_case']:
                errors.append('Nachweis %s: Wert %r widerspricht best_case %r' % (code, n['value'], q['best_case']))
        elif q['type'] == 'SELECT':
            if n['value'] not in {o['value'] for o in q.get('options', [])}:
                errors.append('Nachweis %s: Wert %r nicht in Optionen' % (code, n['value']))
        else:
            errors.append('Nachweis %s: Typ %s nicht vorbelegbar' % (code, q['type']))
        if n.get('min_baujahr') is not None and not isinstance(n['min_baujahr'], int):
            errors.append('Nachweis %s: min_baujahr muss Jahr oder null sein' % code)
    for code in {e[0] for e in NACHWEISE}:
        if code not in qmap:
            warnings.append('Nachweis %s: Frage nicht im Katalog (übersprungen)' % code)
        elif qmap[code]['type'] == 'NUMBER':
            warnings.append('Nachweis %s: Zahlenfrage – erst nach Umstellung auf Schwellenfrage vorbelegbar' % code)
    if not any(q['code'] == D05['code'] for q in seed['questions']):
        errors.append('D05 (%s) fehlt' % D05['code'])
    return errors, warnings


def umfeld_offen(seed):
    """Fragen im Umfeld, die eine Sammelantwort NICHT setzt (kein best_case,
    nicht aus dem Stamm) – zur Kontrolle im Generatorlauf."""
    cat = _cats()['U']
    return [q['code'] for q in seed['questions']
            if q.get('category') == cat and q.get('best_case') is None
            and q.get('source') != 'anlagenstamm']


def kennzahlen(seed):
    """Karten statt Fragen: wie viele Karten sieht der Prüfer je Bereich."""
    from collections import Counter
    grouped = {it['question'] for grp in seed.get('question_groups', []) for it in grp['items']}
    karten = Counter()
    for q in seed['questions']:
        if q['code'] not in grouped:
            karten[q['category'][:2].strip()] += 1
    for grp in seed.get('question_groups', []):
        karten[grp['category'][:2].strip()] += 1
    return dict(karten), sum(karten.values())
