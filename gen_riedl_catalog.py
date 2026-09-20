# -*- coding: utf-8 -*-
"""Erzeugt die GBU-Variante „Riedl" als Teilmenge des mehrfragigen Katalogs
(MF) und des Cyber-Katalogs (CY):

  python3 gen_riedl_catalog.py

Eingaben : norm_81_20_mf.json (81-20-mf-*), norm_cyber_mf.json (cyber-mf-*),
           riedl_content.py (Blattstruktur, Zuordnung, Texte)
Ausgaben : norm_riedl_mf.json     – GBU-Teil   (Regelversion riedl-mf-*)
           norm_riedl_cyber.json  – Cyber-Teil (Regelversion riedl-cyber-*)
           riedl_map.json         – Blattstruktur für Bericht und App
                                    (Blätter -> Zeilen -> Gefährdungen,
                                    Ampel-Zuordnung, Listen, Standardtexte)

Grundsatz (Entscheidung Arne 17.09.2026): abgeleitet, nicht neu formuliert –
Gefährdungen, Fragen, Regeln, Maßnahmen, Karten und Nachweise sind byteweise
identisch mit MF bzw. CY; nur der Umfang ist kleiner (Blätter der VFA-Vorlage
plus TRBS-3121-Anhang-1-Punkte plus Betreiberpflichten). Der Generator
bricht ab, wenn eine MF-/CY-Gefährdung weder zugeordnet noch in
riedl_content.NICHT_ENTHALTEN begründet ist, oder beides zugleich.
"""
import json, os, re, sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import riedl_content as rc  # noqa: E402
import catalog_check  # noqa: E402
from katalog_teilmenge import teilmenge, pruefe_identitaet  # noqa: E402

TRBS_RE = re.compile(r'Anh\. 1 Nr\. (\d+)')

# Fragen, die in der Teilmenge an keiner Gefährdung hängen, aber gebraucht
# werden: Baujahr und Konformitätsnachweis steuern die begründeten Annahmen
# (MF-D06 ist nicht enthalten), „überwachungsbedürftig" die Pflichtfrage 5.13
# des Cyber-Abschlusschecks (CY-O01 ist nicht enthalten). catalog_check meldet
# sie als unbenutzt – das ist hier gewollt und wird nicht ausgegeben.
STEUERFRAGEN = ('qa_baujahr', 'qd_konformitaet_geprueft', 'qa_ueberwachungsbeduerftig')


def lade(name):
    return json.load(open(os.path.join(HERE, name), encoding='utf-8'))


def zeilen_hazards(blaetter):
    out = OrderedDict()
    for b in blaetter:
        for z in b['zeilen']:
            for c in z['hazards']:
                if c in out:
                    raise SystemExit('%s doppelt zugeordnet (%s Zeile %d)' % (c, b['key'], z['nr']))
                out[c] = (b['key'], z['nr'])
    return out


def pruefe_abdeckung(quelle, zugeordnet, praefix):
    """Jede Gefährdung des Quellkatalogs ist zugeordnet ODER begründet weggelassen."""
    codes = [h['code'] for h in quelle['hazards']]
    fehler = []
    for c in codes:
        drin = c in zugeordnet
        raus = c in rc.NICHT_ENTHALTEN
        if drin and raus:
            fehler.append('%s: zugeordnet UND in NICHT_ENTHALTEN' % c)
        if not drin and not raus:
            fehler.append('%s: weder zugeordnet noch in NICHT_ENTHALTEN begründet' % c)
    for c in list(zugeordnet) + [k for k in rc.NICHT_ENTHALTEN if k.startswith(praefix)]:
        if c.startswith(praefix) and c not in codes:
            fehler.append('%s: im Quellkatalog unbekannt' % c)
    return fehler


def trbs_nummern(h):
    out = []
    for s in h.get('sources', []):
        if s.get('document') == 'TRBS 3121':
            m = TRBS_RE.search(s.get('section', ''))
            if m:
                out.append(int(m.group(1)))
    return sorted(set(out))


def blatt_map(blatt, seed, quelle_version):
    H = {h['code']: h for h in seed['hazards']}
    zeilen = []
    for z in blatt['zeilen']:
        eintrag = {
            'nr': z['nr'], 'titel': z['titel'], 'vfa': z.get('vfa', ''),
            'hazards': list(z['hazards']), 'deckung': z['deckung'],
            'bemerkung': z.get('bemerkung', ''),
            'trbs_anhang1': sorted({n for c in z['hazards'] for n in trbs_nummern(H[c])}),
        }
        if z.get('komponente') is not None:
            eintrag['komponente'] = z['komponente']
        if z.get('erlaeuterung') is not None:
            eintrag['erlaeuterung'] = z['erlaeuterung']
        zeilen.append(eintrag)
    return {'key': blatt['key'], 'kuerzel': blatt['kuerzel'], 'titel': blatt['titel'],
            'anlagenbereich': blatt['anlagenbereich'], 'katalog': quelle_version,
            'zeilen': zeilen}


def main():
    mf = lade('norm_81_20_mf.json')
    cy = lade('norm_cyber_mf.json')

    # ---- Zuordnung prüfen ------------------------------------------------
    zug_mf = zeilen_hazards(rc.BLAETTER)
    zug_cy = zeilen_hazards([rc.CYBER_BLATT])
    fehler = pruefe_abdeckung(mf, zug_mf, 'MF-') + pruefe_abdeckung(cy, zug_cy, 'CY-')
    for z in [z for b in rc.BLAETTER for z in b['zeilen']] + rc.CYBER_BLATT['zeilen']:
        if z['deckung'] not in ('voll', 'teilweise', 'freitext'):
            fehler.append('Zeile %s: unbekannte Deckung %r' % (z['titel'], z['deckung']))
    if fehler:
        print('\n'.join('FEHLER ' + f for f in fehler))
        sys.exit(1)

    # ---- Teilmengen bilden -------------------------------------------------
    seed_gbu = teilmenge(mf, list(zug_mf), rc.RULE_VERSION_GBU)
    seed_cy = teilmenge(cy, list(zug_cy), rc.RULE_VERSION_CYBER)

    for name, seed, quelle in (('GBU', seed_gbu, mf), ('Cyber', seed_cy, cy)):
        errors, warnings = catalog_check.check(seed)
        for w in warnings:
            if any(w.endswith('Frage %s wird von keiner Gefährdung benutzt' % q)
                   for q in STEUERFRAGEN):
                continue   # erwartet, siehe STEUERFRAGEN
            print('WARNUNG %s: %s' % (name, w))
        if errors:
            print('\n'.join('FEHLER %s: %s' % (name, e) for e in errors))
            sys.exit(1)
        catalog_check.validate_schema(seed)
        pruefe_identitaet(seed, quelle)

    json.dump(seed_gbu, open(os.path.join(HERE, 'norm_riedl_mf.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    json.dump(seed_cy, open(os.path.join(HERE, 'norm_riedl_cyber.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # ---- Blattstruktur (Bericht / App) ------------------------------------
    blaetter = [blatt_map(b, seed_gbu, mf['rule_version']) for b in rc.BLAETTER]
    cyber = blatt_map(rc.CYBER_BLATT, seed_cy, cy['rule_version'])
    # Cyber-ZÜS-Abschlusscheck: welche Punkte trägt die Teilmenge noch?
    zues = lade('cy_zues_map.json')
    hz = {h['code'] for h in seed_cy['hazards']}
    qs = {q['code'] for q in seed_cy['questions']}
    zues_punkte = []
    for p in zues['punkte']:
        fr = [f for f in p.get('fragen', []) if f in qs]
        hzs = [h for h in p.get('hazards', []) if h in hz]
        deckung = 'voll' if (len(fr) == len(p.get('fragen', [])) and
                             len(hzs) == len(p.get('hazards', []))) else \
            ('teilweise' if (fr or hzs) else 'nicht_erhoben')
        zues_punkte.append({'nr': p['nr'], 'frage': p['frage'], 'erfuellung': p.get('erfuellung'),
                            'fragen': fr, 'hazards': hzs, 'deckung': deckung})

    daten = {
        'variante': rc.VARIANTE,
        'typ_schluessel': rc.TYP_SCHLUESSEL,
        'titel': rc.TITEL, 'untertitel': rc.UNTERTITEL,
        'deckblatt_untertitel': rc.DECKBLATT_UNTERTITEL,
        'vorlagen': {'gbu': rc.VORLAGE_GBU, 'cyber': rc.VORLAGE_CYBER},
        'kataloge': {'gbu': rc.RULE_VERSION_GBU, 'cyber': rc.RULE_VERSION_CYBER,
                     'gbu_quelle': mf['rule_version'], 'cyber_quelle': cy['rule_version']},
        'ampel': rc.AMPEL, 'ampel_text': rc.AMPEL_TEXT, 'ampel_legende': rc.AMPEL_LEGENDE,
        'nohl_legende': [dict(zip(('stufe', 'r', 'potenzial', 'massnahmen'), n)) for n in rc.NOHL_LEGENDE],
        'verantwortlich': rc.VERANTWORTLICH, 'termin': rc.TERMIN,
        'termin_aus_gruppe': rc.TERMIN_AUS_GRUPPE,
        'deckblatt_felder': [dict(key=k, label=l) for k, l in rc.DECKBLATT_FELDER],
        'block_z': [dict(key=k, titel=t, verantwortliche=v) for k, t, v in rc.BLOCK_Z],
        'unterschriften': rc.UNTERSCHRIFTEN,
        'sonstiges': rc.SONSTIGES,
        'blaetter': blaetter,
        'cyber': cyber,
        'cyber_allgemeines': rc.CYBER_ALLGEMEINES,
        'cyber_wirksamkeit': rc.CYBER_WIRKSAMKEIT,
        'cyber_unterschrift': rc.CYBER_UNTERSCHRIFT,
        'cyber_zues': zues_punkte,
        'komponenten_stamm': [dict(key=k, label=l, hersteller=rc.HERSTELLER.get(k, []))
                              for k, l in rc.KOMPONENTEN_STAMM],
        'nicht_enthalten': rc.NICHT_ENTHALTEN,
        'klaerungen': [dict(zip(('id', 'thema', 'vorschlag', 'alternative'), k)) for k in rc.KLAERUNGEN],
    }
    json.dump(daten, open(os.path.join(HERE, 'riedl_map.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # ---- Bericht auf der Konsole -------------------------------------------
    def stats(name, seed, quelle):
        kat = Counter(q['category'] for q in seed['questions'])
        print('%s: %s aus %s' % (name, seed['rule_version'], quelle['rule_version']))
        print('  %d Fragen (Quelle %d), %d Gefährdungen (Quelle %d), %d Regeln (Quelle %d), %d Maßnahmen'
              % (len(seed['questions']), len(quelle['questions']), len(seed['hazards']),
                 len(quelle['hazards']), len(seed['rules']), len(quelle['rules']), len(seed['measures'])))
        if seed.get('question_groups'):
            print('  Karten: %d (Quelle %d), Nachweise: %d (Quelle %d), Annahmen: %d (Quelle %d)'
                  % (len(seed['question_groups']), len(quelle.get('question_groups', [])),
                     len(seed.get('nachweise', [])), len(quelle.get('nachweise', [])),
                     len(seed.get('assumptions', [])), len(quelle.get('assumptions', []))))
        print('  Erhebungsbereiche:', dict(sorted(kat.items())))
        print('  Stufen:', dict(Counter(r['result'] for r in seed['rules'])))
        print('  Freigabe:', dict(Counter(r.get('quality_status') for r in seed['rules'])))

    stats('norm_riedl_mf.json', seed_gbu, mf)
    stats('norm_riedl_cyber.json', seed_cy, cy)
    print('riedl_map.json: %d Blätter mit %d Zeilen, Cyber %d Zeilen; TRBS-Anhang-1-Punkte: %s'
          % (len(blaetter), sum(len(b['zeilen']) for b in blaetter), len(cyber['zeilen']),
             sorted({n for b in blaetter for z in b['zeilen'] for n in z['trbs_anhang1']})))
    print('  ZÜS-Abschlusscheck Cyber:', dict(Counter(p['deckung'] for p in zues_punkte)))
    print('  Schema: gültig; Inhalte identisch mit MF-/CY-Katalog')


if __name__ == '__main__':
    main()
