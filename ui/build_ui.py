# -*- coding: utf-8 -*-
"""Baut die eigenständige Bewertungsoberfläche: bettet die Engine-Katalog-Seeds
(getrimmt) und die Klärungsliste in assessment_ui.html ein -> gbu_bewertung.html.

Lauf:  python3 build_ui.py    (aus engine_model/ui/, Seeds liegen in ../)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = [
    ('norm_81_20_mf.json', 'GBU mehrfragig · EN 81-20 (MF, Entwurf)'),
    ('norm_cyber_mf.json', 'Cyber-GBU komponentenbasiert (CY, Entwurf)'),
    ('norm_en8141.json', 'Plattformaufzug · EN 81-41'),
    ('norm_81_80.json', 'GBU vereinfacht · EN 81-80'),
    ('norm_81_20.json', 'GBU erweitert · EN 81-20'),
    ('norm_2026.json', 'Ergänzung 2026 · Gebäude & Cyber-Matrix'),
    ('norm_cyber_voll.json', 'Cyber · TRBS 1115-1 (voll)'),
    ('norm_cyber_minimal.json', 'Cyber · minimal'),
]

# Beispielanlage für den mehrfragigen Typ: Seilaufzug mit Maschinenraum,
# einige typische Befunde, damit die Oberfläche in einem sprechenden Zustand
# öffnet (Hoch/Mittel/Kein Risiko/Nicht zutreffend/Unvollständig nebeneinander).
DEMO_MF = {
    'qa_aufzugsart': 'seil', 'qa_antrieb': 'geregelt', 'qa_nenngeschwindigkeit': 1.0,
    'qa_gegengewicht': True, 'qa_maschinenraum': True, 'qa_rollenraum': False,
    'qa_mehrere_aufzuege': False, 'qa_raum_unter_schacht': False, 'qa_fahrkorbtuer': True,
    'qa_glas_schachttueren': False, 'qa_glas_fahrkorbtueren': False, 'qa_glas_schacht': False,
    'qa_nutzungsart': 'personen', 'qa_nutzung_pmem': True, 'qa_nutzung_kinder': False,
    'qa_nutzung_flurfoerderzeug': False, 'qa_oeffentlich': True,
    'qa_norm_inverkehrbringen': 'en81_1_2', 'qa_feuerwehraufzug': False, 'qa_bfs_gefordert': False,
    'qa_bma_vorhanden': False, 'qa_entrauchung_vorhanden': True, 'qa_sprinkler_vorhanden': False,
    'qa_ucm_a3': False, 'qa_lagerung_statisch_bestimmt': True, 'qa_grubentiefe': 1.4,
    # Zugang
    'qz_bel_vorhanden': True, 'qz_bel_ausreichend': False, 'qz_bel_defekt': False,
    'qz_weg_sicher': True, 'qz_weg_eng': False, 'qz_aufstieg': 'treppe_handlauf', 'qz_aufstieg_bruch': False,
    'qz_absturzkante': False, 'qz_uebersteigen': False, 'qz_von_innen': 'ja', 'qz_durch_fremde': 'nein',
    'qz_material_erschwert': False, 'qz_tuer_vorhanden': True, 'qz_tuer_abschliessbar': True,
    'qz_tuer_zustand': True, 'qz_tuer_mass': True, 'qz_flucht_frei': True, 'qz_flucht_gekennz': True,
    'qz_flucht_eingeengt': False, 'qz_zugang_befreiung': 'jederzeit',
    # Triebwerksraum
    'qm_bel_vorhanden': True, 'qm_bel_200lux': True, 'qm_bel_geeignet': True, 'qm_bel_splitterschutz': True,
    'qm_beruehrungssicher': True, 'qm_dguv_v3': True, 'qm_bauseitig_ok': True, 'qm_ortsfest_geprueft': True,
    'qm_potenzialausgleich': True, 'qm_einzug_treibscheibe': True, 'qm_einzug_begrenzer': False,
    'qm_einzug_grad': 'teilweise', 'qm_hoehe_180': True, 'qm_freiflaeche': True, 'qm_lagerung': False,
    'qm_niveau': False, 'qm_bodenoeffnung': False, 'qm_boden_rutschhemmend': True, 'qm_boden_oelfest': True,
    'qm_oel_ausgetreten': False, 'qm_hauptschalter': True, 'qm_hauptschalter_abschliessbar': True,
    'qm_hauptschalter_gekennz': True, 'qm_zweikreisbremse': True, 'qm_bremse_ueberwacht': True,
    'qm_motorschutz': True, 'qm_schuetze_unabhaengig': True, 'qm_laufzeit': True,
    'qm_anschlagpunkte': True, 'qm_tragfaehigkeit': True, 'qm_anschlag_geprueft': True,
    'qm_notbetrieb': True, 'qm_notbetrieb_gekennz': True, 'qm_personal_eingewiesen': True,
    'qm_kennz_elektrisch': True, 'qm_stromlaufplan': 'aktuell', 'qm_beschilderung': True,
    'qm_betriebsanleitung': 'aktuell', 'qm_sprechverbindung': 'ok', 'qm_fremd_frei': True,
    # Türen / Fahrkorb
    'qt_verriegelung_elektrisch': True, 'qt_fehlschliess': True, 'qt_selbstschliessend': True,
    'qt_schliesst_nach_notentriegelung': True, 'qt_notentriegelung_alle': True, 'qt_dreikant_hinterlegt': True,
    'qt_notentriegelung_hoehe': True, 'qt_feuerwiderstand': 'nicht_gefordert', 'qt_fk_tuer_automatisch': True,
    'qt_schliesskante': 'lichtgitter',
    'qk_notruf_vorhanden': True, 'qk_notruf_art': 'sprech_staendig', 'qk_notruf_24h': True, 'qk_notruf_en8128': True,
    'qk_notbeleuchtung': 'netzersatz', 'qk_stufe_mm': 15, 'qk_nachregulierung': True, 'qk_schuerze_mm': 750,
    'qk_abstand_schwelle_mm': 120, 'qk_nennlast_gekennz': True, 'qk_nutzflaeche_ok': True, 'qk_ueberlast': True,
    'qk_ueberlast_geprueft': True, 'qk_lueftung': 'ausreichend', 'qk_hinweis_brandfall': True,
    'qk_en8170': True, 'qk_bedienelemente': True, 'qk_rollstuhl_mass': True, 'qk_ausstattung': 'ok',
    'qk_vandalismus_wiederholt': False, 'qk_ucm_sr_modul': True, 'qk_schutz_aufwaerts': 'aktiv',
    # Fahrkorbdach
    'qf_spalt_mm': 250, 'qf_fussleiste': True, 'qf_einzugstellen': True, 'qf_einzug_abdeckung': 'komplett',
    'qf_schutzraum': 'normgerecht', 'qf_inspektion': True, 'qf_inspektion_schutz': True,
    'qf_inspektion_erreichbar': True, 'qf_inspektion_geschw': True, 'qf_nothalt': True, 'qf_nothalt_erreichbar': True,
    'qf_nothalt_wirksam': True, 'qf_dach_tragfaehig': True, 'qf_klappe': False, 'qf_notbeleuchtung': True,
    'qf_notruf_dach': True,
    # Schacht / Grube
    'qs_bel_vorhanden': True, 'qs_bel_ausreichend': True, 'qs_bel_splitterschutz': True, 'qs_zugang_bel': True,
    'qs_vollumwehrt': True, 'qs_wand_fest': True, 'qs_schienen_stahl': True, 'qs_fang': True, 'qs_begrenzer': True,
    'qs_fang_geprueft': True, 'qs_spanngewicht_schalter': True, 'qs_fremd_frei': True, 'qs_zugang_schacht_sicher': True,
    'qg_bel_vorhanden': True, 'qg_bel_50lux': True, 'qg_schutzraum': 'normgerecht', 'qg_nothalt': True,
    'qg_nothalt_aussen': True, 'qg_inspektion': True, 'qg_leiter': 'fest', 'qg_zugangstuer': False,
    'qg_selbstbefreiung': True, 'qg_notruf': True, 'qg_puffer': True, 'qg_puffer_zustand': True,
    'qg_puffer_art': 'speichernd', 'qg_gg_abtrennung': 'normgerecht', 'qg_gg_fuellung': True,
    'qg_wasser': False, 'qg_oel': False,
    # Umfeld / Doku (teils bewusst offen gelassen -> Unvollständig)
    'qu_entrauchung': 'kein_nachweis', 'qu_wartung_gefaehrlicher_zugang': False,
    'qd_notfallplan': True, 'qd_notbefreiungsanleitung': 'aktuell', 'qd_wartungsunterlagen': True,
    'qd_regelmaessige_wartung': True, 'qd_pruefplakette': True, 'qd_pruefung_ueberfaellig': False,
}


# Beispielanlage für den Cyber-Typ: vernetzter Seilaufzug mit Maschinenraum,
# Fernwartung und Gateway; typische Befunde (Hoch/Mittel/Niedrig/Kein Risiko/
# Nicht zutreffend/Unvollständig nebeneinander).
DEMO_CY = {
    'qa_aufzugsart': 'seil', 'qa_ueberwachungsbeduerftig': True, 'qa_steuerungsart': 'vernetzt',
    'qa_maschinenraum': True, 'qa_vernetzt': True, 'qa_gebaeude_anbindung': True,
    'qa_hersteller_vorgaben': 'unbekannt',
    # Zugang
    'qz_steuerung_frei': False, 'qz_triebwerksraum_frei': False, 'qz_schacht_frei': False,
    'qz_service_gesichert': True, 'qz_default_zugangsdaten': True, 'qz_rollen': True,
    'qz_servicegeraete': False,
    # Komponenten
    'qc_steuerung_schnittstelle': 'kabelgebunden', 'qc_steuerung_massnahmen': 'teilweise',
    'qc_steuerung_unabhaengig': True,
    'qc_pessral_vorhanden': True, 'qc_pessral_schnittstelle': 'keine',
    'qc_fu_vorhanden': True, 'qc_fu_schnittstelle': 'kabelgebunden', 'qc_fu_massnahmen': 'keine',
    'qc_fu_unabhaengig': True,
    'qc_notruf_vorhanden': True, 'qc_notruf_schnittstelle': 'kabellos', 'qc_notruf_massnahmen': 'teilweise',
    'qc_notruf_unabhaengig': True,
    'qc_kopierung_vorhanden': True, 'qc_kopierung_schnittstelle': 'kabelgebunden',
    'qc_kopierung_massnahmen': 'umgesetzt', 'qc_kopierung_unabhaengig': True,
    'qc_tuer_vorhanden': True, 'qc_tuer_schnittstelle': 'kabelgebunden',   # Maßnahmen offen -> Unvollständig
    'qc_ucm_vorhanden': True, 'qc_ucm_schnittstelle': 'kabelgebunden', 'qc_ucm_massnahmen': 'umgesetzt',
    'qc_ucm_unabhaengig': True,
    'qc_safue_vorhanden': False, 'qc_tragmittel_vorhanden': True, 'qc_tragmittel_schnittstelle': 'kabelgebunden',
    'qc_tragmittel_massnahmen': 'umgesetzt', 'qc_tragmittel_unabhaengig': True,
    'qc_fernueb_vorhanden': True, 'qc_fernueb_lesend': True,
    'qc_remote_vorhanden': True,
    'qc_gateway_vorhanden': True, 'qc_gateway_firewall': True, 'qc_gateway_default': False,
    'qc_gateway_updates': True,
    'qc_geb_rueckwirkungsfrei': True, 'qc_geb_sicherer_zustand': False,
    # Netz
    'qn_segmentierung': True, 'qn_fern_freigabe': False, 'qn_fern_auth': True, 'qn_protokoll': True,
    'qn_softwarestand': 'unbekannt', 'qn_funktionsreduzierung': True,
    # Organisation (Unterweisung bewusst offen -> Unvollständig)
    'qo_verantwortlich': True, 'qo_fachkunde': True, 'qo_notfall': False,
    'qo_pruefung_fristen': True, 'qo_wirksamkeit': False, 'qo_funktion': True, 'qo_rueckwirkung': True,
    'qo_erkenntnisse': True, 'qo_aenderungen': False,
    'qo_zues_beruecksichtigt': True, 'qo_zues_erfasst': True, 'qo_zues_erhebliches_risiko': True,
    'qo_zues_stand_technik': True,
}


def trim(d):
    q = []
    for x in d.get('questions', []):
        o = {'code': x['code'], 'type': x.get('type', 'SELECT'), 'text': x.get('text', ''),
             'options': x.get('options', [])}
        for k in ('category', 'ui_number', 'help_text', 'visible_when', 'min', 'max'):
            if x.get(k) is not None:
                o[k] = x[k]
        q.append(o)
    hz = []
    for h in d['hazards']:
        o = {'code': h['code'], 'title': h['title'], 'category': h.get('category', ''),
             'questions': h.get('questions', []), 'aggregation_type': h.get('aggregation_type', 'NONE')}
        for k in ('description', 'sources', 'hazard_factor', 'person_groups', 'review_ids'):
            if h.get(k):
                o[k] = h[k]
        hz.append(o)
    ru = []
    for r in d['rules']:
        o = {'hazard': r['hazard'], 'code': r['code'], 'priority': r.get('priority', 100),
             'condition': r['condition'], 'result': r['result']}
        for k in ('applicability', 'aggregation', 'evidence', 'notes'):
            if r.get(k):
                o[k] = r[k]
        if r.get('measures'):
            o['measures'] = [{'measure': m['measure']} for m in r['measures']]
        ru.append(o)
    me = [{'code': m['code'], 'title': m['title'], 'type': m.get('type', '')} for m in d.get('measures', [])]
    return {'rule_version': d.get('rule_version', ''), 'questions': q,
            'hazards': hz, 'rules': ru, 'measures': me}


def main():
    cat = {}
    for f, label in SRC:
        cat[label] = trim(json.load(open(os.path.join(ROOT, f), encoding='utf-8')))
        if f == 'norm_81_20_mf.json':
            cat[label]['demo_answers'] = DEMO_MF
        if f == 'norm_cyber_mf.json':
            cat[label]['demo_answers'] = DEMO_CY
    kl = []
    for name in ('mf_klaerung.json', 'cy_klaerung.json'):
        kl_path = os.path.join(ROOT, name)
        if os.path.exists(kl_path):
            kl += json.load(open(kl_path, encoding='utf-8'))
    html = open(os.path.join(HERE, 'assessment_ui.html'), encoding='utf-8').read()
    html = html.replace('__CATALOGS__', json.dumps(cat, ensure_ascii=False, separators=(',', ':')))
    html = html.replace('__KLAERUNG__', json.dumps(kl, ensure_ascii=False, separators=(',', ':')))
    out = os.path.join(HERE, 'gbu_bewertung.html')
    open(out, 'w', encoding='utf-8').write(html)
    print('geschrieben:', out, round(os.path.getsize(out) / 1024), 'KB',
          '|', sum(len(c['hazards']) for c in cat.values()), 'Gefährdungen')


if __name__ == '__main__':
    main()
