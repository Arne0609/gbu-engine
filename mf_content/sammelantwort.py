# -*- coding: utf-8 -*-
"""Gegenprobe für den unauffälligen Wert (best_case) je Frage – 17.09.2026.

gen_mf_catalog.set_best_case() leitet den unauffälligen Wert aus der Polarität
der Regelblätter ab: Löst nur `nein` einen Befund aus, ist `ja` unauffällig.
Das kippt bei Kompensationsfragen, die in den Regeln nur mit ihrem GUTEN Wert
vorkommen, weil der schlechte Fall schon eine Grundregel ohne diese Frage
abdeckt (Beispiel MF-U06: „Ex möglich“ allein ist Hoch; „Ex möglich UND
bewertet UND umgesetzt“ ist Mittel – „bewertet = ja“ steht nur in Befundregeln
und sähe deshalb wie der auffällige Wert aus). Eine Sammelantwort würde dann
„nicht bewertet“ eintragen: fachlich falsch, im Ergebnis zwar konservativ,
aber eine Aussage, die niemand getroffen hat.

Deshalb hier die Gegenprobe durch Simulation, mit den Regeln der Engine
(evaluator.ts: Applicability, Pflichtfragen, Regeln, Aggregation/Priorität):
Für jede Gefährdung werden alle Belegungen ihrer Fragen durchgerechnet. Ein
Wert ist nur dann unauffällig, wenn er in KEINER Belegung ein schlechteres
Ergebnis liefert als die anderen Werte derselben Frage. Ein best_case, der
diese Probe nicht besteht, wird gestrichen – die Frage bleibt dann eine
Einzelfrage, die der Prüfer bewusst beantwortet. Die Probe setzt NICHTS neu;
was sie zusätzlich für unauffällig hielte, bleibt Entscheidung des Menschen
(gen_mf_catalog.py meldet es als Hinweis).
"""
import collections
import itertools

SEV = {'INCOMPLETE': 0, 'NOT_APPLICABLE': 0, 'NO_RISK': 0, 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
MAX_BELEGUNGEN = 200000


def _leaves(expr, out):
    if not expr:
        return out
    if 'all' in expr:
        for e in expr['all']: _leaves(e, out)
    elif 'any' in expr:
        for e in expr['any']: _leaves(e, out)
    elif 'not' in expr:
        _leaves(expr['not'], out)
    else:
        out.append(expr)
    return out


def _ev(expr, ans):
    if not expr:
        return True
    if 'all' in expr: return all(_ev(e, ans) for e in expr['all'])
    if 'any' in expr: return any(_ev(e, ans) for e in expr['any'])
    if 'not' in expr: return not _ev(expr['not'], ans)
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
    raise ValueError('Operator %s' % op)


def bewerten(hazard, rules, ans):
    """Nachbildung von evaluateHazard() in evaluator.ts – nur das Ergebnis."""
    qs = hazard.get('questions', [])
    for q in qs:
        if q['role'] != 'APPLICABILITY':
            continue
        if q.get('applicable_when'):
            if _ev(q['applicable_when'], ans):
                continue
            refs = {lf['question'] for lf in _leaves(q['applicable_when'], [])}
            if any(ans.get(k) is None for k in refs):
                return 'INCOMPLETE'
            return 'NOT_APPLICABLE'
        if ans.get(q['question']) is False:
            return 'NOT_APPLICABLE'
    for q in qs:
        if q['role'] == 'APPLICABILITY' and not q.get('applicable_when') and ans.get(q['question']) is None:
            return 'INCOMPLETE'
    for q in qs:
        mode = q.get('required_mode', 'NEVER')
        req = mode == 'ALWAYS' or (mode == 'CONDITIONAL' and q.get('required_when') and _ev(q['required_when'], ans))
        if req and ans.get(q['question']) is None:
            return 'INCOMPLETE'
    applicable = [r for r in rules if not r.get('applicability') or _ev(r['applicability'], ans)]
    matching = [r for r in applicable if _ev(r['condition'], ans)]
    if not matching:
        return 'INCOMPLETE' if any(r['result'] == 'NO_RISK' for r in rules) else 'NO_RISK'
    agg = hazard.get('aggregation_type') or 'NONE'
    if agg in ('MAXIMUM', 'ANY'):
        return max(matching, key=lambda r: SEV[r['result']])['result']
    w = matching[0]
    for r in matching[1:]:
        if r['priority'] != w['priority']:
            if r['priority'] > w['priority']:
                w = r
        elif SEV[r['result']] > SEV[w['result']]:
            w = r
    return w['result']


def _kontext(hazard, rules, qmap):
    codes = []
    def add(c):
        if c in qmap and c not in codes:
            codes.append(c)
    for q in hazard.get('questions', []):
        add(q['question'])
        for k in ('applicable_when', 'required_when'):
            for lf in _leaves(q.get(k), []): add(lf['question'])
    for r in rules:
        for lf in _leaves(r['condition'], []): add(lf['question'])
        for lf in _leaves(r.get('applicability'), []): add(lf['question'])
    return codes


def _werte(q, hazard, rules):
    if q['type'] == 'YES_NO':
        return [True, False]
    if q['type'] == 'YES_NO_NA':
        return [True, False, 'na']
    if q['type'] == 'SELECT':
        return [o['value'] for o in q.get('options', [])]
    # NUMBER: die Schwellen der Regeln, je um eins unter- und überschritten
    consts = set()
    for r in rules:
        for lf in _leaves(r['condition'], []) + _leaves(r.get('applicability'), []):
            if lf['question'] == q['code'] and isinstance(lf.get('value'), (int, float)):
                consts.add(lf['value'])
    for x in hazard.get('questions', []):
        for k in ('applicable_when', 'required_when'):
            for lf in _leaves(x.get(k), []):
                if lf['question'] == q['code'] and isinstance(lf.get('value'), (int, float)):
                    consts.add(lf['value'])
    vals = set()
    for c in consts:
        vals.update([c - 1, c, c + 1])
    return sorted(vals) or [0]


def nie_schlechter(seed):
    """Je Frage (YES_NO/SELECT): Menge der Werte, die in keiner Belegung ein
    schlechteres Ergebnis liefern als die anderen Werte, und ob die Frage
    irgendwo überhaupt etwas ändert. Liefert {code: (werte, wirkt)}; Gefährdungen
    mit zu vielen Belegungen werden übersprungen (zweiter Rückgabewert)."""
    qmap = {q['code']: q for q in seed['questions']}
    rules_by_h = collections.defaultdict(list)
    for r in seed['rules']:
        rules_by_h[r['hazard']].append(r)
    result, skipped = {}, []
    for h in seed['hazards']:
        rules = rules_by_h.get(h['code'], [])
        ctx = _kontext(h, rules, qmap)
        dom = {c: _werte(qmap[c], h, rules) for c in ctx}
        n = 1
        for c in ctx:
            n *= len(dom[c])
        if n > MAX_BELEGUNGEN:
            skipped.append((h['code'], n))
            continue
        combos = list(itertools.product(*[dom[c] for c in ctx]))
        sev = {combo: SEV[bewerten(h, rules, dict(zip(ctx, combo)))] for combo in combos}
        for i, c in enumerate(ctx):
            if qmap[c]['type'] not in ('YES_NO', 'SELECT'):
                continue
            werte, wirkt = result.setdefault(c, (set(dom[c]), False))
            groups = collections.defaultdict(dict)
            for combo in combos:
                groups[combo[:i] + combo[i + 1:]][combo[i]] = sev[combo]
            for byval in groups.values():
                best = min(byval.values())
                if len(set(byval.values())) > 1:
                    wirkt = True
                for v, s in byval.items():
                    if s > best:
                        werte.discard(v)
            result[c] = (werte, wirkt)
    return result, skipped


def gegenprobe(seed):
    """Streicht best_case-Werte, die die Simulation nicht bestätigt. Liefert
    (gestrichen, zusaetzlich_moeglich, uebersprungen): gestrichen = Liste
    (code, alter Wert), zusaetzlich_moeglich = {code: wert} für Fragen ohne
    best_case, bei denen genau ein Wert nie schlechter ist (nur Hinweis)."""
    probe, skipped = nie_schlechter(seed)
    gestrichen, moeglich = [], {}
    for q in seed['questions']:
        p = probe.get(q['code'])
        if p is None:
            continue
        werte, wirkt = p
        if q.get('best_case') is not None:
            if q['best_case'] not in werte:
                gestrichen.append((q['code'], q.pop('best_case')))
        elif wirkt and len(werte) == 1 and q['type'] in ('YES_NO', 'SELECT'):
            moeglich[q['code']] = next(iter(werte))
    return gestrichen, moeglich, skipped
