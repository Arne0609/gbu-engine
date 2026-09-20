// Prioritätsinversionen im MF-Katalog suchen.
//
//   node --experimental-strip-types mf_inversionen.ts [norm_81_20_mf.json]
//
// Bei der Aggregation NONE gewinnt die zutreffende Regel mit der HÖCHSTEN
// PRIORITÄT. Wenn dabei eine Regel mit NIEDRIGERER Stufe eine zutreffende Regel
// mit HÖHERER Stufe verdrängt, ist das entweder eine gewollte Kompensation oder
// ein Fehler (so war es in CY-C12, Prüfbericht 20.09.2026 B04). Dieses Skript
// findet jede solche Stelle durch Ausprobieren aller Antwortkombinationen je
// Gefährdung und meldet sie zur fachlichen Entscheidung – es entscheidet nicht
// selbst.
import { readFileSync } from 'node:fs';
import { evaluate } from './evaluator.ts';

const datei = process.argv[2] ?? './norm_81_20_mf.json';
const seed: any = JSON.parse(readFileSync(datei, 'utf-8'));
const GRENZE = 20000;
const RANG: Record<string, number> = { NO_RISK: 0, LOW: 1, MEDIUM: 2, HIGH: 3 };

const Q: Record<string, any> = Object.fromEntries(seed.questions.map((q: any) => [q.code, q]));
const R: Record<string, any> = Object.fromEntries(seed.rules.map((r: any) => [r.code, r]));

function blaetter(e: any, out: any[] = []): any[] {
  if (!e) return out;
  if (e.all) e.all.forEach((x: any) => blaetter(x, out));
  else if (e.any) e.any.forEach((x: any) => blaetter(x, out));
  else if (e.not) blaetter(e.not, out);
  else out.push(e);
  return out;
}

const grenzen = new Map<string, Set<number>>();
for (const r of seed.rules) {
  for (const lf of [...blaetter(r.condition), ...blaetter(r.applicability)]) {
    if (typeof lf.value === 'number') {
      if (!grenzen.has(lf.question)) grenzen.set(lf.question, new Set());
      grenzen.get(lf.question)!.add(lf.value);
    }
  }
}

function werte(code: string): any[] {
  const q = Q[code];
  if (!q) return [undefined];
  if (q.type === 'YES_NO') return [true, false, undefined];
  if (q.type === 'SELECT') return [...q.options.map((o: any) => o.value), undefined];
  const zahlen = new Set<number>();
  for (const x of grenzen.get(code) ?? []) { zahlen.add(x - 1); zahlen.add(x); zahlen.add(x + 1); }
  if (!zahlen.size) zahlen.add(q.min ?? 0);
  return [...zahlen, undefined];
}

type Fall = { hazard: string; sieger: string; verdraengt: string; beispiel: string };
const funde = new Map<string, Fall>();
let gepruefte = 0;

for (const h of seed.hazards) {
  if (h.aggregation_type !== 'NONE') continue;   // nur dort verdrängt Priorität
  const regeln = seed.rules.filter((r: any) => r.hazard === h.code);
  if (regeln.length < 2) continue;

  const codes = new Set<string>(h.questions.map((x: any) => x.question));
  const todo = [...codes];
  for (const r of regeln) {
    for (const lf of [...blaetter(r.condition), ...blaetter(r.applicability)]) {
      if (!codes.has(lf.question)) { codes.add(lf.question); todo.push(lf.question); }
    }
  }
  while (todo.length) {
    const c = todo.pop()!;
    for (const lf of blaetter(Q[c]?.visible_when)) {
      if (!codes.has(lf.question)) { codes.add(lf.question); todo.push(lf.question); }
    }
  }

  const liste = [...codes];
  const optionen = liste.map(werte);
  let gesamt = 1;
  for (const o of optionen) gesamt *= o.length;
  const schritt = gesamt > GRENZE ? Math.ceil(gesamt / GRENZE) : 1;

  for (let i = 0; i < gesamt; i += schritt) {
    const antworten: Record<string, any> = {};
    let rest = i;
    for (let j = 0; j < liste.length; j++) {
      const o = optionen[j];
      const v = o[rest % o.length];
      rest = Math.floor(rest / o.length);
      if (v !== undefined) antworten[liste[j]] = v;
    }
    gepruefte++;
    const res: any = evaluate(seed, antworten).find((x: any) => x.hazard === h.code);
    if (!res || !res.matched_rule) continue;
    const sieger = R[res.matched_rule];
    // Bei NONE stehen die verdraengten Befundregeln in overridden_rules –
    // matched_rules enthaelt dort nur den Gewinner.
    for (const code of [...(res.overridden_rules ?? []), ...(res.matched_rules ?? [])]) {
      const andere = R[code];
      if (!andere || code === sieger.code) continue;
      if (RANG[andere.result] > RANG[sieger.result]) {
        const key = `${sieger.code}>${code}`;
        if (!funde.has(key)) {
          funde.set(key, {
            hazard: h.code, sieger: sieger.code, verdraengt: code,
            beispiel: JSON.stringify(antworten),
          });
        }
      }
    }
  }
}

for (const f of [...funde.values()].sort((a, b) => a.hazard.localeCompare(b.hazard))) {
  const s = R[f.sieger], v = R[f.verdraengt];
  console.log(`${f.hazard}: ${f.sieger} (P${s.priority}, ${s.result}) verdrängt `
    + `${f.verdraengt} (P${v.priority}, ${v.result})`);
  console.log(`   Beispiel: ${f.beispiel}`);
  if (s.notes) console.log(`   Hinweis Sieger: ${s.notes}`);
}
console.log(`\n${gepruefte} Kombinationen geprüft, ${funde.size} Stellen, an denen bei `
  + `NONE eine niedrigere Stufe eine höhere verdrängt.`);
