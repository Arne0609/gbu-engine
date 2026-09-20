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

RULE_VERSION = '81-20-mf-2026.10'  # .10: Prüfbericht Fragenkatalog 20.09.2026 (Lücken, Dopplungen, Bedingungen)
# .9: Erhebung gekürzt – Fragengruppen, Nachweis-Vorbelegung, Stammdaten, Phasen, Schwellenfragen 17.09.2026
# .8: Korrekturen aus zwei Prüfrunden 15./16.09.2026, stabile Regel-IDs
# .7: best_case je Frage (Sammelantwort) 07.09.2026
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
        # Nach dem externen Prüfbericht geänderte Regeln stehen erneut zur
        # Freigabe an – die frühere Klärung deckt den neuen Inhalt nicht mehr.
        if C.PB_MARKER in notes:
            if 'KLÄREN: ' in notes:
                r['notes'] = notes.replace('KLÄREN: ', 'Frühere Klärung (vor der Änderung entschieden): ')
            continue
        if kids and all(k in decided for k in kids):
            if r.get('evidence') == 'HYPOTHESIS':
                r['evidence'] = 'INFERRED'
            r['quality_status'] = 'VERIFIED'
            # Hinweistext: aus „KLÄREN“ wird „entschieden“ (sonst wirkt die
            # Regel in der Oberfläche weiter wie ein offener Punkt).
            r['notes'] = notes.split('KLÄREN: ')[0].rstrip() + \
                (' ' if notes.split('KLÄREN: ')[0].strip() else '') + \
                'Entschieden %s: %s.' % (DATUM, ', '.join(kids))


FP_FREIGABE = {}   # Regel -> Fingerabdruck, auf den sich eine aktuelle Freigabe bezieht


def apply_freigabe(rules, seed=None):
    """Regelfreigabe aus der Gegenlesung (Excel GBU_MF_Regelpruefung,
    Rückweg apply_mf_regelpruefung.py):
    'Freigeben' -> VERIFIED; 'Ändern'/'Streichen' bleiben REVIEW_REQUIRED,
    die Korrektur steht als Hinweis in den notes, bis der Inhalt in
    mf_content/*.py nachgezogen ist. Gleiches Muster wie beim Cyber-Typ.

    Einträge tragen seit 15.09.2026 Datum und Fingerabdruck des
    Regelinhalts. Passt der Fingerabdruck nicht mehr (Regel geändert oder
    Code verschoben), bleibt die Regel offen. Altformat (Entscheidung,
    Korrektur) gilt mit DATUM und ohne Fingerabdruck-Prüfung."""
    try:
        from mf_content.regelfreigabe import FREIGABE, DATUM as FREIGABE_DATUM
    except ImportError:
        return
    from mf_content.fingerabdruck import fingerabdruck
    for r in rules:
        fg = FREIGABE.get(r['code'])
        if not fg:
            continue
        entscheidung, korrektur = fg[0], fg[1]
        datum = fg[2] if len(fg) > 2 and fg[2] else FREIGABE_DATUM
        fp = fg[3] if len(fg) > 3 else ''
        if r.get('quality_status') == 'VERIFIED':
            # schon über eine Klärung freigegeben – eine passende neue Freigabe
            # bestätigt den aktuellen Stand
            if entscheidung == 'Freigeben' and fp and fp == fingerabdruck(r, seed):
                FP_FREIGABE[r['code']] = fp
            continue
        sep = ' ' if r.get('notes', '').strip() else ''
        if fp and fp != fingerabdruck(r, seed):
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'OFFEN: Regel seit der Entscheidung vom %s geändert – neu prüfen.' % datum
            continue
        if entscheidung == 'Freigeben':
            r['quality_status'] = 'VERIFIED'
            if fp:
                FP_FREIGABE[r['code']] = fp
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'Freigegeben %s.' % datum
        else:
            r['notes'] = r.get('notes', '').rstrip() + sep + \
                'OFFEN (%s %s): %s' % (entscheidung, datum, korrektur or '-')


def build():
    # Fragen in Fragebogen-Reihenfolge (Erhebungsbereich, dann Definitionsreihenfolge)
    order = {c: i for i, c in enumerate(C.CATS.values())}
    questions = sorted(C.QUESTIONS, key=lambda q: (order[q['category']], C.QUESTIONS.index(q)))
    hazards = list(C.HAZARDS)
    rules = list(C.RULES)
    # Nur tatsächlich verwendete Maßnahmen ausgeben (ersetzte Texte bleiben
    # sonst als Leichen im Katalog stehen).
    benutzt = {b['measure'] for r in rules for b in r.get('measures', [])}
    measures = [m for m in C.MEASURES.values() if m['code'] in benutzt]
    fix_trbs_sources(hazards)
    from mf_content.hilfetexte import HILFE
    for q in questions:
        if not q.get('help_text') and q['code'] in HILFE:
            q['help_text'] = HILFE[q['code']]
    apply_decisions(rules)
    seed = {'rule_version': RULE_VERSION, 'questions': questions, 'measures': measures,
            'hazards': hazards, 'rules': rules}
    if C.ANNAHMEN:
        seed['assumptions'] = list(C.ANNAHMEN)
        seed['assumptions_void_when'] = C.ANNAHMEN_HINFAELLIG
    # Erhebung kürzen (17.09.2026, mf_content/erhebung.py): erst Struktur
    # (streichen, verschieben, D05, Schwellenfragen), dann best_case, dann
    # Freigabe/Fingerabdrücke auf dem endgültigen Stand, zuletzt Gruppen,
    # Nachweise, Stammdaten und Phasen (rein beschreibend, nicht im Fingerabdruck).
    from mf_content import erhebung
    erhebung.vorbereiten(seed)
    set_best_case(seed)
    apply_freigabe(rules, seed)
    pflege_regel_ids(seed)
    erhebung.anreichern(seed)
    return seed


def pflege_regel_ids(seed):
    """Revision je Regel fortschreiben: ändert sich der Fingerabdruck
    (Inhalt, abhängige Fragen, Gefährdungslogik), steigt die Revision."""
    from mf_content.fingerabdruck import fingerabdruck
    reg = C.REGEL_IDS['regeln']
    for r in seed['rules']:
        e = reg[r['hazard']][r['code']]
        fp = fingerabdruck(r, seed)
        if e.get('fp') and e['fp'] != fp:
            e['rev'] = e.get('rev', 1) + 1
        e['fp'] = fp
        e['stand'] = RULE_VERSION
        # Eine Freigabe gilt nur für den Stand, auf den sie sich bezog – auch
        # wenn sie über eine Klärung oder das Altformat ohne Fingerabdruck kam
        # (zweite Prüfung 16.09.2026, Punkt 6).
        if r.get('quality_status') == 'VERIFIED':
            if FP_FREIGABE.get(r['code']) == fp:
                e['fp_verifiziert'] = fp
            elif 'fp_verifiziert' not in e:
                e['fp_verifiziert'] = fp
            elif e['fp_verifiziert'] != fp:
                r['quality_status'] = 'REVIEW_REQUIRED'
                sep = ' ' if r.get('notes', '').strip() else ''
                r['notes'] = r.get('notes', '').rstrip() + sep + \
                    '[Freigabe bezog sich auf einen früheren Stand (Regel, abhängige Fragen oder ' \
                    'Gefährdungslogik geändert) – neu prüfen]'
    aktiv = {r['code'] for r in seed['rules']}
    for hz_, eintraege in reg.items():
        for code, e in eintraege.items():
            if code not in aktiv:
                e['stillgelegt'] = True
            else:
                e.pop('stillgelegt', None)


ORTSBEREICHE = [
    'Z – Zugang zum Triebwerks-/Steuerungsraum',
    'M – Triebwerks-/Maschinenraum und Steuerung',
    'T – Schachttüren und Fahrkorbtür',
    'K – Fahrkorb',
    'F – Fahrkorbdach und Schachtkopf',
    'S – Schacht',
    'G – Schachtgrube',
]

# Bereiche mit Sammelantwort: die Ortsbereiche und – seit 17.09.2026 auf
# Arnes Wunsch – das Umfeld (U): Der Pruefer soll Umfeld, Gebaeude und Nutzung
# mit einem Klick komplett als unauffaellig setzen koennen. Anlagenmerkmale (A)
# kommen aus dem Anlagenstamm, Unterlagen (D) sind keine Sichtpruefung.
UMFELD = 'U – Umfeld, Gebäude und Nutzung'
SAMMELBEREICHE = ORTSBEREICHE + [UMFELD]

# Auswahlfragen bekommen ueberall dort einen best_case, wo eine Sammelantwort
# traegt (17.09.2026, Arne): Die Auswahl beschreibt einen Zustand
# (Schutzraum normgerecht, Lueftung ausreichend, Zustand der Ausstattung ok),
# und die Gegenprobe in mf_content/sammelantwort.py laesst nur Werte stehen,
# die in keiner Belegung schlechter abschneiden. AUSGENOMMEN bleiben die
# Schwellenfragen (Messwerte) – siehe erhebung.SCHWELLEN: ein Messergebnis ist
# keine Sichtpruefung, das beantwortet der Pruefer bewusst.
AUSWAHL_SAMMELBEREICHE = SAMMELBEREICHE


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
      * die in keiner Befundregel vorkommt (reine Dokumentation; im Umfeld
        setzt mf_content/erhebung.py fuer solche Fragen den Wert ausdruecklich),
      * die ausserhalb der SAMMELBEREICHE liegt. Anlagenmerkmale, Unterlagen
        und Sonderfunktionen sind keine Sichtpruefung an einem Ort; sie
        bleiben Einzelfragen.
    Auswahlfragen (SELECT) in AUSWAHL_SAMMELBEREICHE: best_case ist die eine
    Option, die in keiner Befundregel vorkommt – gibt es mehrere oder keine,
    bleibt die Frage offen. Die Schwellenfragen nimmt erhebung.anreichern()
    danach wieder heraus.
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

    verlangt = {}       # YES_NO: Werte, die einen Befund ausloesen
    ausloeser = {}      # SELECT: Optionen, die einen Befund ausloesen
    unklar = set()      # SELECT: Vergleich, der sich nicht auf Optionen abbilden laesst
    for r in seed['rules']:
        if r['result'] not in ('LOW', 'MEDIUM', 'HIGH'):
            continue
        out = []
        blaetter(r['condition'], False, out)
        for lf, negiert in out:
            if negiert:
                continue
            code = lf['question']
            typ = qmap.get(code, {}).get('type')
            wert = lf.get('value')
            if typ == 'YES_NO':
                if not isinstance(wert, bool):
                    continue
                if lf['operator'] == 'EQ':
                    verlangt.setdefault(code, set()).add(wert)
                elif lf['operator'] == 'NEQ':
                    verlangt.setdefault(code, set()).add(not wert)
            elif typ == 'SELECT':
                if lf['operator'] == 'EQ' and isinstance(wert, str):
                    ausloeser.setdefault(code, set()).add(wert)
                elif lf['operator'] == 'IN' and isinstance(wert, list):
                    ausloeser.setdefault(code, set()).update(wert)
                elif lf['operator'] != 'ANSWERED':
                    unklar.add(code)   # NEQ/NOT_IN: Polaritaet nicht eindeutig

    gesetzt = 0
    for q in seed['questions']:
        q.pop('best_case', None)
        if q['code'] in applicability or q.get('source') == 'anlagenstamm':
            continue
        if q.get('category') not in SAMMELBEREICHE:
            continue
        if q['type'] == 'YES_NO':
            werte = verlangt.get(q['code'], set())
            if len(werte) != 1:
                continue
            q['best_case'] = not werte.pop()
            gesetzt += 1
        elif q['type'] == 'SELECT' and q.get('category') in AUSWAHL_SAMMELBEREICHE:
            if q['code'] in unklar or q['code'] not in ausloeser:
                continue
            frei = [o['value'] for o in q.get('options', []) if o['value'] not in ausloeser[q['code']]]
            if len(frei) != 1:
                continue
            q['best_case'] = frei[0]
            gesetzt += 1

    # Gegenprobe durch Simulation (mf_content/sammelantwort.py, 17.09.2026):
    # Kompensationsfragen, die in den Regeln nur mit ihrem guten Wert stehen,
    # bekaemen oben den falschen best_case. Was die Probe nicht bestaetigt,
    # wird gestrichen und bleibt Einzelfrage.
    from mf_content import sammelantwort
    gestrichen, moeglich, skipped = sammelantwort.gegenprobe(seed)
    for code, wert in gestrichen:
        print('best_case gestrichen (Gegenprobe): %s = %r' % (code, wert))
    if skipped:
        print('best_case-Gegenprobe uebersprungen (zu viele Belegungen): %s' % skipped)
    zusatz = {c: v for c, v in moeglich.items()
              if qmap[c].get('category') in SAMMELBEREICHE and c not in applicability
              and (qmap[c]['type'] == 'YES_NO' or qmap[c].get('category') in AUSWAHL_SAMMELBEREICHE)}
    if zusatz:
        print('Hinweis: laut Simulation ebenfalls eindeutig unauffaellig, aber nicht gesetzt (%d): %s'
              % (len(zusatz), ', '.join('%s=%r' % kv for kv in sorted(zusatz.items()))))
    return gesetzt - len(gestrichen)


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
    for n in seed.get('nachweise', []):
        for lf in (lambda t: (collect(n['when'], t), t)[1])([]):
            check_leaf(lf, 'Nachweis %s/when' % n['question'])
    from mf_content import erhebung
    e2, w2 = erhebung.pruefen(seed)
    errors += e2
    warnings += w2
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
    C.REGEL_IDS['stand'] = RULE_VERSION
    with open(C.REGEL_IDS_PFAD, 'w', encoding='utf-8') as f:
        json.dump(C.REGEL_IDS, f, ensure_ascii=False, indent=1)
    if C.NEUE_IDS:
        print('Neue Regel-IDs:', ', '.join(C.NEUE_IDS))
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
    from mf_content import erhebung
    genutzt = sorted({n['source'].split('Nr.')[-1].strip() for n in seed.get('nachweise', [])
                      if 'Nr.' in n.get('source', '') and n['source'].split('Nr.')[-1].strip().isdigit()},
                     key=int)
    print('ZÜS-Hauptprüfung: %d von %d Prüfpunkten genutzt (%s) | ohne Katalogfrage (Wartung/ZÜS bzw. Cyber): %s'
          % (len(genutzt), erhebung.ZUES_PRUEFPUNKTE, ', '.join(genutzt),
             ', '.join(erhebung.OHNE_KATALOGFRAGE)))
    je, n_karten = erhebung.kennzahlen(seed)
    print('Sammelantwort Umfeld (U): %d von %d Fragen sammelbar; ohne best_case (gewollt: Folgefragen nach Auffälligkeit): %s'
          % (sum(1 for q in seed['questions'] if q.get('category') == UMFELD and q.get('best_case') is not None),
             sum(1 for q in seed['questions'] if q.get('category') == UMFELD),
             ', '.join(erhebung.umfeld_offen(seed)) or '–'))
    print('Erhebung: %d Karten (%d Gruppen, %d Nachweise, %d Stammdaten): %s'
          % (n_karten, len(seed.get('question_groups', [])), len(seed.get('nachweise', [])),
             sum(1 for q in seed['questions'] if q.get('source') == 'anlagenstamm'), je))
    print('Schema: gültig')


if __name__ == '__main__':
    main()
