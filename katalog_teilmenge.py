# -*- coding: utf-8 -*-
"""Teilmenge eines Katalog-Seeds bilden – abgeleitete GBU-Typen.

Gleiches Verfahren wie in gen_en8180_catalog.py (Typ „Bestand nach
DIN EN 81-80"), hier als importierbare Funktion, damit weitere abgeleitete
Typen (z. B. die Riedl-Variante) es ohne Kopie nutzen können:

  * Gefährdungen, Regeln, Fragen und Maßnahmen werden UNVERÄNDERT
    übernommen, mit denselben Codes (Typwechsel ohne Datenverlust, Freigaben
    gelten weiter).
  * Mitgenommen werden alle Fragen, die die behaltenen Gefährdungen brauchen:
    hazard_questions samt required_when/applicable_when, Fragen aus
    Regelbedingungen und -anwendbarkeit sowie die vollständige Kette der
    Sichtbarkeitsregeln.
  * Begründete Annahmen, Karten (question_groups), Nachweise, Phasen und
    Reihenfolge werden auf die vorhandenen Fragen beschnitten.

`pruefe_identitaet()` stellt sicher, dass jedes übernommene Objekt byteweise
dem Original entspricht – der abgeleitete Typ kann nicht auseinanderlaufen.
"""
from collections import OrderedDict


def collect(expr, into):
    if not expr:
        return
    if 'all' in expr:
        for e in expr['all']:
            collect(e, into)
    elif 'any' in expr:
        for e in expr['any']:
            collect(e, into)
    elif 'not' in expr:
        collect(expr['not'], into)
    else:
        into.add(expr['question'])


def teilmenge(quelle, behalten, rule_version):
    """Seed-Teilmenge mit den Gefährdungen `behalten` (Codes) bilden."""
    H = {h['code']: h for h in quelle['hazards']}
    Q = {q['code']: q for q in quelle['questions']}
    M = {m['code']: m for m in quelle['measures']}
    fehlend = [c for c in behalten if c not in H]
    if fehlend:
        raise SystemExit('unbekannte Gefährdungen: %s' % ', '.join(fehlend))
    behalten = set(behalten)

    # Reihenfolge des Quellkatalogs beibehalten (Bericht und UI-Gruppierung).
    hazards = [h for h in quelle['hazards'] if h['code'] in behalten]
    rules = [r for r in quelle['rules'] if r['hazard'] in behalten]

    fragen = set()
    for h in hazards:
        for hq in h.get('questions', []):
            fragen.add(hq['question'])
            for key in ('required_when', 'applicable_when'):
                collect(hq.get(key), fragen)
    for r in rules:
        collect(r['condition'], fragen)
        collect(r.get('applicability'), fragen)
    # Steuerfragen der begründeten Annahmen und der Nachweise: Die Annahme
    # zu einer behaltenen Frage greift nur, wenn auch ihre Bedingung (Baujahr)
    # und die Rücknahmebedingung (assumptions_void_when, z. B. „Konformitäts-
    # erklärung liegt vor?") im Katalog sind – sonst bewertet die Teilmenge
    # anders als das Original (Annahme greift bzw. wird nie zurückgenommen).
    # riedl_smoke.ts prüft diese Deckungsgleichheit auf Zufallsantworten.
    for a in quelle.get('assumptions', []):
        if a['question'] in fragen:
            collect(a.get('when'), fragen)
    void = quelle.get('assumptions_void_when')
    if void and any(a['question'] in fragen for a in quelle.get('assumptions', [])):
        collect(void, fragen)
    for n in quelle.get('nachweise', []):
        if n['question'] in fragen:
            collect(n.get('when'), fragen)
    todo = list(fragen)
    while todo:
        c = todo.pop()
        neu = set()
        collect(Q.get(c, {}).get('visible_when'), neu)
        for n in neu - fragen:
            fragen.add(n)
            todo.append(n)
    fehlend = sorted(c for c in fragen if c not in Q)
    if fehlend:
        raise SystemExit('unbekannte Fragen: %s' % ', '.join(fehlend))
    questions = [q for q in quelle['questions'] if q['code'] in fragen]

    massnahmen = OrderedDict()
    for r in rules:
        for mb in r.get('measures', []):
            code = mb['measure']
            if code in M:
                massnahmen[code] = M[code]

    seed = {'rule_version': rule_version, 'questions': questions,
            'measures': list(massnahmen.values()), 'hazards': hazards,
            'rules': rules}

    annahmen = [a for a in quelle.get('assumptions', []) if a['question'] in fragen]
    if annahmen:
        seed['assumptions'] = annahmen
        # Die Ruecknahmebedingung muss mitkommen, sonst greifen die Annahmen im
        # abgeleiteten Typ IMMER (fail-open). Der frueheren Pruefung
        # `void.get('question') in fragen` entging jede zusammengesetzte Bedingung
        # (z. B. {'not': …}), weil ein solcher Ausdruck kein 'question' traegt
        # (Pruefbericht 20.09.2026, gefunden durch riedl_smoke).
        void = quelle.get('assumptions_void_when')
        if void:
            noetig = set()
            collect(void, noetig)
            fehlend = noetig - fragen
            if fehlend:
                raise SystemExit('assumptions_void_when braucht Fragen, die nicht in der '
                                 'Teilmenge sind: %s' % ', '.join(sorted(fehlend)))
            seed['assumptions_void_when'] = void
    if quelle.get('category_phases'):
        seed['category_phases'] = dict(quelle['category_phases'])
    if quelle.get('category_order'):
        seed['category_order'] = list(quelle['category_order'])
    gruppen = []
    for g in quelle.get('question_groups', []):
        items = [it for it in g['items'] if it['question'] in fragen]
        if items:
            g2 = dict(g)
            g2['items'] = items
            if all(it['mode'] == 'check' for it in items):
                g2['kind'] = 'checklist'
            gruppen.append(g2)
    if gruppen:
        seed['question_groups'] = gruppen
    # Die Freischaltbedingung eines Nachweises kann zusammengesetzt sein
    # (Prüfbericht 20.09.2026 B05: Schutzraum „normgerecht" ab 2017, „altnorm"
    # davor – die zweite Bedingung nennt das Baujahr). Der Nachweis kommt nur
    # mit, wenn die Teilmenge ALLE darin genannten Steuerfragen trägt; sonst
    # bewertet sie anders als das Original.
    def _wenn_fragen(expr):
        noetig = set()
        collect(expr, noetig)
        return noetig

    nachweise = [n for n in quelle.get('nachweise', []) if n['question'] in fragen
                 and _wenn_fragen(n.get('when')) <= fragen]
    if nachweise:
        seed['nachweise'] = nachweise
    return seed


def pruefe_identitaet(seed, quelle):
    """Jede Gefährdung, Frage, Regel und Maßnahme muss dem Original gleichen."""
    H = {h['code']: h for h in quelle['hazards']}
    Q = {q['code']: q for q in quelle['questions']}
    R = {r['code']: r for r in quelle['rules']}
    M = {m['code']: m for m in quelle['measures']}
    for h in seed['hazards']:
        assert h == H[h['code']], 'Gefährdung weicht ab: ' + h['code']
    for q in seed['questions']:
        assert q == Q[q['code']], 'Frage weicht ab: ' + q['code']
    for r in seed['rules']:
        assert r == R[r['code']], 'Regel weicht ab: ' + r['code']
    for m in seed['measures']:
        assert m == M[m['code']], 'Maßnahme weicht ab: ' + m['code']
