import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';

/**
 * Die App liest ihre Regelwerke aus gbu_aufzug_app/assets/engine/. Das sind
 * abgeleitete Dateien: gen_app_asset.py entkernt die Seeds aus engine_model
 * um die Werkstattfelder und schreibt sie kompakt.
 *
 * Bis zum 30.09.2026 erzwang nichts diesen Schritt. Alle fünf Regelwerke der
 * App waren seit dem 21.09.2026 veraltet, ohne dass es irgendwo auffiel: die
 * `rule_version` ist ein von Hand gepflegter String und blieb unverändert.
 * Die App meldete „riedl-mf-2026.2" und rechnete mit 273 statt 287 Regeln –
 * ein erzeugter Bericht wies MF-T02 als „Hoch" aus, obwohl die Regel längst
 * auf „Mittel" korrigiert war.
 *
 * Dieser Test vergleicht deshalb den Inhalt, nicht die Versionsnummer.
 */

const HIER = import.meta.dirname;
const APP = path.join(HIER, '..', 'gbu_aufzug_app', 'assets', 'engine');

/** Seeds: werden entkernt ausgeliefert. */
const SEEDS = ['norm_81_20_mf.json', 'norm_81_80_mf.json', 'norm_cyber_mf.json',
               'norm_riedl_mf.json', 'norm_riedl_cyber.json'];
/** Wörtliche Kopien. */
const KOPIEN = ['riedl_map.json'];

const INTERN = new Set(['quality_status', 'review_ids']);

function ohneInterna(o: unknown): unknown {
  if (Array.isArray(o)) return o.map(ohneInterna);
  if (o && typeof o === 'object') {
    const r: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(o)) {
      if (!INTERN.has(k)) r[k] = ohneInterna(v);
    }
    return r;
  }
  return o;
}

const HINWEIS = 'weicht von engine_model ab – "python3 gen_app_asset.py --alle" '
  + 'laufen lassen und beide Repos committen. Die rule_version sagt nichts, '
  + 'sie wird von Hand gepflegt.';

for (const name of SEEDS) {
  test(`App-Asset ${name} ist auf dem Stand von engine_model`, () => {
    const ziel = path.join(APP, name);
    assert.ok(existsSync(ziel), `${name} fehlt in assets/engine`);
    const soll = ohneInterna(JSON.parse(readFileSync(path.join(HIER, name), 'utf8')));
    const ist = JSON.parse(readFileSync(ziel, 'utf8'));
    assert.deepStrictEqual(ist, soll, `${name} ${HINWEIS}`);
  });
}

for (const name of KOPIEN) {
  test(`App-Asset ${name} ist eine unveränderte Kopie`, () => {
    const ziel = path.join(APP, name);
    assert.ok(existsSync(ziel), `${name} fehlt in assets/engine`);
    assert.equal(readFileSync(ziel, 'utf8'),
                 readFileSync(path.join(HIER, name), 'utf8'),
                 `${name} ${HINWEIS}`);
  });
}
