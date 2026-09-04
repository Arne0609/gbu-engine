# -*- coding: utf-8 -*-
"""Schreibt einen Katalog-Seed als App-Asset (kompaktes JSON ohne die
internen QA-Felder):  python3 gen_app_asset.py norm_cyber_mf.json [Zielpfad]

Ohne Zielpfad wird ../gbu_aufzug_app/assets/engine/<name> geschrieben.
Entfernt rekursiv `quality_status` und `review_ids` – beides ist reine
Werkstatt-Information des Regelwerks und hat in der App nichts zu suchen.
`notes` bleibt erhalten (Hinweis im Bewertungs-Sheet).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit(__doc__)
name = os.path.basename(sys.argv[1])
src = os.path.join(HERE, name)
ziel = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    HERE, '..', 'gbu_aufzug_app', 'assets', 'engine', name)

INTERN = ('quality_status', 'review_ids')


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in INTERN}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


seed = json.load(open(src, encoding='utf-8'))
with open(ziel, 'w', encoding='utf-8') as fh:
    json.dump(strip(seed), fh, ensure_ascii=False, separators=(',', ':'))
print('geschrieben: %s (%d KB) | %s | %d Fragen, %d Gefährdungen, %d Regeln'
      % (os.path.normpath(ziel), os.path.getsize(ziel) // 1024, seed['rule_version'],
         len(seed['questions']), len(seed['hazards']), len(seed['rules'])))
