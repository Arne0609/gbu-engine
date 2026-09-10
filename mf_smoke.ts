// Smoke-Test der Ergänzungen im MF-Katalog gegen den Referenz-Evaluator.
//   node --experimental-strip-types mf_smoke.ts
// Deckt den Lückenschluss EN 81-80 vom 04.09.2026 ab (MF-T07/T08/T09,
// MF-K15, MF-M21) einschließlich Fail-closed-Verhalten bei fehlenden
// Pflichtantworten.
import { readFileSync } from 'node:fs';
import { evaluate } from './evaluator.ts';

const seed = JSON.parse(readFileSync('./norm_81_20_mf.json', 'utf-8'));
let fehler = 0;

function status(answers: Record<string, unknown>, hazard: string): string {
  const r = evaluate(seed as any, answers as any).find((x: any) => x.hazard === hazard);
  if (!r) throw new Error('Gefährdung fehlt: ' + hazard);
  if ((r as any).ruleGap) return 'RULE_GAP';
  return r.status;
}

function pruefe(name: string, hazard: string, answers: Record<string, unknown>, erwartet: string) {
  const ist = status(answers, hazard);
  if (ist !== erwartet) {
    console.error(`FEHLER  ${name}: ${hazard} = ${ist}, erwartet ${erwartet}`);
    fehler++;
  } else {
    console.log(`ok      ${name.padEnd(46)} ${hazard} = ${ist}`);
  }
}

// ---- Nr. 9 – Fläche unterhalb der Schachttürschwelle (EN 81-20 5.2.5.3.2) ----
pruefe('Fläche fehlt', 'MF-T07', { qt_flaeche_unter_schwelle: 'keine' }, 'HIGH');
pruefe('Fläche mit Mängeln', 'MF-T07', { qt_flaeche_unter_schwelle: 'maengel' }, 'MEDIUM');
pruefe('Fläche normgerecht', 'MF-T07', { qt_flaeche_unter_schwelle: 'normgerecht' }, 'NO_RISK');
pruefe('Fläche unbeantwortet', 'MF-T07', {}, 'INCOMPLETE');

// ---- Nr. 26 – Rückhaltung der Türblätter (EN 81-20 5.3.5.3.2) ---------------
pruefe('ohne Rückhaltung', 'MF-T08',
  { qt_rueckhaltung_tuerblatt: false, qt_fuehrung_tuerblatt_ok: true }, 'MEDIUM');
pruefe('ohne Rückhaltung + Führung schadhaft', 'MF-T08',
  { qt_rueckhaltung_tuerblatt: false, qt_fuehrung_tuerblatt_ok: false }, 'HIGH');
pruefe('Führung schadhaft', 'MF-T08',
  { qt_rueckhaltung_tuerblatt: true, qt_fuehrung_tuerblatt_ok: false }, 'MEDIUM');
pruefe('Rückhaltung vorhanden', 'MF-T08',
  { qt_rueckhaltung_tuerblatt: true, qt_fuehrung_tuerblatt_ok: true }, 'NO_RISK');

// ---- Nr. 35 – Verbindung mehrteiliger Türblätter (EN 81-20 5.3.11) ----------
pruefe('einteilige Tür', 'MF-T09', { qt_tuer_mehrteilig: false }, 'NOT_APPLICABLE');
pruefe('Türblätter unverbunden', 'MF-T09',
  { qt_tuer_mehrteilig: true, qt_tuerblatt_verbindung: 'keine' }, 'HIGH');
pruefe('mittelbar ohne Überwachung', 'MF-T09',
  { qt_tuer_mehrteilig: true, qt_tuerblatt_verbindung: 'mittelbar_ohne_ueberwachung' }, 'HIGH');
pruefe('mittelbar überwacht', 'MF-T09',
  { qt_tuer_mehrteilig: true, qt_tuerblatt_verbindung: 'mittelbar_ueberwacht' }, 'NO_RISK');
pruefe('unmittelbar verbunden', 'MF-T09',
  { qt_tuer_mehrteilig: true, qt_tuerblatt_verbindung: 'direkt' }, 'NO_RISK');
pruefe('mehrteilig, Verbindung offen', 'MF-T09', { qt_tuer_mehrteilig: true }, 'INCOMPLETE');

// ---- Nr. 45 – Fahrkorbbeleuchtung (EN 81-20 5.4.10.1 bis .3) ----------------
const licht = { qk_beleuchtung: 'normgerecht', qk_bel_zwei_lampen: true, qk_bel_staendig: true };
pruefe('Beleuchtung normgerecht (100 lx)', 'MF-K15', licht, 'NO_RISK');
pruefe('keine Fahrkorbbeleuchtung', 'MF-K15', { ...licht, qk_beleuchtung: 'keine' }, 'MEDIUM');
pruefe('unter 100 lx', 'MF-K15', { ...licht, qk_beleuchtung: 'gemindert' }, 'LOW');
pruefe('nur eine Lampe', 'MF-K15', { ...licht, qk_bel_zwei_lampen: false }, 'LOW');
pruefe('nicht ständig beleuchtet', 'MF-K15', { ...licht, qk_bel_staendig: false }, 'LOW');
const ohneLampenfrage: any = { ...licht };
delete ohneLampenfrage.qk_bel_zwei_lampen;
pruefe('Modifier unbeantwortet', 'MF-K15', ohneLampenfrage, 'INCOMPLETE');

// ---- Nr. 57 – Notendschalter (EN 81-20 5.12.2) ------------------------------
const nes = {
  qm_notendschalter: 'geprueft',
  qm_notendschalter_getrennt: true,
  qm_notendschalter_verbindung_ueberwacht: true,
};
pruefe('Notendschalter geprüft', 'MF-M21', nes, 'NO_RISK');
pruefe('Notendschalter fehlt', 'MF-M21', { qm_notendschalter: 'fehlt' }, 'HIGH');
pruefe('Verbindung unüberwacht', 'MF-M21',
  { ...nes, qm_notendschalter_verbindung_ueberwacht: false }, 'HIGH');
pruefe('Betätigung nicht getrennt', 'MF-M21',
  { ...nes, qm_notendschalter_getrennt: false }, 'MEDIUM');
pruefe('Wirksamkeit nicht nachgewiesen', 'MF-M21',
  { ...nes, qm_notendschalter: 'ungeprueft' }, 'MEDIUM');
pruefe('Notendschalter unbeantwortet', 'MF-M21', {}, 'INCOMPLETE');

// ---- MF-D06 – Baujahr gegen Ausstattung (Konformitätsmangel) ---------------
// Erkenntnis aus GBU 3.0: Baujahr ist ein Steuerfeld. Bei uns blendet es nichts
// aus, sondern ordnet ein – deshalb wird hier geprüft, dass dieselbe fehlende
// Einrichtung je nach Baujahr unterschiedlich streng bewertet wird.
const konform = {
  qa_baujahr: 2020,
  qa_norm_inverkehrbringen: 'en81_20',
  qa_ucm_a3: true,
  qa_fahrkorbtuer: true,
};
pruefe('Neuanlage vollständig', 'MF-D06', konform, 'NO_RISK');
pruefe('Neuanlage ohne Fahrkorbtür', 'MF-D06',
  { ...konform, qa_fahrkorbtuer: false }, 'HIGH');
pruefe('Neuanlage ohne UCM', 'MF-D06', { ...konform, qa_ucm_a3: false }, 'HIGH');
// Dieselbe fehlende Fahrkorbtür an einer Altanlage: kein Konformitätsmangel,
// sondern ein Nachrüstfall – hier also KEIN Befund (bewertet wird sie über die
// Türgefährdungen).
pruefe('Altanlage ohne Fahrkorbtür ist kein Konformitätsmangel', 'MF-D06',
  { qa_baujahr: 1975, qa_norm_inverkehrbringen: 'tra', qa_ucm_a3: false,
    qa_fahrkorbtuer: false }, 'NO_RISK');
// Zwischen 1999 und 2012: Fahrkorbtür gefordert, UCM noch nicht.
pruefe('Anlage von 2005 ohne Fahrkorbtür', 'MF-D06',
  { qa_baujahr: 2005, qa_norm_inverkehrbringen: 'en81_1_2', qa_ucm_a3: false,
    qa_fahrkorbtuer: false }, 'MEDIUM');
pruefe('Anlage von 2005 ohne UCM ist in Ordnung', 'MF-D06',
  { qa_baujahr: 2005, qa_norm_inverkehrbringen: 'en81_1_2', qa_ucm_a3: false,
    qa_fahrkorbtuer: true }, 'NO_RISK');
// Widersprüchliche Angaben.
pruefe('Baujahr 2020, Regelwerk TRA', 'MF-D06',
  { ...konform, qa_norm_inverkehrbringen: 'tra' }, 'MEDIUM');
pruefe('Baujahr 1985, Regelwerk EN 81-20 (Modernisierung)', 'MF-D06',
  { qa_baujahr: 1985, qa_norm_inverkehrbringen: 'en81_20', qa_ucm_a3: true,
    qa_fahrkorbtuer: true }, 'LOW');
pruefe('Baujahr unbeantwortet', 'MF-D06',
  { qa_norm_inverkehrbringen: 'en81_20', qa_ucm_a3: true, qa_fahrkorbtuer: true },
  'INCOMPLETE');

// ---- Begründete Annahmen aus dem Baujahr (07.09.2026) ----------------------
// Merkmale, die zum Baujahr vorgeschrieben waren, wurden vor der Inbetrieb-
// nahme durch eine ZÜS abgenommen. Sie werden nicht erneut erhoben, sondern
// angenommen – widerlegbar, und ohne dass eine Gefährdung verschwindet.
const bj2020 = { qa_baujahr: 2020, qa_norm_inverkehrbringen: 'en81_20',
                 qa_fahrkorbtuer: true };

// 1. Die Annahme greift: UCM unbeantwortet, Baujahr 2020 -> gilt als vorhanden.
pruefe('UCM wird ab 2012 angenommen', 'MF-D06', bj2020, 'NO_RISK');

// 2. Die Erhebung schlägt die Annahme: ausdrückliches Nein bleibt ein Befund.
pruefe('erhobenes Nein schlägt die Annahme', 'MF-D06',
  { ...bj2020, qa_ucm_a3: false }, 'HIGH');

// 3. Widerlegbar: ohne Abnahmeunterlagen greift keine Annahme.
pruefe('ohne Abnahmeunterlagen keine Annahme', 'MF-D06',
  { ...bj2020, qd_konformitaet_geprueft: false }, 'INCOMPLETE');

// 4. Ohne Baujahr keine Annahme (fail-closed wie bisher).
pruefe('ohne Baujahr keine Annahme', 'MF-D06',
  { qa_norm_inverkehrbringen: 'en81_20', qa_fahrkorbtuer: true }, 'INCOMPLETE');

// 5. Altanlage: die Schwellen liegen ab 1999, hier greift nichts.
pruefe('Altanlage bekommt keine Annahme', 'MF-D06',
  { qa_baujahr: 1990, qa_norm_inverkehrbringen: 'tra', qa_fahrkorbtuer: true },
  'INCOMPLETE');

function pruefeWahr(name: string, bedingung: boolean, zusatz = '') {
  if (bedingung) {
    console.log(`ok      ${name}`);
  } else {
    console.error(`FEHLER  ${name}${zusatz ? ': ' + zusatz : ''}`);
    fehler++;
  }
}

// 6. Das Ergebnis weist aus, worauf es beruht.
const d06 = evaluate(seed as any, bj2020 as any)
  .find((x: any) => x.hazard === 'MF-D06') as any;
pruefeWahr('Befund nennt die angenommene Frage',
  Array.isArray(d06.assumed) && d06.assumed.includes('qa_ucm_a3'),
  JSON.stringify(d06.assumed));

// 7. Annahmen ersetzen keine Erhebung: Mit Baujahr allein bleibt der weit
//    überwiegende Teil des Katalogs unbewertet – Zustands- und
//    Organisationsfragen sind bewusst nicht angenommen.
const nurBaujahr = evaluate(seed as any, { qa_baujahr: 2020 } as any);
const offenTrotzAnnahme = nurBaujahr.filter((r: any) => r.status === 'INCOMPLETE').length;
pruefeWahr('Baujahr allein bewertet den Katalog nicht',
  offenTrotzAnnahme > nurBaujahr.length / 2,
  `${offenTrotzAnnahme} von ${nurBaujahr.length} offen`);

// 8. Keine Annahme darf eine Frage betreffen, die den Katalogumfang steuert.
const appQ = new Set<string>();
for (const h of (seed.hazards ?? [])) {
  for (const q of (h.questions ?? [])) {
    if (q.role === 'APPLICABILITY') appQ.add(q.question);
  }
}
const verboten = (seed.assumptions ?? [])
  .map((a: any) => a.question).filter((q: string) => appQ.has(q));
pruefeWahr('keine Annahme auf einer APPLICABILITY-Frage',
  verboten.length === 0, verboten.join(', '));

// ---- Regellücken über alle Gefährdungen ------------------------------------
const leer = evaluate(seed as any, {} as any);
const gaps = leer.filter((r: any) => r.ruleGap);
if (gaps.length) {
  console.error('FEHLER  Regellücken bei leerem Fragebogen: ' + gaps.map((r: any) => r.hazard).join(', '));
  fehler++;
} else {
  console.log('ok      keine Regellücke bei leerem Fragebogen');
}

console.log(fehler === 0 ? '\nAlle Smoke-Tests bestanden.' : `\n${fehler} Fehler.`);
process.exit(fehler === 0 ? 0 : 1);
