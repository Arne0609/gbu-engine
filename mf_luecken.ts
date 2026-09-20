// Kombinationsprüfung des MF-Katalogs: Gibt es zu einer Gefährdung eine
// Antwortkombination, die von KEINER Regel getroffen wird (rule_gap)?
//
//   node --experimental-strip-types mf_luecken.ts [norm_81_20_mf.json]
//
// Vorbild: die Lückensuche in cy_smoke.ts, hier über alle Gefährdungen. Je
// Gefährdung werden nur ihre EIGENEN Fragen variiert (Ja/Nein, alle Optionen,
// Zahlen an den Regelgrenzen ±1). Fragen aus Sichtbarkeits- und
// Anwendbarkeitsbedingungen kommen hinzu, damit die Gefährdung überhaupt
// anwendbar und die Frage sichtbar ist. Über GRENZE hinaus wird gleichmäßig
// ausgedünnt; die Datei meldet, wo das passiert ist – kein stilles Kürzen.
import { readFileSync } from 'node:fs';
import { evaluate } from './evaluator.ts';

const datei = process.argv[2] ?? './norm_81_20_mf.json';
const seed: any = JSON.parse(readFileSync(datei, 'utf-8'));
const GRENZE = 20000;

const Q: Record<string, any> = Object.fromEntries(seed.questions.map((q: any) => [q.code, q]));

function blaetter(e: any, out: any[] = []): any[] {
  if (!e) return out;
  if (e.all) e.all.forEach((x: any) => blaetter(x, out));
  else if (e.any) e.any.forEach((x: any) => blaetter(x, out));
  else if (e.not) blaetter(e.not, out);
  else out.push(e);
  return out;
}

// Werte, die eine Frage annehmen kann – begrenzt auf das, was Regeln unterscheiden.
function werte(code: string, grenzen: Map<string, Set<number>>): any[] {
  const q = Q[code];
  if (!q) return [undefined];
  if (q.type === 'YES_NO') return [true, false, undefined];
  if (q.type === 'SELECT') return [...q.options.map((o: any) => o.value), undefined];
  const g = [...(grenzen.get(code) ?? new Set<number>())].sort((a, b) => a - b);
  const zahlen = new Set<number>();
  for (const x of g) { zahlen.add(x - 1); zahlen.add(x); zahlen.add(x + 1); }
  if (!zahlen.size) zahlen.add(q.min ?? 0);
  return [...zahlen, undefined];
}

// Zahlgrenzen je Frage aus allen Regelbedingungen sammeln.
const grenzen = new Map<string, Set<number>>();
for (const r of seed.rules) {
  for (const lf of [...blaetter(r.condition), ...blaetter(r.applicability)]) {
    if (typeof lf.value === 'number') {
      if (!grenzen.has(lf.question)) grenzen.set(lf.question, new Set());
      grenzen.get(lf.question)!.add(lf.value);
    }
  }
}
for (const q of seed.questions) {
  for (const lf of blaetter(q.visible_when)) {
    if (typeof lf.value === 'number') {
      if (!grenzen.has(lf.question)) grenzen.set(lf.question, new Set());
      grenzen.get(lf.question)!.add(lf.value);
    }
  }
}

let luecken = 0, gepruefte = 0, ausgeduennt = 0;
const bericht: string[] = [];

for (const h of seed.hazards) {
  const regeln = seed.rules.filter((r: any) => r.hazard === h.code);
  if (!regeln.length) continue;

  // Beteiligte Fragen: die der Gefährdung, dazu alles aus Regel-, Pflicht-,
  // Anwendbarkeits- und Sichtbarkeitsbedingungen (transitiv).
  const codes = new Set<string>(h.questions.map((x: any) => x.question));
  const todo = [...codes];
  for (const r of regeln) {
    for (const lf of [...blaetter(r.condition), ...blaetter(r.applicability)]) {
      if (!codes.has(lf.question)) { codes.add(lf.question); todo.push(lf.question); }
    }
  }
  for (const x of h.questions) {
    for (const lf of [...blaetter(x.required_when), ...blaetter(x.applicable_when)]) {
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
  const optionen = liste.map(c => werte(c, grenzen));
  let gesamt = 1;
  for (const o of optionen) gesamt *= o.length;

  // Gleichmäßig ausdünnen, wenn zu groß: jede n-te Kombination.
  const schritt = gesamt > GRENZE ? Math.ceil(gesamt / GRENZE) : 1;
  if (schritt > 1) { ausgeduennt++; bericht.push(`Hinweis: ${h.code} ausgedünnt – ${gesamt} mögliche Kombinationen, jede ${schritt}. geprüft.`); }

  const beispiele: string[] = [];
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
    const res = evaluate(seed, antworten).find((x: any) => x.hazard === h.code);
    if (res && (res as any).ruleGap) {
      luecken++;
      if (beispiele.length < 3) {
        beispiele.push(JSON.stringify(Object.fromEntries(
          Object.entries(antworten).filter(([c]) => codes.has(c)))));
      }
    }
  }
  if (beispiele.length) {
    bericht.push(`LÜCKE  ${h.code} – ${h.title}`);
    for (const b of beispiele) bericht.push(`         ${b}`);
  }
}

console.log(bericht.join('\n'));
console.log(`\n${gepruefte} Kombinationen geprüft, ${luecken} Regellücken, `
  + `${ausgeduennt} Gefährdungen ausgedünnt (Grenze ${GRENZE} je Gefährdung).`);
process.exit(luecken ? 1 : 0);
