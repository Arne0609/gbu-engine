# -*- coding: utf-8 -*-
"""Begruendete Annahmen fuer den mehrfragigen Katalog (EN 81-20 / EN 81-80).

Jede Zeile hier macht eine Frage optional: Passt das Baujahr, gilt das Merkmal
als vorhanden, bis jemand widerspricht. Rechtsgrundlage ist in jedem Fall die
Abnahme durch eine zugelassene Ueberwachungsstelle vor der Inbetriebnahme
(BetrSichV; frueher TRA/ZUES) - ein Merkmal, das zum Baujahr vorgeschrieben
war, ist dort geprueft worden.

Die drei Grenzen fuer neue Eintraege stehen in common.py bei `annahme`.
Vor dem Erweitern lesen: Zustands- und Organisationsfragen gehoeren NICHT
hierher, und Fragen mit Rolle APPLICABILITY ebenfalls nicht (der Generator
weist beides zurueck).
"""
from .common import (annahme, BJ_AUFZUGSRICHTLINIE, BJ_UCM, BJ_EN8120)

# Rechtsstand fuer den Zweiwege-Notruf: EN 81-28 wurde 2004 harmonisiert und
# ist mit EN 81-20 durchgaengig gefordert. Wir setzen die spaetere, sichere
# Schwelle - eine Anlage von 2005 kann noch ohne gebaut worden sein.
BJ_NOTRUF_EN8128 = BJ_EN8120

_AR = ('Bei Inverkehrbringen ab 01.07.1999 nach Aufzugsrichtlinie 95/16/EG '
       'und DIN EN 81-1/2 gefordert und bei der Abnahme nachgewiesen')
_A3 = ('Seit 01.01.2012 verbindlich (DIN EN 81-1/2 + A3); ohne Nachweis und '
       'Funktionspruefung des UCM-Schutzes durfte die Anlage nicht in Betrieb '
       'genommen werden')
_20 = ('Bei Inverkehrbringen ab 01.09.2017 nach DIN EN 81-20/50 gefordert und '
       'bei der Abnahme nachgewiesen')


def registriere():
    """Traegt alle Annahmen ein. Wird vom Generator nach dem Laden der
    Fragen und Gefaehrdungen gerufen."""

    # ── Ab 2012: unbeabsichtigte Fahrkorbbewegung ────────────────────────
    # Der Anlass fuer die ganze Mechanik: Das UCM-System sieht man der Anlage
    # nicht an, es steht in den Abnahmeunterlagen - und ohne bestandene
    # Funktionspruefung gab es keine Inbetriebnahme.
    annahme('qa_ucm_a3', BJ_UCM, _A3)
    annahme('qm_bremse_ueberwacht', BJ_UCM,
            _A3 + '; die Bremsueberwachung ist Teil dieses Schutzes')

    # ── Ab 1999: Grundausstattung nach Aufzugsrichtlinie ─────────────────
    # Schachttueren
    annahme('qt_verriegelung_elektrisch', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qt_fehlschliess', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qt_notentriegelung_alle', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qt_rueckhaltung_tuerblatt', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qt_glas_normgerecht', BJ_AUFZUGSRICHTLINIE, _AR)

    # Schacht und Tragmittel
    annahme('qs_fang', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qs_begrenzer', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qs_spanngewicht_schalter', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qs_schlaffseil', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qs_vollumwehrt', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qs_wand_fest', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qs_schienen_stahl', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qs_glas_vsg', BJ_AUFZUGSRICHTLINIE, _AR)

    # Schachtgrube
    annahme('qg_puffer', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qg_nothalt', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qg_gg_fuellung', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qg_gg_fang', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qg_nachbar_abtrennung', BJ_AUFZUGSRICHTLINIE, _AR)

    # Triebwerk, Antrieb und Steuerung
    annahme('qm_zweikreisbremse', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_motorschutz', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_schuetze_unabhaengig', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_laufzeit', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_phasenumkehr', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_absperrventil', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_rohrbruch', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_hauptschalter', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_hauptschalter_abschliessbar', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_hauptschalter_gekennz', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_beruehrungssicher', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_einzug_treibscheibe', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_einzug_begrenzer', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_potenzialausgleich', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_hoehe_180', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_freiflaeche', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_notbetrieb', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_notbetrieb_gekennz', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qm_rollenraum_nothalt', BJ_AUFZUGSRICHTLINIE, _AR)

    # Zugang zum Triebwerksraum
    annahme('qz_tuer_abschliessbar', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qz_tuer_mass', BJ_AUFZUGSRICHTLINIE, _AR)

    # Fahrkorb
    annahme('qk_notruf_vorhanden', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qk_nennlast_gekennz', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qk_nutzflaeche_ok', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qk_ueberlast', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qk_bel_zwei_lampen', BJ_AUFZUGSRICHTLINIE, _AR)

    # Fahrkorbdach und Schachtkopf
    annahme('qf_gelaender', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qf_fussleiste', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qf_inspektion', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qf_inspektion_schutz', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qf_inspektion_erreichbar', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qf_inspektion_geschw', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qf_nothalt', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qf_dach_tragfaehig', BJ_AUFZUGSRICHTLINIE, _AR)
    annahme('qf_klappe_ueberwacht', BJ_AUFZUGSRICHTLINIE, _AR)

    # ── Ab 2017: was DIN EN 81-20/50 zusaetzlich fordert ─────────────────
    annahme('qg_nothalt_aussen', BJ_EN8120, _20)
    annahme('qg_nothalt_zwei', BJ_EN8120, _20)
    annahme('qg_inspektion', BJ_EN8120, _20)
    annahme('qg_selbstbefreiung', BJ_EN8120, _20)
    annahme('qg_zugangstuer_schalter', BJ_EN8120, _20)
    annahme('qg_notruf', BJ_EN8120, _20)
    annahme('qk_fk_tuer_verriegelt', BJ_EN8120, _20)
    annahme('qt_glas_einzugsschutz', BJ_EN8120, _20)
    annahme('qf_notbeleuchtung', BJ_EN8120, _20)
    annahme('qf_notruf_dach', BJ_EN8120, _20)
    annahme('qk_notruf_en8128', BJ_NOTRUF_EN8128,
            'Zweiwege-Notrufsystem nach DIN EN 81-28, mit DIN EN 81-20 ab '
            '01.09.2017 durchgaengig gefordert und bei der Abnahme geprueft')
