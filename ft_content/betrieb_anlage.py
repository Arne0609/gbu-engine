# -*- coding: utf-8 -*-
"""B – Betrieb: Handlauf, Sockel, Stufen/Paletten, Kämme, Not-Halt, Wagen.

Bewertet wird der Zustand der Anlage aus Sicht der Nutzer und der Beschäftigten
des Betreibers (nicht der Monteure – das ist Bereich I)."""
from .common import *

BAND = 'Stufen'   # Sprachgebrauch je Anlagenart wird im Fragetext offen gehalten

# ---- Fragen: Handlauf und Balustrade ---------------------------------------
yn('qb_handlauf_gleichlauf', 'Handläufe laufen auf beiden Seiten synchron zum '
   'Stufen-/Palettenband (kein spürbarer Vor- oder Nachlauf)?', ui='3.1')
yn('qb_handlauf_zustand', 'Handläufe unbeschädigt (keine Risse, Aufwölbungen, '
   'offenen Klebestellen, keine klebrigen oder scharfkantigen Stellen)?', ui='3.2')
yn('qb_handlaufeinfuehrung', 'Handlaufeinführungen unbeschädigt und mit wirksamem '
   'Einzugsschutz (Fingerschutz) versehen?', ui='3.3')
yn('qb_handlauf_abschaltung', 'Abschaltung an der Handlaufeinführung vorhanden und '
   'funktionsfähig (Funktionsprobe dokumentiert)?', ui='3.4')
yn('qb_sockelbuersten', 'Sockelleisten/Sockelbürsten auf beiden Seiten vollständig '
   'vorhanden und unbeschädigt?', ui='3.5')
yn('qb_balustrade_zustand', 'Balustrade unbeschädigt, ohne scharfe Kanten, Spalte '
   'oder lose Teile?', ui='3.6')
yn('qb_glas_beschaedigt', 'Beschädigung an der Glasbalustrade (Riss, Sprung, '
   'Schlagstelle)?', ui='3.7', visible_when=yes('qa_glasbalustrade'))

# ---- Fragen: Stufen, Paletten, Kämme ---------------------------------------
yn('qb_stufen_zustand', 'Stufen bzw. Paletten vollständig, unbeschädigt und ohne '
   'fehlende oder verformte Elemente?', ui='4.1')
yn('qb_stufen_rutsch', 'Stufen-/Palettenoberflächen sauber, trocken und rutschhemmend '
   '(kein Öl, kein Fett, keine Nässe)?', ui='4.2')
yn('qb_stufen_niveau', 'Stufen-/Palettenband ohne Niveauversatz zwischen benachbarten '
   'Elementen?', ui='4.3')
yn('qb_stufenspalt', 'Spalt zwischen Stufe/Palette und Sockelblech beidseitig '
   'höchstens 4 mm (Summe beider Seiten höchstens 7 mm)?', ui='4.4')
yn('qb_kamm_zustand', 'Kammplatten vollständig, ohne abgebrochene oder fehlende '
   'Kammzähne?', ui='4.5')
yn('qb_kamm_abschaltung', 'Kammplattenabschaltung vorhanden und funktionsfähig?',
   ui='4.6')
yn('qb_kamm_eingriff', 'Kämme greifen sauber in die Stufen-/Palettenrillen ein '
   '(kein Höhenversatz, keine Fremdkörper)?', ui='4.7')
yn('qb_stufenband_lauf', 'Anlage läuft ruhig und gleichmäßig (keine auffälligen '
   'Geräusche, kein Rucken, kein Rütteln)?', ui='4.8')

# ---- Fragen: Not-Halt und Bedienung ----------------------------------------
yn('qb_nothalt_vorhanden', 'NOT-HALT-Einrichtungen an beiden Zugängen vorhanden?',
   ui='5.1')
yn('qb_nothalt_erreichbar', 'NOT-HALT-Einrichtungen frei zugänglich, deutlich '
   'gekennzeichnet und als solche erkennbar?', ui='5.2',
   visible_when=yes('qb_nothalt_vorhanden'))
yn('qb_nothalt_funktion', 'Funktion der NOT-HALT-Einrichtungen im Rahmen der '
   'Kontrolle geprüft und dokumentiert?', ui='5.3',
   visible_when=yes('qb_nothalt_vorhanden'))
yn('qb_bedienstellen_gesichert', 'Schlüsselschalter und Bedienstellen gegen '
   'Betätigung durch Unbefugte gesichert?', ui='5.4')
yn('qb_wiederanlauf', 'Wiederanlauf nach Stillstand nur durch eine unterwiesene '
   'Person und nach Kontrolle des Bandes (kein automatischer Wiederanlauf mit '
   'Personen auf der Anlage)?', ui='5.5')
yn('qb_bedarf_anlauf', 'Bei Bedarfssteuerung: Anlaufwarnung bzw. ausreichende '
   'Vorlaufzeit vorhanden?', ui='5.6', visible_when=eq('qa_betriebsart', 'bedarf'))

# ---- Fragen: Wagen ---------------------------------------------------------
yn('qb_wagen_geeignet', 'Nur Wagen mit wirksamer Feststell-/Blockiereinrichtung im '
   'Umlauf, die für diese Anlage freigegeben sind?', ui='6.1',
   visible_when=nin('qa_wagen', ['keine']))
yn('qb_wagen_hinweis', 'Kennzeichnung an den Zugängen, welche Wagen befördert werden '
   'dürfen?', ui='6.2', visible_when=nin('qa_wagen', ['keine']))
yn('qb_wagen_fremd', 'Werden regelmäßig nicht freigegebene Wagen, Kinderwagen oder '
   'Rollstühle mitgeführt?', ui='6.3')

# ---- Klärungen -------------------------------------------------------------
k('K-B05', 'Betrieb/Anlage', 'Sockelbürsten',
  'Fehlende Sockelbürsten: Mittel (DGUV 209-085 stuft sie im Instandhaltungs-'
  'kontext gelb ein) oder Hoch aus Nutzersicht?',
  'Mittel', 'Hoch bei erwarteter Kindernutzung',
  'Die DGUV-Einstufung gilt für den Monteur, nicht für Fahrgäste; der Einzug '
  'weicher Schuhe und Kinderfüße ist der typische Unfallhergang.')
k('K-B06', 'Betrieb/Anlage', 'Kammzähne',
  'Abgebrochene Kammzähne: Mittel wie in DGUV 209-085 Anhang 2, oder Hoch, '
  'solange die Kammplattenabschaltung wirksam ist?',
  'Mittel, solange die Kammplattenabschaltung geprüft und wirksam ist; ohne '
  'wirksame Abschaltung Hoch', 'Durchgängig Hoch',
  'DGUV bewertet den Arbeitsplatz des Monteurs; für Fahrgäste ist der Kamm die '
  'häufigste Einzugsstelle.')
k('K-B07', 'Betrieb/Anlage', 'Handlaufgleichlauf',
  'Spürbarer Vor-/Nachlauf des Handlaufs: eigene Stufe Mittel oder nur Hinweis?',
  'Mittel', 'Niedrig, wenn die Abweichung gering ist und keine Sturzfolge droht',
  'EN 115-1 fordert Gleichlauf mit enger Toleranz; die Betriebspraxis toleriert '
  'kleine Abweichungen.')
k('K-B08', 'Betrieb/Anlage', 'Stufenspalt',
  'Spalt über 4 mm: Mittel oder Hoch?',
  'Hoch bei erwarteter Kindernutzung, sonst Mittel',
  'Immer Hoch (Einzug von Schuhen und Kinderfüßen)', '')
k('K-B09', 'Betrieb/Anlage', 'Glasbalustrade',
  'Riss oder Sprung in der Glasbalustrade: sofortige Außerbetriebnahme?',
  'Hoch mit Sofortmaßnahme Außerbetriebnahme',
  'Mittel, wenn die Scheibe gesichert und der Bereich abgesperrt ist', '')
k('K-B10', 'Betrieb/Anlage', 'Wiederanlauf',
  'Automatischer Wiederanlauf nach Störung ohne Kontrolle des Bandes: Hoch?',
  'Hoch', 'Mittel, wenn die Anlage von einer besetzten Stelle einsehbar ist', '')

# ---- Gefährdungen: Handlauf und Balustrade ---------------------------------
hz('FT-B10', 'Einzug an der Handlaufeinführung', GRP_BALUSTRADE,
   [('qb_handlaufeinfuehrung', 'TRIGGER', 'ALWAYS'),
    ('qb_handlauf_abschaltung', 'TRIGGER', 'ALWAYS'),
    ('qa_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qb_handlaufeinfuehrung'), no('qb_handlauf_abschaltung')), 'HIGH', prio=300,
      sofort='Anlage außer Betrieb nehmen und absperren, bis Einzugsschutz und '
             'Abschaltung wiederhergestellt sind',
      mittel='Handlaufeinführung instand setzen und die Abschaltung in die '
             'wiederkehrende Funktionsprüfung aufnehmen'),
    r(no('qb_handlauf_abschaltung'), 'HIGH', prio=250,
      sofort='Anlage außer Betrieb nehmen, bis die Abschaltung an der '
             'Handlaufeinführung wieder funktioniert',
      mittel='Sicherheitseinrichtung instand setzen und Funktionsprüfung '
             'dokumentiert wiederholen'),
    r(no('qb_handlaufeinfuehrung'), 'MEDIUM', prio=200,
      sofort='Beschädigten Einzugsschutz sofort instand setzen; Bereich bis dahin '
             'beobachten',
      mittel='Handlaufeinführung nach Herstellervorgabe erneuern')],
   sources=[en115_1('5.6'), en115_2(), d208_028(), d209_085('Anh. 2')],
   factor=F_EINZUG, persons=[NUTZER, KINDER], bereich='B')

hz('FT-B11', 'Sturz und Verletzung durch Zustand und Gleichlauf der Handläufe',
   GRP_BALUSTRADE,
   [('qb_handlauf_zustand', 'TRIGGER', 'ALWAYS'),
    ('qb_handlauf_gleichlauf', 'TRIGGER', 'ALWAYS')],
   [r(no('qb_handlauf_zustand'), 'MEDIUM', prio=200,
      sofort='Schadstellen am Handlauf sofort entschärfen oder abkleben; bei '
             'scharfkantigen Stellen Anlage außer Betrieb nehmen',
      mittel='Handlauf erneuern und Zustand in die Sichtkontrolle aufnehmen'),
    r(no('qb_handlauf_gleichlauf'), 'MEDIUM', prio=150,
      sofort='Gleichlauf durch den Wartungsdienst nachstellen lassen',
      mittel='Handlaufantrieb instand setzen; Gleichlauf bei jeder Wartung prüfen',
      klaerung=['K-B07'])],
   sources=[en115_1('5.6'), d208_028()],
   factor=F_STURZ, persons=[NUTZER, KINDER], bereich='B', agg='MAXIMUM')

hz('FT-B12', 'Seitlicher Einzug am Sockel durch fehlende oder beschädigte '
   'Sockelbürsten', GRP_BALUSTRADE,
   [('qb_sockelbuersten', 'TRIGGER', 'ALWAYS'),
    ('qa_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qb_sockelbuersten'), yes('qa_kinder')), 'HIGH', prio=300,
      sofort='Anlage bis zur Nachrüstung der Sockelbürsten außer Betrieb nehmen oder '
             'beaufsichtigen',
      mittel='Sockelbürsten beidseitig nachrüsten und in die Sichtkontrolle aufnehmen',
      klaerung=['K-B05']),
    r(no('qb_sockelbuersten'), 'MEDIUM', prio=200,
      sofort='Fehlende oder beschädigte Sockelbürsten kurzfristig ersetzen lassen',
      mittel='Sockelbürsten vollständig herstellen; Zustand in die wiederkehrende '
             'Prüfung aufnehmen',
      klaerung=['K-B05'])],
   sources=[en115_1('5.5.3'), en115_2(), d209_085('Anh. 2'), d208_028()],
   factor=F_EINZUG, persons=[NUTZER, KINDER], bereich='B')

hz('FT-B13', 'Verletzung durch beschädigte Balustrade oder gebrochenes Glas',
   GRP_BALUSTRADE,
   [('qb_balustrade_zustand', 'TRIGGER', 'ALWAYS'),
    ('qa_glasbalustrade', 'MODIFIER', 'NEVER'),
    ('qb_glas_beschaedigt', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qa_glasbalustrade')})],
   [r(yes('qb_glas_beschaedigt'), 'HIGH', prio=300,
      sofort='Anlage außer Betrieb nehmen und absperren; beschädigte Scheibe gegen '
             'Herausfallen sichern',
      mittel='Scheibe durch Verbund-Sicherheitsglas nach DIN EN 115-1 ersetzen',
      klaerung=['K-B09']),
    r(no('qb_balustrade_zustand'), 'MEDIUM', prio=200,
      sofort='Scharfe Kanten und lose Teile sofort entschärfen bzw. sichern',
      mittel='Balustrade instand setzen; Zustand in die Sichtkontrolle aufnehmen')],
   sources=[en115_1('5.5'), en115_2(), d208_028()],
   factor=F_QUETSCH, persons=[NUTZER, KINDER], bereich='B')

# ---- Gefährdungen: Stufen, Paletten, Kämme ---------------------------------
hz('FT-B14', 'Sturz durch beschädigte Stufen oder Paletten und Niveauversatz',
   GRP_STUFEN,
   [('qb_stufen_zustand', 'TRIGGER', 'ALWAYS'),
    ('qb_stufen_niveau', 'TRIGGER', 'ALWAYS'),
    ('qa_anlagenart', 'DOCUMENTATION', 'NEVER'),
    ('qa_neigung', 'DOCUMENTATION', 'NEVER')],
   [r(no('qb_stufen_zustand'), 'HIGH', prio=300,
      sofort='Anlage außer Betrieb nehmen und absperren, bis die beschädigte Stufe '
             'bzw. Palette ersetzt ist',
      mittel='Stufen/Paletten ersetzen; Stufenkettenspannung und Führung prüfen lassen'),
    r(no('qb_stufen_niveau'), 'HIGH', prio=250,
      sofort='Anlage außer Betrieb nehmen; Niveauversatz durch den Wartungsdienst '
             'beseitigen lassen',
      mittel='Ursache des Versatzes (Führung, Rollen, Kettenlängung) beheben und in '
             'die Wartung aufnehmen')],
   sources=[en115_1('5.3'), en115_2(), d208_028()],
   factor=F_STURZ, persons=[NUTZER, KINDER], bereich='B', agg='MAXIMUM')

hz('FT-B15', 'Rutschgefahr durch verschmutzte, nasse oder ölige Stufen und Paletten',
   GRP_STUFEN,
   [('qb_stufen_rutsch', 'TRIGGER', 'ALWAYS'),
    ('qa_aufstellung', 'MODIFIER', 'NEVER')],
   [r(all_(no('qb_stufen_rutsch'), eq('qa_aufstellung', 'aussen')), 'HIGH', prio=300,
      sofort='Anlage außer Betrieb nehmen und reinigen; bei Eis- oder Nässebildung '
             'außer Betrieb halten',
      mittel='Reinigungs- und Witterungskonzept für die Außenanlage festlegen '
             '(Intervalle, Abdeckung, Heizung des Zugangsbereichs prüfen)'),
    r(no('qb_stufen_rutsch'), 'MEDIUM', prio=200,
      sofort='Band umgehend reinigen; Ölverlust durch den Wartungsdienst abstellen '
             'lassen',
      mittel='Reinigungsintervall festlegen; bei Ölaustritt Ursache im Antrieb '
             'beheben lassen')],
   sources=[d208_028(), d209_085('Anh. 2'), asr18()],
   factor=F_STURZ, persons=[NUTZER, BESCHAEFTIGTE], bereich='B')

hz('FT-B16', 'Einzug am Spalt zwischen Stufe/Palette und Sockelblech', GRP_STUFEN,
   [('qb_stufenspalt', 'TRIGGER', 'ALWAYS'),
    ('qa_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qb_stufenspalt'), yes('qa_kinder')), 'HIGH', prio=300,
      sofort='Anlage außer Betrieb nehmen, bis der Spalt auf das zulässige Maß '
             'gebracht ist',
      mittel='Führung und Sockelbleche nachstellen bzw. erneuern; Spaltmaß in die '
             'wiederkehrende Prüfung aufnehmen',
      klaerung=['K-B08']),
    r(no('qb_stufenspalt'), 'MEDIUM', prio=200,
      sofort='Spaltmaß durch den Wartungsdienst kurzfristig nachstellen lassen',
      mittel='Spaltmaß dauerhaft auf das zulässige Maß bringen und dokumentiert '
             'prüfen',
      klaerung=['K-B08'])],
   sources=[en115_1('5.3.4'), en115_2(), d208_028()],
   factor=F_EINZUG, persons=[NUTZER, KINDER], bereich='B')

hz('FT-B17', 'Einzug und Fußverletzung am Kammbereich', GRP_STUFEN,
   [('qb_kamm_zustand', 'TRIGGER', 'ALWAYS'),
    ('qb_kamm_eingriff', 'TRIGGER', 'ALWAYS'),
    ('qb_kamm_abschaltung', 'COMPENSATION', 'ALWAYS'),
    ('qa_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qb_kamm_zustand'), no('qb_kamm_abschaltung')), 'HIGH', prio=300,
      sofort='Anlage außer Betrieb nehmen und absperren, bis Kammplatte und '
             'Abschaltung instand gesetzt sind',
      mittel='Kammplatte erneuern und Kammplattenabschaltung wiederherstellen; '
             'Funktionsprüfung dokumentieren',
      klaerung=['K-B06']),
    r(no('qb_kamm_abschaltung'), 'HIGH', prio=280,
      sofort='Anlage außer Betrieb nehmen, bis die Kammplattenabschaltung wieder '
             'funktioniert',
      mittel='Sicherheitseinrichtung instand setzen und regelmäßig dokumentiert '
             'prüfen'),
    r(all_(no('qb_kamm_zustand'), yes('qb_kamm_abschaltung'), yes('qa_kinder')),
      'HIGH', prio=260,
      sofort='Anlage bis zum Austausch der Kammplatte außer Betrieb nehmen',
      mittel='Kammplatte erneuern; Zustand in die tägliche Sichtkontrolle aufnehmen',
      klaerung=['K-B06']),
    r(all_(no('qb_kamm_zustand'), yes('qb_kamm_abschaltung')), 'MEDIUM', prio=200,
      sofort='Beschädigte Kammsegmente kurzfristig austauschen lassen',
      mittel='Kammplatte erneuern; Zustand in die tägliche Sichtkontrolle aufnehmen',
      klaerung=['K-B06']),
    r(no('qb_kamm_eingriff'), 'MEDIUM', prio=150,
      sofort='Fremdkörper entfernen und Kammeingriff durch den Wartungsdienst '
             'nachstellen lassen',
      mittel='Kammeingriff und Höhenlage bei jeder Wartung prüfen')],
   sources=[en115_1('5.7'), en115_2(), d209_085('Anh. 2'), d208_028()],
   factor=F_EINZUG, persons=[NUTZER, KINDER], bereich='B')

hz('FT-B18', 'Unruhiger Lauf, auffällige Geräusche und Sturz durch plötzliches '
   'Anhalten', GRP_STUFEN,
   [('qb_stufenband_lauf', 'TRIGGER', 'ALWAYS')],
   [r(no('qb_stufenband_lauf'), 'MEDIUM',
      sofort='Anlage außer Betrieb nehmen und durch den Wartungsdienst untersuchen '
             'lassen',
      mittel='Ursache beheben (Kette, Rollen, Bremse, Antrieb); Befund dokumentieren')],
   sources=[d208_028(), en115_2()],
   factor=F_KINETISCH, persons=[NUTZER], bereich='B')

# ---- Gefährdungen: Not-Halt und Bedienung ----------------------------------
hz('FT-B20', 'Fehlende, unzugängliche oder unwirksame NOT-HALT-Einrichtung',
   GRP_NOTHALT,
   [('qb_nothalt_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qb_nothalt_erreichbar', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_nothalt_vorhanden')}),
    ('qb_nothalt_funktion', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_nothalt_vorhanden')})],
   [r(no('qb_nothalt_vorhanden'), 'HIGH', prio=300,
      sofort='Anlage außer Betrieb nehmen, bis NOT-HALT-Einrichtungen an beiden '
             'Zugängen vorhanden sind',
      mittel='NOT-HALT-Einrichtungen nach DIN EN 115-1 nachrüsten'),
    r(no('qb_nothalt_erreichbar'), 'HIGH', prio=250,
      sofort='Verstellte oder verdeckte NOT-HALT-Einrichtung sofort frei machen und '
             'kennzeichnen',
      mittel='Lage und Kennzeichnung dauerhaft sicherstellen; in die Sichtkontrolle '
             'aufnehmen'),
    r(no('qb_nothalt_funktion'), 'MEDIUM', prio=200,
      sofort='Funktionsprobe umgehend durchführen und dokumentieren',
      mittel='Funktionsprüfung der NOT-HALT-Einrichtungen fest in die Betreiber-'
             'kontrolle aufnehmen')],
   sources=[en115_1('5.12'), asr18('Nr. 4.8'), d208_028()],
   factor=F_NOTFALL, persons=[NUTZER, BESCHAEFTIGTE], bereich='B')

hz('FT-B21', 'Unbeabsichtigtes oder unbefugtes Ingangsetzen der Anlage', GRP_NOTHALT,
   [('qb_bedienstellen_gesichert', 'TRIGGER', 'ALWAYS'),
    ('qb_wiederanlauf', 'TRIGGER', 'ALWAYS'),
    ('qa_betriebsart', 'MODIFIER', 'NEVER'),
    ('qb_bedarf_anlauf', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': eq('qa_betriebsart', 'bedarf')})],
   [r(no('qb_wiederanlauf'), 'HIGH', prio=300,
      sofort='Wiederanlauf nur nach Kontrolle des Bandes durch eine unterwiesene '
             'Person zulassen; Bedienstelle bis dahin sichern',
      mittel='Steuerung so einstellen bzw. ändern, dass ein Wiederanlauf nur nach '
             'bewusster Freigabe möglich ist; Ablauf in die Betriebsanweisung '
             'aufnehmen',
      klaerung=['K-B10']),
    r(no('qb_bedienstellen_gesichert'), 'MEDIUM', prio=200,
      sofort='Schlüssel abziehen und Bedienstellen gegen unbefugtes Betätigen sichern',
      mittel='Schlüsselverwaltung regeln; Bedienstellen abschließbar ausführen'),
    r(all_(eq('qa_betriebsart', 'bedarf'), no('qb_bedarf_anlauf')), 'MEDIUM', prio=150,
      sofort='Anlaufwarnung bzw. Vorlaufzeit durch den Wartungsdienst einstellen '
             'lassen',
      mittel='Bedarfssteuerung nach DIN EN 115-1 parametrieren (Warnsignal, '
             'Vorlaufzeit)')],
   sources=[en115_1('5.12'), betrsichv('§ 4'), d208_028()],
   factor=F_BEFEHL, persons=[NUTZER, BESCHAEFTIGTE], bereich='B')

# ---- Gefährdungen: Wagen ---------------------------------------------------
hz('FT-B22', 'Umkippen und Abrollen von Einkaufs- oder Transportwagen', GRP_STUFEN,
   [('qa_wagen', 'APPLICABILITY', 'NEVER',
     {'applicable_when': nin('qa_wagen', ['keine'])}),
    ('qb_wagen_geeignet', 'TRIGGER', 'CONDITIONAL',
     {'required_when': nin('qa_wagen', ['keine'])}),
    ('qb_wagen_hinweis', 'TRIGGER', 'CONDITIONAL',
     {'required_when': nin('qa_wagen', ['keine'])})],
   [r(no('qb_wagen_geeignet'), 'HIGH', prio=300,
      sofort='Beförderung von Wagen bis auf Weiteres untersagen und an den Zugängen '
             'kennzeichnen',
      mittel='Nur für die Anlage freigegebene Wagen mit wirksamer Feststelleinrichtung '
             'beschaffen; ungeeignete Wagen aussondern'),
    r(no('qb_wagen_hinweis'), 'LOW', prio=200,
      sofort='Kennzeichnung an beiden Zugängen anbringen',
      mittel='Beschilderung zur zulässigen Wagenbeförderung dauerhaft vorsehen')],
   sources=[en115_1('7'), d208_028('Abschn. 4')],
   factor=F_LAST, persons=[NUTZER, KINDER], bereich='B')

hz('FT-B23', 'Mitführen ungeeigneter Wagen, Kinderwagen oder Rollstühle', GRP_ORGA,
   [('qb_wagen_fremd', 'TRIGGER', 'ALWAYS'),
    ('qa_pmem', 'MODIFIER', 'NEVER')],
   [r(all_(yes('qb_wagen_fremd'), yes('qa_pmem')), 'HIGH', prio=300,
      sofort='An den Zugängen deutlich auf das Verbot hinweisen und auf den Aufzug '
             'verweisen; Personal zur Ansprache unterweisen',
      mittel='Barrierefreie Alternative (Aufzug) ausschildern und Wegeführung im '
             'Gebäude anpassen'),
    r(yes('qb_wagen_fremd'), 'MEDIUM', prio=200,
      sofort='Verbotszeichen anbringen und Beschäftigte zur Ansprache unterweisen',
      mittel='Wegeführung und Ausschilderung so ändern, dass die Alternative '
             'erkennbar ist')],
   sources=[en115_1('7'), d208_028()],
   factor=F_STURZ, persons=[NUTZER, KINDER], bereich='B')
