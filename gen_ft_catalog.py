# -*- coding: utf-8 -*-
"""Erzeugt den GBU-Typ „Fahrtreppen und Fahrsteige" (FT) als Engine-Seed.

    python3 gen_ft_catalog.py            -> norm_fahrtreppe.json + ft_klaerung.json

Inhalt liegt in ft_content/ (DSL in common.py, die die Register von
mf_content/common.py auf den Fahrtreppen-Typ umstellt). Ein Typ, zwei
Erhebungsbereiche: B (Betrieb/Betreiber) und I (Instandhaltung), gesteuert über
das Anlagenmerkmal qa_teil_instandhaltung.

Anders als beim Aufzugstyp gibt es hier KEIN TRBS-3121-Mapping: Fahrtreppen und
Fahrsteige sind nach BetrSichV Anhang 2 Nr. 2 ausdrücklich keine
überwachungsbedürftigen Anlagen.

Alle Regeln tragen origin=OWN_RULE und quality_status=REVIEW_REQUIRED, bis die
zugehörigen Klärungen in ft_content/entscheidungen.py entschieden sind.
"""
import json, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ft_content import common as C  # noqa: E402  (stellt die Register um)

for mod in ['anlage', 'betrieb_zugang', 'betrieb_anlage', 'betrieb_orga',
            'instandhaltung']:
    importlib.import_module('ft_content.' + mod)

RULE_VERSION = 'fahrtreppe-2026.1'


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


def apply_decisions(rules):
    """Regeln, deren Klärungen alle entschieden sind: HYPOTHESIS -> INFERRED,
    quality_status -> VERIFIED."""
    from ft_content.entscheidungen import ENTSCHEIDUNGEN, DATUM
    decided = {k for k, v in ENTSCHEIDUNGEN.items() if v[0] != 'offen'}
    for r in rules:
        notes = r.get('notes', '')
        kids = notes.split('KLÄREN: ')[1].split(', ') if 'KLÄREN: ' in notes else []
        if kids and all(k in decided for k in kids):
            if r.get('evidence') == 'HYPOTHESIS':
                r['evidence'] = 'INFERRED'
            r['quality_status'] = 'VERIFIED'
            r['notes'] = notes.split('KLÄREN: ')[0].rstrip() + \
                (' ' if notes.split('KLÄREN: ')[0].strip() else '') + \
                'Entschieden %s: %s.' % (DATUM, ', '.join(kids))


def build():
    order = {c: i for i, c in enumerate(C.CATS.values())}
    questions = sorted(C.QUESTIONS, key=lambda q: (order[q['category']],
                                                   C.QUESTIONS.index(q)))
    hazards = list(C.HAZARDS)
    rules = list(C.RULES)
    measures = list(C.MEASURES.values())
    apply_decisions(rules)
    return {'rule_version': RULE_VERSION, 'questions': questions,
            'measures': measures, 'hazards': hazards, 'rules': rules}


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
                errors.append('%s: %s ist YES_NO, Vergleich %s %r ungültig'
                              % (where, qc, op, val))
        elif q['type'] == 'SELECT':
            opts = {o['value'] for o in q.get('options', [])}
            vals = val if isinstance(val, list) else [val]
            for v in vals:
                if v not in opts:
                    errors.append('%s: Wert %r nicht in Optionen von %s'
                                  % (where, v, qc))
        elif q['type'] == 'NUMBER':
            if op not in ('GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ') or \
                    not isinstance(val, (int, float)):
                errors.append('%s: %s ist NUMBER, Vergleich %s %r ungültig'
                              % (where, qc, op, val))

    used_q = set()
    for h in seed['hazards']:
        hq = {x['question'] for x in h.get('questions', [])}
        used_q |= hq
        for x in h.get('questions', []):
            if x['question'] not in qmap:
                errors.append('%s: hazard_question %s unbekannt'
                              % (h['code'], x['question']))
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
                    warnings.append('%s: Frage %s in Regel, aber nicht in '
                                    'hazard_questions' % (r['code'], lf['question']))
    for q in seed['questions']:
        leaves = []
        collect(q.get('visible_when'), leaves)
        for lf in leaves:
            check_leaf(lf, q['code'] + '/visible_when')
        if q['code'] not in used_q:
            warnings.append('Frage %s wird von keiner Gefährdung benutzt' % q['code'])
    for r in seed['rules']:
        if r['hazard'] not in hmap:
            errors.append('%s: Gefährdung %s unbekannt' % (r['code'], r['hazard']))
    return errors, warnings


def validate_schema(seed):
    import jsonschema
    schema = json.load(open(os.path.join(HERE, 'rule_engine.schema.json'),
                            encoding='utf-8'))
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
    out = os.path.join(HERE, 'norm_fahrtreppe.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(seed, f, ensure_ascii=False, indent=1)
    from ft_content.entscheidungen import ENTSCHEIDUNGEN, DATUM
    for kl in C.KLAERUNG:
        e = ENTSCHEIDUNGEN.get(kl['id'])
        if e and e[0] != 'offen':
            kl['entscheidung'], kl['festlegung'], kl['datum'] = e[0], e[1], DATUM
    offen = [kl['id'] for kl in C.KLAERUNG if not kl.get('entscheidung')]
    with open(os.path.join(HERE, 'ft_klaerung.json'), 'w', encoding='utf-8') as f:
        json.dump(C.KLAERUNG, f, ensure_ascii=False, indent=1)
    print('Klärungen offen:', offen or 'keine')
    from collections import Counter
    res = Counter(r['result'] for r in seed['rules'])
    ev = Counter(r['evidence'] for r in seed['rules'])
    types = Counter(q['type'] for q in seed['questions'])
    cats = Counter(q['category'] for q in seed['questions'])
    print('%s: %d Fragen (%s), %d Gefährdungen, %d Regeln, %d Maßnahmen, %d Klärungen'
          % (os.path.basename(out), len(seed['questions']), dict(types),
             len(seed['hazards']), len(seed['rules']), len(seed['measures']),
             len(C.KLAERUNG)))
    print('Erhebungsbereiche:', dict(cats))
    print('Stufen:', dict(res), '| Evidenz:', dict(ev))
    print('Schema: gültig')


if __name__ == '__main__':
    main()
