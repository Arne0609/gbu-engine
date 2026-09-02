# -*- coding: utf-8 -*-
"""B – Betrieb: Zu- und Abgänge, Umfeld, Beleuchtung, Balustrade von außen.

Quellen: ArbStättV Anhang 1.8 / ASR A1.8 (Verkehrswege, Nr. 2 nennt Fahrtreppen
und Fahrsteige ausdrücklich), DGUV Information 208-028, DIN EN 115-1/-2."""
from .common import *

# ---- Fragen ----------------------------------------------------------------
yn('qb_stauraum', 'Ausreichend freier Stau- und Bewegungsraum an Zugang und Abgang '
   '(mindestens Breite des Bandes, freie Tiefe für die abfließenden Personen)?',
   ui='2.1')
yn('qb_zugang_frei', 'Zu- und Abgangsbereiche frei von Einbauten, Warenpräsentation, '
   'Aufstellern, Abstellflächen und Werbeträgern?', ui='2.2')
yn('qb_zugang_engstelle', 'Engstelle, Tür, Kreuzung oder Gegenverkehr unmittelbar am '
   'Abgang (weniger als 3 m Abstand)?', ui='2.3')
yn('qb_boden_zustand', 'Bodenflächen an Zu- und Abgang eben, sauber, trocken und '
   'rutschhemmend?', ui='2.4')
yn('qb_boden_nass', 'Bei der Aufstellung wiederkehrend Nässe, Laub, Eis oder Schnee '
   'im Zugangsbereich?', ui='2.5', visible_when=nin('qa_aufstellung', ['innen']))
yn('qb_bel_vorhanden', 'Beleuchtung der Zu- und Abgangsbereiche vorhanden?', ui='2.6')
yn('qb_bel_ausreichend', 'Beleuchtung ausreichend und gleichmäßig (Kammbereich und '
   'erste Stufen deutlich erkennbar, keine Blendung, keine harten Schattenkanten)?',
   ui='2.7', visible_when=yes('qb_bel_vorhanden'))
yn('qb_bel_defekt', 'Defekte Leuchten im Zu- oder Abgangsbereich?', ui='2.7a',
   visible_when=yes('qb_bel_vorhanden'))
yn('qb_kammbeleuchtung', 'Kammbereich zusätzlich gekennzeichnet oder beleuchtet '
   '(z. B. grüne Kammbeleuchtung, Markierung der Stufenkanten)?', ui='2.8')

yn('qb_abweiser_vorhanden', 'Deckenabweiser bzw. Abweiser an der Kreuzungsstelle '
   'vorhanden?', ui='2.9', visible_when=yes('qa_kreuzung'))
yn('qb_abweiser_zustand', 'Abweiser unbeschädigt, richtig positioniert und wirksam?',
   ui='2.9a', visible_when=all_(yes('qa_kreuzung'), yes('qb_abweiser_vorhanden')))
yn('qb_kreuzungshoehe', 'Freie Höhe über den Stufen/Paletten an jeder Stelle '
   'mindestens 2,30 m?', ui='2.10')

yn('qb_besteig_schutz', 'Wirksame Maßnahme gegen das Besteigen oder Überklettern der '
   'Balustrade von der angrenzenden Ebene aus vorhanden (Absperrung, Umwehrung, '
   'Abweiser)?', ui='2.11', visible_when=yes('qa_besteigbar'))
yn('qb_absturzseite', 'Absturzkante neben der Anlage (offene Seite, Galerie, '
   'Treppenauge) dauerhaft gesichert?', ui='2.12')

yn('qb_hinweise', 'Benutzungshinweise und Warnzeichen an den Zugängen vorhanden '
   '(Handlauf benutzen, Kinder an die Hand nehmen, keine Kinderwagen/Rollstühle, '
   'Tiere tragen)?', ui='2.13')
yn('qb_hinweise_lesbar', 'Hinweise vollständig, lesbar und an beiden Zugängen '
   'angebracht?', ui='2.13a', visible_when=yes('qb_hinweise'))

# ---- Klärungen -------------------------------------------------------------
k('K-B01', 'Betrieb/Zugang', 'Stauraum',
  'Fehlender freier Stauraum am Abgang: Mittel oder Hoch?',
  'Mittel; Hoch, wenn zusätzlich Publikumsverkehr und eine Engstelle unmittelbar '
  'am Abgang zusammentreffen',
  'Durchgängig Hoch (Gefahr des Personenrückstaus mit Sturzfolge)',
  'ASR A1.8 fordert den Stauraum, quantifiziert die Folge aber nicht.')
k('K-B02', 'Betrieb/Zugang', 'Warenpräsentation im Zugang',
  'Warenpräsentation und Aufsteller im Zu-/Abgangsbereich: eigene Stufe oder nur '
  'Dokumentation?', 'Mittel (Sturz- und Staugefahr)',
  'Niedrig, solange die geforderte freie Breite eingehalten bleibt', '')
k('K-B03', 'Betrieb/Zugang', 'Kreuzungshöhe',
  'Freie Höhe unter 2,30 m ohne wirksamen Abweiser: Hoch oder Mittel?',
  'Hoch (Kopfanprall, Quetschgefahr an der Kreuzungsstelle)',
  'Mittel, wenn die Unterschreitung gering ist und der Bereich gekennzeichnet ist',
  'EN 115-1 fordert 2,30 m; für Bestandsanlagen ist die Kompensation über '
  'Abweiser üblich.')
k('K-B04', 'Betrieb/Zugang', 'Besteigen der Balustrade',
  'Besteigbare Balustrade ohne Schutzmaßnahme: Hoch auch ohne Kindernutzung?',
  'Hoch bei erwarteter Kindernutzung, sonst Mittel',
  'Immer Hoch (Absturz aus großer Höhe)',
  'Die Unfallschwerpunkte betreffen ganz überwiegend Kinder und Jugendliche.')

# ---- Gefährdungen ----------------------------------------------------------
hz('FT-B01', 'Personenstau und Sturz durch unzureichenden Stau- und Bewegungsraum '
   'an Zugang und Abgang', GRP_ZUGANG,
   [('qb_stauraum', 'TRIGGER', 'ALWAYS'),
    ('qb_zugang_engstelle', 'MODIFIER', 'ALWAYS'),
    ('qa_oeffentlich', 'MODIFIER', 'NEVER'),
    ('qa_mehrere', 'DOCUMENTATION', 'NEVER'),
    ('qa_foerderhoehe', 'DOCUMENTATION', 'NEVER')],
   [r(all_(no('qb_stauraum'), yes('qb_zugang_engstelle'), yes('qa_oeffentlich')),
      'HIGH', prio=300,
      sofort='Abgangsbereich sofort freiräumen; bei starkem Andrang Anlage abschalten '
             'und absperren, bis der Stauraum hergestellt ist',
      mittel='Stauraum nach ASR A1.8 dauerhaft herstellen: Einbauten, Kassen und '
             'Präsentationsflächen aus dem Abgangsbereich entfernen, Verkehrsführung '
             'im Umfeld anpassen',
      klaerung=['K-B01']),
    r(no('qb_stauraum'), 'MEDIUM', prio=200,
      sofort='Abgangsbereich freihalten und während der Stoßzeiten beobachten',
      mittel='Freien Stau- und Bewegungsraum am Zu- und Abgang dauerhaft sicherstellen '
             '(Markierung, Umplanung der Möblierung)',
      klaerung=['K-B01'])],
   sources=[asr18('Nr. 4.8'), arbstaettv('Anh. 1.8'), d208_028(), en115_1()],
   factor=F_STURZ, persons=[NUTZER, BESCHAEFTIGTE, KINDER], bereich='B')

hz('FT-B02', 'Sturz- und Staugefahr durch Einbauten und Warenpräsentation in den '
   'Zu- und Abgangsbereichen', GRP_UMFELD,
   [('qb_zugang_frei', 'TRIGGER', 'ALWAYS')],
   [r(no('qb_zugang_frei'), 'MEDIUM',
      sofort='Aufsteller, Warenträger und abgestellte Gegenstände aus dem Zu- und '
             'Abgangsbereich entfernen',
      mittel='Freizuhaltende Flächen festlegen, markieren und in die Filial-/'
             'Hausordnung aufnehmen; regelmäßig kontrollieren',
      klaerung=['K-B02'])],
   sources=[asr18('Nr. 4.8'), d208_028()],
   factor=F_STURZ, persons=[NUTZER, BESCHAEFTIGTE], bereich='B')

hz('FT-B03', 'Sturzgefahr durch rutschige, unebene oder verschmutzte Bodenflächen '
   'an Zu- und Abgang', GRP_ZUGANG,
   [('qb_boden_zustand', 'TRIGGER', 'ALWAYS'),
    ('qb_boden_nass', 'MODIFIER', 'CONDITIONAL',
     {'required_when': nin('qa_aufstellung', ['innen'])})],
   [r(all_(no('qb_boden_zustand'), yes('qb_boden_nass')), 'HIGH', prio=300,
      sofort='Bereich sofort reinigen bzw. abstreuen und bis zur Beseitigung '
             'kennzeichnen; bei Eisbildung Anlage außer Betrieb nehmen',
      mittel='Reinigungs-, Räum- und Streuplan für den witterungsbelasteten '
             'Zugangsbereich festlegen; rutschhemmenden Bodenbelag vorsehen'),
    r(no('qb_boden_zustand'), 'MEDIUM', prio=200,
      sofort='Verschmutzung beseitigen, Stolperstellen kennzeichnen',
      mittel='Bodenbelag instand setzen und rutschhemmende Eigenschaft der '
             'Nutzung entsprechend sicherstellen; Reinigungsintervall festlegen')],
   sources=[asr18('Nr. 4.1'), src('OTHER', 'ASR A1.5/1,2'), d208_028()],
   factor=F_STURZ, persons=[NUTZER, BESCHAEFTIGTE], bereich='B', agg='NONE')

hz('FT-B04', 'Unzureichende Beleuchtung der Zu- und Abgangsbereiche und des '
   'Kammbereichs', GRP_LICHT,
   [('qb_bel_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qb_bel_ausreichend', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_bel_vorhanden')}),
    ('qb_bel_defekt', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_bel_vorhanden')}),
    ('qb_kammbeleuchtung', 'COMPENSATION', 'ALWAYS')],
   [r(no('qb_bel_vorhanden'), 'HIGH', prio=300,
      sofort='Anlage bis zur Herstellung einer ausreichenden Beleuchtung außer '
             'Betrieb nehmen oder Ersatzbeleuchtung aufstellen',
      mittel='Beleuchtung der Zu- und Abgangsbereiche nach ASR A3.4 herstellen'),
    r(no('qb_bel_ausreichend'), 'MEDIUM', prio=200,
      sofort='Beleuchtung nachjustieren, Blendquellen abschirmen',
      mittel='Beleuchtungsstärke und Gleichmäßigkeit nach ASR A3.4 herstellen; '
             'Kammbereich zusätzlich kenntlich machen'),
    r(yes('qb_bel_defekt'), 'MEDIUM', prio=150,
      sofort='Defekte Leuchtmittel umgehend austauschen',
      mittel='Beleuchtung in den Wartungsplan aufnehmen und Prüfintervall festlegen')],
   sources=[asr34(), asr18('Nr. 4.8'), d208_028(), en115_1()],
   factor=F_BELEUCHTUNG, persons=[NUTZER, BESCHAEFTIGTE], bereich='B', agg='MAXIMUM')

hz('FT-B05', 'Anprall und Quetschung an der Kreuzungsstelle (Deckenabweiser, freie '
   'Höhe über dem Band)', GRP_UMFELD,
   [('qa_kreuzung', 'APPLICABILITY', 'NEVER'),
    ('qb_kreuzungshoehe', 'TRIGGER', 'ALWAYS'),
    ('qb_abweiser_vorhanden', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': yes('qa_kreuzung')}),
    ('qb_abweiser_zustand', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': all_(yes('qa_kreuzung'), yes('qb_abweiser_vorhanden'))})],
   [r(all_(no('qb_kreuzungshoehe'), no('qb_abweiser_vorhanden')), 'HIGH', prio=300,
      sofort='Kreuzungsbereich absperren oder Anlage außer Betrieb nehmen, bis ein '
             'wirksamer Abweiser montiert ist',
      mittel='Abweiser nach DIN EN 115-1 nachrüsten oder die freie Höhe von 2,30 m '
             'herstellen',
      klaerung=['K-B03']),
    r(all_(no('qb_kreuzungshoehe'), yes('qb_abweiser_vorhanden'),
           no('qb_abweiser_zustand')), 'HIGH', prio=280,
      sofort='Beschädigten oder falsch positionierten Abweiser sofort instand setzen; '
             'bis dahin Bereich absperren',
      mittel='Abweiser dauerhaft instand halten und in die wiederkehrende Prüfung '
             'aufnehmen',
      klaerung=['K-B03']),
    r(all_(no('qb_kreuzungshoehe'), yes('qb_abweiser_vorhanden'),
           yes('qb_abweiser_zustand')), 'LOW', prio=200,
      sofort='Kreuzungsbereich kennzeichnen und Nutzer auf den Abweiser hinweisen',
      mittel='Wirksamkeit des Abweisers regelmäßig prüfen; bei wesentlicher Änderung '
             'die freie Höhe herstellen',
      klaerung=['K-B03'])],
   sources=[en115_1('5.5'), en115_2(), d208_028()],
   factor=F_STOSS, persons=[NUTZER, KINDER], bereich='B')

hz('FT-B06', 'Absturz durch Besteigen oder Überklettern der Balustrade', GRP_BALUSTRADE,
   [('qa_besteigbar', 'APPLICABILITY', 'NEVER'),
    ('qb_besteig_schutz', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qa_besteigbar')}),
    ('qa_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qb_besteig_schutz'), yes('qa_kinder')), 'HIGH', prio=300,
      sofort='Angrenzenden Bereich sofort absperren, sodass die Balustrade nicht '
             'erreichbar ist; Aufsicht sicherstellen',
      mittel='Feste Umwehrung, Abweiser oder Gitter nach DIN EN 115-1 anbringen, die '
             'das Besteigen dauerhaft verhindern',
      klaerung=['K-B04']),
    r(no('qb_besteig_schutz'), 'MEDIUM', prio=200,
      sofort='Zugang zur besteigbaren Fläche einschränken und kennzeichnen',
      mittel='Bauliche Maßnahme gegen das Besteigen der Balustrade vorsehen',
      klaerung=['K-B04'])],
   sources=[en115_1('5.5.3'), en115_2(), d208_028()],
   factor=F_ABSTURZ, persons=[NUTZER, KINDER], bereich='B')

hz('FT-B07', 'Absturz neben der Anlage durch ungesicherte Absturzkante', GRP_UMFELD,
   [('qb_absturzseite', 'TRIGGER', 'ALWAYS')],
   [r(no('qb_absturzseite'), 'HIGH',
      sofort='Absturzkante sofort provisorisch sichern und absperren',
      mittel='Dauerhafte Umwehrung nach ASR A1.8 herstellen')],
   sources=[asr18('Nr. 4.6'), arbstaettv('Anh. 1.8')],
   factor=F_ABSTURZ, persons=[NUTZER, BESCHAEFTIGTE, KINDER], bereich='B')

hz('FT-B08', 'Fehlende Benutzungshinweise und Warnzeichen an den Zugängen', GRP_ORGA,
   [('qb_hinweise', 'TRIGGER', 'ALWAYS'),
    ('qb_hinweise_lesbar', 'TRIGGER', 'CONDITIONAL',
     {'required_when': yes('qb_hinweise')}),
    ('qa_kinder', 'MODIFIER', 'NEVER')],
   [r(all_(no('qb_hinweise'), yes('qa_kinder')), 'MEDIUM', prio=300,
      sofort='Benutzungshinweise und Warnzeichen an beiden Zugängen anbringen',
      mittel='Beschilderung nach DIN EN 115-1 dauerhaft vorsehen und in die '
             'Sichtkontrolle aufnehmen'),
    r(no('qb_hinweise'), 'LOW', prio=200,
      sofort='Benutzungshinweise an beiden Zugängen anbringen',
      mittel='Beschilderung nach DIN EN 115-1 vorsehen'),
    r(no('qb_hinweise_lesbar'), 'LOW', prio=150,
      sofort='Fehlende oder unlesbare Zeichen ersetzen',
      mittel='Zustand der Beschilderung in die regelmäßige Kontrolle aufnehmen')],
   sources=[en115_1('7'), d208_028(), src('OTHER', 'ASR A1.3')],
   factor=F_ORGA, persons=[NUTZER, KINDER], bereich='B')
