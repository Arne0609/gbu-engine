# -*- coding: utf-8 -*-
"""DSL für den mehrfragigen GBU-Typ „EN 81-20 mehrfragig" (MF).

Alle Inhaltsmodule (anlage.py, zugang.py, …) benutzen ausschließlich diese
Helfer. Ergebnis sind vier Listen, die gen_mf_catalog.py in ein Engine-Seed
(rule_engine.schema.json) überführt:

  QUESTIONS  – Fragen mit Typ, Erhebungsbereich, UI-Nummer, Optionen,
               optionaler Sichtbarkeitsregel (visible_when)
  HAZARDS    – Gefährdungen mit Fragenrollen, Pflichtmodus, Aggregation,
               Baugruppe (category), Gefährdungsfaktor, Personengruppen
  RULES      – Bewertungsregeln (Bedingung -> Risikostufe + Maßnahmen)
  KLAERUNG   – offene Punkte für die fachliche Gegenlesung (Klärungsliste)

Grundsätze (aus der Schindler-Analyse übernommen, eigenständig umgesetzt):
  * Frage -> Gefährdung (Rolle) -> Regel -> Stufe. Nie eine Stufe an der Frage.
  * Unbeantwortete Pflichtfrage => INCOMPLETE, nie „Kein Risiko".
  * Anlagenmerkmale filtern (APPLICABILITY): Nein/nicht zutreffend => NOT_APPLICABLE.
  * Erhebungsbereich (UI) != Baugruppe (Bewertung/Bericht).
  * Kompensation über Regelpriorität (spezifischere Regel gewinnt).
"""
import hashlib
from collections import OrderedDict

QUESTIONS = []
HAZARDS = []
RULES = []
KLAERUNG = []
MEASURES = OrderedDict()

# ---- Erhebungsbereiche (Fragebogen) ----------------------------------------
CATS = OrderedDict([
    ('A',  'A – Anlagenmerkmale'),
    ('Z',  'Z – Zugang zum Triebwerks-/Steuerungsraum'),
    ('M',  'M – Triebwerks-/Maschinenraum und Steuerung'),
    ('T',  'T – Schachttüren und Fahrkorbtür'),
    ('K',  'K – Fahrkorb'),
    ('F',  'F – Fahrkorbdach und Schachtkopf'),
    ('S',  'S – Schacht'),
    ('G',  'G – Schachtgrube'),
    ('U',  'U – Umfeld, Gebäude und Nutzung'),
    ('SF', 'SF – Sonderfunktionen'),
    ('D',  'D – Unterlagen und Betreiberorganisation'),
])
_PREFIX2CAT = {'qa_': 'A', 'qz_': 'Z', 'qm_': 'M', 'qt_': 'T', 'qk_': 'K',
               'qf_': 'F', 'qs_': 'S', 'qg_': 'G', 'qu_': 'U', 'qsf_': 'SF',
               'qd_': 'D'}

# ---- Baugruppen (Bewertung/Bericht) ----------------------------------------
GROUPS = [
    'Notruf und Personenbefreiung',
    'Türen und Verriegelung',
    'Fahrkorb und Nutzung',
    'Antrieb, Bremse und Hydraulik',
    'Sicherheitskomponenten',
    'Steuerung und Elektrik',
    'Beleuchtung',
    'Zugang und Verkehrswege',
    'Triebwerksraum – Ausstattung',
    'Fahrkorbdach und Schachtkopf',
    'Schacht und Gegengewicht',
    'Schachtgrube',
    'Beschilderung und Unterlagen',
    'Brandschutz und Gebäudeschnittstelle',
    'Umfeld und Gefahrstoffe',
    'Sonderfunktionen',
    'Betreiberorganisation',
]

# ---- Personengruppen / Gefährdungsfaktoren ---------------------------------
NUTZER, BEAUFTRAGTE, WARTUNG = 'Nutzer', 'Beauftragte Person', 'Wartungspersonal'
FEUERWEHR, FREMDFIRMEN, REINIGUNG, BETREIBER = ('Feuerwehr', 'Fremdfirmen',
                                                'Reinigungspersonal', 'Betreiber')

F_ABSTURZ = 'Mechanische Gefährdung durch Absturz'
F_ABSTURZ_SCHACHT = 'Mechanische Gefährdung durch Absturz in den Schacht'
F_BEWEGT = 'Mechanische Gefährdung durch bewegte Teile (Quetschen, Scheren, Einziehen)'
F_ROTIEREND = 'Mechanische Gefährdung durch rotierende Teile (Erfassen, Einziehen)'
F_KINETISCH = 'Mechanische Gefährdung durch Beschleunigung und Abbremsung (kinetische Energie)'
F_STURZ = 'Mechanische Gefährdung durch Stolpern, Rutschen, Stürzen'
F_ELEKTRISCH = 'Elektrische Gefährdung durch Berühren spannungsführender Teile'
F_BELEUCHTUNG = 'Gefährdung durch Arbeitsumgebungsbedingungen (unzureichende Beleuchtung)'
F_NOTFALL = 'Sonstige Gefährdung durch fehlende oder unzureichende Notfallorganisation'
F_BRAND = 'Brand- und Explosionsgefährdung'
F_UEBERLAST = 'Mechanische Gefährdung durch Überlastung und unkontrollierte Bewegung'
F_UMGEBUNG = 'Gefährdung durch Arbeitsumgebungsbedingungen (Klima, Lärm, Emissionen)'
F_ERGONOMIE = 'Physische Belastung / ergonomische Gefährdung'
F_EINSPERREN = 'Sonstige Gefährdung durch Einschließen von Personen'
F_FLUCHT = 'Gefährdung durch fehlende oder versperrte Flucht- und Rettungswege'
F_LAST = 'Mechanische Gefährdung durch herabfallende oder kippende Lasten'
F_ORGA = 'Gefährdung durch organisatorische Mängel (Unterlagen, Unterweisung, Zuständigkeit)'
F_BEFEHL = 'Gefährdung durch unbeabsichtigtes Betätigen von Befehlsgebern'
F_QUETSCH = 'Mechanische Gefährdung durch Quetschen zwischen Fahrkorb und Schacht'
F_STOSS = 'Mechanische Gefährdung durch Stoß (fehlende Endbegrenzung, Aufprall)'
F_GEFAHRSTOFF = 'Gefährdung durch Gefahrstoffe und biologische Arbeitsstoffe'
F_UCM = 'Mechanische Gefährdung durch unkontrollierte Bewegung bei geöffneten Türen'
F_GLAS = 'Mechanische Gefährdung durch Bruch von Bauteilen und Einziehen an Glastüren'
F_CYBER = 'Gefährdung durch Manipulation sicherheitsrelevanter Steuerungsfunktionen'

# ---- Bedingungen -----------------------------------------------------------
def yes(q):      return {'question': q, 'operator': 'EQ', 'value': True}
def no(q):       return {'question': q, 'operator': 'EQ', 'value': False}
def eq(q, v):    return {'question': q, 'operator': 'EQ', 'value': v}
def neq(q, v):   return {'question': q, 'operator': 'NEQ', 'value': v}
def in_(q, vs):  return {'question': q, 'operator': 'IN', 'value': list(vs)}
def nin(q, vs):  return {'question': q, 'operator': 'NOT_IN', 'value': list(vs)}
def gt(q, v):    return {'question': q, 'operator': 'GT', 'value': v}
def gte(q, v):   return {'question': q, 'operator': 'GTE', 'value': v}
def lt(q, v):    return {'question': q, 'operator': 'LT', 'value': v}
def lte(q, v):   return {'question': q, 'operator': 'LTE', 'value': v}
def answered(q): return {'question': q, 'operator': 'ANSWERED'}
def all_(*xs):   return {'all': list(xs)}
def any_(*xs):   return {'any': list(xs)}
def not_(x):     return {'not': x}

# ---- Fragen ----------------------------------------------------------------
_seen_q = set()

def q(code, text, typ='YES_NO', ui=None, options=None, help=None,
      visible_when=None, legacy=None, cat=None, min=None, max=None):
    """Frage anlegen. options: Liste aus (value, label) oder Strings (value=label-slug)."""
    assert code not in _seen_q, 'doppelte Frage ' + code
    _seen_q.add(code)
    if cat is None:
        for p, c in _PREFIX2CAT.items():
            if code.startswith(p):
                cat = c
                break
    assert cat in CATS, 'unbekannter Erhebungsbereich für ' + code
    d = {'code': code, 'type': typ, 'domain': 'GBU', 'text': text,
         'category': CATS[cat]}
    if ui: d['ui_number'] = ui
    if legacy: d['legacy_id'] = legacy
    if help: d['help_text'] = help
    if visible_when: d['visible_when'] = visible_when
    if min is not None: d['min'] = min
    if max is not None: d['max'] = max
    if options:
        opts = []
        for o in options:
            if isinstance(o, str):
                opts.append({'value': o, 'label': o})
            else:
                opts.append({'value': o[0], 'label': o[1]})
        d['options'] = opts
    QUESTIONS.append(d)
    return code

def yn(code, text, **kw):
    return q(code, text, 'YES_NO', **kw)

def sel(code, text, options, **kw):
    return q(code, text, 'SELECT', options=options, **kw)

def num(code, text, **kw):
    """Zahlenfrage; min/max = fachlich plausibler Wertebereich (UI-Eingabegrenze)."""
    if 'min' not in kw or 'max' not in kw:
        # Kein Abbruch (andere Kataloge wie ft_content nutzen dieselbe DSL);
        # für den MF-Seed erzwingt gen_mf_catalog.check() den Wertebereich.
        print('WARNUNG', code + ': Zahlenfrage ohne min/max (UI-Eingabegrenzen)')
    return q(code, text, 'NUMBER', **kw)

# ---- Maßnahmen -------------------------------------------------------------
def _measure(text, kind):
    text = text.strip()
    typ = 'ORGANISATIONAL' if kind == 'sofort' else 'TECHNICAL'
    pc = 'SOFORT' if kind == 'sofort' else 'MITTELFRISTIG'
    code = 'm_' + hashlib.md5((typ + '|' + text).encode('utf-8')).hexdigest()[:10]
    if code not in MEASURES:
        MEASURES[code] = {'code': code, 'title': text, 'type': typ, 'priority_class': pc}
    return code

def _bindings(sofort, mittel):
    out = []
    if sofort:
        out.append({'measure': _measure(sofort, 'sofort'), 'group_id': 'sofort',
                    'relation': 'SINGLE', 'mandatory': True})
    if mittel:
        out.append({'measure': _measure(mittel, 'mittel'), 'group_id': 'mittel',
                    'relation': 'SINGLE', 'mandatory': True})
    return out

# Maßnahmen aus den bestehenden App-Katalogen (norm_81_20.json / norm_2026.json)
# per Istzustands-Text nachschlagen, damit Arnes freigegebene Formulierungen
# wiederverwendet werden.
_EXISTING = {}   # (hazard_code, label_prefix) -> (sofort, mittel)

def load_existing(seed_paths):
    import json
    for p in seed_paths:
        d = json.load(open(p, encoding='utf-8'))
        meas = {m['code']: m for m in d.get('measures', [])}
        qs = {x['code']: x for x in d.get('questions', [])}
        hq = {h['code']: h['questions'][0]['question'] for h in d['hazards']}
        for r in d['rules']:
            qc = hq[r['hazard']]
            lab = {o['value']: o['label'] for o in qs[qc]['options']}
            label = lab[r['condition']['value']]
            sofort = mittel = None
            for mb in r.get('measures', []):
                m = meas[mb['measure']]
                if mb.get('group_id') == 'sofort': sofort = m['title']
                elif mb.get('group_id') == 'mittel': mittel = m['title']
            _EXISTING[(r['hazard'], label)] = (sofort, mittel, r['result'])

def mx(hazard_code, label_prefix):
    """Maßnahmen (sofort, mittel) der bestehenden Istzustands-Option holen."""
    for (h, label), v in _EXISTING.items():
        if h == hazard_code and label.startswith(label_prefix):
            return v[0], v[1]
    raise KeyError('Option nicht gefunden: %s / %s' % (hazard_code, label_prefix))

# ---- Klärungsliste ---------------------------------------------------------
def k(kid, bereich, thema, frage, vorschlag, alternativen='', grund=''):
    assert not any(x['id'] == kid for x in KLAERUNG), 'doppelte Klärung ' + kid
    KLAERUNG.append({'id': kid, 'bereich': bereich, 'thema': thema, 'frage': frage,
                     'vorschlag': vorschlag, 'alternativen': alternativen,
                     'grund': grund, 'hazards': []})
    return kid

def _attach_k(kids, hazard_code):
    for kid in kids:
        for x in KLAERUNG:
            if x['id'] == kid and hazard_code not in x['hazards']:
                x['hazards'].append(hazard_code)

# ---- Regeln / Gefährdungen -------------------------------------------------
def r(cond, result, prio=100, sofort=None, mittel=None, mfrom=None,
      evidence='INFERRED', notes=None, klaerung=(), applicability=None,
      sources=()):
    """Regel-Rohling; hz() vergibt Code und Gefährdung.
    mfrom=('N20-K6', 'Zu kurze') übernimmt Maßnahmen der bestehenden Option."""
    if mfrom:
        s, m = mx(*mfrom)
        sofort = sofort or s
        mittel = mittel or m
    d = {'prio': prio, 'condition': cond, 'result': result,
         'measures': _bindings(sofort, mittel), 'evidence': evidence,
         'notes': notes, 'klaerung': list(klaerung) if isinstance(klaerung, (list, tuple)) else [klaerung],
         'applicability': applicability, 'sources': list(sources)}
    return d

def _collect(expr, into):
    if not expr:
        return
    if 'all' in expr:
        for e in expr['all']: _collect(e, into)
    elif 'any' in expr:
        for e in expr['any']: _collect(e, into)
    elif 'not' in expr:
        _collect(expr['not'], into)
    else:
        into.add(expr['question'])

_seen_h = set()

def hz(code, title, group, questions, rules, sources=(), factor=None, persons=(),
       agg='NONE', mode='STANDARD', description=None, klaerung=(), bereich=None):
    """Gefährdung anlegen.
    questions: Liste aus (frage, rolle, pflicht[, extras]) mit
      rolle in APPLICABILITY/TRIGGER/COMPENSATION/MODIFIER/OPTIONAL/DOCUMENTATION,
      pflicht in NEVER/ALWAYS/CONDITIONAL,
      extras: dict mit required_when / applicable_when / notes."""
    assert code not in _seen_h, 'doppelte Gefährdung ' + code
    assert len(code) <= 20, code
    assert group in GROUPS, 'unbekannte Baugruppe ' + group
    _seen_h.add(code)
    hqs = []
    for t in questions:
        qc, role, req = t[0], t[1], t[2]
        extra = t[3] if len(t) > 3 else {}
        d = {'question': qc, 'role': role, 'required_mode': req}
        if req == 'CONDITIONAL':
            assert 'required_when' in extra, code + ': CONDITIONAL ohne required_when (' + qc + ')'
        d.update(extra)
        hqs.append(d)
    # Jede Frage, die in einer Regel vorkommt, muss beantwortet sein, bevor die
    # Gefährdung bewertet wird (Review 02.09.2026, Punkt 2): Modifier und
    # Kompensationen werden Pflicht – bedingt, wenn die Frage nur unter einer
    # Sichtbarkeitsregel erscheint; Filterfragen (APPLICABILITY) bleiben unberührt.
    qdef = {x['code']: x for x in QUESTIONS}
    used = set()
    for rule in rules:
        _collect(rule['condition'], used)
        _collect(rule['applicability'], used)
    for d in hqs:
        if d['role'] == 'APPLICABILITY' or d['question'] not in used:
            continue
        if d.get('required_mode', 'NEVER') != 'NEVER':
            continue
        vis = qdef.get(d['question'], {}).get('visible_when')
        if vis:
            d['required_mode'] = 'CONDITIONAL'
            d['required_when'] = vis
        else:
            d['required_mode'] = 'ALWAYS'
        d['notes'] = ((d.get('notes', '') + ' ') if d.get('notes') else '') + \
            'Pflicht, weil bewertungsrelevant (automatisch gesetzt).'
    # Ausdrückliche Kein-Risiko-Regel (Review Punkt 1): kein stiller Fallback mehr.
    # Auch wenn es schon fachliche Kein-Risiko-Regeln gibt (z. B. für eine
    # zulässige Kompensation), decken die nur ihren Sonderfall ab; der Normalfall
    # „alles in Ordnung“ braucht eine eigene Auffangregel (niedrigste Priorität).
    def _catch_all(rule):
        c = rule['condition']
        return rule['result'] == 'NO_RISK' and isinstance(c, dict) and c.get('operator') == 'ANSWERED'
    if not any(_catch_all(rule) for rule in rules):
        anchor = next((d['question'] for d in hqs
                       if d['role'] == 'TRIGGER' and d.get('required_mode') == 'ALWAYS'),
                      next((d['question'] for d in hqs if d['role'] != 'APPLICABILITY'), None))
        if anchor:
            rules = list(rules) + [r(answered(anchor), 'NO_RISK', prio=1,
                                     sofort='Zustand erhalten; bei der wiederkehrenden Prüfung und der Betreiberkontrolle erneut prüfen',
                                     evidence='HIGH_CONFIDENCE',
                                     notes='Kein Risiko: keine Mangelregel trifft zu, alle Pflichtfragen beantwortet.')]
    h = {'code': code, 'domain': 'GBU', 'title': title, 'category': group,
         'aggregation_type': agg, 'evaluation_mode': mode, 'questions': hqs}
    if description: h['description'] = description
    if sources: h['sources'] = list(sources)
    if factor: h['hazard_factor'] = factor
    if persons: h['person_groups'] = list(persons)
    if bereich: h['ui_group'] = CATS[bereich]
    kl = list(klaerung) if isinstance(klaerung, (list, tuple)) else [klaerung]
    for rule in rules:
        kl += rule['klaerung']
    if kl:
        h['review_ids'] = sorted(set(kl))
        _attach_k(set(kl), code)
    HAZARDS.append(h)
    for i, rule in enumerate(rules, 1):
        rd = {'hazard': code, 'code': '%s-R%d' % (code, i), 'priority': rule['prio'],
              'condition': rule['condition'], 'result': rule['result'],
              'origin': 'OWN_RULE', 'evidence': rule['evidence'],
              'quality_status': 'REVIEW_REQUIRED'}
        if rule['applicability']: rd['applicability'] = rule['applicability']
        if rule['measures']: rd['measures'] = rule['measures']
        if rule['sources']: rd['sources'] = rule['sources']
        notes = rule['notes'] or ''
        if rule['klaerung']:
            notes = (notes + ' ' if notes else '') + 'KLÄREN: ' + ', '.join(rule['klaerung'])
        if notes: rd['notes'] = notes
        RULES.append(rd)
    return code

# ---- Quellen ---------------------------------------------------------------
def src(typ, doc, sec=None):
    d = {'type': typ, 'document': doc}
    if sec: d['section'] = sec
    return d

def en8120(sec):  return src('EN', 'DIN EN 81-20', sec)
def trbs3121(sec): return src('TRBS', 'TRBS 3121', sec)
def trbs(doc, sec=None): return src('TRBS', doc, sec)
def law(doc, sec=None):  return src('LAW', doc, sec)
def en(doc, sec=None):   return src('EN', doc, sec)
def dguv(doc, sec=None): return src('DGUV', doc, sec)
def other(doc, sec=None): return src('OTHER', doc, sec)
