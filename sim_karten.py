# -*- coding: utf-8 -*-
"""Zählt je Anlagenprofil, was der Prüfer im gekürzten Katalog sieht: Karten
(Gruppen + Einzelfragen), davon aus Stammdaten, Baujahr-Annahme oder Nachweis
vorbelegt, vorab beantwortbar oder vor Ort offen.

    python3 sim_karten.py [norm_81_20_mf.json]

Bildet Sichtbarkeit, Annahmen und Nachweise nach der Seed-Logik nach; kein App-Test."""
import json, sys, collections

SEED = sys.argv[1] if len(sys.argv) > 1 else 'norm_81_20_mf.json'
seed = json.load(open(SEED, encoding='utf-8'))
Q = {q['code']: q for q in seed['questions']}
BY_UI = {q.get('ui_number'): q['code'] for q in seed['questions'] if q.get('ui_number')}


def ev(expr, ans):
    if not expr:
        return True
    if 'all' in expr: return all(ev(e, ans) for e in expr['all'])
    if 'any' in expr: return any(ev(e, ans) for e in expr['any'])
    if 'not' in expr: return not ev(expr['not'], ans)
    v = ans.get(expr['question']); op = expr['operator']; w = expr.get('value')
    if op == 'ANSWERED': return v is not None
    if op == 'NOT_ANSWERED': return v is None
    if v is None: return False
    if op == 'EQ': return v == w
    if op == 'NEQ': return v != w
    if op == 'IN': return v in w
    if op == 'NOT_IN': return v not in w
    if op == 'GT': return v > w
    if op == 'GTE': return v >= w
    if op == 'LT': return v < w
    if op == 'LTE': return v <= w
    raise ValueError(op)


# Profile (Steuerantworten) – wie in der Auswertung vom 16.09.2026, umgesetzt auf Fragen-Codes
PROFILE = {
 'P1 Seilaufzug, Triebwerksraum, Wohnhaus, Bj. 1995': dict(
     qa_aufzugsart='seil', qa_antrieb='zweigeschw', qa_gegengewicht=True, qa_maschinenraum=True, qa_rollenraum=False,
     qa_mehrere_aufzuege=False, qa_raum_unter_schacht=False, qa_fahrkorbtuer=True, qa_glas_schachttueren=False,
     qa_glas_fahrkorbtueren=False, qa_glas_schacht=False, qa_nutzungsart='personen', qa_nutzung_pmem=False,
     qa_nutzung_kinder=False, qa_baujahr=1995, qa_norm_inverkehrbringen='en81_1_2', qa_feuerwehraufzug=False,
     qa_bfs_gefordert=False, qa_bma_vorhanden=False, qa_entrauchung_vorhanden=True, qa_sprinkler_vorhanden=False,
     qd_konformitaet_geprueft=True, qd_zues_bericht='ohne_maengel', qa_grubentiefe=False, qt_fk_tuer_automatisch=True,
     qk_notruf_vorhanden=True, qz_aufstieg='treppe_handlauf', qk_abstand_schwelle_mm=False, qk_schuerze_mm='ab_750',
     qf_spalt_mm='bis_300', qg_puffer=True, qf_schutzraum='normgerecht', qg_schutzraum='normgerecht',
     qa_barrierefrei_gefordert=False),
 'P2 Seilaufzug ohne Triebwerksraum, Büro mit BMA, Glastüren, Doppelschacht, Bj. 2019': dict(
     qa_aufzugsart='seil', qa_antrieb='geregelt', qa_gegengewicht=True, qa_maschinenraum=False, qa_mehrere_aufzuege=True,
     qa_raum_unter_schacht=False, qa_fahrkorbtuer=True, qa_glas_schachttueren=True, qa_glas_fahrkorbtueren=True,
     qa_glas_schacht=False, qa_nutzungsart='personen', qa_nutzung_pmem=True, qa_barrierefrei_gefordert=True,
     qa_nutzung_kinder=False, qa_baujahr=2019, qa_norm_inverkehrbringen='en81_20', qa_feuerwehraufzug=False,
     qa_bfs_gefordert=True, qa_bma_vorhanden=True, qa_entrauchung_vorhanden=True, qa_sprinkler_vorhanden=False,
     qd_konformitaet_geprueft=True, qd_zues_bericht='ohne_maengel', qa_grubentiefe=False, qt_fk_tuer_automatisch=True,
     qk_notruf_vorhanden=True, qz_aufstieg='ebenerdig', qk_abstand_schwelle_mm=False, qk_schuerze_mm='ab_750',
     qf_spalt_mm='bis_300', qg_puffer=True, qf_schutzraum='normgerecht', qg_schutzraum='normgerecht',
     qt_glas_schiebetuer=True, qf_nachbar_trennung='engmaschig', qg_nachbar_abtrennung=True),
 'P3 Hydraulik-Lastenaufzug mit Personenbegleitung, Bj. 1988': dict(
     qa_aufzugsart='hydraulik', qa_antrieb='hydraulisch', qa_maschinenraum=True, qa_rollenraum=False,
     qa_mehrere_aufzuege=False, qa_raum_unter_schacht=False, qa_fahrkorbtuer=False, qa_glas_schachttueren=False,
     qa_glas_fahrkorbtueren=False, qa_glas_schacht=False, qa_nutzungsart='lasten', qa_nutzung_pmem=False,
     qa_nutzung_kinder=False, qa_baujahr=1988, qa_norm_inverkehrbringen='tra', qa_feuerwehraufzug=False,
     qa_bfs_gefordert=False, qa_bma_vorhanden=False, qa_entrauchung_vorhanden=False, qa_sprinkler_vorhanden=False,
     qd_konformitaet_geprueft=False, qd_zues_bericht='ohne_maengel', qa_grubentiefe=False,
     qk_notruf_vorhanden=True, qz_aufstieg='ebenerdig', qk_abstand_schwelle_mm=False, qk_schuerze_mm='300_749',
     qf_spalt_mm='bis_300', qg_puffer=True, qf_schutzraum='altnorm', qg_schutzraum='altnorm',
     qa_barrierefrei_gefordert=False, qt_nur_eingewiesene=True),
}

ANN = {a['question']: a for a in seed.get('assumptions', [])}
VOID = seed.get('assumptions_void_when')
NACH = {n['question']: n for n in seed.get('nachweise', [])}
PHASE = seed.get('category_phases', {})
GROUP_OF = {it['question']: g for g in seed.get('question_groups', []) for it in g['items']}


def herkunft(code, ans):
    """Woher käme die Antwort, wenn der Prüfer nichts tut?"""
    q = Q[code]
    if q.get('source') == 'anlagenstamm':
        return 'stamm'
    a = ANN.get(code)
    if a and not (VOID and ev(VOID, ans)) and ev(a['when'], ans):
        return 'baujahr'
    n = NACH.get(code)
    if n and ev(n['when'], ans):
        bj = ans.get('qa_baujahr')
        if n.get('min_baujahr') is None or (bj is not None and bj >= n['min_baujahr']):
            return 'nachweis'
    return None


def sim(name, ans):
    sichtbar = [q for q in seed['questions'] if ev(q.get('visible_when'), ans)]
    karten = collections.OrderedDict()   # Karten-ID -> Liste Fragen
    for q in sichtbar:
        g = GROUP_OF.get(q['code'])
        key = ('G', g['id'], g['category']) if g else ('Q', q['code'], q['category'])
        karten.setdefault(key, []).append(q)
    res = collections.Counter(); je_bereich = collections.Counter(); je_bereich_offen = collections.Counter()
    for key, qs in karten.items():
        cat = key[2][:2].strip()
        je_bereich[cat] += 1
        hk = [herkunft(q['code'], ans) for q in qs]
        # Karte gilt als vorbelegt, wenn jede sichtbare Position vorbelegt ist
        if all(hk):
            res['vorbelegt_' + ('stamm' if all(h == 'stamm' for h in hk) else 'baujahr' if all(h in ('baujahr', 'stamm') for h in hk) else 'nachweis')] += 1
            continue
        phase = PHASE.get(key[2], 'vor_ort')
        res[phase] += 1
        je_bereich_offen[cat] += 1
    n = len(karten)
    print('%s\n   Fragen sichtbar: %d | Karten: %d | vorbelegt: Stamm %d, Baujahr %d, Nachweis %d | vorab: %d | vor Ort: %d'
          % (name, len(sichtbar), n, res['vorbelegt_stamm'], res['vorbelegt_baujahr'], res['vorbelegt_nachweis'], res['vorab'], res['vor_ort']))
    print('   Karten je Bereich (offen/alle):', ', '.join('%s %d/%d' % (c, je_bereich_offen[c], je_bereich[c]) for c in ['A', 'D', 'U', 'Z', 'M', 'F', 'S', 'G', 'T', 'K', 'SF'] if je_bereich[c]))
    return dict(fragen=len(sichtbar), karten=n, **res)


if __name__ == '__main__':
    print(seed['rule_version'])
    out = {k: sim(k, v) for k, v in PROFILE.items()}
    json.dump(out, open('sim_karten.json', 'w'), ensure_ascii=False, indent=1)
