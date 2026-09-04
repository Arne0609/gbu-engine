// Smoke-Test des Cyber-MF-Katalogs gegen den Referenz-Evaluator.
//   node --experimental-strip-types cy_smoke.ts
import { readFileSync } from 'node:fs';
import { evaluate, summarize } from './evaluator.ts';

const seed = JSON.parse(readFileSync('./norm_cyber_mf.json', 'utf-8'));
const COMPS = ['pessral', 'fu', 'notruf', 'kopierung', 'tuer', 'ucm', 'safue', 'tragmittel', 'hydraulik'];

/** Vollständig guter Zustand: vernetzter Seilaufzug mit Maschinenraum, alle
 *  Komponenten vorhanden, kabelgebunden, Maßnahmen umgesetzt, Zugang gesichert. */
function gut(): Record<string, any> {
  const a: Record<string, any> = {
    qa_aufzugsart: 'seil', qa_ueberwachungsbeduerftig: true, qa_steuerungsart: 'vernetzt',
    qa_maschinenraum: true, qa_vernetzt: true, qa_gebaeude_anbindung: true,
    qa_hersteller_vorgaben: 'beruecksichtigt',
    qz_steuerung_frei: false, qz_triebwerksraum_frei: false, qz_schacht_frei: false,
    qz_service_gesichert: true, qz_default_zugangsdaten: false, qz_rollen: true, qz_servicegeraete: true,
    qc_steuerung_schnittstelle: 'kabelgebunden', qc_steuerung_massnahmen: 'umgesetzt', qc_steuerung_unabhaengig: true,
    qn_segmentierung: true, qn_fern_freigabe: true, qn_fern_auth: true, qn_protokoll: true,
    qn_softwarestand: 'geregelt', qn_funktionsreduzierung: true,
    qc_fernueb_vorhanden: true, qc_fernueb_lesend: true, qc_remote_vorhanden: true,
    qc_gateway_vorhanden: true, qc_gateway_firewall: true, qc_gateway_default: true, qc_gateway_updates: true,
    qc_geb_rueckwirkungsfrei: true, qc_geb_sicherer_zustand: true,
    qo_verantwortlich: true, qo_fachkunde: true, qo_notfall: true, qo_unterweisung: true,
    qo_pruefung_fristen: true, qo_wirksamkeit: true, qo_funktion: true, qo_rueckwirkung: true,
    qo_erkenntnisse: true, qo_aenderungen: false,
    qo_zues_beruecksichtigt: true, qo_zues_erfasst: true, qo_zues_erhebliches_risiko: true, qo_zues_stand_technik: true,
  };
  for (const c of COMPS) {
    if (c === 'hydraulik') continue; // Seilaufzug: nicht zutreffend
    a[`qc_${c}_vorhanden`] = true;
    a[`qc_${c}_schnittstelle`] = 'kabelgebunden';
    a[`qc_${c}_massnahmen`] = 'umgesetzt';
    if (c !== 'pessral') a[`qc_${c}_unabhaengig`] = true;
  }
  return a;
}

function run(label: string, answers: Record<string, any>) {
  const res = evaluate(seed as any, answers);
  const sum = summarize(res);
  console.log(label.padEnd(34), JSON.stringify(sum));
  return { res, sum, of: (h: string) => res.find(r => r.hazard === h) };
}
function expect(cond: boolean, msg: string) { if (!cond) throw new Error(msg); }

// 1) Leerer Zustand: nichts darf Kein Risiko sein
const leer = run('leer', {});
expect(leer.sum.NO_RISK === 0, 'Unbewertet ergibt Kein Risiko!');
expect(leer.sum.INCOMPLETE === seed.hazards.length, 'Leer: nicht alles unvollständig');

// 2) Alles gut: nur Kein Risiko / Nicht zutreffend
const g = run('alles gut', gut());
const rest = g.res.filter(r => !['NO_RISK', 'NOT_APPLICABLE'].includes(r.status));
expect(rest.length === 0, 'Guter Zustand ergibt Risiko: ' + JSON.stringify(rest.map(r => [r.hazard, r.status, r.matched_rule])));
expect(g.of('CY-C10')?.status === 'NOT_APPLICABLE', 'Hydraulik-Filter greift nicht beim Seilaufzug');

// 3) Relaissteuerung, nicht vernetzt, keine Gebäudeanbindung: Kanäle/Steuerung n. a., kein Unvollständig
const relais = { ...gut(), qa_steuerungsart: 'relais', qa_vernetzt: false, qa_gebaeude_anbindung: false };
for (const k of Object.keys(relais)) if (k.startsWith('qn_') && k !== 'qn_protokoll' && k !== 'qn_softwarestand' && k !== 'qn_funktionsreduzierung') delete relais[k];
for (const k of ['qc_steuerung_schnittstelle', 'qc_steuerung_massnahmen', 'qc_steuerung_unabhaengig',
                 'qc_fernueb_vorhanden', 'qc_fernueb_lesend', 'qc_remote_vorhanden', 'qc_gateway_vorhanden',
                 'qc_gateway_firewall', 'qc_gateway_default', 'qc_gateway_updates',
                 'qc_geb_rueckwirkungsfrei', 'qc_geb_sicherer_zustand']) delete relais[k];
const r3 = run('Relais, nicht vernetzt', relais);
for (const h of ['CY-C01', 'CY-C11', 'CY-C12', 'CY-C13', 'CY-C14'])
  expect(r3.of(h)?.status === 'NOT_APPLICABLE', h + ' nicht abgeschaltet: ' + r3.of(h)?.status);
expect(r3.sum.INCOMPLETE === 0, 'Relais-Anlage unvollständig: ' + JSON.stringify(r3.res.filter(r => r.status === 'INCOMPLETE').map(r => r.hazard)));

// 4) Vorscreening: PESSRAL ohne Schnittstelle -> Kein Risiko, Maßnahmenfrage nicht Pflicht
const vs = { ...gut(), qc_pessral_schnittstelle: 'keine' };
delete vs['qc_pessral_massnahmen'];
const r4 = run('Vorscreening PESSRAL', vs);
expect(r4.of('CY-C02')?.status === 'NO_RISK' && r4.of('CY-C02')?.matched_rule === 'CY-C02-R1',
  'Vorscreening greift nicht: ' + JSON.stringify(r4.of('CY-C02')));

// 5) Hoch erreichbar: Steuerung mit Fernzugriff ohne Maßnahmen, keine Kompensation
const h5 = { ...gut(), qc_steuerung_schnittstelle: 'fernzugriff', qc_steuerung_massnahmen: 'keine', qc_steuerung_unabhaengig: false };
const r5 = run('Steuerung Fernzugriff ohne Maßn.', h5);
expect(r5.of('CY-C01')?.status === 'HIGH', 'Steuerung Fernzugriff ohne Maßnahmen nicht Hoch');

// 6) Kompensation: dieselbe Lage mit unabhängigem Sicherheitskreis -> Mittel
const r6 = run('… mit unabh. Sicherheitskreis', { ...h5, qc_steuerung_unabhaengig: true });
expect(r6.of('CY-C01')?.status === 'MEDIUM', 'Kompensation Steuerung greift nicht: ' + r6.of('CY-C01')?.status);

// 7) Zugangs-Modifier: kabelgebunden, keine Maßnahmen: Zugang frei -> Hoch, gesichert -> Mittel
const z = { ...gut(), qc_ucm_schnittstelle: 'kabelgebunden', qc_ucm_massnahmen: 'keine', qc_ucm_unabhaengig: false };
const r7a = run('UCM lokal ohne Maßn., Zugang frei', { ...z, qz_steuerung_frei: true });
expect(r7a.of('CY-C07')?.status === 'HIGH', 'Zugangsmodifier (frei) wirkt nicht: ' + r7a.of('CY-C07')?.status);
const r7b = run('UCM lokal ohne Maßn., gesichert', z);
expect(r7b.of('CY-C07')?.status === 'MEDIUM', 'lokal ohne Maßnahmen nicht Mittel: ' + r7b.of('CY-C07')?.status);

// 8) Frequenzumrichter mit unabhängiger Sicherheitskette: Deckel Niedrig
const r8 = run('FU Fernzugriff, unabh. Kette', { ...gut(), qc_fu_schnittstelle: 'fernzugriff', qc_fu_massnahmen: 'keine', qc_fu_unabhaengig: true });
expect(r8.of('CY-C03')?.status === 'LOW', 'FU-Deckel greift nicht: ' + r8.of('CY-C03')?.status);

// 9) Fernwartung: dauerhaft offen + nicht authentifiziert -> Hoch; nur keine Freigabe -> Mittel
const r9a = run('Fernwartung offen, keine Auth', { ...gut(), qn_fern_freigabe: false, qn_fern_auth: false });
expect(r9a.of('CY-C12')?.status === 'HIGH', 'Fernwartung offen nicht Hoch');
const r9b = run('Fernwartung ohne Freigabe', { ...gut(), qn_fern_freigabe: false });
expect(r9b.of('CY-C12')?.status === 'LOW', 'Fernwartung ohne Freigabe (authentifiziert) nicht Niedrig (K-C23)');
// 9c) K-C06: Fernzugriff mit umgesetzten Maßnahmen -> Kein Risiko
const r9c = run('UCM Fernzugriff, umgesetzt', { ...gut(), qc_ucm_schnittstelle: 'fernzugriff', qc_ucm_massnahmen: 'umgesetzt' });
expect(r9c.of('CY-C07')?.status === 'NO_RISK', 'Fern umgesetzt nicht Kein Risiko (K-C06)');
// 9d) K-C10: Fernüberwachung rein lesend ohne Segmentierung -> Niedrig
const r9d = run('Fernüberw. lesend, keine Segm.', { ...gut(), qn_segmentierung: false });
expect(r9d.of('CY-C11')?.status === 'LOW', 'Fernüberwachung lesend ohne Segmentierung nicht Niedrig (K-C10)');
// 9e) K-C20: ZÜS-Dokumentationsfrage fehlt -> CY-O05 unvollständig
const zd = gut(); delete zd['qo_zues_erfasst'];
expect(evaluate(seed as any, zd).find(r => r.hazard === 'CY-O05')?.status === 'INCOMPLETE', 'ZÜS-Dokumentationsfrage nicht Pflicht (K-C20)');
// 9f) K-C21/K-C24: entfernte Gefährdungen existieren nicht mehr
for (const h of ['CY-Z02', 'CY-Z03', 'CY-C15']) expect(!seed.hazards.some((x: any) => x.code === h), h + ' sollte entfernt sein');

// 10) Gebäudeschnittstelle nicht rückwirkungsfrei -> Hoch
const r10 = run('Gebäude nicht rückwirkungsfrei', { ...gut(), qc_geb_rueckwirkungsfrei: false });
expect(r10.of('CY-C14')?.status === 'HIGH', 'Gebäudeschnittstelle nicht Hoch');

// 11) Eine fehlende Pflichtantwort -> genau diese Gefährdung unvollständig
const teil = gut(); delete teil['qo_notfall'];
const r11 = run('qo_notfall fehlt', teil);
const inc = r11.res.filter(r => r.status === 'INCOMPLETE').map(r => r.hazard);
expect(inc.length === 1 && inc[0] === 'CY-O03', 'Pflichtfrage wirkt nicht wie erwartet: ' + JSON.stringify(inc));

// 12) Unbeantworteter Modifier darf kein milderes Ergebnis erzeugen
const mod = { ...h5 }; delete mod['qz_steuerung_frei'];
const r12 = run('Zugangsfrage fehlt', mod);
expect(r12.of('CY-C01')?.status === 'INCOMPLETE', 'fehlender Modifier ergibt Stufe statt Unvollständig: ' + r12.of('CY-C01')?.status);

// 13) Ungeprüfte Änderung -> Hoch; geprüft -> Kein Risiko
const r13a = run('Änderung ungeprüft', { ...gut(), qo_aenderungen: true, qo_aenderungen_geprueft: false });
expect(r13a.of('CY-O06')?.status === 'HIGH', 'ungeprüfte Änderung nicht Hoch');
const r13b = run('Änderung geprüft', { ...gut(), qo_aenderungen: true, qo_aenderungen_geprueft: true });
expect(r13b.of('CY-O06')?.status === 'NO_RISK', 'geprüfte Änderung nicht Kein Risiko');

// 14) Worst case: alles schlecht
const bad: Record<string, any> = { ...gut(), qz_steuerung_frei: true, qz_triebwerksraum_frei: true, qz_schacht_frei: true,
  qz_service_gesichert: false, qz_default_zugangsdaten: true, qz_rollen: false, qz_servicegeraete: false,
  qn_segmentierung: false, qn_fern_freigabe: false, qn_fern_auth: false, qn_protokoll: false,
  qn_softwarestand: 'bekannt_ungeregelt', qn_funktionsreduzierung: false, qc_fernueb_lesend: false,
  qc_gateway_firewall: false, qc_gateway_default: false, qc_gateway_updates: false,
  qc_geb_rueckwirkungsfrei: false, qc_geb_sicherer_zustand: false, qa_hersteller_vorgaben: 'nicht_beruecksichtigt',
  qo_verantwortlich: false, qo_fachkunde: false, qo_notfall: false, qo_unterweisung: false, qo_pruefung_fristen: false,
  qo_wirksamkeit: false, qo_funktion: false, qo_rueckwirkung: false, qo_erkenntnisse: false,
  qo_aenderungen: true, qo_aenderungen_geprueft: false,
  qc_steuerung_schnittstelle: 'fernzugriff', qc_steuerung_massnahmen: 'keine', qc_steuerung_unabhaengig: false };
for (const c of COMPS) { if (c === 'hydraulik') continue; bad[`qc_${c}_schnittstelle`] = 'kabellos'; bad[`qc_${c}_massnahmen`] = 'keine'; bad[`qc_${c}_unabhaengig`] = false; }
const r14 = run('alles schlecht', bad);
expect(r14.sum.INCOMPLETE === 0 && r14.sum.NO_RISK === 0, 'Worst case: Unvollständig/Kein Risiko übrig');
expect(r14.sum.HIGH >= 18, 'Worst case: zu wenig Hoch (' + r14.sum.HIGH + ')');

// 15) Regellücken-Suche: alle Kombinationen je Klasse-S-Komponente müssen eine Regel treffen
const IF = ['keine', 'kabelgebunden', 'benutzer', 'kabellos', 'fernzugriff'];
const MS = ['keine', 'teilweise', 'umgesetzt'];
let gaps = 0, checked = 0;
for (const c of ['steuerung', ...COMPS]) {
  if (c === 'hydraulik') continue;
  for (const i of IF) for (const m of MS) for (const u of [true, false]) for (const zf of [true, false]) {
    const a = { ...gut(), qz_steuerung_frei: zf };
    a[`qc_${c}_schnittstelle`] = i; a[`qc_${c}_massnahmen`] = m; a[`qc_${c}_unabhaengig`] = u;
    const code = c === 'steuerung' ? 'CY-C01' : seed.hazards.find((h: any) => h.questions.some((q: any) => q.question === `qc_${c}_schnittstelle`)).code;
    const res = evaluate(seed as any, a).find(r => r.hazard === code)!;
    checked++;
    if (res.status === 'INCOMPLETE' || (res as any).rule_gap) { gaps++; console.log('LÜCKE', code, i, m, u, zf, res.status); }
  }
}
console.log(`Kombinationen geprüft: ${checked}, Lücken: ${gaps}`);
expect(gaps === 0, 'Regellücken vorhanden');

console.log('\nAlle Smoke-Tests bestanden.');
