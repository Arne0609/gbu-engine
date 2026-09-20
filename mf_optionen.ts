// Antwortwerte ohne Regel: Welche Antwort auf eine Befundfrage wird von KEINER
// Mangelregel ihrer Gefährdung ausgewertet und fällt damit auf die Auffangregel
// „Kein Risiko"?
//
//   node --experimental-strip-types mf_optionen.ts [norm_81_20_mf.json]
//
// Hintergrund (Regelprüfung 20.09.2026): Die maschinell erzeugten Auffangregeln
// („Ankerfrage ist beantwortet -> Kein Risiko") setzen die Lückenerkennung der
// Engine außer Kraft – rule_gap meldet nur, wenn GAR KEINE Regel trifft. Eine
// neue Option oder eine geänderte Bedingung erscheint deshalb nicht als Fehler,
// sondern als grünes Ergebnis. mf_luecken.ts kann das nicht finden; dieser Test
// schon, weil er nicht das Ergebnis, sondern die Abdeckung der Antwortwerte
// prüft.
//
// Gemeldet wird jeder Wert einer Befund-, Kompensations- oder Modifikatorfrage,
// der in keiner Bedingung einer Regel der Gefährdung vorkommt. Nicht jeder
// Treffer ist ein Fehler: Der unauffällige Wert („Ja" bei „Verriegelung
// vorhanden?") gehört dort hin, weil ihn die Auffangregel bewertet. Zu prüfen
// sind die Werte, die einen MANGEL beschreiben.
import { readFileSync } from 'node:fs';

const datei = process.argv[2] ?? './norm_81_20_mf.json';
const seed: any = JSON.parse(readFileSync(datei, 'utf-8'));
const Q: Record<string, any> = Object.fromEntries(seed.questions.map((q: any) => [q.code, q]));

function blaetter(e: any, out: any[] = []): any[] {
  if (!e) return out;
  if (e.all) e.all.forEach((x: any) => blaetter(x, out));
  else if (e.any) e.any.forEach((x: any) => blaetter(x, out));
  else if (e.not) blaetter(e.not, out);
  else out.push(e);
  return out;
}

let treffer = 0;
const zeilen: string[] = [];

for (const h of seed.hazards) {
  const regeln = seed.rules.filter((r: any) => r.hazard === h.code);
  const auffang = regeln.filter((r: any) => r.result === 'NO_RISK' && r.priority === 1
    && r.condition?.operator === 'ANSWERED');
  if (!auffang.length) continue;          // ohne Auffangregel meldet die Engine rule_gap

  // Welche Werte prüft überhaupt eine Regel dieser Gefährdung?
  const geprueft = new Map<string, Set<string>>();
  for (const r of regeln) {
    if (r.result === 'NO_RISK' && r.priority === 1) continue;   // Auffangregel zählt nicht
    for (const lf of [...blaetter(r.condition), ...blaetter(r.applicability)]) {
      if (!geprueft.has(lf.question)) geprueft.set(lf.question, new Set());
      const s = geprueft.get(lf.question)!;
      if (Array.isArray(lf.value)) lf.value.forEach((v: any) => s.add(String(v)));
      else if (lf.value !== undefined) s.add(String(lf.value));
      else s.add('*');   // ANSWERED o. ä. – deckt alles ab
    }
  }

  for (const x of h.questions) {
    if (x.role === 'APPLICABILITY' || x.role === 'DOCUMENTATION') continue;
    const q = Q[x.question];
    if (!q || q.type === 'NUMBER') continue;
    const s = geprueft.get(x.question);
    if (s?.has('*')) continue;
    const alle = q.type === 'YES_NO' ? ['true', 'false']
      : q.options.map((o: any) => String(o.value));
    const offen = alle.filter(v => !s?.has(v));
    if (!offen.length) continue;
    // Genau EIN unabgedeckter Wert je Frage ist der Normalfall: der
    // unauffällige. Ihn bewertet die Auffangregel, das ist gewollt. Gemeldet
    // wird deshalb nur, was darüber hinausgeht – bei Ja/Nein also nur, wenn
    // BEIDE Werte ohne Regel sind (Frage ohne Wirkung), bei Auswahlfragen die
    // Optionen ab der zweiten. Ist ein best_case hinterlegt, entscheidet der.
    const gut = q.best_case !== undefined ? String(q.best_case)
      : (offen.length === 1 ? offen[0] : null);
    const verdaechtig = offen.filter(v => v !== gut);
    if (!verdaechtig.length) continue;
    treffer += verdaechtig.length;
    const label = (v: string) => {
      if (q.type === 'YES_NO') return v === 'true' ? 'Ja' : 'Nein';
      const o = q.options.find((o: any) => String(o.value) === v);
      return o ? `„${o.label}"` : v;
    };
    zeilen.push(`${h.code}  ${q.ui_number ?? x.question} (${x.question}, ${x.role})`);
    zeilen.push(`   ohne Regel: ${verdaechtig.map(label).join(' | ')}`
      + (gut ? `   [unauffällig laut best_case: ${label(gut)}]` : '   [kein best_case hinterlegt]'));
  }
}

console.log(zeilen.join('\n'));
console.log(`\n${treffer} Antwortwerte, die von keiner Mangelregel ihrer Gefährdung `
  + `ausgewertet werden und auf die Auffangregel „Kein Risiko" fallen.`);
