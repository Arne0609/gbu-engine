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
- `norm_*.json` – sieben Regelversionen (81-20, 81-80, 2026, EN 81-41, Cyber voll/minimal, **81-20 mehrfragig**).
- `gen_mf_catalog.py` + `mf_content/` – Generator und Inhalt des mehrfragigen Typs (Frage → Gefährdung mit Rollen, Anlagenmerkmale als Filter, Zahlenschwellen, Kompensation über Priorität). `gen_mf_review_xlsx.py` erzeugt daraus die Klärungsliste `GBU_MF_Klaerungsliste.xlsx` für die fachliche Gegenlesung.
- `gen_ft_catalog.py` + `ft_content/` – Generator und Inhalt des Typs **Fahrtreppen und Fahrsteige** (ein Typ, zwei Erhebungsbereiche: B Betrieb/Betreiber, I Instandhaltung; Umschalter `qa_teil_instandhaltung`). `gen_ft_review_xlsx.py` erzeugt `GBU_Fahrtreppe_Klaerungsliste.xlsx`, `ft_smoke.ts` prüft den Katalog gegen den Referenz-Evaluator.
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
python3 gen_mf_catalog.py        # -> norm_81_20_mf.json, mf_klaerung.json (validiert gegen rule_engine.schema.json)
python3 gen_mf_review_xlsx.py    # -> GBU_MF_Klaerungsliste.xlsx
python3 ui/build_ui.py           # -> ui/gbu_bewertung.html
npm test                         # 43 Tests inkl. mf_catalog.test.ts (braucht PostgreSQL, PG*-Variablen)
```

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
