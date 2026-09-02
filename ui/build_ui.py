# -*- coding: utf-8 -*-
"""Baut die eigenständige Bewertungsoberfläche: bettet die Engine-Katalog-Seeds
(getrimmt) in assessment_ui.html ein -> gbu_bewertung.html.

Lauf:  python3 build_ui.py    (aus engine_model/ui/, Seeds liegen in ../)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = [
    ('norm_en8141.json', 'Plattformaufzug · EN 81-41'),
    ('norm_81_80.json', 'GBU vereinfacht · EN 81-80'),
    ('norm_81_20.json', 'GBU erweitert · EN 81-20'),
    ('norm_2026.json', 'Ergänzung 2026 · Gebäude & Cyber-Matrix'),
    ('norm_cyber_voll.json', 'Cyber · TRBS 1115-1 (voll)'),
    ('norm_cyber_minimal.json', 'Cyber · minimal'),
]

def trim(d):
    q = [{'code': x['code'], 'options': x.get('options', [])} for x in d.get('questions', [])]
    hz = []
    for h in d['hazards']:
        o = {'code': h['code'], 'title': h['title'], 'category': h.get('category', ''),
             'questions': h.get('questions', []), 'aggregation_type': h.get('aggregation_type', 'NONE')}
        if h.get('description'):
            o['description'] = h['description']
        if h.get('sources'):
            o['sources'] = h['sources']
        hz.append(o)
    ru = []
    for r in d['rules']:
        o = {'hazard': r['hazard'], 'code': r['code'], 'priority': r.get('priority', 100),
             'condition': r['condition'], 'result': r['result']}
        if r.get('applicability'):
            o['applicability'] = r['applicability']
        if r.get('aggregation'):
            o['aggregation'] = r['aggregation']
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
    blob = json.dumps(cat, ensure_ascii=False, separators=(',', ':'))
    html = open(os.path.join(HERE, 'assessment_ui.html'), encoding='utf-8').read()
    html = html.replace('__CATALOGS__', blob)
    out = os.path.join(HERE, 'gbu_bewertung.html')
    open(out, 'w', encoding='utf-8').write(html)
    print('geschrieben:', out, round(os.path.getsize(out) / 1024), 'KB',
          '|', sum(len(c['hazards']) for c in cat.values()), 'Gefährdungen')

if __name__ == '__main__':
    main()
