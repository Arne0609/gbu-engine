# -*- coding: utf-8 -*-
"""Konvertiert die bestehenden App-Kataloge in Engine-Seed-Dateien
(questions + hazards + evaluation_rules, origin=NORM_DERIVED).

Quellen:
  * istzustand_optionen.dart  -> 81-80, 81-20, 2026-Ergaenzung
  * GBU_EN8141_Variante.xlsx  -> EN 81-41

Modell-Abbildung:
  App-Kategorie  -> hazard
  je Kategorie   -> eine SELECT-Frage (required_mode ALWAYS => unbeantwortet
                    ergibt INCOMPLETE, nicht NO_RISK)
  je Istzustand  -> eine Antwortoption + eine Regel (Ampel/Bauart -> risk_status)

Ampel-Abbildung:  gruen->NO_RISK, gelb->MEDIUM, rot->HIGH;
                  "Nicht anwendbar/zutreffend" -> NOT_APPLICABLE.
EN 81-41 (xlsx) nutzt eine 4-stufige Skala mit eigener Risikospalte:
                  kein->NO_RISK, Niedriges->LOW, Mittleres->MEDIUM, Hohes->HIGH.
Sofort-/Mittelfristmassnahme werden (vorerst) in rule.notes erhalten.
"""
import re, json, hashlib, os

DART = "/mnt/user-data/uploads/GBU_APP/gbu_aufzug_app/lib/data/istzustand_optionen.dart"
XLSX = "/root/.claude/uploads/b8038905-5da7-5229-bb16-cf5de25fcfef/004fb1b1-GBU_EN8141_Variante.xlsx"
OUT = "/home/claude/engine_model"

GEE_DART = "/mnt/user-data/uploads/GBU_APP/gbu_aufzug_app/lib/models/gefaehrdungseintrag.dart"

def unesc(s):
    return s.replace("\\'", "'").replace('\\$', '$').replace('\\\\', '\\')

def _classify_ref(seg):
    """(type, document, section) aus einem einzelnen Normbezug-Segment."""
    seg = seg.strip().rstrip('.')
    tests = [
        (r'(TRBS\s*\d+[\d\-]*(?:\s*Teil\s*\d+)?)\s*(.*)', 'TRBS'),
        (r'(DIN\s+EN\s+[\d\-]+|EN\s+[\d\-]+)\s*(.*)', 'EN'),
        (r'(BetrSichV)\s*(.*)', 'LAW'),
        (r'(ArbSchG)\s*(.*)', 'LAW'),
        (r'(ASR\s*\S+)\s*(.*)', 'OTHER'),
        (r'(Maschinenrichtlinie[^;]*|Richtlinie\s*[\d/]+/EG)\s*(.*)', 'EU_DIRECTIVE'),
        (r'(Verordnung\s*\(EU\)[^;]*)\s*(.*)', 'EU_REGULATION'),
        (r'(DGUV[^;]*?)\s*(.*)', 'DGUV'),
        (r'(TÜV[^;]*)', 'OTHER'),
    ]
    for pat, typ in tests:
        m = re.match(pat, seg)
        if m:
            doc = m.group(1).strip()
            sec = (m.group(2).strip(' ,.;:') if m.lastindex and m.lastindex >= 2 else '')
            return typ, doc[:80], sec[:120]
    return 'OTHER', seg[:80], ''

def parse_ref(text):
    """Zerlegt einen Normbezug-Text in strukturierte Quellen."""
    out, seen = [], set()
    for seg in re.split(r'\s*;\s*', (text or '').strip()):
        seg = seg.strip()
        if not seg or seg.startswith('http'):
            continue
        typ, doc, sec = _classify_ref(seg)
        key = (typ, doc, sec)
        if key in seen:
            continue
        seen.add(key)
        out.append({'type': typ, 'document': doc, **({'section': sec} if sec else {})})
    return out

def parse_norm_map(text, mapname):
    """Liest eine Map<String,String> (Kategorie -> Normbezug) aus Dart."""
    m = re.search(mapname + r'\s*=\s*\{(.*?)\n\s{2}\};', text, re.S)
    if not m:
        return {}
    body = m.group(1)
    pairs = re.findall(r"'((?:[^'\\]|\\.)*)'\s*:\s*'((?:[^'\\]|\\.)*)'", body)
    return {unesc(k): unesc(v) for k, v in pairs}

def arg(line, name):
    m = re.search(name + r":\s*'((?:[^'\\]|\\.)*)'", line)
    return unesc(m.group(1)) if m else None

def risk_from(ampel, text):
    t = (text or '').strip().lower()
    if t.startswith('nicht anwendbar') or t.startswith('nicht zutreffend'):
        return 'NOT_APPLICABLE'
    return {'gruen': 'NO_RISK', 'gelb': 'MEDIUM', 'rot': 'HIGH'}.get(ampel, 'NO_RISK')

def oval(text):
    return 'o' + hashlib.md5(text.encode('utf-8')).hexdigest()[:8]

def suffix(prefix_raw):
    return re.sub(r'[^A-Za-z0-9]', '_', prefix_raw).lower()

def reg_measure(measures, text, kind):
    """Registriert eine Maßnahme (dedupliziert) und liefert ihren Code.
    kind: 'sofort' (organisatorisch/Sofortmaßnahme) | 'mittel' (technisch)."""
    text = str(text).strip()
    typ = 'ORGANISATIONAL' if kind == 'sofort' else 'TECHNICAL'
    pc = 'SOFORT' if kind == 'sofort' else 'MITTELFRISTIG'
    code = 'm_' + hashlib.md5((typ + '|' + text).encode('utf-8')).hexdigest()[:10]
    if code not in measures:
        measures[code] = {'code': code, 'title': text, 'type': typ, 'priority_class': pc}
    return code

def measure_bindings(measures, sofort, mittel):
    mb = []
    if sofort and str(sofort).strip():
        mb.append({'measure': reg_measure(measures, sofort, 'sofort'),
                   'group_id': 'sofort', 'relation': 'SINGLE', 'mandatory': True})
    if mittel and str(mittel).strip():
        mb.append({'measure': reg_measure(measures, mittel, 'mittel'),
                   'group_id': 'mittel', 'relation': 'SINGLE', 'mandatory': True})
    return mb

# ---- Dart-Kataloge parsen --------------------------------------------------
# Eigene Ergänzungen zu App-Optionen ohne hinterlegte Maßnahme (Review 02.09.2026,
# Punkt 5): jede Risikooption braucht mindestens eine Maßnahme. Schlüssel = Optionstext.
ERGAENZUNGEN = {
    'UCM nicht notwendig, weil kein SR-Modul, 2K-Bremse mit Schalter und statisch bestimmte Lagerung vorhanden': {
        'sofort': 'Bremsüberwachung und Bremsprüfung im Wartungsumfang halten',
        'mittel': 'Bei Steuerungs- oder Antriebsmodernisierung UCM-Schutz nach EN 81-20 5.6.7 vorsehen',
    },
}

def parse_dart():
    cats = {'81_80': [], '81_20': [], '2026': []}  # type -> list[(key, [opt...])]
    name2type = {'optionen': '81_80', 'optionen81_20': '81_20', 'optionen2026': '2026'}
    cur_type = None
    cur_key = None
    cur_opts = None
    start_re = re.compile(r'Map<String, List<IstzustandOption>>\s+(\w+)\s*=\s*\{')
    key_re = re.compile(r"^\s{4}'((?:[^'\\]|\\.)*)':\s*\[")
    for line in open(DART, encoding='utf-8'):
        m = start_re.search(line)
        if m:
            cur_type = name2type.get(m.group(1))
            cur_key = None
            continue
        if cur_type is None:
            continue
        if re.match(r'^\s{2}\};', line):  # Ende einer Top-Level-Map
            cur_type = None
            cur_key = None
            continue
        km = key_re.match(line)
        if km:
            cur_key = unesc(km.group(1))
            cur_opts = []
            cats[cur_type].append((cur_key, cur_opts))
            continue
        if cur_key is not None and 'IstzustandOption(' in line:
            text = arg(line, 'text')
            ampel = arg(line, 'ampel')
            if text is None:
                continue
            ext = ERGAENZUNGEN.get(text, {}) if ampel in ('gelb', 'rot') else {}
            cur_opts.append({
                'text': text, 'ampel': ampel,
                'sofort': arg(line, 'sofortMassnahme') or ext.get('sofort'),
                'mittel': arg(line, 'mittelfristigMassnahme') or ext.get('mittel'),
            })
    return cats

def build_from_cats(entries, typ_pfx, typ_low, domain_default='GBU', normmap=None):
    normmap = normmap or {}
    questions, hazards, rules = [], [], []
    measures = {}
    for key, opts in entries:
        prefix_raw = re.split(r'\s[–-]\s', key, maxsplit=1)[0].strip()
        sfx = suffix(prefix_raw)
        hcode = f'{typ_pfx}-{prefix_raw}'[:20]
        qcode = f'q_{typ_low}_{sfx}'
        domain = 'CYBER' if prefix_raw[:1] == 'C' and typ_low == 'e26' else domain_default
        # Optionen deduplizieren (gleicher Text -> gleicher value)
        seen, options = set(), []
        for o in opts:
            v = oval(o['text'])
            if v in seen:
                continue
            seen.add(v)
            options.append({'value': v, 'label': o['text']})
        questions.append({'code': qcode, 'type': 'SELECT', 'domain': domain,
                          'text': key, 'category': key, 'options': options})
        srcs = parse_ref(normmap.get(key, ''))
        hazards.append({'code': hcode, 'domain': domain, 'title': key, 'category': key,
                        'aggregation_type': 'NONE', 'evaluation_mode': 'STANDARD',
                        'questions': [{'question': qcode, 'role': 'TRIGGER',
                                       'required_mode': 'ALWAYS'}],
                        **({'sources': srcs} if srcs else {})})
        idx = 0
        seen.clear()
        for o in opts:
            v = oval(o['text'])
            if v in seen:
                continue
            seen.add(v)
            idx += 1
            mb = measure_bindings(measures, o.get('sofort'), o.get('mittel'))
            rules.append({
                'hazard': hcode, 'code': f'{hcode}-R{idx}', 'priority': 100,
                'condition': {'question': qcode, 'operator': 'EQ', 'value': v},
                'result': risk_from(o['ampel'], o['text']),
                'origin': 'NORM_DERIVED', 'evidence': 'DIRECT', 'quality_status': 'VERIFIED',
                **({'measures': mb} if mb else {}),
            })
    return questions, hazards, rules, list(measures.values())

# ---- EN 81-41 aus xlsx -----------------------------------------------------
def build_en8141():
    import openpyxl
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    kat = wb['Katalog_EN81-41']
    RISK = {'kein Risiko': 'NO_RISK', 'Niedriges Risiko': 'LOW',
            'Mittleres Risiko': 'MEDIUM', 'Hohes Risiko': 'HIGH',
            'Nicht zutreffend': 'NOT_APPLICABLE'}
    from collections import OrderedDict
    pp = OrderedDict()
    for row in kat.iter_rows(min_row=4, values_only=True):
        if not row[0]:
            continue
        _id, nr, bereich, frage, ist, risklabel, sofort, mittel = [row[i] for i in range(8)]
        basis = row[8] if len(row) > 8 else None
        nr = int(nr)
        pp.setdefault(nr, {'bereich': bereich, 'frage': frage, 'basis': basis, 'opt': []})
        pp[nr]['opt'].append({'id': _id, 'text': ist, 'risk': RISK[risklabel],
                              'sofort': sofort, 'mittel': mittel})
    questions, hazards, rules = [], [], []
    measures = {}
    for nr, d in pp.items():
        hcode = f'EN8141-P{nr}'
        qcode = f'q_en8141_p{nr}'
        options = [{'value': o['id'], 'label': o['text']} for o in d['opt']]
        questions.append({'code': qcode, 'type': 'SELECT', 'domain': 'GBU',
                          'text': d['frage'], 'category': d['bereich'], 'options': options})
        srcs = parse_ref(d.get('basis'))
        hazards.append({'code': hcode, 'domain': 'GBU', 'title': d['frage'],
                        'category': d['bereich'], 'aggregation_type': 'NONE',
                        'evaluation_mode': 'STANDARD',
                        'questions': [{'question': qcode, 'role': 'TRIGGER',
                                       'required_mode': 'ALWAYS'}],
                        **({'sources': srcs} if srcs else {})})
        for i, o in enumerate(d['opt'], 1):
            mb = measure_bindings(measures, o.get('sofort'), o.get('mittel'))
            rules.append({
                'hazard': hcode, 'code': f'{hcode}-R{i}', 'priority': 100,
                'condition': {'question': qcode, 'operator': 'EQ', 'value': o['id']},
                'result': o['risk'], 'origin': 'NORM_DERIVED', 'evidence': 'DIRECT',
                'quality_status': 'VERIFIED',
                **({'measures': mb} if mb else {}),
            })
    return questions, hazards, rules, list(measures.values())

CYBER_DART = "/mnt/user-data/uploads/GBU_APP/gbu_aufzug_app/lib/data/cyber_pruefkatalog.dart"

def _join_strings(blob):
    """Fasst aufeinanderfolgende Dart-String-Literale ('a' 'b') zusammen."""
    parts = re.findall(r"'((?:[^'\\]|\\.)*)'", blob)
    return unesc(' '.join(p.strip() for p in parts)).strip()

def _field(chunk, name):
    m = re.search(name + r":\s*((?:'(?:[^'\\]|\\.)*'\s*)+)", chunk)
    return _join_strings(m.group(1)) if m else ''

def parse_cyber_list(text, listname):
    m = re.search(r'List<CyberPrueffeld>\s+' + listname + r'\s*=\s*\[(.*?)\n\s{2}\];',
                  text, re.S)
    if not m:
        return []
    body = m.group(1)
    chunks = re.split(r'CyberPrueffeld\(', body)[1:]
    felder = []
    for ch in chunks:
        nummer = re.search(r'nummer:\s*(\d+)', ch)
        art = re.search(r'pruefart:\s*CyberPruefart\.(\w+)', ch)
        felder.append({
            'nummer': int(nummer.group(1)) if nummer else 0,
            'prueffeld': _field(ch, 'prueffeld'),
            'sollzustand': _field(ch, 'sollzustand'),
            'standardMassnahme': _field(ch, 'standardMassnahme'),
            'pruefart': art.group(1) if art else 'ordnung',
            'regelbezug': _field(ch, 'regelbezug'),
        })
    return felder

def build_cyber(felder, typ_pfx, typ_low):
    """Je Prüffeld: hazard + SELECT-Frage mit 4 Standardstufen + Regeln."""
    questions, hazards, rules, measures = [], [], [], {}
    STUFEN = [
        ('erfuellt', 'Anforderung erfüllt', 'NO_RISK'),
        ('teilweise', 'Teilweise erfüllt', 'MEDIUM'),
        ('nicht_erfuellt', 'Nicht erfüllt', 'HIGH'),
        ('na', 'Nicht anwendbar (begründet)', 'NOT_APPLICABLE'),
    ]
    for f in felder:
        nr = f['nummer']
        hcode = f'{typ_pfx}-{nr}'
        qcode = f'q_{typ_low}_{nr}'
        title = f['prueffeld']
        # Maßnahme (Standardmaßnahme bei Abweichung); Prüfart bestimmt den Typ.
        mtype = 'ORGANISATIONAL' if f['pruefart'] == 'ordnung' else 'TECHNICAL'
        mcode = None
        if f['standardMassnahme']:
            mcode = 'm_' + hashlib.md5((mtype + '|' + f['standardMassnahme']).encode('utf-8')).hexdigest()[:10]
            measures.setdefault(mcode, {'code': mcode, 'title': f['standardMassnahme'],
                                        'type': mtype, 'priority_class': 'MASSNAHME'})
        qtext = title + ' — Sollzustand: ' + f['sollzustand'] if f['sollzustand'] else title
        questions.append({'code': qcode, 'type': 'SELECT', 'domain': 'CYBER',
                          'text': qtext, 'category': 'Cybersicherheit (TRBS 1115-1)',
                          'options': [{'value': v, 'label': l} for v, l, _ in STUFEN]})
        srcs = parse_ref(f['regelbezug'])
        hazards.append({'code': hcode, 'domain': 'CYBER', 'title': title,
                        'description': f['sollzustand'],
                        'category': 'Cybersicherheit', 'aggregation_type': 'NONE',
                        'evaluation_mode': 'STANDARD',
                        'questions': [{'question': qcode, 'role': 'TRIGGER',
                                       'required_mode': 'ALWAYS'}],
                        **({'sources': srcs} if srcs else {})})
        for i, (v, l, risk) in enumerate(STUFEN, 1):
            rule = {'hazard': hcode, 'code': f'{hcode}-R{i}', 'priority': 100,
                    'condition': {'question': qcode, 'operator': 'EQ', 'value': v},
                    'result': risk, 'origin': 'NORM_DERIVED', 'evidence': 'DIRECT',
                    'quality_status': 'VERIFIED'}
            if mcode and risk in ('MEDIUM', 'HIGH'):
                rule['measures'] = [{'measure': mcode, 'group_id': 'massnahme',
                                     'relation': 'SINGLE', 'mandatory': True}]
            rules.append(rule)
    return questions, hazards, rules, list(measures.values())

def write_seed(fname, version, q, h, r, m):
    doc = {'rule_version': version, 'questions': q, 'measures': m, 'hazards': h, 'rules': r}
    with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f'{fname}: {len(q)} Fragen, {len(h)} Gefaehrdungen, {len(r)} Regeln, '
          f'{len(m)} Maßnahmen')

def main():
    cats = parse_dart()
    gee = open(GEE_DART, encoding='utf-8').read()
    nref81_20 = parse_norm_map(gee, 'normReferenz81_20')
    nref2026 = parse_norm_map(gee, 'normReferenz2026')
    q, h, r, m = build_from_cats(cats['81_80'], 'N80', 'n80')
    write_seed('norm_81_80.json', '81-80-2026.1', q, h, r, m)
    q, h, r, m = build_from_cats(cats['81_20'], 'N20', 'n20', normmap=nref81_20)
    write_seed('norm_81_20.json', '81-20-2026.1', q, h, r, m)
    q, h, r, m = build_from_cats(cats['2026'], 'E26', 'e26', normmap=nref2026)
    write_seed('norm_2026.json', '2026add-2026.1', q, h, r, m)
    q, h, r, m = build_en8141()
    write_seed('norm_en8141.json', 'en8141-2026.1', q, h, r, m)
    ctext = open(CYBER_DART, encoding='utf-8').read()
    q, h, r, m = build_cyber(parse_cyber_list(ctext, 'prueffelder'), 'CYV', 'cyv')
    write_seed('norm_cyber_voll.json', 'cyber-voll-2026.1', q, h, r, m)
    q, h, r, m = build_cyber(parse_cyber_list(ctext, 'minimalPrueffelder'), 'CYM', 'cym')
    write_seed('norm_cyber_minimal.json', 'cyber-minimal-2026.1', q, h, r, m)

if __name__ == '__main__':
    main()
