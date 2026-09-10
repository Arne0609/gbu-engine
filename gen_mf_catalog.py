# -*- coding: utf-8 -*-
"""Erzeugt den mehrfragigen GBU-Typ „EN 81-20 mehrfragig" (MF) als Engine-Seed.

    python3 gen_mf_catalog.py            -> norm_81_20_mf.json + mf_klaerung.json

Inhalt liegt in mf_content/ (DSL in common.py, ein Modul je Erhebungsbereich).
Maßnahmen werden – wo vorhanden – aus den bestehenden Katalogen norm_81_20.json
und norm_2026.json übernommen (gleiche Texte, gleiche Codes), Norm-/Quellen-
bezug ist je Gefährdung hinterlegt. Alle Regeln tragen origin=OWN_RULE und
quality_status=REVIEW_REQUIRED, bis Arne sie freigegeben hat.

Prüfungen am Ende: Schema-Validierung, verwaiste Referenzen, gültige
Optionswerte, jede Gefährdung mindestens eine Regel, jede Frage in mindestens
einer Gefährdung.
"""
import json, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from mf_content import common as C  # noqa: E402

C.load_existing([os.path.join(HERE, 'norm_81_20.json'), os.path.join(HERE, 'norm_2026.json')])
for mod in ['anlage', 'zugang', 'triebwerksraum', 'tueren_fahrkorb', 'fahrkorbdach',
            'schacht_grube', 'umfeld', 'sonderfunktion_doku']:
    importlib.import_module('mf_content.' + mod)

# Annahmen erst nach allen Fragen eintragen – so kann die Pruefung unten jede
# angenommene Frage gegen den fertigen Katalog halten.
from mf_content import annahmen as ANN  # noqa: E402
ANN.registriere()

RULE_VERSION = '81-20-mf-2026.7'  # .7: best_case je Frage (Sammelantwort) 07.09.2026
# .6: begruendete Annahmen (Baujahr) 07.09.2026
# .5: 26 neue Regeln freigegeben 04.09.2026
# .4: Baujahr als Steuerfeld + MF-D06 Konformitaetspruefung 04.09.2026
# .2: Review 02.09.2026 (Kein-Risiko-Regeln, Pflichtfragen, TRBS-Fundstellen, K-K12)


def collect(expr, into):
    if not expr:
        return
    if 'all' in expr:
        for e in expr['all']: collect(e, into)
    elif 'any' in expr:
        for e in expr['any']: collect(e, into)
    elif 'not' in expr:
        collect(expr['not'], into)
    else:
        into.append(expr)


def fix_trbs_sources(hazards):
    """TRBS-3121-Anhang-1-Fundstellen nach der 22er-Liste setzen (Review Punkt 4)."""
    from mf_content.trbs_anhang1 import HAZARD_TO_NR, ANHANG1
    for h in hazards:
        srcs = [s for s in h.get('sources', [])
                if not (s.get('document') == 'TRBS 3121' and str(s.get('section', '')).startswith('Anh. 1'))]
        for nr in HAZARD_TO_NR.get(h['code'], []):
            srcs.append({'type': 'TRBS', 'document': 'TRBS 3121',
                         'section': 'Anh. 1 Nr. %d (%s)' % (nr, ANHANG1[nr])})
        if srcs:
            h['sources'] = srcs
        elif 'sources' in h:
            del h['sources']


def apply_decisions(rules):
    """Regeln, deren Klärungen alle entschieden sind: HYPOTHESIS -> INFERRED,
    quality_status -> VERIFIED (Review Punkt 8)."""
    from mf_content.entscheidungen import ENTSCHEIDUNGEN, DATUM
    decided = {k for k, v in ENTSCHEIDUNGEN.items() if v[0] != 'offen'}
    for r in rules:
        notes = r.get('notes', '')
        kids = notes.split('KLÄREN: ')[1].split(', ') if 'KLÄREN: ' in notes else []
        if kids and all(k in decided for k in kids):
            if r.get('evidence') == 'HYPOTHESIS':
                r['evidence'] = 'INFERRED'
            r['quality_status'] = 'VERIFIED'
            # Hinweistext: aus „KLÄREN“ wird „entschieden“ (sonst wirkt die
            # Regel in der Oberfläche weiter wie ein offener Punkt).
            r['notes'] = notes.split('KLÄREN: ')[0].rstrip() + \
                (' ' if notes.split('KLÄREN: ')[0].strip() else '') + \
                'Entschieden %s: %s.' % (DATUM, ', '.join(kids))


def apply_freigabe(rules):
    """Regelfreigabe aus der Gegenlesung (Excel GBU_MF_Regelpruefung):
    'Freigeben' -> VERIFIED; 'Ändern'/'Streichen' bleiben REVIEW_REQUIRED,
    die Korrektur steht als Hinweis in den notes, bis der Inhalt in
    mf_content/*.py nachgezogen ist. Gleiches Muster wie beim Cyber-Typ."""
    try:
        from mf_content.regelfreigabe import FREIGABE, DATUM as FREIGABE_DATUM
    except ImportError:
        return
    for r in rules:
        fg = FREIGABE.get(r['code'])
        if not fg or r.get('quality_status') == 'VERIFIED':
            continue
        entscheidung, korrektur = fg
        sep = ' ' if r.get('notes', '').strip() else ''
        if entscheidung == 'Freigeben':
            r['quality_status'] = 'VERIFIED'
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'Freigegeben %s.' % FREIGABE_DATUM
        else:
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'OFFEN (%s %s): %s' % (entscheidung, FREIGABE_DATUM,
                                       korrektur or '-')


def build():
    # Fragen in Fragebogen-Reihenfolge (Erhebungsbereich, dann Definitionsreihenfolge)
    order = {c: i for i, c in enumerate(C.CATS.values())}
    questions = sorted(C.QUESTIONS, key=lambda q: (order[q['category']], C.QUESTIONS.index(q)))
    hazards = list(C.HAZARDS)
    rules = list(C.RULES)
    measures = list(C.MEASURES.values())
    fix_trbs_sources(hazards)
    apply_decisions(rules)
    apply_freigabe(rules)
    seed = {'rule_version': RULE_VERSION, 'questions': questions, 'measures': measures,
            'hazards': hazards, 'rules': rules}
    if C.ANNAHMEN:
        seed['assumptions'] = list(C.ANNAHMEN)
        seed['assumptions_void_when'] = C.ANNAHMEN_HINFAELLIG
    set_best_case(seed)
    return seed


ORTSBEREICHE = [
    'Z – Zugang zum Triebwerks-/Steuerungsraum',
    'M – Triebwerks-/Maschinenraum und Steuerung',
    'T – Schachttüren und Fahrkorbtür',
    'K – Fahrkorb',
    'F – Fahrkorbdach und Schachtkopf',
    'S – Schacht',
    'G – Schachtgrube',
]


def set_best_case(seed):
    """Leitet je Ja/Nein-Frage ab, welcher Wert unauffaellig ist.

    Grundlage der Sammelantwort ("Sichtpruefung ohne Befund"): Der Pruefer
    geht einen Ort ab und haelt nur fest, was auffaellt. Damit die App den
    Rest setzen kann, muss sie wissen, welcher Wert je Frage der unauffaellige
    ist - und das steht bereits im Regelwerk: Loest ausschliesslich `nein`
    einen Befund aus, ist `ja` der unauffaellige Wert und umgekehrt.

    Bewusst konservativ. Kein best_case bekommt eine Frage,
      * bei der BEIDE Werte irgendwo einen Befund ausloesen (z. B. die
        Fahrkorbtuer - ihr Fehlen ist ein Mangel, ihr Vorhandensein macht
        andere Regeln scharf),
      * die als APPLICABILITY den Katalogumfang steuert,
      * die in keiner Befundregel vorkommt,
      * die ausserhalb der sieben Ortsbereiche liegt. Anlagenmerkmale,
        Unterlagen, Umfeld und Sonderfunktionen sind keine Sichtpruefung an
        einem Ort; sie bleiben Einzelfragen.
    Blaetter unter einem `not` zaehlen nicht mit - dort ist die Polaritaet
    umgekehrt und die Ableitung nicht mehr eindeutig.
    """
    qmap = {q['code']: q for q in seed['questions']}
    applicability = set()
    for h in seed['hazards']:
        for hq in h.get('questions', []):
            if hq['role'] == 'APPLICABILITY':
                applicability.add(hq['question'])

    def blaetter(expr, negiert, out):
        if not expr:
            return
        if 'all' in expr:
            for e in expr['all']: blaetter(e, negiert, out)
        elif 'any' in expr:
            for e in expr['any']: blaetter(e, negiert, out)
        elif 'not' in expr:
            blaetter(expr['not'], not negiert, out)
        else:
            out.append((expr, negiert))

    verlangt = {}
    for r in seed['rules']:
        if r['result'] not in ('LOW', 'MEDIUM', 'HIGH'):
            continue
        out = []
        blaetter(r['condition'], False, out)
        for lf, negiert in out:
            if negiert:
                continue
            code = lf['question']
            if qmap.get(code, {}).get('type') != 'YES_NO':
                continue
            wert = lf.get('value')
            if not isinstance(wert, bool):
                continue
            if lf['operator'] == 'EQ':
                verlangt.setdefault(code, set()).add(wert)
            elif lf['operator'] == 'NEQ':
                verlangt.setdefault(code, set()).add(not wert)

    gesetzt = 0
    for q in seed['questions']:
        q.pop('best_case', None)
        if q['type'] != 'YES_NO' or q['code'] in applicability:
            continue
        if q.get('category') not in ORTSBEREICHE:
            continue
        werte = verlangt.get(q['code'], set())
        if len(werte) != 1:
            continue
        q['best_case'] = not werte.pop()
        gesetzt += 1
    return gesetzt


def check(seed):
    errors, warnings = [], []
    qmap = {q['code']: q for q in seed['questions']}
    hmap = {h['code']: h for h in seed['hazards']}
    rules_by_h = {}
    for r in seed['rules']:
        rules_by_h.setdefault(r['hazard'], []).append(r)

    def check_leaf(leaf, where):
        qc = leaf['question']
        if qc not in qmap:
            errors.append('%s: unbekannte Frage %s' % (where, qc)); return
        q = qmap[qc]
        op, val = leaf['operator'], leaf.get('value')
        if op in ('ANSWERED', 'NOT_ANSWERED'):
            return
        if q['type'] == 'YES_NO':
            if op not in ('EQ', 'NEQ') or not isinstance(val, bool):
                errors.append('%s: %s ist YES_NO, Vergleich %s %r ungültig' % (where, qc, op, val))
        elif q['type'] == 'SELECT':
            opts = {o['value'] for o in q.get('options', [])}
            vals = val if isinstance(val, list) else [val]
            for v in vals:
                if v not in opts:
                    errors.append('%s: Wert %r nicht in Optionen von %s' % (where, v, qc))
        elif q['type'] == 'NUMBER':
            if op not in ('GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ') or not isinstance(val, (int, float)):
                errors.append('%s: %s ist NUMBER, Vergleich %s %r ungültig' % (where, qc, op, val))

    used_q = set()
    for h in seed['hazards']:
        hq = {x['question'] for x in h.get('questions', [])}
        used_q |= hq
        for x in h.get('questions', []):
            if x['question'] not in qmap:
                errors.append('%s: hazard_question %s unbekannt' % (h['code'], x['question']))
            for key in ('required_when', 'applicable_when'):
                leaves = []
                collect(x.get(key), leaves)
                for lf in leaves:
                    check_leaf(lf, '%s/%s' % (h['code'], key))
        if h['code'] not in rules_by_h:
            errors.append('%s: keine Regel' % h['code'])
        elif not any(x['result'] == 'NO_RISK' for x in rules_by_h[h['code']]):
            errors.append('%s: keine ausdrückliche Kein-Risiko-Regel' % h['code'])
        for x in rules_by_h.get(h['code'], []):
            if x['result'] in ('LOW', 'MEDIUM', 'HIGH') and not x.get('measures'):
                errors.append('%s: risikotragende Regel ohne Maßnahme' % x['code'])
        for r in rules_by_h.get(h['code'], []):
            leaves = []
            collect(r['condition'], leaves)
            collect(r.get('applicability'), leaves)
            for lf in leaves:
                check_leaf(lf, r['code'])
                if lf['question'] not in hq:
                    warnings.append('%s: Frage %s in Regel, aber nicht in hazard_questions'
                                    % (r['code'], lf['question']))
    for q in seed['questions']:
        if q['type'] == 'NUMBER' and (q.get('min') is None or q.get('max') is None):
            errors.append('%s: Zahlenfrage ohne min/max' % q['code'])
        leaves = []
        collect(q.get('visible_when'), leaves)
        for lf in leaves:
            check_leaf(lf, q['code'] + '/visible_when')
        if q['code'] not in used_q:
            warnings.append('Frage %s wird von keiner Gefährdung benutzt' % q['code'])
    for r in seed['rules']:
        if r['hazard'] not in hmap:
            errors.append('%s: Gefährdung %s unbekannt' % (r['code'], r['hazard']))

    # Annahmen: die drei Grenzen aus mf_content/common.py hart prüfen, damit
    # beim Erweitern der Liste keine Zustands- oder Steuerfrage hineinrutscht.
    applicability_q = set()
    for h in seed['hazards']:
        for hq_ in h.get('questions', []):
            if hq_['role'] == 'APPLICABILITY':
                applicability_q.add(hq_['question'])
    gesehen = set()
    for a in seed.get('assumptions', []):
        code = a['question']
        wo = 'Annahme ' + code
        if code in gesehen:
            errors.append('%s: doppelt eingetragen' % wo)
        gesehen.add(code)
        if code not in qmap:
            errors.append('%s: unbekannte Frage' % wo)
            continue
        if qmap[code]['type'] != 'YES_NO':
            errors.append('%s: nur Ja/Nein-Fragen dürfen angenommen werden' % wo)
        if not isinstance(a['value'], bool):
            errors.append('%s: angenommener Wert muss Ja/Nein sein' % wo)
        if code in applicability_q:
            errors.append('%s: steuert als APPLICABILITY-Frage den Katalogumfang '
                          'und darf nicht angenommen werden' % wo)
        if not a.get('reason'):
            errors.append('%s: ohne Begründung' % wo)
        for lf in (lambda t: (collect(a['when'], t), t)[1])([]):
            check_leaf(lf, wo + '/when')
    for lf in (lambda t: (collect(seed.get('assumptions_void_when'), t), t)[1])([]):
        check_leaf(lf, 'assumptions_void_when')
    return errors, warnings


def validate_schema(seed):
    import jsonschema
    schema = json.load(open(os.path.join(HERE, 'rule_engine.schema.json'), encoding='utf-8'))
    jsonschema.Draft202012Validator(schema).validate(seed)


def main():
    seed = build()
    errors, warnings = check(seed)
    for w in warnings:
        print('WARNUNG', w)
    if errors:
        for e in errors:
            print('FEHLER', e)
        sys.exit(1)
    validate_schema(seed)
    out = os.path.join(HERE, 'norm_81_20_mf.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(seed, f, ensure_ascii=False, indent=1)
    from mf_content.entscheidungen import ENTSCHEIDUNGEN, DATUM
    for kl in C.KLAERUNG:
        e = ENTSCHEIDUNGEN.get(kl['id'])
        if e and e[0] != 'offen':
            kl['entscheidung'], kl['festlegung'], kl['datum'] = e[0], e[1], DATUM
    offen = [kl['id'] for kl in C.KLAERUNG if not kl.get('entscheidung')]
    with open(os.path.join(HERE, 'mf_klaerung.json'), 'w', encoding='utf-8') as f:
        json.dump(C.KLAERUNG, f, ensure_ascii=False, indent=1)
    print('Klärungen offen:', offen or 'keine')
    from collections import Counter
    res = Counter(r['result'] for r in seed['rules'])
    ev = Counter(r['evidence'] for r in seed['rules'])
    types = Counter(q['type'] for q in seed['questions'])
    print('%s: %d Fragen (%s), %d Gefährdungen, %d Regeln, %d Maßnahmen, %d Klärungen'
          % (os.path.basename(out), len(seed['questions']), dict(types), len(seed['hazards']),
             len(seed['rules']), len(seed['measures']), len(C.KLAERUNG)))
    print('Stufen:', dict(res), '| Evidenz:', dict(ev))
    print('Schema: gültig')


if __name__ == '__main__':
    main()
