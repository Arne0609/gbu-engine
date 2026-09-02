# GBU APP 4.0 – Datenmodell & Regelengine

Stand 31.08.2026. Grundlage: das Konzept „Fragebogen und Bewertungsengine
vollständig getrennt" und der Reverse-Engineering-Stand (Delta-Bericht 3,
M-Katalog + Engine-Regeln). Dieses Dokument beschreibt das gebaute Datenmodell
und wie die bekannten Fehler der untersuchten App strukturell vermieden werden.

> Stand nach Delta-Bericht 4: vier verbindliche Nachschärfungen eingebaut
> (siehe Abschnitt „Delta-4-Nachschärfungen").

## Dateien

- **`gbu_engine_schema.sql`** – vollständiges PostgreSQL-Schema (Greenfield):
  21 Enum-Typen, 31 Tabellen. Gegen PostgreSQL 16 lauffähig ausgeführt (0 Fehler).
- **`rule_engine.schema.json`** – JSON-Schema (Draft 2020-12) der kontrollierten
  Bedingungssprache, der Gefährdungen (inkl. Rollen + `required_mode`) und des
  Bewertungsregel-Objekts.
- **`seed_rules.json`** – 13 Gefährdungen und 14 rekonstruierte Regeln (M032;
  Cyber MC4 + Template MC4–MC9, MC11; Ortsblöcke M087/M090/M103; Kunden-
  befragung M088/M089/M091/M092/M093/M106/M108), gegen das Schema validiert.
- **`evaluator.ts`** – Referenz-Evaluator (`answers` + Regelwerk →
  `evaluation_results`), dependency-frei, portierbar nach Dart/Node.
- **`evaluator.test.ts`** – 18 Unit-Tests gegen die Decision Tables
  (`node --test --experimental-strip-types evaluator.test.ts`, 18/18 grün).
- **`dart_engine/`** – Dart-Portierung (`lib/gbu_engine.dart`) für die
  Flutter-Offline-Bewertung, ohne Flutter-Abhängigkeit; `test/evaluator_test.dart`
  spiegelt dieselben 18 Fälle gegen dieselbe `seed_rules.json`
  (`dart pub get && dart test`).
- **`engine_service.ts`** – Backend-Anbindung: lädt das Regelwerk der zugehörigen
  `rule_version`, liest die Antworten, ruft den Evaluator und schreibt
  `evaluation_results` + `assessment_summary` transaktional; schont bestehende
  `manual_overrides`. Enthält Express-Routen (`registerEngineRoutes`).
- **`seed_loader.ts`** – lädt ein Seed (rule_versions, questions +
  question_options, hazards, hazard_questions, evaluation_rules) in die DB,
  idempotent. Unterstützt SELECT-Fragen mit Antwortoptionen.
- **`gen_norm_catalog.py`** – Generator App-Katalog → Engine-Seed
  (`origin = NORM_DERIVED`): erzeugt `norm_81_80.json` (35 Gefährdungen/296
  Regeln), `norm_81_20.json` (63/331), `norm_2026.json` (23/213),
  `norm_en8141.json` (48/192). Abbildung: App-Kategorie → hazard; je Kategorie
  eine SELECT-Frage (`required_mode ALWAYS` → unbeantwortet = INCOMPLETE); je
  Istzustand eine Option + Regel (Ampel → risk_status; „Nicht anwendbar" →
  NOT_APPLICABLE). Sofort-/Mittelfristmaßnahme vorerst in `rule.notes`.
- **`norm_catalog.test.ts`** – E2E der importierten Kataloge gegen PostgreSQL:
  81-80 und EN 81-41 laden, auswählen, evaluieren. 2/2 grün.
- **`engine_service.test.ts`** – End-to-End gegen ein echtes PostgreSQL:
  frische DB aus dem Schema, Seed, Anlage/Beurteilung/Antworten, Persistenz
  prüfen. 2/2 grün.

## Die eine zentrale Entscheidung

Es wird **nie** eine Bewertung an einer Frage gespeichert. Der Weg ist immer:

```
Frage  →  Gefährdung (Rolle)  →  Regel  →  Risikostufe
```

Eine Frage kann beliebig viele Gefährdungen beeinflussen (`hazard_questions`,
m:n mit Rolle), eine Gefährdung entsteht aus mehreren Fragen. Die
**UI-Kategorie** (`question_categories`) ist reine Erhebungsstruktur und erzwingt
keine Bindung an die Gefährdungsstruktur – eine Frage unter „Schacht" darf
M035, M060 und M081 zugleich beeinflussen.

## Sechs Bewertungszustände statt vier

`risk_status = INCOMPLETE · NOT_APPLICABLE · NO_RISK · LOW · MEDIUM · HIGH`

Damit werden die zwei gravierenden Fehler der Original-App strukturell
unmöglich:

1. **Fehlende Antwort ≠ „Kein Risiko".** Eine noch nicht bewertbare Gefährdung
   ist `INCOMPLETE`, nicht `NO_RISK`. „Unvollständig" bekommt in der Auswertung
   und im UI eine eigene Kachel.
2. **Fehlende Pflichtantwort lässt eine Gefährdung nicht verschwinden.**
   Pflicht-Sein liegt **gefährdungsspezifisch** in
   `hazard_questions.required_mode` (`ALWAYS` → fehlt sie, `INCOMPLETE`).
   (Beleg: MC4–MC9 – eine unbeantwortete Schnittstellenfrage ließ im Original
   die ganze Gefährdung auf „Kein Risiko" zurückfallen – „PARTIAL_EVALUATION_BUG".)

## Referenz-Evaluator

`evaluator.ts` ist die ausführbare, seiteneffektfreie Umsetzung des
Auswertungsalgorithmus: `evaluate(ruleset, answers, opts) → results[]`. Bewusst
ohne Fremdabhängigkeiten, damit der Code 1:1 nach Dart (Flutter-Offline-
Bewertung) und ins Node-Backend übernommen werden kann. Fehlende Antworten
werden im Ausdruck als „falsch" (nie „unbekannt = wahr") behandelt, sodass ein
Ortsblock mit lauter leeren Fragen auf `NO_RISK` fällt statt zu triggern. Die
Option `includeOrigins: ['RECONSTRUCTED_ORIGINAL']` schaltet in einen
Reconstructed-only-Modus, der das beobachtete Original reproduziert (ohne die
eigenen `OWN_RULE`-Verbesserungen) – nützlich zum Abgleich gegen die
Reverse-Engineering-Befunde.

Die 18 Unit-Tests in `evaluator.test.ts` decken u. a. ab: M032-Decision-Table
in beiden Regelwelten, den MC4-Bug-Fix (`INCOMPLETE` statt `NO_RISK` bei
fehlender Pflichtfrage), den Ortsblock-Gegenpol (M087 `HIGH` trotz drei leerer
Fragen), Einzeltrigger, den A73-Modifier und die Statusübersicht.

## Auswertungsalgorithmus (je Gefährdung)

```
1. Applicability prüfen
     unbekannt        → INCOMPLETE
     nicht zutreffend → NOT_APPLICABLE
2. Pflichtfragen (rule_required_questions) prüfen
     eine fehlt       → INCOMPLETE
3. Regeln der Gefährdung auswerten (condition_expression)
     keine passt      → NO_RISK
4. Kompensations- und Modifier-Rollen berücksichtigen
5. höchste priority der zutreffenden Regeln gewinnt → result_status
6. evaluation_results schreiben (inkl. input_snapshot der genutzten Antworten)
```

Die Reihenfolge ist bewusst: erst Anwendbarkeit, dann Vollständigkeit, erst
dann Risiko. So kann eine unvollständige Anlage nie „grün" wirken.

## Kontrollierte Bedingungssprache

Regeln enthalten **keinen** frei ausführbaren Code, sondern einen JSON-
Ausdrucksbaum (`rule_engine.schema.json`): Knoten sind `all` (UND), `any` (ODER),
`not`, Blätter sind `{ question, operator, value }` mit den Operatoren
`EQ · NEQ · GT · GTE · LT · LTE · IN · NOT_IN · ANSWERED · NOT_ANSWERED`. Fragen
werden über ihren stabilen `code` referenziert, nie über `legacy_id` (f033…).
Das Schema erzwingt u. a., dass `EQ` einen Wert hat, `IN` ein Array bekommt und
je Knoten genau ein Operator steht – fehlerhafte Regeln werden abgewiesen.

## Delta-4-Nachschärfungen

1. **`required` gefährdungsspezifisch, nicht global/regelweit.**
   `hazard_questions` hat `required_mode` (`NEVER · ALWAYS · CONDITIONAL`).
   Dieselbe Frage kann in einer Gefährdung Pflicht und in einer anderen
   optional sein: die Ortsfragen von M087/M090/M103 sind `NEVER` (eine Ja-
   Antwort genügt), die Schnittstellenfragen von MC4–MC9 sind `ALWAYS`. Eine
   eigene `rule_required_questions`-Tabelle entfällt.
2. **Aggregation als Gefährdungseigenschaft.** `hazards.aggregation_type`
   (`ANY/ALL/MAXIMUM/…`) und `hazards.evaluation_mode`
   (`STANDARD · PARTIAL_ALLOWED · STRICT_REQUIRED`). Für M087/M090/M103 ist
   `ANY / PARTIAL_ALLOWED` belegt (Delta 4, HIGH_CONFIDENCE). Eine Regel darf
   die Aggregation überschreiben, erbt sie sonst von der Gefährdung.
3. **Mangeltyp-×-Ort-Matrix** als `defect_types` × `hazard_locations`
   (ACCESS/MACHINE_ROOM/SHAFT_CAR/PIT/OTHER) mit optionaler Verknüpfung
   `question_defect_context`. Bildet die a-ID-Systematik ab (a4xx = Grube,
   z. B. a447 „brandfördernd in der Grube").

## Zwei Regelwelten + Qualitätsstatus

Drei getrennte Dimensionen an `evaluation_rules`:

- **`origin`** – welche Welt: `RECONSTRUCTED_ORIGINAL` · `NORM_DERIVED` ·
  `OWN_RULE`.
- **`evidence_level`** – wie gut das *Original*-Verhalten belegt ist:
  `DIRECT · HIGH_CONFIDENCE · INFERRED · HYPOTHESIS`.
- **`quality_status`** – unsere *fachliche Haltung*: `VERIFIED ·
  REVIEW_REQUIRED · KNOWN_BUG · NOT_IMPLEMENTED`.

Beispiel M032: die rekonstruierte Regel „kein Notruf → HOCH" ist
`RECONSTRUCTED_ORIGINAL / DIRECT / REVIEW_REQUIRED` (fachlich fragwürdig, dass
ein nicht aufgeschalteter Notruf „kein Risiko" ergibt); die Ziel-Verbesserung
„Notruf ohne 24h-Aufschaltung → MITTEL" liegt als `OWN_RULE / REVIEW_REQUIRED`
daneben und wird erst nach normativer Prüfung aktiv. So bleiben bewusst nicht
übernommene Original-Fehler (`KNOWN_BUG`) und fehlende Gefährdungen wie MC13
(`NOT_IMPLEMENTED`) dokumentiert, ohne die eigene Logik zu verfälschen.

## Maßnahmen, Übersteuerung, Quellen

- **Maßnahmen** stehen nicht in der Regel, sondern in `measures` + `rule_measures`
  mit UND/ODER-Gruppen und optionaler Bedingung („organisatorische Maßnahme nur,
  wenn kein besonderer Nutzerkreis betroffen").
- **Manuelle fachliche Bewertung**: der Sachverständige darf das Engine-Ergebnis
  ändern, aber nur mit Pflichtbegründung (`manual_overrides`); Automatik- und
  Manuell-Status stehen beide im `evaluation_results`.
- **Quellen** hängen an Gefährdung (`hazard_sources`) und Regel (`rule_sources`)
  – so ist im Bericht/Admin nachvollziehbar, warum eine Regel existiert.

## Versionierung & Reproduzierbarkeit

Jede GBU hängt an genau einer `rule_versions`-Zeile. `evaluation_results`
speichert `rule_version_id`, `matched_rule_id` und einen `input_snapshot` der
tatsächlich verwendeten Antworten. Ein späteres Regel-Update ändert nie
rückwirkend einen abgeschlossenen Bericht; ein fertiger Bericht ist exakt
reproduzierbar. `audit_log` (Daten) und `rule_change_log` (Regelwerk)
protokollieren Änderungen getrennt.

## Abschlussregel

`assessment_summary.hazards_incomplete > 0` blockiert die Finalisierung. Ein
Zwischenbericht ist jederzeit möglich; ein finaler Bericht nur bei null
unvollständigen Gefährdungen – oder mit bewusster, begründeter Freigabe.

## Verhältnis zur aktuellen App

Das ist ein **Neuaufbau der Bewertungsschicht**, kein Migrationspatch am
jetzigen `gbu_aufzug_app`/`gbu_backend`. Die heutige App speichert
Gefährdungen mit direkt zugeordneter Ampel (`IstzustandOption`, `AmpelBewertung`)
und festen `BereichsTyp`-Bereichen – funktional, aber ohne die
Frage↔Gefährdung-Trennung. Migrationsweg (später, nicht Teil dieses Schritts):
bestehende Kataloge (81-80/81-20/EN 81-41, Cyber) als `questions` + `hazards` +
`evaluation_rules` mit `origin = NORM_DERIVED` abbilden; die vier heutigen
Ampelwerte auf `risk_status` mappen (Grün→NO_RISK, Gelb→MEDIUM/LOW, Rot→HIGH,
Grau→NOT_APPLICABLE) und fehlende Einträge als `INCOMPLETE` führen.

## Nächste sinnvolle Schritte

Erledigt: Referenz-Evaluator (`evaluator.ts`, 18/18), Dart-Portierung
(`dart_engine/`), Backend-Anbindung (`engine_service.ts`, E2E 2/2 gegen
PostgreSQL 16).

1. Fragenkatalog aufbauen (`questions` + `question_options` + Sichtbarkeits-
   regeln) und die vier GBU-Typen der heutigen App als `hazards` +
   `evaluation_rules` (`origin = NORM_DERIVED`) einspeisen.
2. Integration: Flutter zeigt auf `dart_engine`, das Backend bindet
   `registerEngineRoutes` ein; Bewertungsübersicht + Gefährdungsdetail bauen.
3. Restlicher Regelbestand: der Katalog ist arithmetisch geschlossen
   (M001–M120 + M019a/M019b/M020a/M024a = 124); die 23 offenen M-Kennungen im
   technischen Teil werden gezielt ergänzt, wenn im Eigenbau gebraucht.

## Validierung dieses Stands

- `gbu_engine_schema.sql` gegen **PostgreSQL 16** ausgeführt: 31 Tabellen,
  21 Enum-Typen, 0 Fehler.
- `rule_engine.schema.json` als **JSON-Schema Draft 2020-12** geprüft;
  `seed_rules.json` (13 Gefährdungen, 14 Regeln) dagegen validiert.
- Querchecks bestanden: jede Regel referenziert eine definierte Gefährdung,
  jede Gefährdung hat mindestens eine Regel, und **jeder Enum-Wert im Seed
  existiert in den Postgres-Enums**.
- Negativtests werden korrekt abgewiesen: fehlender Wert, zwei Operatoren je
  Knoten, unbekannter Status/Operator, entfernte Rolle `REQUIRED`, ungültiges
  `required_mode`, `CONDITIONAL` ohne `required_when`, alte Enum-Werte
  (`RECONSTRUCTED`, `UNVERIFIED`).
