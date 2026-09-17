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

import catalog_check  # noqa: E402  (gemeinsame Prüfungen, ohne Nebenwirkungen)
from ft_content import common as C  # noqa: E402  (stellt die Register um)

for mod in ['anlage', 'betrieb_zugang', 'betrieb_anlage', 'betrieb_orga',
            'instandhaltung', 'bestand_en115_2']:
    importlib.import_module('ft_content.' + mod)

RULE_VERSION = 'fahrtreppe-2026.2'  # .2: Bereich N (EN 115-2 Anhang B)


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


def main():
    seed = build()
    errors, warnings = catalog_check.check(seed)
    for w in warnings:
        print('WARNUNG', w)
    if errors:
        for e in errors:
            print('FEHLER', e)
        sys.exit(1)
    catalog_check.validate_schema(seed)
    # Stabile Regel-IDs des FT-Typs sichern (eigene Registry, siehe
    # ft_content/common.py).
    if C.NEUE_IDS:
        print('neue Regel-IDs:', len(C.NEUE_IDS))
    with open(C.REGEL_IDS_PFAD, 'w', encoding='utf-8') as f:
        json.dump({'regeln': C.REGEL_IDS['regeln']}, f, ensure_ascii=False, indent=1)
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
