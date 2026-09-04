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
