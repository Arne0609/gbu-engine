# -*- coding: utf-8 -*-
"""Gemeinsame Konsistenzprüfung und Schema-Validierung für DSL-erzeugte
Katalog-Seeds (identisch mit check()/validate_schema() in gen_ft_catalog.py,
hier ohne Nebenwirkungen importierbar – gen_ft_catalog.py lädt beim Import den
Fahrtreppen-Inhalt in die geteilten DSL-Register)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))


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


