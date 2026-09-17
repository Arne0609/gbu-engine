# -*- coding: utf-8 -*-
"""Fingerabdruck einer Regel für die Regelfreigabe.

Gehasht wird alles, was über die Einstufung entscheidet (Prüfbericht vom
15.09.2026, Punkt 6: Freigaben müssen auch bei Änderungen an abhängigen
Fragen, Anwendbarkeit oder Prioritäten erneut geprüft werden):

  * die Regel selbst: Priorität, Bedingung, Anwendbarkeit, Stufe, Maßnahmen
    (Code und Wortlaut)
  * die Gefährdung: Bewertungslogik, Fragenrollen mit Pflicht- und
    Anwendbarkeitsbedingungen
  * jede Frage, die in Regel oder Gefährdung vorkommt: Typ, Text, Optionen,
    Sichtbarkeit, Wertebereich

Nicht dazu gehören notes, evidence und quality_status – die ändert die
Freigabe selbst bzw. sie sind Begleittext. Ohne seed (Altaufruf) wird nur
die Regel gehasht.
"""
import hashlib, json


def _fragen(expr, into):
    if not expr:
        return
    if isinstance(expr, dict):
        if 'question' in expr:
            into.add(expr['question'])
        for v in expr.values():
            if isinstance(v, (dict, list)):
                _fragen(v, into)
    elif isinstance(expr, list):
        for x in expr:
            _fragen(x, into)


def sachverhalt(regel):
    """Kennung des Sachverhalts: Bedingung und Anwendbarkeit. Bleibt sie
    gleich, behält die Regel ihre ID (auch wenn sich Stufe oder Maßnahme
    ändern); ein neuer Sachverhalt bekommt eine neue ID."""
    roh = json.dumps({'c': regel.get('condition'), 'a': regel.get('applicability')},
                     sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha1(roh.encode('utf-8')).hexdigest()[:12]


def fingerabdruck(regel, seed=None):
    kern = {k: regel.get(k) for k in
            ('hazard', 'priority', 'condition', 'applicability', 'result', 'measures')}
    if seed is not None:
        M = {m['code']: m for m in seed.get('measures', [])}
        kern['massnahmen_text'] = [M.get(b['measure'], {}).get('title') for b in regel.get('measures', [])]
        h = next((x for x in seed['hazards'] if x['code'] == regel['hazard']), {})
        kern['gefaehrdung'] = {'agg': h.get('aggregation_type'), 'fragen': h.get('questions')}
        codes = set()
        _fragen(regel.get('condition'), codes)
        _fragen(regel.get('applicability'), codes)
        _fragen(h.get('questions'), codes)
        Q = {q['code']: q for q in seed['questions']}
        kern['fragendef'] = {c: {k: Q.get(c, {}).get(k) for k in
                                 ('type', 'text', 'options', 'visible_when', 'min', 'max')}
                             for c in sorted(codes)}
    roh = json.dumps(kern, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha1(roh.encode('utf-8')).hexdigest()[:12]
