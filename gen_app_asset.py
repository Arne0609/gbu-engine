# -*- coding: utf-8 -*-
"""Katalog-Seeds als App-Assets schreiben (kompaktes JSON ohne die internen
QA-Felder).

    python3 gen_app_asset.py norm_cyber_mf.json [Zielpfad]   ein Seed
    python3 gen_app_asset.py --alle                          alle Assets
    python3 gen_app_asset.py --pruefen                       nur vergleichen

Ohne Zielpfad wird ../gbu_aufzug_app/assets/engine/<name> geschrieben.
Entfernt rekursiv `quality_status` und `review_ids` – beides ist reine
Werkstatt-Information des Regelwerks und hat in der App nichts zu suchen.
`notes` bleibt erhalten (Hinweis im Bewertungs-Sheet).

Warum --alle und --pruefen:
Am 30.09.2026 stellte sich heraus, dass ALLE fünf Regelwerke der App seit dem
21.09.2026 veraltet waren – die Regelüberarbeitung aus der Prüfbericht-Runde
war nie in die Assets gelangt. Zu sehen war das nirgends, denn `rule_version`
wird von Hand gepflegt und blieb unverändert; die App meldete weiter
„riedl-mf-2026.2", rechnete aber mit 273 statt 287 Regeln. Ein erzeugter
Bericht (Fabriknr. 234) wies MF-T02 deshalb als „Hoch" aus, obwohl die Regel
längst auf „Mittel" korrigiert war.

`--pruefen` wird von app_assets.test.ts über `npm test` mitgeführt und schlägt
fehl, sobald ein Asset von seiner Quelle abweicht. Nach jeder Katalogänderung
gehört `--alle` in denselben Arbeitsgang wie der Katalogaufbau.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', 'gbu_aufzug_app', 'assets', 'engine')

# Seeds: werden entkernt und kompakt geschrieben.
SEEDS = ('norm_81_20_mf.json', 'norm_81_80_mf.json', 'norm_cyber_mf.json',
         'norm_riedl_mf.json', 'norm_riedl_cyber.json')
# Wörtliche Kopien: keine Seeds, werden unverändert übernommen.
KOPIEN = ('riedl_map.json',)

INTERN = ('quality_status', 'review_ids')


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in INTERN}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


def erzeuge(name):
    """Sollinhalt des Assets als bytes."""
    roh = open(os.path.join(HERE, name), encoding='utf-8').read()
    if name in KOPIEN:
        return roh.encode('utf-8')
    seed = json.loads(roh)
    return json.dumps(strip(seed), ensure_ascii=False,
                      separators=(',', ':')).encode('utf-8')


def kennzahlen(name):
    seed = json.load(open(os.path.join(HERE, name), encoding='utf-8'))
    if 'rule_version' not in seed:
        return '(Kopie)'
    return '%s | %d Fragen, %d Gefährdungen, %d Regeln' % (
        seed['rule_version'], len(seed['questions']),
        len(seed['hazards']), len(seed['rules']))


def schreibe(name, ziel=None):
    ziel = ziel or os.path.join(APP, name)
    daten = erzeuge(name)
    with open(ziel, 'wb') as fh:
        fh.write(daten)
    print('geschrieben: %s (%d KB) | %s'
          % (os.path.normpath(ziel), len(daten) // 1024, kennzahlen(name)))


def pruefe():
    """0 = alle Assets aktuell, 1 = mindestens eines veraltet."""
    abweichend = []
    for name in SEEDS + KOPIEN:
        ziel = os.path.join(APP, name)
        if not os.path.exists(ziel):
            abweichend.append((name, 'fehlt'))
            continue
        soll, ist = erzeuge(name), open(ziel, 'rb').read()
        if soll == ist:
            print('aktuell:  %-22s %s' % (name, kennzahlen(name)))
            continue
        grund = 'inhaltlich abweichend'
        if name in SEEDS:
            a, b = json.loads(ist), json.loads(soll)
            teile = ['%s %d->%d' % (k, len(a.get(k, [])), len(b.get(k, [])))
                     for k in ('questions', 'hazards', 'rules', 'measures')
                     if len(a.get(k, [])) != len(b.get(k, []))]
            if teile:
                grund = ', '.join(teile)
        abweichend.append((name, grund))
    for name, grund in abweichend:
        print('VERALTET: %-22s %s' % (name, grund))
    if abweichend:
        print('\n%d Asset(e) veraltet – "python3 gen_app_asset.py --alle" laufen '
              'lassen und beide Repos committen.\nAchtung: die rule_version sagt '
              'nichts, sie wird von Hand gepflegt.' % len(abweichend))
        return 1
    return 0


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == '--pruefen':
        sys.exit(pruefe())
    elif arg == '--alle':
        for n in SEEDS + KOPIEN:
            schreibe(n)
    elif arg and not arg.startswith('-'):
        schreibe(os.path.basename(arg),
                 sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        sys.exit(__doc__)
