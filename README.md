# GBU 4.0 – Bewertungsengine (Engine + REST-API)

Engine-getrennte Gefährdungsbeurteilung für Aufzüge: **Frage → Gefährdung → Regel → Risikostufe**. Fragebogen und Bewertung sind vollständig getrennt; eine fehlende Antwort ist `INCOMPLETE` (nicht „kein Risiko"), und eine Regellücke (alle Pflichtfragen beantwortet, keine Regel passt) ebenfalls – die Engine arbeitet fail-closed (`rule_gap`). Sechs Zustände: `INCOMPLETE, NOT_APPLICABLE, NO_RISK, LOW, MEDIUM, HIGH`.

Dieses Verzeichnis enthält die Engine, die REST-API und die Referenz-UI. Der Server läuft ohne Build-Schritt (Node 22, Type Stripping).

## Bestandteile

- `evaluator.ts` – reiner Auswerter (Applicability → Pflichtfragen → Regeln → Aggregation).
- `engine_service.ts` – Katalog/Antworten aus der DB, transaktionale Bewertung (Overrides bleiben erhalten).
- `engine_api.ts` – REST-Routen; liefert den Anzeige-Katalog in derselben Form wie die Seeds.
- `server.ts` – Express-Bootstrap; **self-seed** beim Start (idempotent).
- `db.ts` – Pool aus `DATABASE_URL` (Railway, SSL automatisch) oder `PG*`-Variablen; optionales Schema.
- `seed_catalogs.ts` / `seed_loader.ts` – Schema anlegen und die sechs Norm-Kataloge laden.
- `gbu_engine_schema.sql` – Datenmodell (21 Enums, 31 Tabellen).
- `norm_*.json` – neun Regelversionen (81-20, 81-80, 2026, EN 81-41, Cyber voll/minimal, **81-20 mehrfragig**, **Cyber komponentenbasiert**, **81-80 Bestand als Fragebogen**); dazu `norm_fahrtreppe.json` (noch nicht in `seed_catalogs.ts`).
- `gen_mf_catalog.py` + `mf_content/` – Generator und Inhalt des mehrfragigen Typs (Frage → Gefährdung mit Rollen, Anlagenmerkmale als Filter, Zahlenschwellen, Kompensation über Priorität). `gen_mf_review_xlsx.py` erzeugt daraus die Klärungsliste `GBU_MF_Klaerungsliste.xlsx` für die fachliche Gegenlesung.
- `gen_ft_catalog.py` + `ft_content/` – Generator und Inhalt des Typs **Fahrtreppen und Fahrsteige** (ein Typ, zwei Erhebungsbereiche: B Betrieb/Betreiber, I Instandhaltung; Umschalter `qa_teil_instandhaltung`). `gen_ft_review_xlsx.py` erzeugt `GBU_Fahrtreppe_Klaerungsliste.xlsx`, `ft_smoke.ts` prüft den Katalog gegen den Referenz-Evaluator.
- `gen_cy_catalog.py` + `cy_content/` – Generator und Inhalt des Typs **Cyber-GBU komponentenbasiert** (fünf Erhebungsbereiche A/Z/C/N/O; je Komponente „vorhanden → Schnittstellenkategorie → Zugang frei → Maßnahmen", unabhängige Sicherheitseinrichtung als Kompensation; 14 ZÜS-Prüfpunkte in `cy_zues_map.json`; Regelversion `cyber-mf-2026.2`, 25 Klärungen entschieden und alle 188 Regeln fachlich freigegeben 03.09.2026). `gen_cy_review_xlsx.py` erzeugt `GBU_Cyber_Klaerungsliste.xlsx`, `gen_cy_regelpruefung_xlsx.py`/`apply_cy_regelpruefung.py` bilden die Regelprüfung (Freigabe der Eigenregeln ohne Klärungspunkt), `cy_smoke.ts` prüft den Katalog gegen den Referenz-Evaluator (inkl. Lückensuche über alle Schnittstellen-/Maßnahmen-Kombinationen), `cy_catalog.test.ts` ist der E2E-Test gegen PostgreSQL. `catalog_check.py` bündelt die Konsistenz-/Schemaprüfung ohne Import-Nebenwirkungen.
- `ui/` – eigenständige Bewertungsoberfläche (`python3 ui/build_ui.py` → `ui/gbu_bewertung.html`), unterstützt Ein- und Mehrfragen-Kataloge.
- `flutter_ui/`, `dart_engine/` – Referenz-App und Dart-Port der Engine (nicht Teil des Server-Images).

## Endpunkte

`GET /health` · `GET /rule-versions` · `GET /rule-versions/:id/catalog` · `POST /assessments` · `PUT /assessments/:id/answers` · `POST /assessments/:id/evaluate` · `GET /assessments/:id/results` · `GET /assessments/:id`

## Lokal starten

```bash
npm install
# gegen eine Railway-DB (public URL) – oder PG*-Variablen setzen
export DATABASE_URL='postgresql://postgres:PASS@HOST.proxy.rlwy.net:PORT/railway'
npm start          # Server + Self-Seed
```

Der Server legt beim ersten Start Schema `gbu` an und lädt die Kataloge. `/health` → `{"ok":true}`.
Bei bestehenden Datenbanken laufen beim Start idempotente Spaltenerweiterungen (`applyMigrations`: `hazards.hazard_factor`, `hazards.person_groups`, `hazard_questions.applicable_expression`); fehlende Kataloge (z. B. der mehrfragige Typ) werden nachgeladen.

## Mehrfragiger Typ ändern

```bash
# Inhalt in mf_content/*.py anpassen, dann:
python3 gen_mf_catalog.py                    # -> norm_81_20_mf.json, mf_klaerung.json (validiert gegen rule_engine.schema.json)
python3 gen_mf_review_xlsx.py                # -> GBU_MF_Klaerungsliste.xlsx
node --experimental-strip-types mf_smoke.ts  # Smoke-Test gegen evaluator.ts
python3 gen_app_asset.py norm_81_20_mf.json  # -> gbu_aufzug_app/assets/engine/ (ohne QA-Felder)
python3 ui/build_ui.py                       # -> ui/gbu_bewertung.html
npm test                                     # Tests inkl. mf_catalog.test.ts (braucht PostgreSQL, PG*-Variablen)
```

Regelversion **`81-20-mf-2026.3`** (04.09.2026): Lückenschluss gegenüber
DIN EN 81-80 – fünf Gefährdungssituationen, die der Katalog bis dahin nicht
erhoben hat, mit ihrem Bezug in DIN EN 81-20 ergänzt:

| EN 81-80 | neue Gefährdung | DIN EN 81-20 |
|---|---|---|
| Nr. 9  | MF-T07 Fläche unterhalb der Schachttürschwelle | 5.2.5.3.2 |
| Nr. 26 | MF-T08 Rückhaltung der Türblätter | 5.3.5.3.2 |
| Nr. 35 | MF-T09 Verbindung mehrteiliger Türblätter | 5.3.11 |
| Nr. 45 | MF-K15 Fahrkorbbeleuchtung (100 lx) | 5.4.10.1 bis 5.4.10.3 |
| Nr. 57 | MF-M21 Notendschalter | 5.12.2 |

Damit 282 Fragen, 99 Gefährdungen, 387 Regeln. Die 20 neuen Regeln stehen auf
`quality_status = REVIEW_REQUIRED`, bis sie über `GBU_MF_Klaerungsliste.xlsx`
(Blatt „Regeln") gegengelesen sind.

## Fahrtreppen-Typ ändern

```bash
# Inhalt in ft_content/*.py anpassen, dann:
python3 gen_ft_catalog.py                    # -> norm_fahrtreppe.json, ft_klaerung.json (Schema-validiert)
python3 gen_ft_review_xlsx.py                # -> GBU_Fahrtreppe_Klaerungsliste.xlsx
node --experimental-strip-types ft_smoke.ts  # Smoke-Test gegen evaluator.ts
```

`ft_content/common.py` stellt die Register von `mf_content/common.py` (Erhebungs-
bereiche, Baugruppen, Fragen-Präfixe) in place auf den Fahrtreppen-Typ um.
Deshalb in einem Prozess **entweder** den MF- **oder** den FT-Katalog erzeugen –
die Generatoren laufen getrennt.

Fachlich abweichend von den Aufzugstypen: Fahrtreppen und Fahrsteige sind nach
BetrSichV Anhang 2 Nr. 2 ausdrücklich **keine** überwachungsbedürftigen Anlagen –
kein ZÜS-Pfad, kein TRBS-3121-Mapping. Maßgeblich sind ArbStättV/ASR A1.8,
BetrSichV § 3 und § 14, DIN EN 115-1/-2 sowie die DGUV Informationen 208-028,
208-029 und 209-085.

## Typ „Bestand nach DIN EN 81-80"

Eigenständiger GBU-Typ (Festlegung 04.09.2026), **abgeleitet** aus dem
mehrfragigen Katalog – gleiche Fragen, Gefährdungen, Regeln und Codes, nur
weniger Umfang:

```bash
python3 gen_en8180_catalog.py                # -> norm_81_80_mf.json (81-80-mf-2026.1)
python3 gen_app_asset.py norm_81_80_mf.json  # -> gbu_aufzug_app/assets/engine/
```

Umfang = die 68 Gefährdungen der 74 Gefährdungssituationen (aus
`en8180_content.ZUORDNUNG`) plus 18 organisatorische Gefährdungen (`ZUSATZ` in
`gen_en8180_catalog.py`: Unterlagen, Betreiberorganisation, Umfeld,
Sonderfunktionen), ohne die keine vollständige Beurteilung nach BetrSichV
entsteht. Ergebnis: **256 Fragen, 86 Gefährdungen, 341 Regeln** (MF: 282/99/387).
Der Generator prüft Schema und Konsistenz und stellt sicher, dass jede
übernommene Gefährdung, Frage und Regel **byteweise identisch** mit dem
MF-Katalog ist – der Typ kann nicht auseinanderlaufen. Weil die Codes gleich
sind, verliert ein Wechsel des GBU-Typs an einer Anlage keine Antworten.

In `seed_catalogs.ts` eingetragen (neunter Katalog).

## EN 81-80 als Sicht auf den mehrfragigen Katalog

Der GBU-Typ „vereinfacht (DIN EN 81-80, Bestand)" ist in der App eingefroren.
Sein Nachfolger im neuen Modell ist kein zweiter Fragebogen, sondern eine
**Sicht** auf den MF-Katalog: Eine Bestandsanlage wird einmal nach EN 81-20
(mehrfragig) erhoben, der Bericht weist den Nachrüstbedarf nach EN 81-80
zusätzlich mit Nummer, Abschnitt und Prioritätsstufe der Norm aus – gleiches
Muster wie der ZÜS-Abschlusscheck des Cyber-Fragebogens.

```bash
python3 gen_en8180_map.py     # -> en8180_map.json,
                              #    ../gbu_aufzug_app/lib/data/en8180_katalog.dart,
                              #    GBU_EN8180_Zuordnung.xlsx (Gegenlesung)
```

Inhalt in `en8180_content.py`: je Gefährdungssituation (1…74) Abschnitt,
eigene Kurzbezeichnung, zugeordnete MF-Gefährdungen und die Deckung
(`voll` / `teilweise` / `offen`). Grundlage sind Tabelle 1 der
DIN EN 81-80:2004-02 sowie Anhang A (Tabelle A.1 Risikoprofil, Tabelle A.2
Prioritäten und Zeitplan); die Prioritätsstufe wird aus A.1/A.2 berechnet
(erscheint eine Nummer mehrfach, gilt die höhere Stufe). Stand 04.09.2026:
**71 Punkte voll abgedeckt, 3 teilweise, keiner mehr offen** – die fünf Lücken
(Nr. 9, 26, 35, 45, 57) sind mit der Regelversion `81-20-mf-2026.3` im
MF-Katalog geschlossen. 68 der 99 MF-Gefährdungen haben eine Entsprechung in
EN 81-80; der MF-Katalog ist bewusst weiter gefasst (Umfeld, Gebäude,
Betreiberorganisation).

## Cyber-Typ ändern

```bash
# Inhalt in cy_content/*.py anpassen, dann:
python3 gen_cy_catalog.py                    # -> norm_cyber_mf.json, cy_klaerung.json, cy_zues_map.json
python3 gen_cy_review_xlsx.py                # -> GBU_Cyber_Klaerungsliste.xlsx
node --experimental-strip-types cy_smoke.ts  # Smoke-Test + Lückensuche gegen evaluator.ts
python3 gen_app_asset.py norm_cyber_mf.json  # -> gbu_aufzug_app/assets/engine/ (ohne QA-Felder)
python3 ui/build_ui.py                       # Prototyp (Katalog „Cyber-GBU komponentenbasiert")
```

Fachliche Freigabe der Regeln – zwei Wege, beide enden in `quality_status = VERIFIED`:

- **Klärungspunkte** (`cy_content/entscheidungen.py`): Regeln mit `KLÄREN:` in den
  notes werden verifiziert, sobald alle ihre Klärungen entschieden sind
  (25 Punkte, entschieden 03.09.2026).
- **Regelprüfung** (`cy_content/regelfreigabe.py`): die Eigenregeln ohne
  Klärungspunkt. `python3 gen_cy_regelpruefung_xlsx.py` legt sie als
  `GBU_Cyber_Regelpruefung.xlsx` vor (Blatt „Muster": die 6 Komponenten-Muster
  gelten für CY-C01…C10 gemeinsam; Blatt „Regeln": Einzelentscheidung geht vor).
  Rücklauf mit `python3 apply_cy_regelpruefung.py [xlsx] [--datum JJJJ-MM-TT]`,
  danach `gen_cy_catalog.py`. „Freigeben" → VERIFIED; „Ändern"/„Streichen"
  bleiben REVIEW_REQUIRED mit `OFFEN (…)`-Hinweis, bis der Inhalt in
  `cy_content/*.py` nachgezogen ist. Stand 03.09.2026: alle 98 freigegeben,
  188 von 188 Regeln VERIFIED.

`cy_content/common.py` stellt – wie `ft_content` – die Register von
`mf_content/common.py` in place um; pro Prozess nur einen Katalog erzeugen.
Alle Fragen und Gefährdungen tragen `domain = CYBER`. Grundlage: TRBS 1115
Teil 1, EK-ZÜS B-002 rev. 5 (Anhang 2) und BA-017, DEKRA-Ausfüllhilfe 09/2024,
BetrSichV § 3/§ 12, ÜAnlG. Methode nach Schindler-Muster (geteilte
Zugangsfragen als Modifier), aber fail-closed und mit erreichbarer Stufe Hoch.
Seit der Gegenlesung (03.09.2026) in `seed_catalogs.ts` eingetragen; Railway lädt
den Katalog beim nächsten Start (`bootstrapDb`).

## Railway-Deployment

1. Repo zu GitHub pushen (siehe unten).
2. In Railway **New → Deploy from GitHub repo** → dieses Repo wählen. Der `Dockerfile` wird automatisch verwendet; `railway.json` setzt Healthcheck `/health`.
3. Im neuen Service unter **Variables** die DB referenzieren:
   - `DATABASE_URL = ${{Postgres.DATABASE_URL}}` (interne URL des Postgres-Service; SSL wird automatisch aus erkannt).
   - Optional `PGSCHEMA=gbu` (Default ohnehin `gbu`).
4. Deploy abwarten. Der Server seedet sich beim ersten Start selbst (Schema + 6 Kataloge). Danach eine öffentliche Domain erzeugen (**Settings → Networking → Generate Domain**).

Die Engine lebt komplett im Schema `gbu` und berührt bestehende Tabellen in `public` nicht.

## App anbinden

```bash
cd flutter_ui
flutter run -d chrome --dart-define=GBU_API_BASE=https://DEIN-SERVICE.up.railway.app
```

Der Statuschip zeigt dann „Server"; Katalog und Persistenz kommen aus der Cloud.

## Absicherung (Auth + CORS)

Ohne Konfiguration ist die API offen (Entwicklung). Für den Produktivbetrieb:

- **`API_TOKENS`** (oder `API_TOKEN`) setzen – danach brauchen alle Endpunkte außer `/health` einen Token, per Header `Authorization: Bearer <token>` oder `X-API-Key: <token>`. Mehrere Tokens komma-getrennt (Rotation). `/health` bleibt offen für den Railway-Healthcheck.
- **`CORS_ORIGINS`** (komma-getrennt) beschränkt CORS auf bekannte Origins; ohne Angabe `*`.
- Die App sendet den Token per `--dart-define=GBU_API_TOKEN=<token>` (zusätzlich zu `GBU_API_BASE`).

## Variablen

Siehe `.env.example`: `DATABASE_URL`, `PGSCHEMA`, `PGSSL`, `SEED_ON_BOOT`, `PORT`, `API_TOKENS`, `CORS_ORIGINS`.

## Tests

```bash
npm test evaluator.test.ts engine_service.test.ts norm_catalog.test.ts engine_api.test.ts
```

Braucht ein erreichbares PostgreSQL (die E2E-Tests legen eigene Testdatenbanken an).
