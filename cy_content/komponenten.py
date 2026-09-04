# -*- coding: utf-8 -*-
"""C – Komponenten und Schnittstellen. Je sicherheitsrelevanter Komponente eine
Gefährdung nach dem Muster

    vorhanden? → höchste Schnittstellenkategorie → Zugang frei? (geteilt, Z)
    → Schutzmaßnahmen (keine / teilweise / umgesetzt) → [unabhängige
    Sicherheitseinrichtung als Kompensation]

Komponentenliste = zues-Katalog der App (EK-ZÜS B-002 rev. 5 / BA-017), ergänzt
um Gateway/Router/Modem und die Gebäudeschnittstelle (TRBS-1115-1-Prüffelder 8
und 9 des voll-Katalogs).

Stufenlogik (Klasse S = unmittelbar sicherheitsrelevant):
  keine Schnittstelle                                   -> Kein Risiko (Vorscreening BA-017)
  Fernzugriff/kabellos, Maßnahmen nicht umgesetzt       -> Hoch
  lokal, keine Maßnahmen, Zugang frei                   -> Hoch
  lokal, keine Maßnahmen, Zugang gesichert              -> Mittel
  lokal, teilweise, Zugang frei                         -> Mittel
  lokal, teilweise, Zugang gesichert                    -> Niedrig
  Fernzugriff/kabellos, Maßnahmen umgesetzt             -> Kein Risiko (K-C06)
  lokal, umgesetzt, Zugang frei                         -> Niedrig
  lokal, umgesetzt, Zugang gesichert                    -> Kein Risiko
  Kompensation „unabhängige Sicherheitseinrichtung":     Hoch -> Mittel
  Frequenzumrichter mit unabhängiger Sicherheitskette:   Deckel Niedrig
"""
from .common import *

ZUGANG_ALLE = any_(yes('qz_steuerung_frei'), yes('qz_triebwerksraum_frei'),
                   yes('qz_schacht_frei'))
ZUGANG_Q = ['qz_steuerung_frei', 'qz_triebwerksraum_frei', 'qz_schacht_frei']

# ---- Klärungen (Komponentenlogik) ------------------------------------------
k('K-C01', 'Komponenten', 'Stufe Hoch im Cyber-Teil',
  'Soll der Cyber-Teil die Stufe Hoch erreichen können (Fernzugriff/kabellos '
  'ohne umgesetzte Maßnahmen an sicherheitsrelevanter Komponente)?',
  'Ja, Hoch erreichbar', 'Deckel bei Mittel (so verhält sich die Schindler-App)',
  'In der Schindler-App wurde Hoch im Cyber-Teil mit keiner Kombination erreicht. '
  'Bei überwachungsbedürftigen Anlagen ist nach ÜAnlG von erheblichem Risiko '
  'auszugehen (B-002 Anhang 2 Nr. 3); ein aus der Ferne manipulierbarer '
  'Sicherheitskreis ohne Maßnahmen ist fachlich Hoch.')
k('K-C02', 'Komponenten', 'Vorscreening ohne Schnittstelle',
  'Komponente ohne kompromittierbare Schnittstelle: Kein Risiko (DEKRA/BA-017 '
  'Vorscreening) – oder Niedrig?', 'Kein Risiko', 'Niedrig',
  'BA-017 und die DEKRA-Ausfüllhilfe schließen die Betrachtung in diesem Fall ab.')
k('K-C03', 'Komponenten', 'Eine Schnittstellenkategorie je Komponente',
  'Erfasst wird die HÖCHSTE vorhandene Schnittstellenkategorie (eine Auswahl); '
  'die konkreten Schnittstellen bleiben Dokumentation in der App. Reicht das?',
  'Ja, höchste Kategorie', 'Mehrfachauswahl je Komponente (mehr Klicks)',
  'Für die Stufe ist nur die angreifbarste Schnittstelle maßgeblich.')
k('K-C04', 'Komponenten', 'Reihenfolge der Schnittstellenkategorien',
  'Angreifbarkeit: keine < kabelgebunden < Benutzerschnittstelle < kabellos < '
  'Fernzugriff. Benutzerschnittstelle wird wie kabelgebunden (lokal) bewertet – '
  'einverstanden?', 'Ja', 'Benutzerschnittstelle wie kabellos',
  'Ein Bedienfeld setzt physische Anwesenheit voraus; kabellos nicht.')
k('K-C05', 'Komponenten', 'Lokale Schnittstelle ohne Maßnahmen bei freiem Zugang',
  'Kabelgebundene Schnittstelle, keine Maßnahmen, Steuerung/Raum frei zugänglich: '
  'Hoch – oder Mittel (Schindler-Baum)?', 'Hoch', 'Mittel (Schindler MC4-Muster)',
  'Der Schindler-Baum stuft nur um eine Stufe hoch (Niedrig -> Mittel). Ohne jede '
  'Maßnahme und mit freiem Zugang ist die Sicherheitsfunktion für jedermann '
  'manipulierbar.')
k('K-C06', 'Komponenten', 'Umgesetzte Maßnahmen bei kabellos/Fernzugriff',
  'Fernzugriff oder Funk mit umgesetzten, nachgewiesenen Maßnahmen: Niedrig '
  '(Restrisiko) – oder Kein Risiko?', 'Niedrig', 'Kein Risiko',
  'Ein Fernzugang bleibt eine Angriffsfläche; TRBS 1115-1 verlangt hier die '
  'laufende Überwachung.')
k('K-C07', 'Komponenten', 'Frequenzumrichter mit unabhängiger Sicherheitskette',
  'Umrichter mit unabhängiger elektromechanischer Sicherheitskette (STO/'
  'Sicherheitskreis unabhängig): Deckel Niedrig, auch ohne Maßnahmen?',
  'Deckel Niedrig', 'Wie andere Komponenten (Hoch möglich)',
  'BA-017/zues-Katalog: bei mechanischen Rückfallebenen i. d. R. keine '
  'Personengefährdung; es bleibt die Verfügbarkeit.')
k('K-C08', 'Komponenten', 'Unabhängige Sicherheitseinrichtung als Kompensation',
  'Bleibt die Sicherheitsfunktion bei Manipulation der Komponente durch eine '
  'unabhängige, nicht programmierbare Einrichtung gewährleistet: Hoch -> Mittel?',
  'Ja, Hoch -> Mittel', 'Keine Kompensation',
  'TRBS-1115-1-Prüffeld „Unabhängigkeit und sicherer Zustand".')
k('K-C09', 'Komponenten', 'Notruf: Testruf als Kompensation',
  'Notrufsystem mit automatischem Testruf und Ausfallmeldung (EN 81-28): '
  'Hoch -> Mittel?', 'Ja', 'Keine Kompensation',
  'Ein manipulierter/ausgefallener Notruf wird so innerhalb der Testfrist erkannt.')
k('K-C10', 'Komponenten', 'Fernüberwachung rein lesend',
  'Rein lesende Fernüberwachung ohne Netztrennung: Mittel – oder Niedrig?',
  'Mittel', 'Niedrig',
  'Ohne Segmentierung ist der Lesekanal ein Einstieg ins Aufzugsnetz.')
k('K-C11', 'Komponenten', 'Gebäudeschnittstelle ohne Rückwirkungsfreiheit',
  'Bauseitige Signale (BMA/Brandfallsteuerung/GLT) können Sicherheitsfunktionen '
  'außer Kraft setzen: Hoch?', 'Hoch', 'Mittel',
  'Eine manipulierte Brandfallsteuerung kann den Aufzug im Brandfall in die '
  'Brandetage schicken (EN 81-73).')
k('K-C23', 'Komponenten', 'Fernwartung dauerhaft aktiv',
  'Fernwartungszugang dauerhaft aktiv (keine Freigabe je Bedarf), aber '
  'authentifiziert: Mittel?', 'Mittel', 'Niedrig',
  'TRBS 1115-1 / DEKRA: Fernzugriff nur bei Bedarf und mit Freigabe.')
k('K-C24', 'Komponenten', 'Platzhalter „weitere Komponente"',
  'Generische Gefährdung „weitere programmierbare sicherheitsrelevante '
  'Komponente" mit Klasse-S-Logik aufnehmen (z. B. Lastmessung, Evakuierungs'
  'steuerung, Zutritt mit Fahrtfreigabe)?', 'Ja, ein Platzhalter',
  'Weglassen; nur Freitext in der App',
  'Der zues-Katalog der App kennt „Weitere Komponente" ohne Logik.')


# ---- Fabrik für Klasse-S-Komponenten -------------------------------------------
def komponente(code, key, name, ui, group, factor, persons, schutz, folge,
               standard, sources, zugang=ZUGANG_ALLE, zugang_q=ZUGANG_Q,
               unab_text=None, unab_deckel='MEDIUM', vorhanden_text=None,
               vorhanden_help=None, vis=None, applic=(), klaer=()):
    """Legt Fragen und Gefährdung einer Komponente an.
    unab_text: Frage der Kompensation (None = keine); unab_deckel: 'MEDIUM'
    (Hoch -> Mittel) oder 'LOW' (alles -> Niedrig/Kein Risiko).
    vis: Sichtbarkeitsregel für alle Fragen (z. B. Hydraulik); applic: zusätzliche
    APPLICABILITY-Einträge (Frage, extras)."""
    qv = qs = qm = qu = None
    vk = {'visible_when': vis} if vis else {}
    if vorhanden_text:
        qv = yn('qc_%s_vorhanden' % key, vorhanden_text, ui=ui + '.1',
                help=vorhanden_help or ('Schutzfunktion: %s Mögliche Cyberfolge: %s'
                                        % (schutz, folge)), **vk)
        vis2 = all_(vis, yes(qv)) if vis else yes(qv)
    else:
        vis2 = vis
    vk2 = {'visible_when': vis2} if vis2 else {}
    qs = sel('qc_%s_schnittstelle' % key, 'Höchste vorhandene Schnittstellenkategorie '
             'der Komponente „%s"' % name, IF_OPTIONS, ui=ui + '.2',
             help='Maßgeblich ist die angreifbarste Schnittstelle. Konkrete '
                  'Schnittstellen (USB, CAN, Mobilfunk …) in der App dokumentieren.',
             **vk2)
    vis3 = all_(vis2, neq(qs, IF_KEINE)) if vis2 else neq(qs, IF_KEINE)
    qm = sel('qc_%s_massnahmen' % key, 'Schutzmaßnahmen nach TRBS 1115-1 für „%s"'
             % name, M_OPTIONS, ui=ui + '.3',
             help='Einschlägige Kategorien: %s.' % standard[1],
             visible_when=vis3)
    if unab_text:
        qu = yn('qc_%s_unabhaengig' % key, unab_text, ui=ui + '.4', visible_when=vis3)

    lokal_none = all_(in_(qs, IF_LOKAL), eq(qm, M_KEINE))
    lokal_teil = all_(in_(qs, IF_LOKAL), eq(qm, M_TEILWEISE))
    lokal_ok = all_(in_(qs, IF_LOKAL), eq(qm, M_UMGESETZT))
    fern_bad = all_(in_(qs, IF_ENTFERNT), neq(qm, M_UMGESETZT))
    fern_ok = all_(in_(qs, IF_ENTFERNT), eq(qm, M_UMGESETZT))
    mittel = standard[0]

    rules = [
        r(eq(qs, IF_KEINE), 'NO_RISK', prio=600, evidence='HIGH_CONFIDENCE',
          sofort='Keine kompromittierbare Schnittstelle – Feststellung dokumentieren '
                 '(Vorscreening nach BA-017); bei Nachrüstung erneut bewerten',
          klaerung=['K-C02'], notes='Vorscreening: Betrachtung abgeschlossen.'),
    ]
    if unab_text:
        if unab_deckel == 'LOW':
            rules += [
                r(all_(yes(qu), neq(qs, IF_KEINE), neq(qm, M_UMGESETZT)), 'LOW', prio=520,
                  sofort='Unabhängige Sicherheitskette bei jeder Prüfung mitprüfen',
                  mittel=mittel + ' Wirksamkeit nachweisen (TRBS 1115-1 Abschn. 5).',
                  klaerung=['K-C07']),
                r(all_(yes(qu), neq(qs, IF_KEINE), eq(qm, M_UMGESETZT)), 'NO_RISK', prio=510,
                  sofort='Zustand erhalten; unabhängige Sicherheitskette und Maßnahmen '
                         'bei der wiederkehrenden Prüfung erneut prüfen',
                  klaerung=['K-C07']),
            ]
        else:
            rules += [
                r(all_(yes(qu), fern_bad), 'MEDIUM', prio=520,
                  sofort='Fern-/Funkzugang der Komponente bis zur Umsetzung der '
                         'Maßnahmen deaktivieren; unabhängige Sicherheitseinrichtung '
                         'bei jeder Prüfung mitprüfen',
                  mittel=mittel + ' Wirksamkeit nachweisen (TRBS 1115-1 Abschn. 5).',
                  klaerung=['K-C08']),
                r(all_(yes(qu), lokal_none, zugang), 'MEDIUM', prio=510,
                  sofort='Zugang zur Komponente sofort beschränken; Service'
                         'schnittstellen sichern; unabhängige Sicherheitseinrichtung '
                         'bei jeder Prüfung mitprüfen',
                  mittel=mittel, klaerung=['K-C08']),
            ]
    rules += [
        r(all_(eq(qs, IF_FERN), neq(qm, M_UMGESETZT)), 'HIGH', prio=400,
          sofort='Fernzugang der Komponente „%s" deaktivieren oder physisch trennen, '
                 'bis die Schutzmaßnahmen umgesetzt und nachgewiesen sind' % name,
          mittel=mittel + ' Wirksamkeit nachweisen (TRBS 1115-1 Abschn. 5).',
          klaerung=['K-C01']),
        r(all_(eq(qs, IF_KABELLOS), neq(qm, M_UMGESETZT)), 'HIGH', prio=390,
          sofort='Funkschnittstelle der Komponente „%s" deaktivieren oder auf das '
                 'Notwendige beschränken, bis die Schutzmaßnahmen umgesetzt sind' % name,
          mittel=mittel + ' Wirksamkeit nachweisen (TRBS 1115-1 Abschn. 5).',
          klaerung=['K-C01']),
        r(all_(lokal_none, zugang), 'HIGH', prio=380,
          sofort='Zugang zur Komponente/zum Steuerschrank sofort beschränken; Service- '
                 'und Programmierschnittstellen sichern',
          mittel=mittel, klaerung=['K-C05']),
        r(lokal_none, 'MEDIUM', prio=300,
          sofort='Serviceschnittstellen der Komponente gegen unbefugte Nutzung sichern',
          mittel=mittel),
        r(all_(lokal_teil, zugang), 'MEDIUM', prio=290,
          sofort='Zugang beschränken; offene Maßnahmen priorisiert umsetzen',
          mittel='Festgelegte Maßnahmen vollständig umsetzen und Wirksamkeit nachweisen'),
        r(lokal_teil, 'LOW', prio=280,
          sofort='Offene Maßnahmen terminieren und Verantwortliche benennen',
          mittel='Festgelegte Maßnahmen vollständig umsetzen und Wirksamkeit nachweisen'),
        r(fern_ok, 'NO_RISK', prio=270, evidence='HIGH_CONFIDENCE',
          sofort='Zustand erhalten; Fern-/Funkzugang regelmäßig auf Notwendigkeit prüfen, '
                 'Wirksamkeit bei der wiederkehrenden Prüfung erneut nachweisen',
          klaerung=['K-C06']),
        r(all_(lokal_ok, zugang), 'LOW', prio=260,
          sofort='Physischen Zugang zur Steuerung bzw. zum Raum beschränken '
                 '(siehe Gefährdungen Zugang)',
          mittel='Zugangskontrolle (Hardware) dauerhaft herstellen'),
        r(lokal_ok, 'NO_RISK', prio=250, evidence='HIGH_CONFIDENCE',
          sofort='Zustand erhalten; Maßnahmen bei der wiederkehrenden Prüfung '
                 'erneut nachweisen'),
    ]
    qlist = [(q_, 'APPLICABILITY', 'NEVER', ex) for q_, ex in applic]
    if qv:
        qlist.append((qv, 'APPLICABILITY', 'ALWAYS'))
    qlist += [(qs, 'TRIGGER', 'ALWAYS'), (qm, 'TRIGGER', 'NEVER')]
    if qu:
        qlist.append((qu, 'COMPENSATION', 'NEVER'))
    qlist += [(z, 'MODIFIER', 'NEVER') for z in zugang_q]
    hz(code, 'Manipulation oder Ausfall: %s' % name, group, qlist, rules,
       sources=list(sources) + [trbs1115('4.5.2'), zues_ba017()],
       factor=factor, persons=persons, agg='NONE',
       description='Schutzfunktion: %s Mögliche Cyberfolge: %s' % (schutz, folge),
       klaerung=list(klaer), bereich='C')
    return code


# ---- Komponenten (Klasse S) -------------------------------------------------
STEUERUNG_MASS = ('Zugang zu Schnittstellen vor Unbefugten schützen; nicht benötigte '
                  'Schnittstellen deaktivieren; Parameteränderungen dokumentieren.',
                  'Zugangskontrolle (Hardware/Software), Funktionsreduzierung')

komponente('CY-C01', 'steuerung', 'Aufzugssteuerung', '3.1', GRP_STEUERUNG, F_MANIP,
           [NUTZER, WARTUNG],
           schutz='Sicherer Betrieb, Überwachung des Sicherheitskreises und der Fahrbefehle.',
           folge='Sicherheitsfunktion deaktiviert oder manipuliert; unzulässige Fahrbewegung '
                 'oder Geschwindigkeit.',
           standard=STEUERUNG_MASS,
           sources=[en('DIN EN 81-20', '5.11'), zues_ba017('Beispiel Steuerung')],
           unab_text='Bleibt der Sicherheitskreis (Türkontakte, Endschalter, Fang-/'
                     'Begrenzerkontakte) bei Manipulation der Steuerung durch eine '
                     'unabhängige elektromechanische Kette wirksam?',
           vis=neq('qa_steuerungsart', 'relais'),
           applic=[('qa_steuerungsart', {'applicable_when': neq('qa_steuerungsart', 'relais')})],
           klaer=['K-C03', 'K-C04', 'K-C21'])
# Maschinenraum-Merkmal an der Steuerung dokumentieren (steuert die Sichtbarkeit
# der Zugangsfrage 2.2; nach K-C21 keine eigene Gefährdung mehr).
next(h for h in HAZARDS if h['code'] == 'CY-C01')['questions'].append(
    {'question': 'qa_maschinenraum', 'role': 'DOCUMENTATION', 'required_mode': 'ALWAYS',
     'notes': 'Anlagenmerkmal; steuert die Zugangsfrage 2.2 (Triebwerksraum).'})

komponente('CY-C02', 'pessral', 'PESSRAL (programmierbare Sicherheitsschaltung)', '3.2',
           GRP_STEUERUNG, F_MANIP, [NUTZER, WARTUNG],
           schutz='Elektronische Sicherheitsfunktionen im Sicherheitsstromkreis.',
           folge='Manipulation oder Deaktivierung von Sicherheitsfunktionen.',
           standard=('Serviceschnittstellen nur für Berechtigte; Parametrierung schützen; '
                     'nach Eingriffen Sicherheitsfunktionen prüfen.',
                     'Zugangskontrolle (Hardware), Funktionsreduzierung'),
           sources=[en('DIN EN 81-20', '5.11.2.6'), en8150('5.6')],
           vorhanden_text='PESSRAL / programmierbare Sicherheitsschaltung vorhanden?')

komponente('CY-C03', 'fu', 'Frequenzumrichter', '3.3', GRP_ANTRIEB, F_MANIP,
           [NUTZER, WARTUNG],
           schutz='Regelung von Fahrgeschwindigkeit und Antrieb.',
           folge='Unzulässige Geschwindigkeit oder Beschleunigung, wenn keine unabhängige '
                 'Rückfallebene wirkt.',
           standard=('Parameterzugriff schützen; zulässigen Parametersatz sichern; nach '
                     'Änderungen Antrieb und Fahrverhalten prüfen.',
                     'Zugangskontrolle (Software), Funktionsreduzierung'),
           sources=[en('DIN EN 81-20', '5.9')],
           vorhanden_text='Frequenzumrichter (geregelter Antrieb) vorhanden?',
           unab_text='Wirkt bei Manipulation des Umrichters eine unabhängige Sicherheits'
                     'kette (STO/sicher abgeschaltetes Moment, Bremse und Geschwindigkeits'
                     'begrenzer unabhängig vom Umrichter)?',
           unab_deckel='LOW')

komponente('CY-C04', 'notruf', 'Notrufsystem (Zwei-Wege-Kommunikation)', '3.4',
           GRP_NOTRUF, F_NOTRUF, [NUTZER],
           schutz='Hilfe und Kommunikation bei Personeneinschluss.',
           folge='Notruf wird nicht oder an die falsche Stelle weitergeleitet; '
                 'Personeneinschluss bleibt unbemerkt.',
           standard=('Zugriff auf Schnittstellen verhindern/begrenzen; Werkszugangsdaten '
                     'ändern; Notrufverbindung regelmäßig prüfen.',
                     'Zugangskontrolle (Software/Hardware), Überwachung'),
           sources=[en8128('4.2'), zues_ba017('Beispiel Notruf')],
           vorhanden_text='Notrufsystem mit digitaler Komponente (Mobilfunk/IP, '
                          'programmierbares Notrufgerät) vorhanden?',
           unab_text='Automatischer Testruf mit Ausfallmeldung an die Notrufzentrale '
                     '(EN 81-28) vorhanden und wirksam?',
           klaer=['K-C09'])

komponente('CY-C05', 'kopierung', 'Schachtkopierung / Positionierung', '3.5',
           GRP_STEUERUNG, F_MANIP, [NUTZER],
           schutz='Positionserfassung und Haltegenauigkeit (Bündigkeit).',
           folge='Fehlpositionierung oder Fehlbündigkeit; Stolper-/Absturzgefahr.',
           standard=('Schnittstellen auf das Notwendige beschränken; unbefugte Änderung '
                     'der Positions-/Schachtinformation verhindern.',
                     'Zugangskontrolle (Hardware), Funktionsreduzierung'),
           sources=[en('DIN EN 81-20', '5.12.1')],
           vorhanden_text='Digitale Schachtkopierung / Absolutwertgeber vorhanden?',
           unab_text='Bleiben Bündigkeit und Endlagen bei Manipulation der Kopierung '
                     'durch unabhängige Schalter/Endschalter gesichert?')

komponente('CY-C06', 'tuer', 'Türsteuerung', '3.6', GRP_ANTRIEB, F_MANIP, [NUTZER],
           schutz='Türbewegung und Begrenzung der Schließkräfte.',
           folge='Unzulässige Türkräfte oder Türbewegung; Quetsch-/Schergefahr.',
           standard=('Serviceschnittstellen nur für Berechtigte; Parameter sichern; nach '
                     'Eingriffen Türfunktionen und Schutzeinrichtungen prüfen.',
                     'Zugangskontrolle (Hardware), Funktionsreduzierung'),
           sources=[en('DIN EN 81-20', '5.3.6')],
           vorhanden_text='Programmierbare Türsteuerung / Türantrieb mit Parametrierzugang '
                          'vorhanden?',
           unab_text='Wirkt die Schließkraftbegrenzung/Reversierung unabhängig von der '
                     'programmierbaren Türsteuerung (mechanisch oder separates Gerät)?')

komponente('CY-C07', 'ucm', 'UCM-Erkennung', '3.7', GRP_STEUERUNG, F_MANIP, [NUTZER],
           schutz='Verhinderung unkontrollierter Fahrkorbbewegung bei offenen Türen.',
           folge='Quetsch-/Schergefahr durch Deaktivierung oder Parameteränderung.',
           standard=('Zugang zu Schnittstellen vor Unbefugten schützen; Funktionsumfang '
                     'auf das Erforderliche reduzieren.',
                     'Zugangskontrolle (Hardware), Funktionsreduzierung'),
           sources=[en('DIN EN 81-20', '5.6.7')],
           vorhanden_text='UCM-Erkennung (Schutz gegen unbeabsichtigte Bewegung) mit '
                          'programmierbarer Komponente vorhanden?',
           unab_text='Wirkt das UCM-Bremselement (Bremse/Fangvorrichtung) über eine '
                     'unabhängige, nicht programmierbare Auslösung?')

komponente('CY-C08', 'safue', 'SAFÜ (Schutz gegen Übergeschwindigkeit)', '3.8',
           GRP_STEUERUNG, F_MANIP, [NUTZER],
           schutz='Schutz gegen Übergeschwindigkeit.',
           folge='Deaktivierung oder Manipulation des Übergeschwindigkeitsschutzes.',
           standard=('Zugang zu Schnittstellen vor Unbefugten schützen; Parametrierung '
                     'gegen unbefugte Änderung sichern.',
                     'Zugangskontrolle (Hardware), Funktionsreduzierung'),
           sources=[en('DIN EN 81-20', '5.6.2')],
           vorhanden_text='Elektronischer Geschwindigkeitsbegrenzer / SAFÜ mit '
                          'programmierbarer Komponente vorhanden?',
           unab_text='Bleibt die Fangvorrichtung bei Manipulation der elektronischen '
                     'Überwachung durch einen mechanischen Begrenzer auslösbar?')

komponente('CY-C09', 'tragmittel', 'Tragmittelüberwachung', '3.9', GRP_STEUERUNG,
           F_AUSFALL, [NUTZER, WARTUNG],
           schutz='Überwachung des Zustands der Tragmittel (Riemen/Seile).',
           folge='Ausfall oder Umgehung der Überwachung bleibt unbemerkt.',
           standard=('Schnittstellen schützen; Wirksamkeit der Überwachung regelmäßig '
                     'prüfen.', 'Zugangskontrolle (Hardware), Überwachung'),
           sources=[en('DIN EN 81-20', '5.5.5')],
           vorhanden_text='Elektronische Tragmittelüberwachung (z. B. Riemenüberwachung) '
                          'vorhanden?',
           unab_text='Wird der Tragmittelzustand zusätzlich unabhängig geprüft '
                     '(Sichtprüfung nach Wartungsplan, Ablegereife)?')

komponente('CY-C10', 'hydraulik', 'Hydraulischer Steuerblock', '3.10', GRP_ANTRIEB,
           F_MANIP, [NUTZER],
           schutz='Schutz gegen Absinken und Übergeschwindigkeit bei Hydraulikaufzügen.',
           folge='Manipulation von Ventilen/Parametern; unkontrolliertes Absinken.',
           standard=('Zugang zu Schnittstellen vor Unbefugten schützen; Parametrierung '
                     'sichern und nach Änderungen prüfen.',
                     'Zugangskontrolle (Hardware), Funktionsreduzierung'),
           sources=[en('DIN EN 81-20', '5.9.3')],
           vorhanden_text='Elektronisch geregelter Hydraulik-Steuerblock vorhanden?',
           vis=in_('qa_aufzugsart', ['hydraulik', 'seil_hydraulik']),
           applic=[('qa_aufzugsart',
                    {'applicable_when': in_('qa_aufzugsart', ['hydraulik', 'seil_hydraulik'])})],
           unab_text='Wirken Rohrbruchventil und Absinkschutz mechanisch/hydraulisch '
                     'unabhängig von der Elektronik?')

# Kein Platzhalter „weitere Komponente" (K-C24): weitere programmierbare
# Komponenten werden in der App als Freitext dokumentiert.

# ---- Kanal-Komponenten (Klasse K) --------------------------------------------
NETZ_VIS = yes('qa_vernetzt')
yn('qc_fernueb_vorhanden', 'Fernüberwachung (Zustandsmeldung, Störungsmeldung an '
   'Leitstelle/Hersteller) vorhanden?', ui='3.11.1', visible_when=NETZ_VIS)
yn('qc_fernueb_lesend', 'Ist die Fernüberwachung ausschließlich lesend (kein Schreib-, '
   'Steuer- oder Parametrierzugriff über diesen Kanal)?', ui='3.11.2',
   visible_when=all_(NETZ_VIS, yes('qc_fernueb_vorhanden')))

hz('CY-C11', 'Unbefugter Zugriff über die Fernüberwachung', GRP_NETZ,
   [('qa_vernetzt', 'APPLICABILITY', 'ALWAYS'),
    ('qc_fernueb_vorhanden', 'APPLICABILITY', 'ALWAYS'),
    ('qc_fernueb_lesend', 'TRIGGER', 'NEVER'),
    ('qn_segmentierung', 'TRIGGER', 'NEVER'),
    ('qn_fern_auth', 'TRIGGER', 'NEVER'),
    ('qn_protokoll', 'TRIGGER', 'NEVER')],
   [r(all_(no('qn_segmentierung'), no('qc_fernueb_lesend')), 'HIGH', prio=400,
      sofort='Fernüberwachung mit Schreibzugriff vom Aufzugsnetz trennen oder '
             'deaktivieren, bis Segmentierung und Authentifizierung umgesetzt sind',
      mittel='Netz segmentieren (Firewall, eigenes Segment); Kanal auf lesenden '
             'Zugriff beschränken; Zugriffe authentifizieren und protokollieren',
      klaerung=['K-C01']),
    r(all_(no('qn_segmentierung'), yes('qc_fernueb_lesend')), 'LOW', prio=350,
      sofort='Erreichbarkeit der Steuerung aus dem Überwachungsnetz prüfen und '
             'unterbinden',
      mittel='Aufzugsnetz vom Gebäude-/Büronetz und Internet trennen (Segmentierung)',
      klaerung=['K-C10']),
    r(all_(yes('qn_segmentierung'), no('qc_fernueb_lesend'), no('qn_fern_auth')), 'MEDIUM',
      prio=300,
      sofort='Schreibzugriffe über die Fernüberwachung bis zur individuellen '
             'Authentifizierung sperren',
      mittel='Individuelle, verschlüsselte Authentifizierung für den Kanal einführen'),
    r(all_(yes('qn_segmentierung'), no('qc_fernueb_lesend'), yes('qn_fern_auth'),
           no('qn_protokoll')), 'LOW', prio=250,
      sofort='Zugriffsprotokollierung aktivieren',
      mittel='Protokolle regelmäßig auswerten (Überwachung nach TRBS 1115-1)')],
   sources=[trbs1115('4.5.2 Segmentierung, Überwachung'), dekra('Schritt 3')],
   factor=F_MANIP, persons=[NUTZER, WARTUNG, BETREIBER], agg='NONE',
   description='Schutzfunktion: Zustandsüberwachung und Störungsmeldung. Mögliche '
               'Cyberfolge: Fehlmeldung, Ausfall der Meldung oder unbefugter '
               'Fremdzugriff auf das Aufzugsnetz.', bereich='C')

yn('qc_remote_vorhanden', 'Remote-Service / Fernwartung (Hersteller-Fernzugriff, '
   'Service-App, VPN) vorhanden?', ui='3.12.1', visible_when=NETZ_VIS)

hz('CY-C12', 'Unbefugter Fernzugriff über Remote-Service / Fernwartung', GRP_NETZ,
   [('qa_vernetzt', 'APPLICABILITY', 'ALWAYS'),
    ('qc_remote_vorhanden', 'APPLICABILITY', 'ALWAYS'),
    ('qn_segmentierung', 'TRIGGER', 'NEVER'),
    ('qn_fern_freigabe', 'TRIGGER', 'NEVER'),
    ('qn_fern_auth', 'TRIGGER', 'NEVER'),
    ('qn_protokoll', 'TRIGGER', 'NEVER')],
   [r(all_(no('qn_fern_freigabe'), no('qn_fern_auth')), 'HIGH', prio=400,
      sofort='Dauerhaft offenen, nicht individuell authentifizierten Fernwartungs'
             'zugang sofort deaktivieren',
      mittel='Fernzugriff nur nach Freigabe durch den Betreiber, individuell '
             'authentifiziert und verschlüsselt; Zugriffe protokollieren',
      klaerung=['K-C01']),
    r(all_(no('qn_segmentierung'), no('qn_fern_auth')), 'HIGH', prio=380,
      sofort='Fernwartungszugang deaktivieren, bis Netztrennung und Authentifizierung '
             'umgesetzt sind',
      mittel='Aufzugsnetz segmentieren; individuelle Authentifizierung einführen',
      klaerung=['K-C01']),
    r(no('qn_fern_freigabe'), 'LOW', prio=300,
      sofort='Fernwartungszugang nur bei Bedarf freischalten (Betreiberfreigabe)',
      mittel='Freigabeverfahren mit der Wartungsfirma vertraglich festlegen',
      klaerung=['K-C23']),
    r(no('qn_fern_auth'), 'MEDIUM', prio=290,
      sofort='Gemeinsam genutzte oder unverschlüsselte Fernzugänge sperren',
      mittel='Individuelle, verschlüsselte Authentifizierung (Zwei-Faktor oder '
             'gleichwertig) einführen'),
    r(no('qn_segmentierung'), 'MEDIUM', prio=280,
      sofort='Direkte Erreichbarkeit der Steuerung aus Fremdnetzen unterbinden',
      mittel='Aufzugsnetz vom Gebäude-/Büronetz und Internet trennen (Segmentierung)'),
    r(no('qn_protokoll'), 'LOW', prio=250,
      sofort='Protokollierung der Fernzugriffe aktivieren',
      mittel='Protokolle regelmäßig auswerten (Überwachung nach TRBS 1115-1)')],
   sources=[trbs1115('4.5.2 Zugangskontrolle, Segmentierung, Überwachung'),
            dekra('Schritt 3'), zues_ba017()],
   factor=F_MANIP, persons=[NUTZER, WARTUNG, BETREIBER], agg='NONE',
   description='Schutzfunktion: Wartungs- und Diagnosezugang. Mögliche Cyberfolge: '
               'unbefugter Fernzugriff auf Steuerung und Parameter.', bereich='C')

yn('qc_gateway_vorhanden', 'Gateway / Router / Modem / WLAN- oder Service-Dongle an der '
   'Anlage vorhanden?', ui='3.13.1', visible_when=NETZ_VIS)
GW_VIS = all_(NETZ_VIS, yes('qc_gateway_vorhanden'))
yn('qc_gateway_firewall', 'Ist das Gateway mit Firewall/Netztrennung zur Aufzugssteuerung '
   'konfiguriert und sind nur benötigte Ports und Dienste freigegeben?', ui='3.13.2',
   visible_when=GW_VIS)
yn('qc_gateway_default', 'Sind die Werkszugangsdaten des Gateways/Routers geändert und '
   'ist die Administration nur für Berechtigte erreichbar?', ui='3.13.3',
   visible_when=GW_VIS)
yn('qc_gateway_updates', 'Ist die Firmware des Gateways aktuell und ein Update-Verfahren '
   'geregelt?', ui='3.13.4', visible_when=GW_VIS)

hz('CY-C13', 'Ungesichertes Gateway / Router / Modem als Einstieg in das Aufzugsnetz',
   GRP_NETZ,
   [('qa_vernetzt', 'APPLICABILITY', 'ALWAYS'),
    ('qc_gateway_vorhanden', 'APPLICABILITY', 'ALWAYS'),
    ('qc_gateway_firewall', 'TRIGGER', 'NEVER'),
    ('qc_gateway_default', 'TRIGGER', 'NEVER'),
    ('qc_gateway_updates', 'TRIGGER', 'NEVER')],
   [r(all_(no('qc_gateway_firewall'), no('qc_gateway_default')), 'HIGH', prio=400,
      sofort='Gateway vom Netz trennen oder Fernzugang sperren, bis Werkszugangsdaten '
             'geändert und Firewall konfiguriert sind',
      mittel='Gateway härten: Netztrennung, nur benötigte Dienste, individuelle '
             'Zugangsdaten, Update-Verfahren',
      klaerung=['K-C01']),
    r(no('qc_gateway_firewall'), 'MEDIUM', prio=300,
      sofort='Nicht benötigte Ports und Dienste am Gateway schließen',
      mittel='Firewall/Netztrennung zwischen Gateway und Aufzugssteuerung einrichten'),
    r(no('qc_gateway_default'), 'MEDIUM', prio=290,
      sofort='Werkszugangsdaten des Gateways ändern; Administration nur aus dem '
             'Aufzugsnetz zulassen',
      mittel='Zugangskontrolle (Software) für Netzkomponenten festlegen'),
    r(no('qc_gateway_updates'), 'LOW', prio=250,
      sofort='Firmwarestand prüfen und Herstellerhinweise einholen',
      mittel='Update-Verfahren für Netzkomponenten festlegen')],
   sources=[trbs1115('4.5.2 Segmentierung, Härtung'), dekra('Schritt 3')],
   factor=F_MANIP, persons=[NUTZER, WARTUNG, BETREIBER], agg='NONE',
   description='TRBS-1115-1-Prüffeld „Gateway / Router / Modem / WLAN-/Service-Dongle".',
   bereich='C')

# ---- Gebäudeschnittstelle ---------------------------------------------------
GEB_VIS = yes('qa_gebaeude_anbindung')
yn('qc_geb_rueckwirkungsfrei', 'Ist die Schnittstelle zu den bauseitigen Systemen '
   'rückwirkungsfrei (definierte Signale/potenzialfreie Kontakte; bauseitige '
   'Signale können Sicherheitsfunktionen des Aufzugs nicht außer Kraft setzen)?',
   ui='3.14.1', visible_when=GEB_VIS)
yn('qc_geb_sicherer_zustand', 'Nimmt der Aufzug bei Ausfall oder Manipulation des '
   'bauseitigen Signals (z. B. Brandfallsteuerung) einen sicheren Zustand ein '
   '(Brandfallfahrt in die Evakuierungshaltestelle, kein Weiterbetrieb)?',
   ui='3.14.2', visible_when=GEB_VIS)

hz('CY-C14', 'Manipulierbare Gebäudeschnittstelle (Brandfallsteuerung, Entrauchung, '
   'Gebäudeleittechnik)', GRP_GEBAEUDE,
   [('qa_gebaeude_anbindung', 'APPLICABILITY', 'ALWAYS'),
    ('qc_geb_rueckwirkungsfrei', 'TRIGGER', 'NEVER'),
    ('qc_geb_sicherer_zustand', 'TRIGGER', 'NEVER')],
   [r(no('qc_geb_rueckwirkungsfrei'), 'HIGH', prio=400,
      sofort='Bauseitige Signale mit Einfluss auf Sicherheitsfunktionen prüfen und bis '
             'zur Klärung auf definierte Schnittstellen beschränken',
      mittel='Rückwirkungsfreie Schnittstelle (potenzialfreie Kontakte, definierte '
             'Signale) herstellen; Nachweis mit Gebäudebetreiber/Errichter',
      klaerung=['K-C11']),
    r(no('qc_geb_sicherer_zustand'), 'MEDIUM', prio=300,
      sofort='Verhalten bei Signalausfall/Manipulation mit Hersteller klären',
      mittel='Sicheren Zustand bei Signalausfall (Brandfallfahrt, Sperrung) '
             'konfigurieren und prüfen')],
   sources=[trbs1115('4.5.2 Rückwirkungsfreiheit'), en8173('5.2'),
            zues_b002('Anhang 2 Nr. 9')],
   factor=F_BRAND, persons=[NUTZER, FEUERWEHR], agg='NONE',
   description='TRBS-1115-1-Prüffeld „Schachtentrauchung / Brandfallsteuerung / '
               'bauseitige Systeme".', bereich='C')
