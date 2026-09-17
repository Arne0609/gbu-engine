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

// ---- Korrekturen aus dem externen Prüfbericht (15.09.2026) ----------------
const GLAS = { qa_glas_schachttueren: true, qa_glas_fahrkorbtueren: false,
  qt_glas_beschaedigt: false, qt_glas_schiebetuer: true, qt_glas_einzugsschutz: true };
pruefe('B06 intaktes Drahtglas = Niedrig', 'MF-T04',
  { ...GLAS, qt_glas_normgerecht: false, qt_glas_drahtglas: true }, 'LOW');
pruefe('B06 anderes Nicht-VSG = Hoch', 'MF-T04',
  { ...GLAS, qt_glas_normgerecht: false, qt_glas_drahtglas: false }, 'HIGH');
pruefe('B06 beschädigtes Glas = Hoch', 'MF-T04',
  { ...GLAS, qt_glas_normgerecht: true, qt_glas_drahtglas: false, qt_glas_beschaedigt: true }, 'HIGH');
const OHNE_TUER = { qa_fahrkorbtuer: false, qt_lichtgitter_ohne_tuer: true, qt_scherengitter: false,
  qa_nutzung_pmem: false, qa_nutzung_kinder: false };
pruefe('B07 Lichtgitter im Personenaufzug = Hoch', 'MF-T06',
  { ...OHNE_TUER, qa_nutzungsart: 'personen', qt_nur_eingewiesene: false }, 'HIGH');
pruefe('B07 Lichtgitter, Personenaufzug, "eingewiesen"', 'MF-T06',
  { ...OHNE_TUER, qa_nutzungsart: 'personen', qt_nur_eingewiesene: true }, 'HIGH');
pruefe('B07 Lichtgitter, Lastenaufzug, eingewiesen = Mittel', 'MF-T06',
  { ...OHNE_TUER, qa_nutzungsart: 'lasten', qt_nur_eingewiesene: true }, 'MEDIUM');
pruefe('B07 Nutzungsart fehlt = unvollständig', 'MF-T06',
  { ...OHNE_TUER, qt_nur_eingewiesene: true }, 'INCOMPLETE');
const SBEL = { qs_bel_vorhanden: true, qs_bel_splitterschutz: true };
pruefe('B05 unter 50 lx, Altnorm erfüllt = Niedrig', 'MF-S01',
  { ...SBEL, qs_bel_ausreichend: false, qs_bel_altnorm: true }, 'LOW');
pruefe('B05 unter 50 lx, Altnorm nicht erfüllt = Mittel', 'MF-S01',
  { ...SBEL, qs_bel_ausreichend: false, qs_bel_altnorm: false }, 'MEDIUM');
pruefe('B05 Altnorm-Frage fehlt = unvollständig', 'MF-S01',
  { ...SBEL, qs_bel_ausreichend: false }, 'INCOMPLETE');
pruefe('H03 Grube: automatische Abschaltung = Kein Risiko', 'MF-G08',
  { qa_mehrere_aufzuege: true, qg_nachbar_abtrennung: false, qg_nachbar_abschaltung: true,
    qg_nachbar_abschaltung_geprueft: true }, 'NO_RISK');
pruefe('H03 Grube: weder Abtrennung noch Abschaltung = Hoch', 'MF-G08',
  { qa_mehrere_aufzuege: true, qg_nachbar_abtrennung: false, qg_nachbar_abschaltung: false }, 'HIGH');
pruefe('H03 Fahrkorbdach: automatische Abschaltung = Kein Risiko', 'MF-F03',
  { qa_mehrere_aufzuege: true, qf_nachbar_trennung: 'fehlt', qf_nachbar_abschaltung: true,
    qf_nachbar_abschaltung_geprueft: true }, 'NO_RISK');
pruefe('H03 Fahrkorbdach: ohne Abschaltung = Hoch', 'MF-F03',
  { qa_mehrere_aufzuege: true, qf_nachbar_trennung: 'fehlt', qf_nachbar_abschaltung: false }, 'HIGH');
pruefe('H15 reduzierter Schachtkopf ohne Kennzeichnung = Mittel', 'MF-F04',
  { qf_schutzraum: 'reduziert', qf_kopffreiheit_gekennz: false }, 'MEDIUM');
pruefe('H06 Asbestsituation unbekannt = Mittel', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: false, qs_asbest: false,
    qg_asbest: false, qu_asbest_unbekannt: true }, 'MEDIUM');
pruefe('H06 Asbest gefunden = Hoch', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: true, qs_asbest: false,
    qg_asbest: false, qu_asbest_unbekannt: true }, 'HIGH');

// ---- Zweite Prüfung (16.09.2026) --------------------------------------------
pruefe('Abschaltung ohne Funktionsnachweis = Mittel (Grube)', 'MF-G08',
  { qa_mehrere_aufzuege: true, qg_nachbar_abtrennung: false, qg_nachbar_abschaltung: true,
    qg_nachbar_abschaltung_geprueft: false }, 'MEDIUM');
pruefe('Abschaltung ohne Funktionsnachweis = Mittel (Dach)', 'MF-F03',
  { qa_mehrere_aufzuege: true, qf_nachbar_trennung: 'fehlt', qf_nachbar_abschaltung: true,
    qf_nachbar_abschaltung_geprueft: false }, 'MEDIUM');
pruefe('Scherengitter + Lichtgitter, Personenaufzug = Hoch', 'MF-T06',
  { qa_fahrkorbtuer: false, qt_lichtgitter_ohne_tuer: true, qt_scherengitter: true,
    qa_nutzung_pmem: false, qa_nutzung_kinder: false, qa_nutzungsart: 'personen',
    qt_nur_eingewiesene: false }, 'HIGH');
pruefe('Scherengitter, Lastenaufzug, eingewiesen = Mittel', 'MF-T06',
  { qa_fahrkorbtuer: false, qt_lichtgitter_ohne_tuer: false, qt_scherengitter: true,
    qa_nutzung_pmem: false, qa_nutzung_kinder: false, qa_nutzungsart: 'lasten',
    qt_nur_eingewiesene: true }, 'MEDIUM');
pruefe('Keine Schließkantensicherung + PmeM = Hoch', 'MF-T06',
  { qa_fahrkorbtuer: true, qt_schliesskante: 'keine', qa_nutzung_pmem: true, qa_nutzung_kinder: false }, 'HIGH');
pruefe('Einzel-Lichtschranke + PmeM = Hoch', 'MF-T06',
  { qa_fahrkorbtuer: true, qt_schliesskante: 'lichtschranke', qa_nutzung_pmem: true, qa_nutzung_kinder: false }, 'HIGH');
pruefe('Drehtür mit Drahtglas ohne Einzugsschutz = Niedrig', 'MF-T04',
  { qa_glas_schachttueren: true, qa_glas_fahrkorbtueren: false, qt_glas_normgerecht: false,
    qt_glas_drahtglas: true, qt_glas_beschaedigt: false, qt_glas_schiebetuer: false }, 'LOW');
pruefe('Separate Grubenzugangstür mit Kontakt, keine Leiter = Kein Risiko', 'MF-G04',
  { qg_zugangstuer: true, qg_zugangstuer_schalter: true }, 'NO_RISK');
pruefe('Zugang über Leiter, keine Leiter = Hoch', 'MF-G04',
  { qg_zugangstuer: false, qg_leiter: 'keine' }, 'HIGH');
pruefe('Beleuchteter Notruftaster allein = Niedrig', 'MF-K02', { qk_notbeleuchtung: 'nur_taster' }, 'LOW');
pruefe('Ex bewertet, nicht umgesetzt = Hoch', 'MF-U06',
  { qu_ex_moeglich: true, qu_ex_bewertet: true, qu_ex_umgesetzt: false }, 'HIGH');
pruefe('Ex bewertet und umgesetzt = Mittel', 'MF-U06',
  { qu_ex_moeglich: true, qu_ex_bewertet: true, qu_ex_umgesetzt: true }, 'MEDIUM');
pruefe('Schwelle > 150 mm, eine Verriegelung = Niedrig (TRBS)', 'MF-K05',
  { qk_abstand_schwelle_mm: true, qk_fk_tuer_verriegelt: true, qk_schachttuer_zusatzverriegelung: false,
    qa_nutzung_kinder: false }, 'LOW');
pruefe('Schwelle > 150 mm, keine Maßnahme = Mittel', 'MF-K05',
  { qk_abstand_schwelle_mm: true, qk_fk_tuer_verriegelt: false, qk_schachttuer_zusatzverriegelung: false,
    qa_nutzung_kinder: false }, 'MEDIUM');
pruefe('Schwelle > 150 mm, keine Maßnahme, Kinder = Hoch (eigener Standard)', 'MF-K05',
  { qk_abstand_schwelle_mm: true, qk_fk_tuer_verriegelt: false, qk_schachttuer_zusatzverriegelung: false,
    qa_nutzung_kinder: true }, 'HIGH');
pruefe('Barrierefreiheit gefordert, keine PmeM-Nutzung = bewertet', 'MF-K10',
  { qa_nutzung_pmem: false, qa_barrierefrei_gefordert: true, qk_en8170: true, qk_bedienelemente: true,
    qk_rollstuhl_mass: false }, 'HIGH');
pruefe('Barrierefreiheit weder gefordert noch genutzt = nicht anwendbar', 'MF-K10',
  { qa_nutzung_pmem: false, qa_barrierefrei_gefordert: false }, 'NOT_APPLICABLE');
pruefe('Indirekte Hydraulik: Betriebsbremse nicht anwendbar', 'MF-M08',
  { qa_aufzugsart: 'seil_hydraulik' }, 'NOT_APPLICABLE');
pruefe('Indirekte Hydraulik: Wellenlagerung nicht anwendbar', 'MF-K14',
  { qa_aufzugsart: 'seil_hydraulik' }, 'NOT_APPLICABLE');

// Monotonie MF-T06: Bei sonst gleicher Anlage darf eine schwächere
// Schließkantensicherung nie günstiger bewertet werden als eine stärkere.
const RANG: Record<string, number> = { NO_RISK: 0, LOW: 1, MEDIUM: 2, HIGH: 3 };
const staerke = ['lichtgitter', 'lichtschranke', 'keine'];
let monotonFehler = '';
for (const pmem of [true, false]) {
  for (const kinder of [true, false]) {
    let vorher = -1;
    for (const sk of staerke) {
      const st = status({ qa_fahrkorbtuer: true, qt_schliesskante: sk, qa_nutzung_pmem: pmem,
        qa_nutzung_kinder: kinder }, 'MF-T06');
      if (RANG[st] < vorher) monotonFehler += `${sk}/pmem=${pmem}/kinder=${kinder} `;
      vorher = RANG[st];
    }
  }
}
// ... und ohne Fahrkorbtür darf kein Ersatz die Stufe senken, solange die
// Voraussetzung (Lastenaufzug, nur Eingewiesene) fehlt.
for (const lg of [true, false]) for (const sg of [true, false]) {
  const st = status({ qa_fahrkorbtuer: false, qt_lichtgitter_ohne_tuer: lg, qt_scherengitter: sg,
    qa_nutzung_pmem: false, qa_nutzung_kinder: false, qa_nutzungsart: 'personen',
    qt_nur_eingewiesene: true }, 'MF-T06');
  if (st !== 'HIGH') monotonFehler += `ohne Tür lg=${lg} sg=${sg} -> ${st} `;
}
pruefeWahr('Monotonie MF-T06 (Schutz weg = nie günstiger)', monotonFehler === '', monotonFehler);

// Jede risikotragende Regel hat eine Sofort- und eine mittelfristige Maßnahme (H11).
const luecken = (seed.rules ?? []).filter((r: any) =>
  ['LOW', 'MEDIUM', 'HIGH'].includes(r.result) &&
  !(['sofort', 'mittel'].every((g) => (r.measures ?? []).some((m: any) => m.group_id === g))));
pruefeWahr('H11 jede Befundregel mit Sofort- und Folgemaßnahme',
  luecken.length === 0, luecken.map((r: any) => r.code).join(', '));

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
