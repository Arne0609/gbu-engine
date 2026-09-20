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
- `norm_*.json` – elf Regelversionen (81-20, 81-80, 2026, EN 81-41, Cyber voll/minimal, **81-20 mehrfragig**, **Cyber komponentenbasiert**, **81-80 Bestand als Fragebogen**, **Variante Riedl** GBU + Cyber); dazu `norm_fahrtreppe.json` (noch nicht in `seed_catalogs.ts`).
- `gen_mf_catalog.py` + `mf_content/` – Generator und Inhalt des mehrfragigen Typs (Frage → Gefährdung mit Rollen, Anlagenmerkmale als Filter, Zahlenschwellen, Kompensation über Priorität). `gen_mf_review_xlsx.py` erzeugt daraus die Klärungsliste `GBU_MF_Klaerungsliste.xlsx` für die fachliche Gegenlesung.
- `gen_ft_catalog.py` + `ft_content/` – Generator und Inhalt des Typs **Fahrtreppen und Fahrsteige** (ein Typ, drei Erhebungsbereiche: B Betrieb/Betreiber, I Instandhaltung, N Bestandsanlage nach DIN EN 115-2 Anhang B; Umschalter `qa_teil_instandhaltung` und `qa_teil_en115_2`). `gen_ft_review_xlsx.py` erzeugt `GBU_Fahrtreppe_Klaerungsliste.xlsx`, `ft_smoke.ts` prüft den Katalog gegen den Referenz-Evaluator.
- `gen_cy_catalog.py` + `cy_content/` – Generator und Inhalt des Typs **Cyber-GBU komponentenbasiert** (fünf Erhebungsbereiche A/Z/C/N/O; je Komponente „vorhanden → Schnittstellenkategorie → Zugang frei → Maßnahmen", unabhängige Sicherheitseinrichtung als Kompensation; 14 ZÜS-Prüfpunkte in `cy_zues_map.json`; Erhebungskarten in `cy_content/karten.py`; Regelversion `cyber-mf-2026.3`, 25 Klärungen entschieden, 187 von 190 Regeln freigegeben – offen sind seit dem Prüfbericht 20.09.2026 zwei neue Auffangregeln (CY-Z04, CY-N01) und die in der Priorität geänderte CY-C12-R3). `gen_cy_review_xlsx.py` erzeugt `GBU_Cyber_Klaerungsliste.xlsx`, `gen_cy_regelpruefung_xlsx.py`/`apply_cy_regelpruefung.py` bilden die Regelprüfung (Freigabe der Eigenregeln ohne Klärungspunkt), `cy_smoke.ts` prüft den Katalog gegen den Referenz-Evaluator (inkl. Lückensuche über alle Schnittstellen-/Maßnahmen-Kombinationen), `cy_catalog.test.ts` ist der E2E-Test gegen PostgreSQL. `catalog_check.py` bündelt die Konsistenz-/Schemaprüfung ohne Import-Nebenwirkungen.
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

Regelprüfung vom 20.09.2026: Die 354 Regeln, die durch die Inhaltsänderungen
auf `REVIEW_REQUIRED` zurückgefallen waren, sind Regel für Regel gegen den
Normbezug geprüft (14 Prüfagenten je Erhebungsbereich, dazu je Paket eine
adversarische Gegenprüfung, die die Beanstandungen zu widerlegen versucht).
Ergebnis: **270 freigegeben, 82 zu ändern, 2 zu streichen**. Die 84 Punkte
betrafen fast ausschließlich Stufen, die der eigene Stufenmaßstab nicht trägt,
Sofortmaßnahmen, die nicht sofort wirken, und Verstöße gegen das TOP-Prinzip;
jede Korrektur steht als Hinweis an der Regel und im Blatt „Zu ändern" von
`GBU_MF_Regelpruefung_Ergebnis_2026-09-20.xlsx`.

**66 davon sind umgesetzt** (alles, was ohne neue Frage oder neue Antwortoption
auskommt): 9 Regeln entfallen ersatzlos (MF-D06-R1/-R2/-R3, MF-F01-R5,
MF-K01-R7, MF-K10-R2, MF-M17-R1, MF-T06-R9, MF-U12-R2), die übrigen sind in
Stufe, Maßnahmentext oder Maßnahmenart berichtigt; dazu kommen fünf
Fragenberichtigungen (5.7b Sicherheitsabstand nach ASR A2.1, 5.12c 2,00 m →
1,80 m nach DIN EN 81-20 5.2.3.3, 7.9 „ausschließlich Drahtglas?", 10.2 mind.
50 lx, 10.11 auch beim Seil-Hydraulikaufzug) und die Hilfetexte zu 5.10 und
5.44. Jede geänderte Regel trägt eine Notiz „Regelprüfung 20.09.2026: …", die
den Befund und die Entscheidung nennt. Damit stehen im MF-Katalog **397 von 415
Regeln auf `VERIFIED`** (Riedl: 274 von 282), im Cyber-Katalog alle 190.

Die **18 Punkte, die die Erhebung ändern**, sind nach Rücksprache in vier
Paketen ebenfalls umgesetzt (jede neue oder geänderte Frage ist fail-closed
ausgelegt: der unklare Fall bekommt die strengere Stufe, eine unbeantwortete
Pflichtfrage ergibt `INCOMPLETE`, nicht `NO_RISK`):

- **B1 – Asbest-Zustandsfrage** (MF-U01): Je Fundort (5.60a, 5.61a, 10.20a,
  11.20a) eine Zustandsfrage „fest gebunden und unbeschädigt | schwach gebunden,
  beschädigt oder abriebbelastet | Zustand nicht beurteilbar". Hoch bei den
  beiden letzten, Mittel beim fest gebundenen Fund; im Triebwerksraum eine
  vierte Option für asbesthaltige Bremsbeläge und Bremsstaub (immer Hoch, Abrieb
  im bestimmungsgemäßen Betrieb). Vorher gab jeder Fund Hoch.
- **B2 – Kompensationsfragen für Gefahrstofftransporte** (MF-U05): 15.32a bis
  15.35a nach dem Muster von MF-U06 und MF-U12. Geregelt und unterwiesen ergibt
  **Niedrig, nicht Kein Risiko** – Fortschreibung und Unterweisung bleiben nach
  GefStoffV § 14 geschuldet. Vorher erzeugte allein die Nutzungsart einen
  Dauerbefund Mittel.
- **B3 – gebündelte Fragen getrennt**: 11.10a Puffer als Auswahlfrage
  (Funktionsverlust = Hoch, Verschleiß bei erhaltener Funktion = Mittel),
  11.10c/11.10d Ölstand und Kennzeichnung getrennt (Mittel / Niedrig),
  6.10a/6.10b Absperrventil Zugänglichkeit und Kennzeichnung getrennt
  (Mittel [TECH] / Niedrig [ORGA]).
- **B4 – zu weite Bedingungen** (7 Regeln): 6.11a Absturzsicherung nach
  DIN EN 81-20 Tabelle 12 (Drossel und Fangvorrichtung mit Begrenzer sind
  zulässige Alternativen zum Leitungsbruchventil), 7.9b Glasfläche über
  Sichtfenstergröße (150 mm nach 5.3.7.2.1 a) 4)), 11.15 als Auswahlfrage
  (stehendes Wasser an Bauteilen und „nicht beurteilbar" = Hoch, bloße Feuchte =
  Mittel), 15.8d als Optionsfrage (Rettung behindert = Hoch, nur Betrieb
  behindert = Mittel), 15.9a mit getrennter Option „Funktion unklar oder kein
  Nachweis" (Mittel statt Hoch), 15.10a/15.10b Löschanlage auf den prüfbaren
  Sachverhalt umgestellt, 15.24a wirksame Lüftung als Kompensation.

Damit stehen **alle 432 Regeln des MF-Katalogs auf `VERIFIED`** (EN 81-80: 429,
Riedl GBU: 287, Cyber: 190, Riedl Cyber: 116).

Maßnahmenarten, bei denen die Heuristik in `common.massnahmenart()` an der
Wortstellung scheitert (Maßnahmen, die eine technische und eine organisatorische
Komponente nennen), stehen seit der Regelprüfung von Hand in
`mf_content/massnahmenart.py`; `common.py` zieht die Tabelle vor die Heuristik.

**Am Normtext nachgeschlagen** (DIN EN 81-20:2014 und EN 81-1:1998 aus dem
Normenbestand, nicht aus Sekundärquellen) – zwei Punkte, bei denen die
Regelprüfung eine Zahl oder Fundstelle offengelassen hatte, und einer, an dem
sie selbst danebenlag:

- **Tabelle 11** (Treibscheiben-, **Trommel-** und Kettenaufzüge) nennt für den
  freien Fall des **Fahrkorbs** ausschließlich den Geschwindigkeitsbegrenzer
  (5.6.2.2.1) als Betätigungsmittel. Die Alternative „für Nenngeschwindigkeiten
  bis 1 m/s ausgelöst durch Bruch der Tragmittel (5.6.2.2.2) oder das
  Sicherheitsseil (5.6.2.2.3)" gilt dort **nur für Gegengewicht und
  Ausgleichsgewicht** – wortgleich in EN 81-1:1998 9.8.3.1. Ein erster Entwurf
  dieser Regelprüfung hatte daraus eine allgemeine Alternative für Trommel- und
  Hydraulikaufzüge gemacht und MF-S05-R2 auf die Treibscheibe eingeengt; das
  hätte beim Trommelaufzug eine Lücke gerissen und ist zurückgenommen.
- **Tabelle 12** lässt beim **indirekt angetriebenen** Hydraulikaufzug drei
  Kombinationen zu; zwei kommen ohne Begrenzer aus, verlangen dann aber
  Leitungsbruchventil (5.6.3) oder Drossel (5.6.4) zusammen mit einer durch
  Tragmittelbruch oder Sicherheitsseil ausgelösten Fangvorrichtung. Dafür stehen
  jetzt die Fragen 10.8a und 6.11a. Die Schlaffseil-/Schlaffkettenüberwachung
  (10.11) ist nach **5.5.5.3 b)** eine eigenständige elektrische
  Sicherheitseinrichtung und ausdrücklich **kein** Auslösemittel der
  Fangvorrichtung.
- **Anschlagpunkte**: DIN EN 81-20 **5.2.1.7 „Hebezeuge"**; Vorgänger ist
  EN 81-1:1998 **6.3.7 „Hebezeuge für Aufzugsteile"**, die Angabe der
  Tragfähigkeit verlangt dort **15.4.5**.
- **Einzugsschutz an Glas-Schiebetüren**: DIN EN 81-20 5.3.6.2.2.1 i) fordert
  ihn nur für Glasscheiben, die größer sind als die Sichtfenster nach 5.3.7.2;
  deren Breite ist nach **5.3.7.2.1 a) 4)** auf 60 bis 150 mm begrenzt. Damit
  ist die 150-mm-Grenze in Frage 7.9b belegt.

Vier mechanische Gegenproben laufen seither bei jeder Änderung mit und melden,
was eine fachliche Durchsicht nicht sieht:

```bash
node --experimental-strip-types mf_luecken.ts      # Regellücken (alle Antwortkombinationen je Gefährdung)
node --experimental-strip-types mf_inversionen.ts  # bei NONE: niedrigere Stufe verdrängt höhere
node --experimental-strip-types mf_tote_regeln.ts  # Regeln ohne erfüllbare Bedingung / nie maßgeblich
node --experimental-strip-types mf_optionen.ts     # Antwortwerte, die keine Mangelregel auswertet
```

Stand 20.09.2026 (nach Umsetzung aller Korrekturen): 0 Regellücken (101 520
Kombinationen), 17 Prioritätsinversionen – alle mit dokumentierter Kompensation
–, keine Regel ohne erfüllbare Bedingung und 43 Antwortwerte ohne Mangelregel.
Gefährdungen mit sehr vielen Antwortkombinationen (MF-T06, MF-U01, MF-SF01)
werden ausgedünnt geprüft; `mf_tote_regeln.ts` kennzeichnet Treffer aus diesen
Gefährdungen ausdrücklich als nachzuprüfen, weil sie Stichprobenartefakte sein
können.
`mf_optionen.ts` schließt eine Lücke der beiden erstgenannten Tests: Die 95
maschinell erzeugten Auffangregeln („Ankerfrage ist beantwortet → Kein Risiko")
setzen die `rule_gap`-Erkennung der Engine außer Kraft, weil immer eine Regel
trifft. Eine neue Antwortoption erscheint deshalb nicht als Fehler, sondern als
grünes Ergebnis – `mf_optionen.ts` prüft deshalb nicht das Ergebnis, sondern die
Abdeckung der Antwortwerte.

Regelversion **`81-20-mf-2026.10`** (20.09.2026): Prüfung des Fragenkatalogs
der Variante „Riedl" (53 Befunde zu Dopplungen, unnötigen Schritten, unklaren
Bedingungen und Bewertungslücken). Geändert wurde der INHALT, nicht die
Mechanik; die Regel-IDs bleiben, inhaltlich geänderte Regeln fallen über den
Fingerabdruck auf `quality_status = REVIEW_REQUIRED` zurück (zunächst 354 von
415, davon 94 Auffangregeln; nach der Regelprüfung und der Umsetzung ihrer
Korrekturen sind es noch 18 – Gegenlesung über `GBU_MF_Regelpruefung.xlsx`).
Das Wichtigste:

- **Bewertungslücken geschlossen** – MF-M13 bewertet jetzt auch ein merkliches
  Absinken bei vorhandener Kolbenabsinkverhinderung (6.12 = Ja **und** 6.13 =
  Ja); MF-D04 bewertet den ZÜS-Prüfbericht selbst (offene sicherheitsrelevante
  Mängel → Hoch, kein Bericht → Mittel); MF-Z07 hat für maschinenraumlose
  Anlagen ein Gegenstück zu 5.12a (abschließbarer Steuerschrank) und
  `qa_maschinenraum` als Modifier, damit keine Regellücke bleibt.
- **Annahmen hängen am Regelwerk, nicht am Baujahr** (Entscheidung Arne,
  20.09.2026). Der Nachweis ist die Norm, nach der die Anlage in Verkehr
  gebracht wurde (1.28); das Baujahr ist davon nur eine Ableitung – so steht es
  seit jeher im Hilfetext von 1.28, die Annahmen sind ihm nur nicht gefolgt.
  `common.norm_ab()` ersetzt `bj_ab()` in `annahme()` und schließt damit zwei
  Lücken: Eine 1985 gebaute, 2020 nach EN 81-20 modernisierte Anlage bekommt die
  Annahme jetzt, eine als TRA-Anlage dokumentierte mit Baujahr 2014 nicht mehr.
  Wo ein Regelwerk die Schwelle umspannt (EN 81-1/2 1999–2016, UCM-Anforderung
  ab 2012), entscheidet weiterhin das Baujahr; bei „Unbekannt" ebenfalls; eine
  unbeantwortete 1.28 trägt nichts.
- **fail-closed durchgezogen** – eine nicht nachgewiesene automatische
  Abschaltung senkt Hoch nicht mehr auf Mittel (MF-F03, MF-G08); acht Annahmen
  zu Zustands- und Kennzeichnungsfragen sind entfallen, weil das Baujahr über
  den Zustand nichts aussagt; 1.29 (Konformitätserklärung) ist ab Baujahr 1999
  Pflicht und ihre Abschaltbedingung positiv formuliert (eine unbeantwortete
  1.29 ließ vorher alle Annahmen greifen).
- **Nachweis-Vorbelegung begrenzt** – neue Liste `erhebung.NICHT_VORBELEGBAR`
  (Prüfpunkte 1, 22, 29): Die ZÜS prüft Bestandsanlagen gegen ihre
  Errichtungsgrundlage, deshalb belegt ihr Bericht keine Nachrüstthemen des
  Stands der Technik. Der Schutzraum (9.7, 11.3) wird jetzt zweifach vorbelegt –
  „normgerecht" ab Baujahr 2017, „altnorm" für 1999–2016 –, passend zu den
  eigenen Regeln MF-F04-R3 / MF-G02-R2. Dafür trägt ein Nachweis-Eintrag
  optional eine Zusatzbedingung (sechstes Element in `erhebung.NACHWEISE`);
  mehrere Vorbelegungen je Frage sind zulässig, solange die Bedingungen sich
  unterscheiden.
- **Türen und Fahrkorb** – 8.8 (Schließkantensicherung) wird nur noch bei
  kraftbetätigter Fahrkorbtür bewertet; die Option „Andere" bekommt eine eigene
  Regel statt still durchzulaufen; der Nutzerkreis „Kinder" wirkt jetzt
  einheitlich (auch bei fehlender Schließkantensicherung); 8.21 ist in
  „Brandfallsteuerung vorhanden" und „Auslösung/Einbindung" getrennt, damit die
  Maßnahme zum Befund passt; 8.23/8.24 sind Teilaspekte von 8.22 und entfallen
  bei normgerechter Ausführung nach EN 81-70; 8.28 ist auf denselben Umfang
  gebracht wie MF-K13/K14.
- **Dopplungen aufgelöst** – MF-K01 fasst drei wortgleiche Notruf-Regeln zu
  einer zusammen; 5.2/5.2a und 5.3a/5.3b sind Folgefragen mit eigener Maßnahme
  statt optionaler Fragen ohne Wirkung; 5.34 hat eine eigene Regel (Niedrig);
  10.13 ist in Türkontakt und Verriegelung getrennt; die Abgrenzungen 5.35/5.37
  und 15.23a/11.15 sind im Fragetext geschärft. 10.2 (Beleuchtung an den
  Schachtzugängen) fordert jetzt 50 lx statt 75 Lux – der alte Wert stammte aus
  dem übernommenen App-Katalog und widersprach der eigenen Quellenangabe
  DIN EN 81-20 5.3.7.1 (Entscheidung Arne, 20.09.2026).
- **Maßnahmen ortsbezogen** – die vier Ortsmatrix-Gefährdungen (MF-U02/U03)
  nennen in Sofort- und Folgemaßnahme jetzt den Ort („Schachtgrube: …"), statt
  vier Orte mit demselben Satz zu bedienen.

Regelversion **`81-20-mf-2026.9`** (17.09.2026): Erhebung gekürzt –
`mf_content/erhebung.py` (Fragengruppen als Karten, Nachweis-Vorbelegung aus
dem ZÜS-Prüfbericht über D05, Stammdaten aus dem Anlagenstamm, Phasen
stamm/vorab/vor_ort, vier Fragen gestrichen, sechs Zahlenfragen als
Schwellenfragen). Die Regeln, Regel-IDs und Freigaben bleiben; die Umstellung
der Schwellenfragen (8.10, 8.12, 8.14, 9.1, 9.3, 11.1) geschieht auf Seed-Ebene
und schreibt die betroffenen Bedingungen mechanisch um – in `mf_content/*.py`
stehen sie weiter als Zahlvergleiche. Seed-Felder `question_groups`,
`nachweise`, `category_phases`, `category_order`, je Frage `group`, `source`,
`stamm_key`; die Engine wertet unverändert Einzelfragen. Karten je Profil:
`python3 sim_karten.py`.

Erhebungsaufwand weiter gesenkt (17.09.2026, zweiter Durchgang): Karten statt
Einzelfragen auch dort, wo bisher Einzelkarten standen – 30 Fragen mit
eindeutigem unauffälligem Wert sind in die Ortskarten gewandert, vier Karten
sind neu (M17 Notendschalter, F07 Schutzraum Schachtkopf, T10 Türblätter,
K15 Beleuchtung im Fahrkorb). Auswahlfragen bekommen jetzt auch in den
Ortsbereichen einen `best_case` (AUSWAHL_SAMMELBEREICHE = SAMMELBEREICHE), und
`erhebung.KEIN_SAMMEL` nimmt davon aus, was Bauart-, Ausstattungs- oder
Prüfaussage ist (Pufferbauart, Art der Notrufeinrichtung/Notbeleuchtung,
Schutzraum Schachtkopf, Notendschalter, Erreichbarkeit für die Befreiung);
`erhebung.SCHWELLEN` bleibt ohnehin außen vor. `erhebung.DOKU_OPTIONAL` macht
zwei reine Dokumentationsfragen optional. Wirkung je Profil (`sim_karten.py`):
Karten vor Ort 70 → 58 (P2 48 → 44, P3 66 → 54), Einzelantworten vor Ort
39 → 22. Die App setzt mit „Keine weiteren Auffälligkeiten" seither auch
Auswahlpositionen mit `best_case`.

Prüfpunkte der ZÜS-Hauptprüfung (17.09.2026): Von den 31 Punkten in TRBS 1201
Teil 4, 3.3 (2) werden 25 für Vorbelegungen genutzt (47 Einträge in
`erhebung.NACHWEISE`). Neu ausgewertet wurden Nr. 1 (sicherer und ungehinderter
Zugang → 5.4 Durchgangsmaße) und Nr. 7 (Schutz gegen Quetschen, Scheren,
Einziehen von Händen → 7.10). Ohne Entsprechung im Katalog bleiben Nr. 15
(Seilführung, Seilendbefestigungen), 16 (Seilrollen, Umlenkrollen), 17
(Treibscheibe, Treibfähigkeit), 24 (Gegengewichtsausgleich) und 25
(Aufsetzvorrichtung); Nr. 28 (MSR, funktionale Sicherheit, Software-Stand)
liegt im Cyber-Fragebogen. Das ist entschieden, nicht übersehen (Arne,
17.09.2026): Diese Punkte betreffen den technischen Zustand von Tragmitteln
und Antrieb und bleiben der Wartung und der ZÜS-Hauptprüfung überlassen – die
Gefährdungsbeurteilung fragt die Schutzeinrichtungen ab, die bei deren
Versagen wirken (Fangvorrichtung Nr. 21, Begrenzer Nr. 12, Schlaffseil­
sicherung Nr. 11, Führungen Nr. 13). Festgehalten in
`erhebung.OHNE_KATALOGFRAGE`; der Generator meldet die Abdeckung bei jedem
Lauf und warnt, sobald ein Prüfpunkt weder genutzt noch dort begründet ist.

Sammelantwort im Umfeld (17.09.2026): Bereich U ist Sammelbereich – ein Klick
setzt Umfeld, Gebäude und Nutzung komplett auf den unauffälligen Wert; offen
bleiben nur Folgefragen nach einer Auffälligkeit (Ex-Schutz, Zugangskonzept).
Auswahlfragen bekommen dort einen `best_case` (Optionswert, Schema
`boolean|string`), reine Dokumentationsfragen den Wert aus
`erhebung.SAMMEL_DOKU`. Neu ist die Gegenprobe `mf_content/sammelantwort.py`:
Sie rechnet je Gefährdung alle Belegungen mit den Engine-Regeln durch und
streicht jeden `best_case`, der irgendwo ein schlechteres Ergebnis liefert –
das traf vier Kompensationsfragen (8.13, 9.6a, 11.14a, 15.25a), die vorher den
falschen Wert trugen. Der Generator meldet Gestrichenes und was laut Simulation
zusätzlich eindeutig wäre, setzt Letzteres aber nicht.

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

Ein Typ, drei Erhebungsbereiche, jeder über ein Anlagenmerkmal zuschaltbar:

| Bereich | Inhalt | Schalter |
|---|---|---|
| **B** | Betrieb und Nutzung (Betreiber-GBU) | immer |
| **I** | Instandhaltung, Montage, Reinigung | `qa_teil_instandhaltung` |
| **N** | Bestandsanlage nach DIN EN 115-2, Anhang B (74 Prüfpunkte) | `qa_teil_en115_2` |

Im Bereich N ergibt sich die Stufe aus der Prioritätsstufe der Norm
(H → Hoch, M → Mittel, N → Niedrig); der Zeitplan aus Tabelle A.2 steht in der
mittelfristigen Maßnahme. Wo Bereich B oder I dieselbe Sache schon fragt, wird
die vorhandene Frage wiederverwendet (`ref` in `ft_content/bestand_en115_2.py`) –
der Prüfpunkt wird daraus abgeleitet, niemand antwortet zweimal.

`ft_content/common.py` stellt die Register von `mf_content/common.py` (Erhebungs-
bereiche, Baugruppen, Fragen-Präfixe, Regel-ID-Registry) in place auf den
Fahrtreppen-Typ um. Deshalb in einem Prozess **entweder** den MF- **oder** den
FT-Katalog erzeugen – die Generatoren laufen getrennt. Die stabilen Regel-IDs
des Typs liegen in `ft_content/regel_ids.json`.

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

## Variante „Riedl" (VFA-Umfang, abgeleitet)

GBU-Variante für Riedl Aufzüge (Festlegung 17.09.2026), die die beiden bislang
genutzten Excel-Vorlagen ersetzt (VFA „GBU Anlage leer" R 1.7.2 und „Vorlage
GBU Cybersicherheit ab 04-26"). **Abgeleitet** aus dem mehrfragigen Katalog
und dem Cyber-Katalog – gleiche Fragen, Gefährdungen, Regeln, Maßnahmen,
Karten und Nachweise mit denselben Codes, nur weniger Umfang, plus die
Blattstruktur der Vorlage für den Bericht:

```bash
python3 gen_riedl_catalog.py                    # -> norm_riedl_mf.json (riedl-mf-2026.2),
                                                #    norm_riedl_cyber.json (riedl-cyber-2026.2),
                                                #    riedl_map.json (Blätter, Zeilen, Ampel, Texte)
python3 gen_riedl_review_xlsx.py                # -> GBU_Riedl_Zuordnung.xlsx (Gegenlesung)
python3 gen_riedl_fragenkatalog_xlsx.py         # -> GBU_Riedl_Fragenkatalog.xlsx (Fragen, Regeln,
                                                #    Karten, Annahmen, Nachweise mit Logik im Klartext)
node --experimental-strip-types riedl_smoke.ts  # Struktur, Deckungsgleichheit, Ampel, leerer Bogen
python3 gen_app_asset.py norm_riedl_mf.json     # -> gbu_aufzug_app/assets/engine/
python3 gen_app_asset.py norm_riedl_cyber.json  #    (riedl_map.json unverändert als Asset kopieren)
```

Inhalt in `riedl_content.py`: sechs Blätter (Kabine, Zugang, Maschinenraum,
Kabinendach, Fahrschacht/Schachtgrube, Cybersicherheit) mit den Zeilen der
Vorlage; je Zeile die MF- bzw. CY-Gefährdungen, die sie bilden. Umfangsregel:
VFA-Zeile **oder** TRBS-3121-Anhang-1-Punkt (alle 22 vertreten) **oder**
Betreiberpflicht des Deckblatts; alles andere steht mit Begründung in
`NICHT_ENTHALTEN` – der Generator bricht ab, wenn eine Gefährdung weder
zugeordnet noch begründet ist. Ergebnis (Stand 20.09.2026): **209 Fragen,
63 Gefährdungen, 287 Regeln, 65 Karten** (MF: 313/100/432/83) und **58 Fragen,
19 Gefährdungen, 116 Regeln, 11 Karten** (CY: 83/27/190/16). Bewertung:
Engine-Stufe als Ampel (Kein Risiko/Niedrig = Grün, Mittel = Gelb, Hoch = Rot;
unvollständig = offen), Blatt- und Gesamtampel nach der Deckblatt-Formel der
Vorlage.

Brücke zur Riedl-Matrix W×S→R (festgelegt 20.09.2026, `riedl_content.py`): Die
Engine-Stufe ist führend, die Risikozahl R wird daraus abgeleitet
(`r_aus_stufe`: Kein Risiko → 0, Niedrig → 1, Mittel → 5, Hoch → 7) und ist im
Bericht überschreibbar; die Umkehrung `stufe_aus_r` (R ≥ 7 Hoch, ≥ 3 Mittel,
≥ 1 Niedrig, 0 Kein Risiko) entspricht der App. R = 10 entsteht nur durch
manuelle Verschärfung. Damit stehen nicht mehr zwei Bewertungssysteme
nebeneinander.

`katalog_teilmenge.py` ist das gemeinsame Ableitungsverfahren (wie
`gen_en8180_catalog.py`, aber importierbar); es nimmt auch die Steuerfragen
der begründeten Annahmen und Nachweise mit (Baujahr, Konformitätsnachweis,
ZÜS-Bericht), sonst würde die Teilmenge anders bewerten als das Original –
`riedl_smoke.ts` prüft das auf 300 zufälligen Antwortsätzen je Katalog.
In `seed_catalogs.ts` eingetragen (zehnter und elfter Katalog).

## Cyber-Typ ändern

```bash
# Inhalt in cy_content/*.py anpassen, dann:
python3 gen_cy_catalog.py                    # -> norm_cyber_mf.json, cy_klaerung.json, cy_zues_map.json
python3 gen_cy_review_xlsx.py                # -> GBU_Cyber_Klaerungsliste.xlsx
node --experimental-strip-types cy_smoke.ts  # Smoke-Test + Lückensuche gegen evaluator.ts
python3 gen_app_asset.py norm_cyber_mf.json  # -> gbu_aufzug_app/assets/engine/ (ohne QA-Felder)
python3 ui/build_ui.py                       # Prototyp (Katalog „Cyber-GBU komponentenbasiert")
```

Regelversion **`cyber-mf-2026.3`** (20.09.2026), aus derselben Prüfung:
Prioritätsinversion in CY-C12 behoben (bei der Aggregation `NONE` gewann die
Niedrig-Regel „Fernzugriff ohne Freigabe" über die Mittel-Regeln zu fehlender
Segmentierung und Authentifizierung – jetzt P300/P290/P280 nach Schwere);
CY-N01 stuft „Softwarestand nicht bekannt" höher ein (wer den Stand nicht
kennt, kann auch nicht beurteilen, ob er trägt); 4.2 wird nur noch bei
vorhandener Fernwartung gefragt; die Doppelfrage 2.5 ist in
„Werkszugangsdaten in Gebrauch" und „Zugangsdaten dem Betreiber bekannt"
getrennt; die vier ZÜS-Dokumentationsfragen 5.11–5.14 halten die Erhebung
nicht mehr auf (`required_mode = NEVER`), fehlen aber sichtbar im Bericht;
4.1/4.3/4.4 sagen im Hinweistext, dass sie kanalübergreifend nach dem
schlechtesten Fall zu beantworten sind. Neu ist `cy_content/karten.py`:
16 Erhebungskarten (Riedl: 11) über die 83 Cyber-Fragen. Anders als im
81-20-Typ sind alle Positionen `native` und keine Karte ist eine `checklist` –
Cyber-Befunde sind keine Sichtprüfung, ein Sammel-„unauffällig" würde
unbelegte Tatsachen behaupten. Die Bewertung ändert sich dadurch nicht.

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
