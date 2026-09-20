// Tote Regeln im MF-Katalog suchen: Regeln, die in KEINER Antwortkombination
// ihrer Gefährdung zutreffen (Bedingung unerfüllbar oder von der Anwendbarkeit
// ausgeschlossen) – und Regeln, die zwar zutreffen, aber NIE gewinnen, weil
// eine andere sie immer verdrängt.
//
//   node --experimental-strip-types mf_tote_regeln.ts [norm_81_20_mf.json]
//
// Eine nie zutreffende Regel ist ein Defekt. Eine nie gewinnende Regel ist
// meist gewollt (Grundstufe unter einer Kompensation), aber jede Stelle gehört
// angesehen – deshalb werden beide getrennt gemeldet.
import { readFileSync } from 'node:fs';
import { evaluate, evalExpression } from './evaluator.ts';

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

const nieGewonnen = new Set<string>(seed.rules.map((r: any) => r.code));
const nieBeteiligt = new Set<string>(seed.rules.map((r: any) => r.code));
const ausgeduennt: string[] = [];

for (const h of seed.hazards) {
  const regeln = seed.rules.filter((r: any) => r.hazard === h.code);
  if (!regeln.length) continue;

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
  const optionen = liste.map(werte);
  let gesamt = 1;
  for (const o of optionen) gesamt *= o.length;
  const schritt = gesamt > GRENZE ? Math.ceil(gesamt / GRENZE) : 1;
  if (schritt > 1) ausgeduennt.push(`${h.code} (jede ${schritt}. von ${gesamt})`);

  for (let i = 0; i < gesamt; i += schritt) {
    const antworten: Record<string, any> = {};
    let rest = i;
    for (let j = 0; j < liste.length; j++) {
      const o = optionen[j];
      const v = o[rest % o.length];
      rest = Math.floor(rest / o.length);
      if (v !== undefined) antworten[liste[j]] = v;
    }
    // „Zutreffend" direkt an der Bedingung messen, nicht am Gewinner: eine
    // verdraengte Kein-Risiko-Regel taucht in overridden_rules nicht auf
    // (dort stehen nur Befundregeln) und sähe sonst tot aus.
    for (const r of regeln) {
      if (!nieBeteiligt.has(r.code)) continue;
      if (r.applicability && !evalExpression(r.applicability, antworten as any)) continue;
      if (evalExpression(r.condition, antworten as any)) nieBeteiligt.delete(r.code);
    }
    const res: any = evaluate(seed, antworten).find((x: any) => x.hazard === h.code);
    if (res?.matched_rule) nieGewonnen.delete(res.matched_rule);
  }
}

const R: Record<string, any> = Object.fromEntries(seed.rules.map((r: any) => [r.code, r]));
const tot = [...nieBeteiligt].sort();
const stumm = [...nieGewonnen].filter(c => !nieBeteiligt.has(c)).sort();
// Ausgeduennte Gefaehrdungen koennen falsche Treffer liefern – ausdruecklich benennen.
const unsicher = new Set(ausgeduennt.map(a => a.split(' ')[0]));

console.log('NIE ZUTREFFEND (Defekt – Bedingung unerfüllbar oder Anwendbarkeit schließt aus):');
console.log(tot.length ? tot.map(c => `  ${c}  ${R[c].result}  ${R[c].hazard}`
  + (unsicher.has(R[c].hazard) ? '   (Gefährdung ausgedünnt – von Hand nachprüfen)' : '')).join('\n') : '  keine');
console.log('\nZUTREFFEND, ABER NIE MASSGEBLICH (immer verdrängt – meist gewollte Grundstufe):');
console.log(stumm.length ? stumm.map(c => `  ${c}  P${R[c].priority}  ${R[c].result}  ${R[c].hazard}`
  + (unsicher.has(R[c].hazard) ? '   (Gefährdung ausgedünnt – von Hand nachprüfen)' : '')).join('\n') : '  keine');
if (ausgeduennt.length) console.log('\nAusgedünnt: ' + ausgeduennt.join(', '));
