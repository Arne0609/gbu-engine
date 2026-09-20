// Smoke-Test der Ergänzungen im MF-Katalog gegen den Referenz-Evaluator.
//   node --experimental-strip-types mf_smoke.ts
// Deckt den Lückenschluss EN 81-80 vom 04.09.2026 ab (MF-T07/T08/T09,
// MF-K15, MF-M21) einschließlich Fail-closed-Verhalten bei fehlenden
// Pflichtantworten.
import { readFileSync } from 'node:fs';
import { evaluate, applyAssumptions } from './evaluator.ts';

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
// Prüfbericht 20.09.2026: 1.29 ist ab Baujahr 1999 Pflicht – das Baujahr trägt nur
// dann eine Konformitätsvermutung, wenn die Unterlagen vorliegen.
const konform = {
  qa_baujahr: 2020,
  qa_norm_inverkehrbringen: 'en81_20',
  qa_ucm_a3: true,
  qa_fahrkorbtuer: true,
  qd_konformitaet_geprueft: true,
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
    qa_fahrkorbtuer: false, qd_konformitaet_geprueft: true }, 'MEDIUM');
pruefe('Anlage von 2005 ohne UCM ist in Ordnung', 'MF-D06',
  { qa_baujahr: 2005, qa_norm_inverkehrbringen: 'en81_1_2', qa_ucm_a3: false,
    qa_fahrkorbtuer: true, qd_konformitaet_geprueft: true }, 'NO_RISK');
// Widersprüchliche Angaben.
pruefe('Baujahr 2020, Regelwerk TRA', 'MF-D06',
  { ...konform, qa_norm_inverkehrbringen: 'tra' }, 'MEDIUM');
pruefe('Baujahr 1985, Regelwerk EN 81-20 (Modernisierung)', 'MF-D06',
  { qa_baujahr: 1985, qa_norm_inverkehrbringen: 'en81_20', qa_ucm_a3: true,
    qa_fahrkorbtuer: true }, 'LOW');
pruefe('Baujahr unbeantwortet', 'MF-D06',
  { qa_norm_inverkehrbringen: 'en81_20', qa_ucm_a3: true, qa_fahrkorbtuer: true },
  'INCOMPLETE');
// 1.29 fehlt an einer Anlage ab 1999 -> unvollständig (Prüfbericht 20.09.2026).
pruefe('Konformitätsnachweis fehlt ab 1999', 'MF-D06',
  { qa_baujahr: 2020, qa_norm_inverkehrbringen: 'en81_20', qa_ucm_a3: true,
    qa_fahrkorbtuer: true }, 'INCOMPLETE');

// ---- Begründete Annahmen aus dem Baujahr (07.09.2026) ----------------------
// Merkmale, die zum Baujahr vorgeschrieben waren, wurden vor der Inbetrieb-
// nahme durch eine ZÜS abgenommen. Sie werden nicht erneut erhoben, sondern
// angenommen – widerlegbar, und ohne dass eine Gefährdung verschwindet.
const bj2020 = { qa_baujahr: 2020, qa_norm_inverkehrbringen: 'en81_20',
                 qa_fahrkorbtuer: true, qd_konformitaet_geprueft: true };

// 1. Prüfbericht 20.09.2026 B07 (Entscheidung Arne): Der Nachweis ist das
//    ERRICHTUNGSREGELWERK (1.28), das Baujahr nur dessen Ableitung. Eine nach
//    EN 81-20 in Verkehr gebrachte Anlage mit Konformitätserklärung trägt die
//    Annahme – unabhängig vom Baujahr.
pruefe('UCM wird aus dem Errichtungsregelwerk angenommen', 'MF-D06', bj2020, 'NO_RISK');

// 1a. Dieselbe Anlage, aber als TRA-Anlage dokumentiert: Die Anforderung galt
//     nach diesem Regelwerk nie – die Jahreszahl allein trägt sie nicht.
pruefe('TRA-Regelwerk trägt die UCM-Annahme nicht trotz Baujahr 2020', 'MF-D06',
  { ...bj2020, qa_norm_inverkehrbringen: 'tra' }, 'INCOMPLETE');

// 1b. EN 81-1/2 umspannt die Schwelle 2012 – dort entscheidet das Baujahr.
pruefe('EN 81-1/2 vor 2012: keine UCM-Annahme', 'MF-D06',
  { ...bj2020, qa_baujahr: 2008, qa_norm_inverkehrbringen: 'en81_1_2' }, 'INCOMPLETE');
pruefe('EN 81-1/2 ab 2012: UCM-Annahme greift', 'MF-D06',
  { ...bj2020, qa_baujahr: 2014, qa_norm_inverkehrbringen: 'en81_1_2' }, 'NO_RISK');

// 1c. Ohne Angabe des Regelwerks bleibt das Baujahr die einzige Ableitung.
pruefe('unbekanntes Regelwerk: Baujahr entscheidet', 'MF-D06',
  { ...bj2020, qa_norm_inverkehrbringen: 'unbekannt' }, 'NO_RISK');

// 1d. Eine UNBEANTWORTETE Frage 1.28 trägt nichts (fail-closed).
pruefe('unbeantwortetes Regelwerk trägt keine Annahme', 'MF-D06',
  { qa_baujahr: 2020, qa_fahrkorbtuer: true, qd_konformitaet_geprueft: true },
  'INCOMPLETE');

// 1b. Mit erhobenem Ja ist die Gefährdung bewertet.
pruefe('UCM erhoben = Kein Risiko', 'MF-D06', { ...bj2020, qa_ucm_a3: true }, 'NO_RISK');

// 2. Die Erhebung schlägt die Annahme: ausdrückliches Nein bleibt ein Befund.
pruefe('erhobenes Nein schlägt die Annahme', 'MF-D06',
  { ...bj2020, qa_ucm_a3: false }, 'HIGH');

// 3. Widerlegbar: ohne Abnahmeunterlagen greift keine Annahme.
pruefe('ohne Abnahmeunterlagen keine Annahme', 'MF-D06',
  { ...bj2020, qd_konformitaet_geprueft: false }, 'INCOMPLETE');

// 3b. Prüfbericht 20.09.2026: Die Abschaltbedingung ist positiv formuliert – eine
//     UNBEANTWORTETE Frage 1.29 lässt keine Annahme mehr greifen (vorher fail-open).
pruefeWahr('unbeantwortete Konformitätsfrage schaltet Annahmen ab',
  applyAssumptions(seed as any, { qa_baujahr: 2020 } as any).applied.length === 0);
pruefeWahr('bestätigte Konformität lässt Annahmen greifen',
  applyAssumptions(seed as any,
    { qa_baujahr: 2020, qa_norm_inverkehrbringen: 'en81_20',
      qd_konformitaet_geprueft: true } as any).applied.length > 0);
// 3c. Prüfbericht 20.09.2026 B07: Ohne Angabe des Errichtungsregelwerks greift
//     keine Annahme mehr – das Baujahr allein ist kein Nachweis.
pruefeWahr('Baujahr ohne Regelwerk lässt keine Annahme greifen',
  applyAssumptions(seed as any,
    { qa_baujahr: 2020, qd_konformitaet_geprueft: true } as any).applied.length === 0);

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
const m08 = evaluate(seed as any,
  { ...bj2020, qa_aufzugsart: 'seil', qm_zweikreisbremse: true } as any)
  .find((x: any) => x.hazard === 'MF-M08') as any;
pruefeWahr('Befund nennt die angenommene Frage',
  Array.isArray(m08.assumed) && m08.assumed.includes('qm_bremse_ueberwacht'),
  JSON.stringify(m08.assumed));

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
  qt_glas_beschaedigt: false, qt_glas_schiebetuer: true, qt_glas_flaeche_gross: true,
  qt_glas_einzugsschutz: true };
pruefe('B06 intaktes Drahtglas = Niedrig', 'MF-T04',
  { ...GLAS, qt_glas_normgerecht: false, qt_glas_drahtglas: true }, 'LOW');
pruefe('B06 anderes Nicht-VSG = Hoch', 'MF-T04',
  { ...GLAS, qt_glas_normgerecht: false, qt_glas_drahtglas: false }, 'HIGH');
pruefe('B06 beschädigtes Glas = Hoch', 'MF-T04',
  { ...GLAS, qt_glas_normgerecht: true, qt_glas_drahtglas: false, qt_glas_beschaedigt: true }, 'HIGH');
// Regelprüfung 20.09.2026 (B4): Der Einzugsschutz ist nach DIN EN 81-20
// 5.3.6.2.2.1 i) nur für Glasflächen gefordert, die größer sind als ein
// Sichtfenster nach 5.3.7.2 (Breite über 150 mm nach 5.3.7.2.1 a) 4)).
pruefe('B4 Schiebetür mit großer Glasfläche ohne Einzugsschutz = Hoch', 'MF-T04',
  { ...GLAS, qt_glas_normgerecht: true, qt_glas_drahtglas: false,
    qt_glas_flaeche_gross: true, qt_glas_einzugsschutz: false }, 'HIGH');
pruefe('B4 Schiebetür nur mit Sichtfenster, kein Einzugsschutz nötig = Kein Risiko', 'MF-T04',
  { qa_glas_schachttueren: true, qa_glas_fahrkorbtueren: false, qt_glas_beschaedigt: false,
    qt_glas_schiebetuer: true, qt_glas_flaeche_gross: false,
    qt_glas_normgerecht: true, qt_glas_drahtglas: false }, 'NO_RISK');
pruefe('B4 Glasflächengröße unbeantwortet = unvollständig', 'MF-T04',
  { qa_glas_schachttueren: true, qa_glas_fahrkorbtueren: false, qt_glas_beschaedigt: false,
    qt_glas_schiebetuer: true, qt_glas_normgerecht: true, qt_glas_drahtglas: false },
  'INCOMPLETE');
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
pruefe('H06 Asbest gefunden, beschädigt = Hoch', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: true, qm_asbest_zustand: 'beschaedigt',
    qs_asbest: false, qg_asbest: false, qu_asbest_unbekannt: true }, 'HIGH');
// Regelprüfung 20.09.2026 (B1): Die Stufe hängt jetzt am Zustand des Fundes.
// Fest gebunden und unbeschädigt = Mittel; beschädigt ODER nicht beurteilbar =
// Hoch (fail-closed); asbesthaltige Bremsbeläge im Triebwerksraum immer Hoch.
pruefe('B1 Asbest fest gebunden und unbeschädigt = Mittel', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: true, qm_asbest_zustand: 'fest',
    qs_asbest: false, qg_asbest: false, qu_asbest_unbekannt: false }, 'MEDIUM');
pruefe('B1 Asbest Zustand nicht beurteilbar = Hoch (fail-closed)', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: true, qm_asbest_zustand: 'unklar',
    qs_asbest: false, qg_asbest: false, qu_asbest_unbekannt: false }, 'HIGH');
pruefe('B1 Asbesthaltige Bremsbeläge = Hoch', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: true, qm_asbest_zustand: 'bremsbelag',
    qs_asbest: false, qg_asbest: false, qu_asbest_unbekannt: false }, 'HIGH');
pruefe('B1 Zustandsfrage unbeantwortet = unvollständig', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: true,
    qs_asbest: false, qg_asbest: false, qu_asbest_unbekannt: false }, 'INCOMPLETE');
pruefe('B1 Fahrkorb beschädigt schlägt fest gebundenen Fund im TWR (ANY = höchste)', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: true, qm_asbest_zustand: 'fest',
    qs_asbest: true, qs_asbest_zustand: 'beschaedigt', qg_asbest: false,
    qu_asbest_unbekannt: false }, 'HIGH');
pruefe('B1 Kein Fund, Situation bekannt = Kein Risiko', 'MF-U01',
  { qa_maschinenraum: true, qz_asbest: false, qm_asbest: false, qs_asbest: false,
    qg_asbest: false, qu_asbest_unbekannt: false }, 'NO_RISK');

// ---- Zweite Prüfung (16.09.2026) --------------------------------------------
// Prüfbericht 20.09.2026: Ohne Funktionsnachweis ist die automatische Abschaltung
// keine wirksame Kompensation – sie senkt die Grundstufe nicht mehr (vorher Mittel).
pruefe('Abschaltung ohne Funktionsnachweis senkt nicht (Grube)', 'MF-G08',
  { qa_mehrere_aufzuege: true, qg_nachbar_abtrennung: false, qg_nachbar_abschaltung: true,
    qg_nachbar_abschaltung_geprueft: false }, 'HIGH');
pruefe('Abschaltung ohne Funktionsnachweis senkt nicht (Dach, keine Abtrennung)', 'MF-F03',
  { qa_mehrere_aufzuege: true, qf_nachbar_trennung: 'fehlt', qf_nachbar_abschaltung: true,
    qf_nachbar_abschaltung_geprueft: false }, 'HIGH');
pruefe('Abschaltung ohne Funktionsnachweis: Teilabdeckung bleibt Mittel', 'MF-F03',
  { qa_mehrere_aufzuege: true, qf_nachbar_trennung: 'teilweise', qf_nachbar_abschaltung: true,
    qf_nachbar_abschaltung_geprueft: false }, 'MEDIUM');
pruefe('Abschaltung MIT Funktionsnachweis = Kein Risiko (Grube)', 'MF-G08',
  { qa_mehrere_aufzuege: true, qg_nachbar_abtrennung: false, qg_nachbar_abschaltung: true,
    qg_nachbar_abschaltung_geprueft: true }, 'NO_RISK');
pruefe('Scherengitter + Lichtgitter, Personenaufzug = Hoch', 'MF-T06',
  { qa_fahrkorbtuer: false, qt_lichtgitter_ohne_tuer: true, qt_scherengitter: true,
    qa_nutzung_pmem: false, qa_nutzung_kinder: false, qa_nutzungsart: 'personen',
    qt_nur_eingewiesene: false }, 'HIGH');
// Regelprüfung 20.09.2026: MF-T06-R9 ist entfallen. Ein Scherengitter ohne
// Schließstellungsüberwachung ersetzt die Fahrkorbtür nicht (ein überwachtes
// Gitter wäre nach dem Hilfetext zu 8.6 bereits Fahrkorbabschlusstür, dann wäre
// 8.9a gar nicht sichtbar); die Kompensation auf Mittel war eine
// Prioritätsinversion zugunsten eines wirkungslosen Schutzes. Es greift jetzt
// MF-T06-R11 (P150, Hoch) – auch beim Lastenaufzug mit eingewiesenem
// Nutzerkreis, denn dieser Vorbehalt gilt nur noch für das Lichtgitter.
pruefe('Scherengitter, Lastenaufzug, eingewiesen = Hoch (R9 entfallen)', 'MF-T06',
  { qa_fahrkorbtuer: false, qt_lichtgitter_ohne_tuer: false, qt_scherengitter: true,
    qa_nutzung_pmem: false, qa_nutzung_kinder: false, qa_nutzungsart: 'lasten',
    qt_nur_eingewiesene: true }, 'HIGH');
pruefe('Lichtgitter, Lastenaufzug, eingewiesen = Mittel (R10 bleibt)', 'MF-T06',
  { qa_fahrkorbtuer: false, qt_lichtgitter_ohne_tuer: true, qt_scherengitter: false,
    qa_nutzung_pmem: false, qa_nutzung_kinder: false, qa_nutzungsart: 'lasten',
    qt_nur_eingewiesene: true }, 'MEDIUM');
pruefe('Keine Schließkantensicherung + PmeM = Hoch', 'MF-T06',
  { qa_fahrkorbtuer: true, qt_fk_tuer_automatisch: true, qt_schliesskante: 'keine',
    qa_nutzung_pmem: true, qa_nutzung_kinder: false }, 'HIGH');
pruefe('Einzel-Lichtschranke + PmeM = Hoch', 'MF-T06',
  { qa_fahrkorbtuer: true, qt_fk_tuer_automatisch: true, qt_schliesskante: 'lichtschranke',
    qa_nutzung_pmem: true, qa_nutzung_kinder: false }, 'HIGH');
// Prüfbericht 20.09.2026: Kinder wirken jetzt wie PmeM (vorher nur ohne Fahrkorbtür).
pruefe('Einzel-Lichtschranke + Kinder = Hoch', 'MF-T06',
  { qa_fahrkorbtuer: true, qt_fk_tuer_automatisch: true, qt_schliesskante: 'lichtschranke',
    qa_nutzung_pmem: false, qa_nutzung_kinder: true }, 'HIGH');
// Handbetätigte Fahrkorbtür: keine Schließkantensicherung gefordert, kein Befund.
pruefe('Handbetätigte Fahrkorbtür braucht keine Schließkantensicherung', 'MF-T06',
  { qa_fahrkorbtuer: true, qt_fk_tuer_automatisch: false,
    qa_nutzung_pmem: false, qa_nutzung_kinder: false }, 'NO_RISK');
pruefe('Drehtür mit Drahtglas ohne Einzugsschutz = Niedrig', 'MF-T04',
  { qa_glas_schachttueren: true, qa_glas_fahrkorbtueren: false, qt_glas_normgerecht: false,
    qt_glas_drahtglas: true, qt_glas_beschaedigt: false, qt_glas_schiebetuer: false }, 'LOW');
pruefe('Separate Grubenzugangstür mit Kontakt, keine Leiter = Kein Risiko', 'MF-G04',
  { qg_zugangstuer: true, qg_zugangstuer_schalter: true }, 'NO_RISK');
pruefe('Zugang über Leiter, keine Leiter = Hoch', 'MF-G04',
  { qg_zugangstuer: false, qg_leiter: 'keine' }, 'HIGH');
pruefe('Beleuchteter Notruftaster allein = Niedrig', 'MF-K02', { qk_notbeleuchtung: 'nur_taster' }, 'LOW');
// Regelprüfung 20.09.2026 (B4): Sieben Regeln vergaben Hoch bzw. Mittel auch
// für normkonforme Anlagen.
pruefe('B4 Hydraulik ohne Leitungsbruchventil und ohne Alternative = Hoch', 'MF-M13',
  { qa_aufzugsart: 'hydraulik', qm_absperrventil: true, qm_absperrventil_zugang: true,
    qm_absperrventil_gekennz: true, qm_rohrbruch: false,
    qm_absturzsicherung_alt: 'keine', qm_kav: true, qm_absinkt: false }, 'HIGH');
pruefe('B4 Hydraulik mit zulässiger Drossel = Kein Risiko', 'MF-M13',
  { qa_aufzugsart: 'hydraulik', qm_absperrventil: true, qm_absperrventil_zugang: true,
    qm_absperrventil_gekennz: true, qm_rohrbruch: false,
    qm_absturzsicherung_alt: 'drossel', qm_kav: true, qm_absinkt: false }, 'NO_RISK');
pruefe('B4 Grube nur Feuchte ohne Bauteilkontakt = Mittel', 'MF-U07',
  { qg_wasser: 'feuchte', qg_oel: false, qu_temperatur: false,
    qu_feuchte_sicherheitsteile: false, qu_korrosion: false }, 'MEDIUM');
pruefe('B4 Stehendes Wasser an Bauteilen = Hoch', 'MF-U07',
  { qg_wasser: 'wasser', qg_oel: false, qu_temperatur: false,
    qu_feuchte_sicherheitsteile: false, qu_korrosion: false }, 'HIGH');
pruefe('B4 Wasserumfang nicht beurteilbar = Hoch (fail-closed)', 'MF-U07',
  { qg_wasser: 'unklar', qg_oel: false, qu_temperatur: false,
    qu_feuchte_sicherheitsteile: false, qu_korrosion: false }, 'HIGH');
pruefe('B4 Brandschutz behindert Rettung = Hoch', 'MF-U09',
  { qa_bma_vorhanden: false, qu_brandschutz_behindert: 'rettung' }, 'HIGH');
pruefe('B4 Brandschutz behindert nur den Betrieb = Mittel', 'MF-U09',
  { qa_bma_vorhanden: false, qu_brandschutz_behindert: 'betrieb' }, 'MEDIUM');
pruefe('B4 RWA-Funktion unklar = Mittel (nicht mehr Hoch)', 'MF-U10',
  { qa_entrauchung_vorhanden: true, qu_entrauchung: 'kein_nachweis' }, 'MEDIUM');
pruefe('B4 RWA blockiert oder defekt = Mittel', 'MF-U10',
  { qa_entrauchung_vorhanden: true, qu_entrauchung: 'gestoert' }, 'MEDIUM');
pruefe('B4 Sprinkler-Abschaltung fehlt = Hoch', 'MF-U11',
  { qa_sprinkler_vorhanden: true, qu_sprinkler_abschaltung: false }, 'HIGH');
pruefe('B4 Sprinkler-Abschaltung vorhanden, Nachweis fehlt = Mittel', 'MF-U11',
  { qa_sprinkler_vorhanden: true, qu_sprinkler_abschaltung: true,
    qu_sprinkler_geprueft: false }, 'MEDIUM');
pruefe('B4 Sprinkler unbeantwortet = unvollständig (nicht Kein Risiko)', 'MF-U11',
  { qa_sprinkler_vorhanden: true }, 'INCOMPLETE');
pruefe('B4 Abgase mit nachgewiesener Lüftung = Kein Risiko', 'MF-U15',
  { qu_abgase: true, qu_abgase_lueftung: true }, 'NO_RISK');
pruefe('B4 Abgase ohne wirksame Lüftung = Mittel', 'MF-U15',
  { qu_abgase: true, qu_abgase_lueftung: false }, 'MEDIUM');
// Regelprüfung 20.09.2026 (B3): Drei Fragen bündelten je einen schweren und
// einen leichten Mangel und bewerteten beide gleich.
pruefe('B3 Puffer mit Funktionsverlust = Hoch', 'MF-G06',
  { qg_puffer: true, qg_puffer_zustand: 'defekt', qg_puffer_art: 'speichernd',
    qa_nenngeschwindigkeit: 0.6 }, 'HIGH');
pruefe('B3 Puffer mit Verschleiß bei erhaltener Funktion = Mittel', 'MF-G06',
  { qg_puffer: true, qg_puffer_zustand: 'verschleiss', qg_puffer_art: 'speichernd',
    qa_nenngeschwindigkeit: 0.6 }, 'MEDIUM');
pruefe('B3 Puffer unbeschädigt = Kein Risiko', 'MF-G06',
  { qg_puffer: true, qg_puffer_zustand: 'ok', qg_puffer_art: 'speichernd',
    qa_nenngeschwindigkeit: 0.6 }, 'NO_RISK');
pruefe('B3 Ölstand nicht prüfbar = Mittel', 'MF-G06',
  { qg_puffer: true, qg_puffer_zustand: 'ok', qg_puffer_art: 'verzehrend',
    qg_puffer_oelstand: false, qg_puffer_kennz: true, qa_nenngeschwindigkeit: 1.6 }, 'MEDIUM');
pruefe('B3 nur Kennzeichnung des Puffers fehlt = Niedrig', 'MF-G06',
  { qg_puffer: true, qg_puffer_zustand: 'ok', qg_puffer_art: 'verzehrend',
    qg_puffer_oelstand: true, qg_puffer_kennz: false, qa_nenngeschwindigkeit: 1.6 }, 'LOW');
pruefe('B3 Absperrventil schlecht zugänglich = Mittel', 'MF-M13',
  { qa_aufzugsart: 'hydraulik', qm_absperrventil: true, qm_absperrventil_zugang: false,
    qm_absperrventil_gekennz: true, qm_rohrbruch: true, qm_kav: true,
    qm_absinkt: false }, 'MEDIUM');
pruefe('B3 nur Kennzeichnung des Absperrventils fehlt = Niedrig', 'MF-M13',
  { qa_aufzugsart: 'hydraulik', qm_absperrventil: true, qm_absperrventil_zugang: true,
    qm_absperrventil_gekennz: false, qm_rohrbruch: true, qm_kav: true,
    qm_absinkt: false }, 'LOW');
// Regelprüfung 20.09.2026 (B2): MF-U05 bewertete eine Nutzungsart, keinen
// Mangel – jeder Transport gab dauerhaft Mittel. Jetzt entscheidet die
// Kompensationsfrage; geregelt = Niedrig (nicht Kein Risiko, die Fortschreibung
// bleibt geschuldet), ungeregelt = Mittel wie bisher.
pruefe('B2 Gefahrstofftransport ungeregelt = Mittel', 'MF-U05',
  { qu_transport_chem: true, qu_transport_chem_geregelt: false, qu_transport_bio: false,
    qu_transport_brennbar: false, qu_transport_radioaktiv: false }, 'MEDIUM');
pruefe('B2 Gefahrstofftransport geregelt = Niedrig', 'MF-U05',
  { qu_transport_chem: true, qu_transport_chem_geregelt: true, qu_transport_bio: false,
    qu_transport_brennbar: false, qu_transport_radioaktiv: false }, 'LOW');
pruefe('B2 Kompensationsfrage unbeantwortet = unvollständig', 'MF-U05',
  { qu_transport_chem: true, qu_transport_bio: false,
    qu_transport_brennbar: false, qu_transport_radioaktiv: false }, 'INCOMPLETE');
pruefe('B2 Kein Transport = Kein Risiko', 'MF-U05',
  { qu_transport_chem: false, qu_transport_bio: false,
    qu_transport_brennbar: false, qu_transport_radioaktiv: false }, 'NO_RISK');
pruefe('B2 eine Stoffgruppe geregelt, eine nicht = Mittel (MAXIMUM)', 'MF-U05',
  { qu_transport_chem: true, qu_transport_chem_geregelt: true,
    qu_transport_bio: true, qu_transport_bio_geregelt: false,
    qu_transport_brennbar: false, qu_transport_radioaktiv: false }, 'MEDIUM');
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
// Regelprüfung 20.09.2026, am Normtext nachgeschlagen (DIN EN 81-20:2014
// Tabelle 11/12, EN 81-1:1998 9.8.3.1): Der Geschwindigkeitsbegrenzer ist bei
// Treibscheiben- UND Trommel-/Kettenaufzügen für den Fahrkorb zwingend; nur der
// indirekt angetriebene Hydraulikaufzug darf ihn durch Leitungsbruchventil bzw.
// Drossel plus eine durch Tragmittelbruch oder Sicherheitsseil ausgelöste
// Fangvorrichtung ersetzen (Frage 10.8a).
pruefe('Kein Begrenzer, Treibscheibe = Hoch', 'MF-S05',
  { qa_aufzugsart: 'seil', qs_fang: true, qs_begrenzer: false, qs_fang_geprueft: true,
    qs_spanngewicht_schalter: true }, 'HIGH');
pruefe('Kein Begrenzer, Trommelaufzug = Hoch (Tabelle 11, keine Alternative)', 'MF-S05',
  { qa_aufzugsart: 'trommel', qs_fang: true, qs_begrenzer: false, qs_fang_geprueft: true,
    qs_spanngewicht_schalter: true, qs_schlaffseil: true }, 'HIGH');
pruefe('Kein Begrenzer, indirekte Hydraulik MIT Ersatzauslösung = Kein Risiko', 'MF-S05',
  { qa_aufzugsart: 'seil_hydraulik', qs_fang: true, qs_begrenzer: false,
    qs_fang_ersatzausloesung: true, qs_fang_geprueft: true, qs_spanngewicht_schalter: true,
    qs_schlaffseil: true }, 'NO_RISK');
pruefe('Kein Begrenzer, indirekte Hydraulik OHNE Ersatzauslösung = Hoch', 'MF-S05',
  { qa_aufzugsart: 'seil_hydraulik', qs_fang: true, qs_begrenzer: false,
    qs_fang_ersatzausloesung: false, qs_fang_geprueft: true, qs_spanngewicht_schalter: true,
    qs_schlaffseil: true }, 'HIGH');
pruefe('Kein Begrenzer, indirekte Hydraulik, 10.8a unbeantwortet = unvollständig', 'MF-S05',
  { qa_aufzugsart: 'seil_hydraulik', qs_fang: true, qs_begrenzer: false,
    qs_fang_geprueft: true, qs_spanngewicht_schalter: true, qs_schlaffseil: true },
  'INCOMPLETE');
pruefe('Schlaffseilsicherung fehlt (5.5.5.3 b) = Hoch, auch mit Begrenzer', 'MF-S05',
  { qa_aufzugsart: 'trommel', qs_fang: true, qs_begrenzer: true, qs_fang_geprueft: true,
    qs_spanngewicht_schalter: true, qs_schlaffseil: false }, 'HIGH');
// Regelprüfung 20.09.2026: MF-K10-R1 (Rollstuhlmaß) ist von Hoch auf Mittel
// gesenkt – ein zu kleiner Fahrkorb ist eine Nutzungseinschränkung, keine
// unmittelbare Gefahr, und der Teilaspekt darf über MAXIMUM nicht über der
// Oberregel R2 liegen.
pruefe('Barrierefreiheit gefordert, keine PmeM-Nutzung = bewertet', 'MF-K10',
  { qa_nutzung_pmem: false, qa_barrierefrei_gefordert: true, qk_en8170: true, qk_bedienelemente: true,
    qk_rollstuhl_mass: false }, 'MEDIUM');
// Aufspaltung von R2 (Regelprüfung 20.09.2026): EN 81-70 nicht erfüllt ist nur
// dann Mittel, wenn die barrierefreie Ausführung gefordert ist; sonst Niedrig
// als Nachrüstbedarf nach EN 81-80.
pruefe('EN 81-70 nicht erfüllt, barrierefrei gefordert = Mittel', 'MF-K10',
  { qa_nutzung_pmem: true, qa_barrierefrei_gefordert: true, qk_en8170: false,
    qk_bedienelemente: true, qk_rollstuhl_mass: true }, 'MEDIUM');
pruefe('EN 81-70 nicht erfüllt, barrierefrei NICHT gefordert = Niedrig', 'MF-K10',
  { qa_nutzung_pmem: true, qa_barrierefrei_gefordert: false, qk_en8170: false,
    qk_bedienelemente: true, qk_rollstuhl_mass: true }, 'LOW');
pruefe('EN 81-70 nicht erfüllt, 4.9a unbeantwortet = unvollständig', 'MF-K10',
  { qa_nutzung_pmem: true, qk_en8170: false,
    qk_bedienelemente: true, qk_rollstuhl_mass: true }, 'INCOMPLETE');
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
