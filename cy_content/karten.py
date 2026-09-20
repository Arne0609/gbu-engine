# -*- coding: utf-8 -*-
"""Erhebungskarten (question_groups) für den Cyber-Typ.

Umsetzung des Reduktionsbefundes R12 aus dem Prüfbericht vom 20.09.2026
(„Cyber integriert"): Die Cyber-Quellfragen bleiben VOLLSTÄNDIG im Datenmodell
– gleiche Codes, gleiche Gefährdungen, gleiche Regeln, gleiche Regel-IDs –,
werden dem Prüfer aber als wenige Sammelkarten gezeigt. Für die Riedl-Variante
verdichten sich die 58 Cyber-Fragen damit auf 11 Karten, für den vollen
Cyber-Katalog auf 16.

Wie im 81-20-Typ (mf_content/erhebung.py, Mechanik 1) ist das eine reine
DARSTELLUNG: Antworten bleiben Antworten auf die Einzelfragen, die Engine
rechnet unverändert.

Unterschied zum 81-20-Typ – alle Positionen laufen im Modus `native`, keine
Karte ist eine `checklist`:
  Die Ankreuz-Mechanik der 81-20-Karten setzt beim Bestätigen („keine weiteren
  Auffälligkeiten") alle nicht angekreuzten, sichtbaren Positionen auf ihren
  unauffälligen Wert. Das trägt dort, wo der Befund eine Sichtprüfung ist
  (Leuchte defekt, Not-Halt fehlt) – deshalb hat dort jede Frage ein
  `best_case`. Die Cyber-Fragen sind keine Sichtbefunde: „Zugriffsrechte
  rollenbasiert vergeben?", „Werkszugangsdaten geändert?", „Wirksamkeits-
  nachweis vorhanden?" werden erfragt, in Unterlagen geprüft oder am Gerät
  nachgesehen. Ein Sammel-„unauffällig" würde hier unbelegte Tatsachen
  behaupten – genau das fail-open-Verhalten, das der Katalog sonst vermeidet
  (unbeantwortet ≠ kein Risiko). Cyber-Fragen tragen folgerichtig kein
  `best_case` (set_best_case läuft nur im 81-20-Typ). Die Verdichtung liegt
  deshalb in der Gruppierung und Gliederung (Zeilen), nicht im Vorbelegen.

Aufruf aus gen_cy_catalog.build():  karten.anreichern(seed)
und aus main():                     errors += karten.pruefen(seed)
"""
from cy_content import common as C

KARTEN = []


def k(gid, bereich, titel, items, ui=None, help=None):
    """items: Frage-Code oder (Frage-Code, Zeile)."""
    assert not any(x['id'] == gid for x in KARTEN), 'doppelte Karte ' + gid
    its = []
    for t in items:
        code, row = (t, None) if isinstance(t, str) else t
        it = {'question': code, 'mode': 'native'}
        if row:
            it['row'] = row
        its.append(it)
    d = {'id': gid, 'bereich': bereich, 'title': titel, 'items': its}
    if ui:
        d['ui_number'] = ui
    if help:
        d['help'] = help
    KARTEN.append(d)
    return gid


# ---------------------------------------------------------------------------
# A – Systemabgrenzung
# ---------------------------------------------------------------------------
k('CY-A', 'A', 'Systemabgrenzung der Anlage', [
    'qa_aufzugsart',
    'qa_steuerungsart',
    'qa_ueberwachungsbeduerftig',
    'qa_maschinenraum',
    ('qa_vernetzt', 'Schnittstellen nach außen'),
    ('qa_gebaeude_anbindung', 'Schnittstellen nach außen'),
    'qa_hersteller_vorgaben'], ui='1',
  help='Systemabgrenzung nach TRBS 1115 Teil 1 Abschn. 4.2: Welche Einrichtungen gehören '
       'zum betrachteten System und welche Schnittstellen führen aus ihm heraus? Die '
       'Antworten auf 1.5 (Netzanbindung) und 1.6 (bauseitige Systeme) schalten die '
       'Karten „Netz, Fernzugriff und Härtung" und „Bauseitige Einrichtungen".')

# ---------------------------------------------------------------------------
# Z – Zugang und Zugriff (geteilte Modifier über alle Komponenten)
# ---------------------------------------------------------------------------
k('CY-Z', 'Z', 'Zugang und Servicezugriff', [
    ('qz_steuerung_frei', 'Örtlicher Zugang'),
    ('qz_triebwerksraum_frei', 'Örtlicher Zugang'),
    ('qz_schacht_frei', 'Örtlicher Zugang'),
    ('qz_service_gesichert', 'Schnittstellen und Zugangsdaten'),
    ('qz_default_zugangsdaten', 'Schnittstellen und Zugangsdaten'),
    ('qz_zugangsdaten_bekannt', 'Schnittstellen und Zugangsdaten'),
    ('qz_rollen', 'Rollen und Geräte'),
    ('qz_servicegeraete', 'Rollen und Geräte')], ui='2',
  help='Zugangskontrolle Hardware und Software nach TRBS 1115-1 Abschn. 4.5.2. Diese '
       'Antworten wirken als Modifier auf ALLE Komponenten: freier Zugang oder '
       'Werkszugangsdaten heben die Bewertung jeder Komponente mit Schnittstelle an.')

# ---------------------------------------------------------------------------
# C – Komponenten (je Komponente eine Karte: vorhanden? Schnittstelle?
#     Maßnahmen? unabhängige Rückfallebene?)
# ---------------------------------------------------------------------------
_KOMPONENTEN = [
    ('CY-C1', 'Aufzugssteuerung', '3.1', 'steuerung',
     'Die Aufzugssteuerung ist immer vorhanden; erhoben werden Schnittstelle, Maßnahmen '
     'und die Frage, ob der Sicherheitskreis unabhängig von ihr wirkt.'),
    ('CY-C2', 'PESSRAL (programmierbare Sicherheitsschaltung)', '3.2', 'pessral', None),
    ('CY-C3', 'Frequenzumrichter', '3.3', 'fu', None),
    ('CY-C4', 'Notrufsystem (Zwei-Wege-Kommunikation)', '3.4', 'notruf', None),
    ('CY-C5', 'Schachtkopierung / Positionierung', '3.5', 'kopierung', None),
    ('CY-C6', 'Türsteuerung', '3.6', 'tuer', None),
    ('CY-C7', 'UCM-Erkennung', '3.7', 'ucm', None),
    ('CY-C8', 'SAFÜ (Schutz gegen Übergeschwindigkeit)', '3.8', 'safue', None),
    ('CY-C9', 'Tragmittelüberwachung', '3.9', 'tragmittel', None),
    ('CY-C10', 'Hydraulischer Steuerblock', '3.10', 'hydraulik', None),
]
_HILFE_KOMP = ('Komponentenbasierte Betrachtung nach EK-ZÜS B-002 rev. 5 / BA-017: '
               'Ohne kompromittierbare Schnittstelle endet die Betrachtung hier '
               '(Vorscreening). Sonst entscheiden die Schutzmaßnahmen nach '
               'TRBS 1115-1 Abschn. 4.5.2 und die unabhängige Rückfallebene über die Stufe.')
# Nicht jede Komponente hat alle vier Fragen: die Aufzugssteuerung ist immer
# vorhanden (keine „vorhanden?"-Frage), PESSRAL hat keine unabhängige
# Rückfallebene (es IST die Sicherheitsebene). Deshalb werden die Positionen
# gegen die tatsächlich definierten Fragen gefiltert – ein Tippfehler im
# Präfix fiele dadurch auf, dass die Karte leer bliebe (pruefen() meldet dann
# die verwaisten Fragen).
_VORHANDEN = {q['code'] for q in C.QUESTIONS}
for _gid, _titel, _ui, _pre, _hilfe in _KOMPONENTEN:
    _items = [c for c in ('qc_%s_vorhanden' % _pre, 'qc_%s_schnittstelle' % _pre,
                          'qc_%s_massnahmen' % _pre, 'qc_%s_unabhaengig' % _pre)
              if c in _VORHANDEN]
    assert _items, 'Komponentenkarte ohne Fragen: ' + _gid
    k(_gid, 'C', 'Komponente: ' + _titel, _items, ui=_ui,
      help=(_hilfe + ' ' + _HILFE_KOMP) if _hilfe else _HILFE_KOMP)

# ---------------------------------------------------------------------------
# N – Netz, Fernzugriff, Gateway und Härtung
#     (Karte quer über die Bereiche C und N: die Gateway-/Fernzugriffsfragen
#      sind fachlich ein Block, auch wenn sie im Datenmodell auf C und N liegen.)
# ---------------------------------------------------------------------------
k('CY-N', 'N', 'Netz, Fernzugriff, Gateway und Härtung', [
    ('qc_fernueb_vorhanden', 'Fernüberwachung'),
    ('qc_fernueb_lesend', 'Fernüberwachung'),
    ('qc_remote_vorhanden', 'Fernwartung / Remote-Service'),
    ('qn_fern_freigabe', 'Fernwartung / Remote-Service'),
    ('qn_fern_auth', 'Fernwartung / Remote-Service'),
    ('qc_gateway_vorhanden', 'Gateway / Router / Dongle'),
    ('qc_gateway_firewall', 'Gateway / Router / Dongle'),
    ('qc_gateway_default', 'Gateway / Router / Dongle'),
    ('qc_gateway_updates', 'Gateway / Router / Dongle'),
    ('qn_segmentierung', 'Netztrennung und Protokollierung'),
    ('qn_protokoll', 'Netztrennung und Protokollierung'),
    ('qn_softwarestand', 'Härtung und Softwarestand'),
    ('qn_funktionsreduzierung', 'Härtung und Softwarestand')], ui='4',
  help='Segmentierung, Funktionsreduzierung und Überwachung nach TRBS 1115-1 '
       'Abschn. 4.5.2. Die Zeilen Fernüberwachung, Fernwartung und Gateway erscheinen '
       'nur bei vernetzter Anlage (1.5); Protokollierung und Härtung gelten auch ohne '
       'Netzanbindung, weil Servicegeräte vor Ort dieselben Schnittstellen benutzen.')

# ---------------------------------------------------------------------------
# C – Bauseitige Einrichtungen (Gebäudeschnittstelle)
# ---------------------------------------------------------------------------
k('CY-G', 'C', 'Bauseitige Einrichtungen (Brandfallsteuerung, Entrauchung, Zutritt)', [
    'qc_geb_rueckwirkungsfrei',
    'qc_geb_sicherer_zustand'], ui='3.14',
  help='Schnittstelle zu Anlagen, die nicht zum Aufzug gehören und nicht vom '
       'Aufzugsbetreiber gepflegt werden. Maßgeblich ist die Rückwirkungsfreiheit '
       '(ZÜS-Prüfpunkt 9) und das Verhalten bei Ausfall oder Manipulation des '
       'bauseitigen Signals.')

# ---------------------------------------------------------------------------
# O – Organisation und Notfall
# ---------------------------------------------------------------------------
k('CY-O', 'O', 'Organisation, Fachkunde und Notfallmanagement', [
    ('qo_verantwortlich', 'Verantwortung und Fachkunde'),
    ('qo_fachkunde', 'Verantwortung und Fachkunde'),
    ('qo_unterweisung', 'Verantwortung und Fachkunde'),
    ('qo_notfall', 'Notfall und laufende Kontrolle'),
    ('qo_pruefung_fristen', 'Notfall und laufende Kontrolle'),
    ('qo_erkenntnisse', 'Notfall und laufende Kontrolle'),
    ('qo_rueckwirkung', 'Änderungen und Rückwirkungsfreiheit'),
    ('qo_aenderungen', 'Änderungen und Rückwirkungsfreiheit'),
    ('qo_aenderungen_geprueft', 'Änderungen und Rückwirkungsfreiheit')], ui='5a',
  help='Organisatorische Pflichten des Betreibers: BetrSichV § 3 Abs. 1 und § 12, '
       'TRBS 1115-1 Abschn. 3.3.2 (Fachkunde) und 4.5.2 (Notfallmanagement).')

# ---------------------------------------------------------------------------
# O – Nachweise für den ZÜS-Abschlusscheck
# ---------------------------------------------------------------------------
k('CY-D', 'O', 'Nachweise für den ZÜS-Abschlusscheck', [
    ('qo_wirksamkeit', 'Wirksamkeit und Funktion'),
    ('qo_funktion', 'Wirksamkeit und Funktion'),
    ('qo_zues_beruecksichtigt', 'Dokumentation der Gefährdungsbeurteilung'),
    ('qo_zues_erfasst', 'Dokumentation der Gefährdungsbeurteilung'),
    ('qo_zues_erhebliches_risiko', 'Dokumentation der Gefährdungsbeurteilung'),
    ('qo_zues_stand_technik', 'Dokumentation der Gefährdungsbeurteilung')], ui='5b',
  help='Die vier Dokumentationsfragen 5.11–5.14 belegen die ZÜS-Prüfpunkte 1, 2, 3 und 5 '
       '(EK-ZÜS B-002 rev. 5, Anhang 2); 5.6 und 5.7 belegen die Prüfpunkte 12 und 13 '
       '(TRBS 1115-1 Abschn. 5 und 8.2). Sie halten die Erhebung nicht auf '
       '(Pflichtmodus NIE), fehlen aber im Bericht sichtbar.')


# ---------------------------------------------------------------------------
def anreichern(seed):
    """Karten in den Seed schreiben und die Fragen ihrer Karte zuordnen."""
    qmap = {q['code']: q for q in seed['questions']}
    gruppen = []
    for karte in KARTEN:
        items = [dict(it) for it in karte['items'] if it['question'] in qmap]
        if not items:
            continue
        for it in items:
            qmap[it['question']]['group'] = karte['id']
        g = {'id': karte['id'], 'title': karte['title'],
             'category': C.CATS[karte['bereich']], 'kind': 'card', 'items': items}
        if karte.get('ui_number'):
            g['ui_number'] = karte['ui_number']
        if karte.get('help'):
            g['help'] = karte['help']
        gruppen.append(g)
    seed['question_groups'] = gruppen
    return seed


def pruefen(seed):
    """Jede Frage genau einmal auf genau einer Karte."""
    errors = []
    qmap = {q['code']: q for q in seed['questions']}
    gesehen = {}
    for karte in KARTEN:
        if karte['bereich'] not in C.CATS:
            errors.append('karten: %s – unbekannter Erhebungsbereich %s'
                          % (karte['id'], karte['bereich']))
        for it in karte['items']:
            code = it['question']
            if code not in qmap:
                errors.append('karten: %s – unbekannte Frage %s' % (karte['id'], code))
            elif code in gesehen:
                errors.append('karten: %s liegt auf zwei Karten (%s, %s)'
                              % (code, gesehen[code], karte['id']))
            else:
                gesehen[code] = karte['id']
    ohne = [q['code'] for q in seed['questions'] if q['code'] not in gesehen]
    if ohne:
        errors.append('karten: Fragen ohne Karte: %s' % ', '.join(ohne))
    return errors
