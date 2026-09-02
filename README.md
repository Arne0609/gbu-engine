# GBU 4.0 – Bewertungsengine (Engine + REST-API)

Engine-getrennte Gefährdungsbeurteilung für Aufzüge: **Frage → Gefährdung → Regel → Risikostufe**. Fragebogen und Bewertung sind vollständig getrennt; eine fehlende Antwort ist `INCOMPLETE` (nicht „kein Risiko"). Sechs Zustände: `INCOMPLETE, NOT_APPLICABLE, NO_RISK, LOW, MEDIUM, HIGH`.

Dieses Verzeichnis enthält die Engine, die REST-API und die Referenz-UI. Der Server läuft ohne Build-Schritt (Node 22, Type Stripping).

## Bestandteile

- `evaluator.ts` – reiner Auswerter (Applicability → Pflichtfragen → Regeln → Aggregation).
- `engine_service.ts` – Katalog/Antworten aus der DB, transaktionale Bewertung (Overrides bleiben erhalten).
- `engine_api.ts` – REST-Routen; liefert den Anzeige-Katalog in derselben Form wie die Seeds.
- `server.ts` – Express-Bootstrap; **self-seed** beim Start (idempotent).
- `db.ts` – Pool aus `DATABASE_URL` (Railway, SSL automatisch) oder `PG*`-Variablen; optionales Schema.
- `seed_catalogs.ts` / `seed_loader.ts` – Schema anlegen und die sechs Norm-Kataloge laden.
- `gbu_engine_schema.sql` – Datenmodell (21 Enums, 31 Tabellen).
- `norm_*.json` – sechs Regelversionen (81-20, 81-80, 2026, EN 81-41, Cyber voll/minimal).
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
