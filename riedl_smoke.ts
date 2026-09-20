// Smoke-Test der GBU-Variante „Riedl" gegen den Referenz-Evaluator.
//   node --experimental-strip-types riedl_smoke.ts
//
// Prüft
//   1. Struktur: jede Gefährdung der Teilmenge steht in genau einer Zeile der
//      Blattstruktur (riedl_map.json), jede Zeilen-Gefährdung im Katalog;
//   2. Deckungsgleichheit: auf zufälligen (auch unvollständigen) Antwortsätzen
//      liefert die Teilmenge je Gefährdung dasselbe Ergebnis wie der volle
//      MF- bzw. CY-Katalog (Status, Regeln, Annahmen) – der abgeleitete Typ
//      bewertet also nie anders als sein Original;
//   3. Ampel: Zeilen-, Blatt- und Gesamtampel (VFA-Deckblatt-Logik) auf der
//      Engine-Stufe, Fail-closed bei offenen Zeilen;
//   4. Leerer Fragebogen: keine Regellücke, nur INCOMPLETE / NOT_APPLICABLE.
import { readFileSync } from 'node:fs';
import { evaluate } from './evaluator.ts';

const mf = JSON.parse(readFileSync('./norm_81_20_mf.json', 'utf-8'));
const cy = JSON.parse(readFileSync('./norm_cyber_mf.json', 'utf-8'));
const rg = JSON.parse(readFileSync('./norm_riedl_mf.json', 'utf-8'));
const rc = JSON.parse(readFileSync('./norm_riedl_cyber.json', 'utf-8'));
const map = JSON.parse(readFileSync('./riedl_map.json', 'utf-8'));

let fehler = 0;
function ok(name: string, bedingung: boolean, zusatz = '') {
  if (bedingung) console.log(`ok      ${name}${zusatz ? '  ' + zusatz : ''}`);
  else { console.error(`FEHLER  ${name}${zusatz ? '  ' + zusatz : ''}`); fehler++; }
}

// ---- 1. Struktur ------------------------------------------------------------
function pruefeStruktur(name: string, seed: any, blaetter: any[]) {
  const imKatalog = new Set<string>(seed.hazards.map((h: any) => h.code));
  const zaehler = new Map<string, number>();
  for (const b of blaetter) for (const z of b.zeilen) for (const c of z.hazards)
    zaehler.set(c, (zaehler.get(c) ?? 0) + 1);
  const fehlend = [...imKatalog].filter((c) => !zaehler.has(c));
  const fremd = [...zaehler.keys()].filter((c) => !imKatalog.has(c));
  const doppelt = [...zaehler.entries()].filter(([, n]) => n > 1).map(([c]) => c);
  ok(`${name}: jede Katalog-Gefährdung in genau einer Zeile`,
    fehlend.length === 0 && fremd.length === 0 && doppelt.length === 0,
    `(${imKatalog.size} Gefährdungen, ${zaehler.size} zugeordnet)` +
    (fehlend.length ? ' fehlend: ' + fehlend.join(',') : '') +
    (fremd.length ? ' fremd: ' + fremd.join(',') : '') +
    (doppelt.length ? ' doppelt: ' + doppelt.join(',') : ''));
}
pruefeStruktur('GBU', rg, map.blaetter);
pruefeStruktur('Cyber', rc, [map.cyber]);
ok('GBU: Regelversion', rg.rule_version === map.kataloge.gbu, rg.rule_version);
ok('Cyber: Regelversion', rc.rule_version === map.kataloge.cyber, rc.rule_version);
ok('TRBS 3121 Anhang 1: alle 22 Punkte vertreten',
  new Set(map.blaetter.flatMap((b: any) => b.zeilen.flatMap((z: any) => z.trbs_anhang1))).size === 22);

// ---- 2. Deckungsgleichheit auf Zufallsantworten -------------------------------
// Deterministischer Zufall (mulberry32), damit der Lauf wiederholbar ist.
function rng(seed: number) {
  return () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function zufallsAntworten(seed: any, rand: () => number, anteil: number): Record<string, unknown> {
  const a: Record<string, unknown> = {};
  for (const q of seed.questions) {
    if (rand() > anteil) continue;
    if (q.type === 'YES_NO') a[q.code] = rand() < 0.5;
    else if (q.type === 'SELECT') a[q.code] = q.options[Math.floor(rand() * q.options.length)].value;
    else if (q.type === 'NUMBER') {
      const lo = q.min ?? 0, hi = q.max ?? 100;
      a[q.code] = q.code === 'qa_baujahr' ? 1960 + Math.floor(rand() * 66)
        : Math.round((lo + rand() * (hi - lo)) * 100) / 100;
    }
  }
  return a;
}

function vergleiche(name: string, voll: any, teil: any, laeufe: number, start: number) {
  const rand = rng(start);
  const behalten = new Set<string>(teil.hazards.map((h: any) => h.code));
  let abweichungen = 0; let verglichen = 0;
  const stati: Record<string, number> = {};
  for (let i = 0; i < laeufe; i++) {
    const anteil = i % 3 === 0 ? 1 : i % 3 === 1 ? 0.7 : 0.35;   // vollständig / teilweise / dünn
    const antworten = zufallsAntworten(voll, rand, anteil);
    const ev = new Map(evaluate(voll as any, antworten as any).map((r: any) => [r.hazard, r]));
    for (const r of evaluate(teil as any, antworten as any)) {
      const o: any = ev.get(r.hazard);
      verglichen++;
      stati[r.status] = (stati[r.status] ?? 0) + 1;
      const gleich = o && o.status === r.status &&
        JSON.stringify(o.matched_rules) === JSON.stringify(r.matched_rules) &&
        JSON.stringify(o.overridden_rules) === JSON.stringify(r.overridden_rules) &&
        !!o.rule_gap === !!r.rule_gap &&
        JSON.stringify(o.assumed ?? []) === JSON.stringify(r.assumed ?? []);
      if (!gleich) {
        abweichungen++;
        if (abweichungen <= 5) console.error(`   Abweichung ${r.hazard}: Teil ${r.status} / Voll ${o?.status}`);
      }
    }
    // Rückrichtung: keine Gefährdung der Teilmenge fehlt in der Bewertung
    if ([...behalten].some((c) => !ev.has(c))) abweichungen++;
  }
  ok(`${name}: Teilmenge bewertet wie der volle Katalog`, abweichungen === 0,
    `(${laeufe} Antwortsätze, ${verglichen} Bewertungen, Stati ${JSON.stringify(stati)})`);
}
vergleiche('GBU', mf, rg, 300, 20260917);
vergleiche('Cyber', cy, rc, 300, 426);

// ---- 3. Ampel -------------------------------------------------------------------
const AMPEL: Record<string, string> = map.ampel;
function ampelFarben(farben: string[]): string {
  const f = farben.filter((x) => x !== 'na');
  if (f.length === 0) return 'na';
  if (f.includes('offen')) return 'offen';
  for (const x of ['rot', 'gelb', 'gruen']) if (f.includes(x)) return x;
  return 'gruen';
}
const ampelZeile = (stati: string[]) => ampelFarben(stati.map((s) => AMPEL[s]));

ok('Ampel Zeile: Kein Risiko + Niedrig = Grün', ampelZeile(['NO_RISK', 'LOW']) === 'gruen');
ok('Ampel Zeile: Mittel = Gelb', ampelZeile(['NO_RISK', 'MEDIUM']) === 'gelb');
ok('Ampel Zeile: Hoch schlägt Mittel', ampelZeile(['MEDIUM', 'HIGH', 'LOW']) === 'rot');
ok('Ampel Zeile: nicht zutreffend zählt nicht', ampelZeile(['NOT_APPLICABLE', 'LOW']) === 'gruen');
ok('Ampel Zeile: nur nicht zutreffend = n. a.', ampelZeile(['NOT_APPLICABLE']) === 'na');
ok('Ampel Zeile: unvollständig hält offen (fail-closed)', ampelZeile(['HIGH', 'INCOMPLETE']) === 'offen');
ok('Ampel Blatt: alles Grün = Grün', ampelFarben(['gruen', 'gruen', 'na']) === 'gruen');
ok('Ampel Blatt: ein Gelb = Gelb', ampelFarben(['gruen', 'gelb']) === 'gelb');
ok('Ampel Blatt: ein Rot = Rot', ampelFarben(['gelb', 'rot', 'gruen']) === 'rot');
ok('Ampel Gesamt: offenes Blatt = offen', ampelFarben(['gruen', 'offen', 'rot']) === 'offen');

// Ende-zu-Ende an einer Zeile: Kabine 4 (Haltegenauigkeit, MF-K03)
function zeile(blattKey: string, nr: number) {
  return map.blaetter.find((b: any) => b.key === blattKey).zeilen.find((z: any) => z.nr === nr);
}
function zeilenAmpel(seed: any, z: any, antworten: Record<string, unknown>): string {
  const ev = new Map(evaluate(seed as any, antworten as any).map((r: any) => [r.hazard, r.status]));
  return ampelZeile(z.hazards.map((c: string) => ev.get(c) as string));
}
const k4 = zeile('kabine', 4);
ok('Kabine 4: Stufe bis 10 mm -> Grün',
  zeilenAmpel(rg, k4, { qk_stufe_mm: 'bis_10', qa_nutzung_pmem: false }) === 'gruen');
ok('Kabine 4: Stufe 11–20 mm -> Gelb',
  zeilenAmpel(rg, k4, { qk_stufe_mm: '11_20', qa_nutzung_pmem: false }) === 'gelb');
ok('Kabine 4: Stufe über 20 mm -> Rot',
  zeilenAmpel(rg, k4, { qk_stufe_mm: 'ueber_20', qa_nutzung_pmem: false }) === 'rot');
ok('Kabine 4: unbeantwortet -> offen', zeilenAmpel(rg, k4, {}) === 'offen');
const z5 = zeile('zugang', 5);
ok('Zugang 5: Schlüsseltresor -> Grün', zeilenAmpel(rg, z5, { qz_zugang_befreiung: 'jederzeit' }) === 'gruen');
ok('Zugang 5: kein Zugang -> nicht Grün', zeilenAmpel(rg, z5, { qz_zugang_befreiung: 'nein' }) !== 'gruen');
const c1 = map.cyber.zeilen.find((z: any) => z.nr === 1);
ok('Cyber 1: Relaissteuerung -> n. a.', zeilenAmpel(rc, c1, { qa_steuerungsart: 'relais' }) === 'na');
const c8 = map.cyber.zeilen.find((z: any) => z.nr === 8);
const nichtVernetzt = { qa_vernetzt: false, qn_softwarestand: 'aktuell', qn_funktionsreduzierung: true } as any;
const evC8 = new Map(evaluate(rc as any, nichtVernetzt).map((r: any) => [r.hazard, r.status]));
ok('Cyber 8: nicht vernetzt -> C11–C13 nicht zutreffend',
  ['CY-C11', 'CY-C12', 'CY-C13'].every((c) => evC8.get(c) === 'NOT_APPLICABLE'),
  JSON.stringify(Object.fromEntries(c8.hazards.map((c: string) => [c, evC8.get(c)]))));

// ---- 4. Leerer Fragebogen ---------------------------------------------------------
for (const [name, seed] of [['GBU', rg], ['Cyber', rc]] as const) {
  const leer = evaluate(seed as any, {} as any);
  const gaps = leer.filter((r: any) => r.rule_gap).length;
  const fremd = leer.filter((r: any) => !['INCOMPLETE', 'NOT_APPLICABLE'].includes(r.status)).length;
  ok(`${name}: leerer Fragebogen ohne Regellücke, nur unvollständig/n. a.`, gaps === 0 && fremd === 0,
    `(${leer.length} Gefährdungen)`);
}

if (fehler > 0) { console.error(`\n${fehler} Fehler`); process.exit(1); }
console.log('\nalle Prüfungen bestanden');
