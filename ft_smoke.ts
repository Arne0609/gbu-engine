// Smoke-Test des Fahrtreppen-Katalogs gegen den Referenz-Evaluator.
import { readFileSync } from 'node:fs';
import { evaluate, summarize } from './evaluator.ts';

const seed = JSON.parse(readFileSync('./norm_fahrtreppe.json', 'utf-8'));
const qs = new Map<string, any>(seed.questions.map((q: any) => [q.code, q]));

function fill(overrides: Record<string, any>, base: 'gut' | 'leer' | 'schlecht') {
  const a: Record<string, any> = {};
  if (base !== 'leer') {
    for (const q of seed.questions) {
      if (q.type === 'YES_NO') a[q.code] = base === 'gut';
      else if (q.type === 'NUMBER') a[q.code] = 1;
      else if (q.type === 'SELECT') a[q.code] = q.options[base === 'gut' ? 0 : q.options.length - 1].value;
    }
    // Fragen, bei denen "Ja" der Mangel ist bzw. Merkmale, die neutral bleiben
    for (const c of ['qb_zugang_engstelle', 'qb_boden_nass', 'qb_bel_defekt',
                     'qb_glas_beschaedigt', 'qb_wagen_fremd', 'qb_reinigung_betrieb',
                     'qi_absturz_zugang', 'qi_alleinarbeit']) {
      a[c] = base === 'gut' ? false : true;
    }
  }
  return { ...a, ...overrides };
}

function run(label: string, answers: Record<string, any>) {
  const res = evaluate(seed as any, answers);
  const sum = summarize(res);
  console.log(label, JSON.stringify(sum));
  return { res, sum };
}

// 1) Leerer Zustand: nichts darf NO_RISK sein
const leer = run('leer          ', fill({}, 'leer'));
if (leer.sum.NO_RISK > 0) throw new Error('Unbewertet ergibt Kein Risiko!');

// 2) Alles in Ordnung, beide Bereiche
const gut = run('alles gut     ', fill({ qa_teil_instandhaltung: true }, 'gut'));
if (gut.sum.HIGH || gut.sum.MEDIUM || gut.sum.LOW || gut.sum.INCOMPLETE)
  throw new Error('Guter Zustand ergibt Risiko: ' + JSON.stringify(
    gut.res.filter(r => !['NO_RISK', 'NOT_APPLICABLE'].includes(r.status))));

// 3) Nur Betreiber-GBU: alle I-Gefährdungen NOT_APPLICABLE, keine INCOMPLETE
const nurB = run('nur Betreiber ', fill({ qa_teil_instandhaltung: false }, 'gut'));
const iHaz = seed.hazards.filter((h: any) => h.code.startsWith('FT-I')).map((h: any) => h.code);
const bad = nurB.res.filter(r => iHaz.includes(r.hazard) && r.status !== 'NOT_APPLICABLE');
if (bad.length) throw new Error('I-Bereich nicht abgeschaltet: ' + JSON.stringify(bad.slice(0, 3)));
if (nurB.sum.INCOMPLETE) throw new Error('Betreiber-GBU unvollständig trotz vollständiger Antworten');

// 4) Schlechter Zustand
const schlecht = run('alles schlecht', fill({ qa_teil_instandhaltung: true }, 'schlecht'));
if (!schlecht.sum.HIGH) throw new Error('Kein Hoch im schlechten Zustand');

// 5) Kompensation: Kammplatte beschädigt, Abschaltung wirksam, keine Kinder -> MEDIUM
const komp = evaluate(seed as any, fill({ qa_teil_instandhaltung: false, qa_kinder: false,
  qb_kamm_zustand: false, qb_kamm_abschaltung: true, qb_kamm_eingriff: true }, 'gut'),
  ).find(r => r.hazard === 'FT-B17');
console.log('FT-B17 (Kamm beschädigt, Abschaltung wirksam):', komp?.status, komp?.matched_rule);
if (komp?.status !== 'MEDIUM') throw new Error('Kompensation Kammplatte greift nicht');

// 6) Ohne Abschaltung -> HIGH
const komp2 = evaluate(seed as any, fill({ qa_teil_instandhaltung: false, qa_kinder: false,
  qb_kamm_zustand: false, qb_kamm_abschaltung: false }, 'gut'),
  ).find(r => r.hazard === 'FT-B17');
if (komp2?.status !== 'HIGH') throw new Error('Fehlende Kammplattenabschaltung nicht Hoch');

// 7) Eine fehlende Pflichtantwort -> genau diese Gefährdung INCOMPLETE
const teil = fill({ qa_teil_instandhaltung: false }, 'gut');
delete teil['qb_nothalt_vorhanden'];
const inc = evaluate(seed as any, teil).filter(r => r.status === 'INCOMPLETE').map(r => r.hazard);
console.log('fehlende Antwort qb_nothalt_vorhanden -> INCOMPLETE:', inc);
if (!inc.includes('FT-B20')) throw new Error('Pflichtfrage wirkt nicht');

// 8) Nicht zutreffendes Merkmal: keine Wagen -> FT-B22 NOT_APPLICABLE
const wagen = evaluate(seed as any, fill({ qa_teil_instandhaltung: false, qa_wagen: 'keine' }, 'gut'),
  ).find(r => r.hazard === 'FT-B22');
if (wagen?.status !== 'NOT_APPLICABLE') throw new Error('Wagen-Filter greift nicht: ' + wagen?.status);

console.log('\nAlle Smoke-Tests bestanden.');
