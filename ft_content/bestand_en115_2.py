# -*- coding: utf-8 -*-
"""N – Bestandsanlage nach DIN EN 115-2:2021-12.

Setzt die Prüfliste aus Anhang B (Tabelle B.2, „Sicherheitsprüfung an
bestehenden Fahrtreppen und Fahrsteigen") als dritten Erhebungsbereich um:
je Prüfpunkt eine Gefährdung, deren Stufe sich aus der Prioritätsstufe der Norm
ergibt (H → Hoch, M → Mittel, N → Niedrig). Der Zeitplan aus Tabelle A.2 steht
in der mittelfristigen Maßnahme.

Aufbau und Grenzen:
  * Die Norm ist urheberrechtlich geschützt. Übernommen sind Nummer, Abschnitts-
    bezug und Prioritätsstufe als Fundstelle; Fragetexte und Maßnahmen sind
    eigene Formulierungen.
  * Anhang A und Anhang B sind INFORMATIV. Die Prioritätsstufe ist eine
    Empfehlung der Norm, keine Rechtspflicht – deshalb trägt jede Regel den
    Quellenbezug, und Abweichungen laufen über die Klärungsliste.
  * Anhang A erlaubt eine nationale Filterung (A.3): Punkte, die nach dem beim
    Bau geltenden Regelwerk bereits gleichwertig abgedeckt waren, dürfen aus dem
    Risikoprofil gestrichen werden. Diese Filterung ist hier NICHT eingebaut
    (offene Klärung K-N02) – ohne sie wird zu viel erhoben, mit ihr zu wenig
    bewertet.
  * Wo der Bereich B oder I dieselbe Sache schon fragt, wird die vorhandene
    Frage wiederverwendet (Feld `ref`), damit niemand zweimal antwortet. Die
    Gefährdung entsteht trotzdem neu – sie trägt die Sicht der Norm.

Schalter: qa_teil_en115_2. Nein → der ganze Bereich ist NOT_APPLICABLE.
"""
from .common import *

# ---- Schalter --------------------------------------------------------------
yn('qa_teil_en115_2', 'Soll die Anlage zusätzlich nach DIN EN 115-2 '
   '(Bestandsanlage, Anhang B) bewertet werden?', ui='1.21',
   help='Ja = die Prüfliste der Norm wird als eigener Erhebungsbereich '
        'abgearbeitet und zeigt den Abstand zum Stand der Technik nach '
        'DIN EN 115-1:2017. Nein = nur Betreiber- und Instandhaltungsteil.')

EN = yes('qa_teil_en115_2')
FILTER = ('qa_teil_en115_2', 'APPLICABILITY', 'NEVER')

ZEITPLAN = {'H': 'kurzfristig umsetzen',
            'M': 'mittelfristig oder im Rahmen einer umfangreichen Modernisierung umsetzen',
            'N': 'langfristig oder im Rahmen einer Modernisierung der betroffenen '
                 'Komponente umsetzen'}
STUFE = {'H': 'HIGH', 'M': 'MEDIUM', 'N': 'LOW'}
PRIO_LABEL = {'H': 'Hoch', 'M': 'Mittel', 'N': 'Niedrig'}

# ---- Klärungen -------------------------------------------------------------
k('K-N01', 'EN 115-2', 'Doppelbewertung',
  'Der Bereich N bewertet teilweise dieselben Sachverhalte wie B und I '
  '(z. B. Kammplattenabschaltung). Soll er in die Gesamtübersicht einfließen '
  'oder getrennt als „Abstand zum Stand der Technik" ausgewiesen werden?',
  'Getrennt ausweisen: eigene Übersicht im Bericht, nicht in die Ampel des '
  'Betreiberteils einrechnen',
  'Alles in eine Gesamtübersicht (dann erscheinen einzelne Mängel doppelt)',
  'EN 115-2 ist eine Modernisierungsnorm, die Betreiber-GBU eine Pflicht nach '
  'BetrSichV – die Adressaten und Fristen sind verschieden.')
k('K-N02', 'EN 115-2', 'Nationale Filterung nach A.3',
  'Anhang A.3 erlaubt, Punkte zu streichen, die das beim Bau geltende '
  'Regelwerk bereits gleichwertig abgedeckt hat. Soll der Katalog das über das '
  'Baujahr bzw. den Normstand automatisch tun?',
  'Vorerst nein – alle Punkte erheben, Filterung erst nach fachlicher '
  'Festlegung der Gleichwertigkeiten je Baujahr',
  'Ja, Punkte nach Normstand ausblenden (spart Erhebungsaufwand, verdeckt aber '
  'Gefährdungen)',
  'Die Norm überlässt die Filterung ausdrücklich der nationalen Ebene; eine '
  'deutsche Festlegung dazu liegt nicht vor.')
k('K-N03', 'EN 115-2', 'Priorität Extrem',
  'Tabelle A.2 kennt über „Hoch" hinaus die Stufe „Extrem – sofort, Anlage '
  'muss stillgesetzt werden". Tabelle B.2 vergibt nur H/M/N. Soll es im Typ '
  'eine Stillsetz-Automatik geben?',
  'Nein – „Hoch" bleibt die oberste Stufe; die Stillsetzung entscheidet die '
  'Fachkraft im Einzelfall über die Sofortmaßnahme',
  'Ja – bestimmte Punkte (z. B. Bremse, Kammabschaltung) auf Extrem heben und '
  'die Stillsetzung als Sofortmaßnahme erzwingen',
  'B.2 selbst stuft keinen Punkt als Extrem ein; Extrem entsteht erst über die '
  'anlagenbezogene Risikobeurteilung nach A.3.')

# ---- Prüfliste (Tabelle B.2) -----------------------------------------------
# nr · Abschnitt EN 115-1:2017 · Priorität · Baugruppe · Faktor · Personen ·
# Frage (eigene Formulierung) · Maßnahme · na = „nicht anwendbar" zulässig ·
# ref = vorhandene Frage statt neuer Frage · cond = eigene Mangelbedingung
P = []


def p(nr, ab, prio, grp, fak, pers, frage, mass, na=False, ref=None, cond=None,
      sofort=None, help=None):
    P.append(dict(nr=nr, ab=ab, prio=prio, grp=grp, fak=fak, pers=pers,
                  frage=frage, mass=mass, na=na, ref=ref, cond=cond,
                  sofort=sofort, help=help))


N_, W_, B_ = [NUTZER], [WARTUNG], [NUTZER, BESCHAEFTIGTE]
NK = [NUTZER, KINDER]

# 5.1 Allgemeine Anforderungen
p('1', '5.1', 'H', GRP_STOFFE, F_GEFAHRSTOFF, [WARTUNG, REINIGUNG],
  'Ist die Anlage frei von zerfallenden Gefahrstoffen (z. B. asbesthaltige '
  'Bremsbeläge oder Verkleidungen)?',
  'Gefahrstoffhaltige Bauteile ersetzen; solange sie verbleiben, Bauteile '
  'kennzeichnen und Arbeiten daran ausschließen',
  sofort='Arbeiten an den betroffenen Bauteilen einstellen, bis das Material '
         'bestimmt ist')

# 5.2 Tragkonstruktion und Verkleidung
p('2', '5.2.1', 'M', GRP_TRAG, F_BEWEGT, W_,
  'Sind mechanisch bewegte Teile durch vollwandige Abdeckungen verkleidet?',
  'Vollwandige Abdeckungen nach DIN EN 115-1:2017 einbauen')
p('3', '5.2.1', 'M', GRP_TRAG, F_BEWEGT, W_,
  'Entsprechen die Lüftungsöffnungen den Sicherheitsabständen nach '
  'DIN EN ISO 13857?',
  'Abdeckungen einbauen, die die Sicherheitsabstände nach DIN EN ISO 13857 '
  'einhalten', na=True)
p('4', '5.2.1', 'M', GRP_TRAG, F_BEWEGT, W_,
  'Sind die Zugänge zu Maschinenräumen sowie zur Antriebs- und Umkehrstation '
  'durch Sicherheitskontakte überwacht?',
  'Zugänge mit Sicherheitskontakten nach DIN EN 115-1:2017 überwachen')
p('5', '5.2.1', 'M', GRP_TRAG, F_BEWEGT, W_,
  'Sind Wartungstüren, Wartungsklappen und Bodenplatten, die geöffnet werden '
  'können, durch Sicherheitseinrichtungen überwacht?',
  'Sicherheitseinrichtungen an Wartungstüren, -klappen und Bodenplatten '
  'nachrüsten')
p('6.1', '5.2.2.1', 'M', GRP_TRAG, F_BRAND, W_,
  'Liegen Anweisungen für die regelmäßige Reinigung der Tragkonstruktion vor '
  'und werden sie umgesetzt?',
  'Anweisungen für die regelmäßige Reinigung erstellen und die Durchführung '
  'nachweisen')
p('6.2', '5.2.2.2', 'M', GRP_TRAG, F_BRAND, B_,
  'Lässt die Bauart eine regelmäßige Reinigung zu, sodass sich keine '
  'brennbaren Stoffe ansammeln?',
  'Reinigungsmöglichkeit schaffen oder eine Einrichtung zur Brandbekämpfung '
  'einbauen')

# 5.3 Stufen, Paletten und Gurt
p('7', '5.3.1', 'H', GRP_STUFEN, F_STURZ, NK,
  'Ist die Trittsicherheit auf den Trittflächen gegeben?',
  'Trittsicherheit der Trittflächen wiederherstellen (Belag, Profilierung, '
  'Reinigung)', ref='qb_stufen_rutsch')
p('8', '5.3.2', 'M', GRP_STUFEN, F_STURZ, NK,
  'Sind die Stufen bzw. Paletten an den Rändern gekennzeichnet '
  '(Stufenmarkierung)?',
  'Stufenmarkierung nach DIN EN 115-1:2017 anbringen oder eine '
  'Unterstufenbeleuchtung an den Zu- und Abgängen einbauen', na=True)
p('9', '5.3.3', 'H', GRP_STUFEN, F_EINZUG, NK,
  'Bleiben die seitlichen Verschiebungen der Stufen bzw. Paletten im '
  'zulässigen Bereich?',
  'Führung und Abstände nach DIN EN 115-1:2017 wiederherstellen', na=True,
  ref='qb_stufenspalt')
p('10', '5.3.4', 'H', GRP_STUFEN, F_EINZUG, NK,
  'Bleiben die Abstände zwischen aufeinanderfolgenden Stufen bzw. Paletten im '
  'zulässigen Bereich (bei unprofilierter Setzstufe und nicht ineinander '
  'greifenden Paletten höchstens 5 mm)?',
  'Abstände nach DIN EN 115-1:2017 einstellen; bei unprofilierter Setzstufe '
  'und nicht ineinandergreifenden Paletten 5 mm nicht überschreiten', na=True)
p('11', '5.3.5', 'M', GRP_STUFEN, F_STURZ, NK,
  'Ist eine Einrichtung zur Erkennung fehlender Stufen bzw. Paletten '
  'vorhanden?',
  'Einrichtung zur Erkennung fehlender Stufen/Paletten nachrüsten', na=True)
p('12', '5.3.6', 'M', GRP_STUFEN, F_KINETISCH, NK,
  'Ist die Ketten- bzw. Gurtspanneinrichtung gegen übermäßige Bewegung '
  'überwacht?',
  'Einrichtung zur Erkennung von Bruch oder unzulässiger Längung der '
  'Antriebselemente nachrüsten')

# 5.4 Antriebssysteme
p('13.1', '5.4.1', 'H', GRP_ANTRIEB, F_KINETISCH, N_,
  'Wird der Antrieb durch zwei voneinander unabhängige Schütze angehalten?',
  'Zwei voneinander unabhängige Schütze nach DIN EN 115-1:2017 einbauen')
p('13.2', '5.4.1', 'H', GRP_ANTRIEB, F_KINETISCH, N_,
  'Ist das erneute Anfahren eindeutig an den Zustand beider Schütze gebunden?',
  'Steuerung so ändern, dass das Anfahren nur bei einwandfreiem Zustand beider '
  'Schütze möglich ist')
p('13.3', '5.4.1', 'M', GRP_ANTRIEB, F_BEWEGT, W_,
  'Ist der sichere Betrieb der Handdrehvorrichtung gewährleistet?',
  'Handdrehvorrichtung nach DIN EN 115-1:2017 ausführen (Überwachung, '
  'Zugänglichkeit)', na=True)
p('14', '5.4.2.1.1', 'M', GRP_ANTRIEB, F_KINETISCH, N_,
  'Ist ein Schutz gegen Übergeschwindigkeit vorhanden?',
  'Schutzeinrichtung gegen Übergeschwindigkeit nachrüsten', na=True)
p('15', '5.4.2.1.2', 'M', GRP_ANTRIEB, F_KINETISCH, N_,
  'Ist ein Schutz gegen unbeabsichtigte Umkehr der Fahrtrichtung vorhanden?',
  'Schutzeinrichtung gegen unbeabsichtigte Richtungsumkehr nachrüsten')
p('16', '5.4.2.1', 'H', GRP_ANTRIEB, F_KINETISCH, N_,
  'Wird die Energiezufuhr zur elektromechanischen Bremse durch mindestens zwei '
  'voneinander unabhängige elektrische Betriebsmittel unterbrochen?',
  'Bremsansteuerung auf zwei unabhängige Betriebsmittel umbauen')
p('17.1', '5.4.2.1.3', 'N', GRP_ANTRIEB, F_KINETISCH, N_,
  'Wird erkannt, wenn die Betriebsbremse nicht lüftet?',
  'Einrichtung zur Erkennung des Nichtlüftens der Betriebsbremse nachrüsten')
p('17.2', '5.4.2.2', 'M', GRP_ANTRIEB, F_KINETISCH, N_,
  'Wird erkannt, wenn die Hilfsbremse nicht lüftet?',
  'Einrichtung zur Erkennung des Nichtlüftens der Hilfsbremse nachrüsten')
p('18', '5.4.2.2', 'M', GRP_ANTRIEB, F_KINETISCH, N_,
  'Ist eine Zusatzbremse vorhanden?',
  'Zusatzbremse nach DIN EN 115-1:2017 nachrüsten', na=True)
p('19', '5.4.2.1.4', 'H', GRP_ANTRIEB, F_KINETISCH, NK,
  'Hält die Anlage ohne Last innerhalb der zulässigen Anhaltewege an?',
  'Bremssystem so einstellen bzw. instand setzen, dass die Anhaltewege nach '
  'DIN EN 115-1:2017 eingehalten werden',
  sofort='Anhalteweg messen lassen; bei deutlicher Überschreitung Anlage außer '
         'Betrieb nehmen')

# 5.5 Balustrade
p('20', '5.5.2.1', 'N', GRP_BALUSTRADE, F_ABSTURZ, NK,
  'Liegt die Handlaufhöhe im geneigten Bereich zwischen 0,90 m und 1,10 m?',
  'Umgebung auf ausreichenden Absturzschutz beurteilen; danach Handlaufhöhe '
  'anpassen oder einen angemessenen Absturzschutz vorsehen')
p('21', '5.5.2.2', 'N', GRP_BALUSTRADE, F_STURZ, NK,
  'Beträgt der Neigungswinkel der inneren Abdeckleiste mindestens 25°?',
  'Innere Abdeckleiste nach DIN EN 115-1:2017 ausführen', na=True)
p('22', '5.5.2.3', 'H', GRP_BALUSTRADE, F_ABSTURZ, NK,
  'Sind Anti-Kletter-Einrichtungen an der äußeren Abdeckleiste vorhanden?',
  'Anti-Kletter-Einrichtungen an der äußeren Abdeckleiste nachrüsten', na=True)
p('23', '5.5.2.3', 'N', GRP_BALUSTRADE, F_ABSTURZ, NK,
  'Sind Anti-Rutscheinrichtungen auf den Balustradendeckleisten vorhanden '
  '(zwischen benachbarten Anlagen oder zu seitlichen Wänden)?',
  'Anti-Rutscheinrichtungen auf den Deckleisten nachrüsten', na=True)
p('24', '5.5.3', 'H', GRP_BALUSTRADE, F_EINZUG, NK,
  'Sind Sockelabweiser vorhanden, die das Einklemmen zwischen '
  'Balustradensockel und Stufen verringern?',
  'Sockelabweiser nach DIN EN 115-1:2017 einbauen; lassen die Maße das nicht '
  'zu, den Abstand zwischen Sockelabweiser und Stufennase auf 8 mm verringern',
  na=True)

# 5.6 Handlaufsystem
p('25', '5.6.1', 'M', GRP_BALUSTRADE, F_STURZ, NK,
  'Ist eine Einrichtung zur Überwachung der Handlaufgeschwindigkeit oder '
  'wenigstens zur Erkennung der Handlaufbewegung vorhanden?',
  'Überwachung der Handlaufgeschwindigkeit nachrüsten; ist das nicht möglich, '
  'eine Einrichtung zur Erkennung der Bewegung einbauen')
p('26', '5.6.2', 'H', GRP_BALUSTRADE, F_EINZUG, NK,
  'Liegt der horizontale Abstand zwischen Handlauf, Verkleidungs- und '
  'Führungsprofilen im zulässigen Bereich?',
  'Bauteile so ändern, dass die zulässigen Abstände erreicht werden')
p('27', '5.6.3.1', 'H', GRP_BALUSTRADE, F_EINZUG, NK,
  'Ist eine Schutzeinrichtung an der Einlaufstelle des Handlaufs vorhanden?',
  'Schutzeinrichtung an der Einlaufstelle des Handlaufs nachrüsten',
  ref='qb_handlaufeinfuehrung')
p('28', '5.6.3.1', 'M', GRP_BALUSTRADE, F_EINZUG, NK,
  'Ist an der Einlaufstelle des Handlaufs eine elektrische '
  'Sicherheitseinrichtung vorhanden?',
  'Elektrische Sicherheitseinrichtung an der Einlaufstelle nachrüsten',
  ref='qb_handlauf_abschaltung')
p('29', '5.6.3.2', 'M', GRP_BALUSTRADE, F_EINZUG, NK,
  'Entsprechen die Balustradenköpfe der DIN EN 115-1:2017?',
  'Balustradenköpfe anpassen oder angemessene trennende Schutzeinrichtungen '
  'einbauen', na=True)

# 5.7 Zu- und Abgänge
p('30', '5.7.1', 'H', GRP_ZUGANG, F_STURZ, NK,
  'Ist die Trittsicherheit an den Zu- und Abgängen gegeben (Kammplatte und '
  'Bodenplatte)?',
  'Kamm- und Bodenplatten mit trittsicherem Belag versehen')
p('31', '5.7.2', 'H', GRP_STUFEN, F_EINZUG, NK,
  'Greifen die Kammzähne korrekt in die Stufen- bzw. Palettenrillen ein?',
  'Kammeingriff nach DIN EN 115-1:2017 herstellen und überwachen',
  ref='qb_kamm_eingriff')
p('32', '5.7.3', 'H', GRP_STUFEN, F_EINZUG, NK,
  'Ist im Kammbereich eine elektrische Sicherheitseinrichtung vorhanden?',
  'Elektrische Sicherheitseinrichtung im Kammbereich nachrüsten',
  ref='qb_kamm_abschaltung')
p('33', '5.7.4', 'H', GRP_STUFEN, F_STURZ, NK,
  'Ist eine Einrichtung zur Erkennung des Absenkens einer Stufe oder Palette '
  'vorhanden?',
  'Einrichtung zur Erkennung abgesenkter Stufen/Paletten nachrüsten')

# 5.8 Betriebsräume, Antriebs- und Umkehrstation
p('34', '5.8.1', 'M', GRP_STATION, F_ROTIEREND, W_,
  'Sind zugängliche bewegliche und rotierende Teile in den Betriebsräumen '
  'geschützt?',
  'Schutz der beweglichen und rotierenden Teile nach DIN EN 115-1:2017 '
  'herstellen', ref='qi_schutzabdeckungen')
p('35', '5.8.2', 'M', GRP_STATION, F_STURZ, W_,
  'Stehen ausreichende Standflächen für Instandhaltungsarbeiten zur Verfügung?',
  'Ausreichende Standflächen herstellen; ist das nicht möglich, eine '
  'Erkennungseinrichtung (z. B. Lichtschranke) einbauen', ref='qi_station_platz')
p('36', '5.8.3', 'M', GRP_STATION, F_LAST, W_,
  'Sind geeignete Lastanschlagpunkte für bewegbare Schaltschränke vorhanden?',
  'Geeignete Lastanschlagpunkte nachrüsten', na=True)
p('37', '5.8.4', 'H', GRP_LICHT, F_BELEUCHTUNG, W_,
  'Sind in den Betriebsräumen Steckdosen für die Beleuchtung vorhanden?',
  'Geeignete Steckdosen nach DIN EN 115-1:2017 einbauen')
p('38', '5.8.4', 'M', GRP_LICHT, F_BELEUCHTUNG, W_,
  'Wird in den Arbeitsbereichen eine Beleuchtungsstärke von 200 Lux erreicht?',
  'Beleuchtung so ergänzen, dass die Beleuchtungsstärke nach '
  'DIN EN 115-1:2017 erreicht wird')
p('39.1', '5.8.5', 'H', GRP_NOTHALT, F_BEWEGT, W_,
  'Ist in der Antriebs- und Umkehrstation ein Ausschalter im Arbeitsbereich '
  'vorhanden?',
  'Ausschalter im Arbeitsbereich der Antriebs- und Umkehrstation nachrüsten',
  ref='qi_nothalt_arbeitsbereich')
p('39.2', '5.8.5', 'N', GRP_NOTHALT, F_BEWEGT, W_,
  'Entspricht dieser Ausschalter in Ausführung und Anordnung der '
  'DIN EN 115-1:2017?',
  'Ausschalter in geeigneter Ausführung nachrüsten')

# 5.11 Elektrische Installationen und Einrichtungen
p('40', '5.11.1.2', 'H', GRP_ELEKTRO, F_ELEKTRISCH, W_,
  'Sind spannungsführende Teile ausreichend gegen direktes Berühren '
  'abgedeckt?',
  'Schutz gegen direktes Berühren nach DIN EN 115-1:2017 herstellen',
  ref='qi_elektrik_beruehrsicher')
p('41', '5.11.1.3', 'H', GRP_ELEKTRO, F_ELEKTRISCH, W_,
  'Ist die Isolation der elektrischen Anlage geeignet und unbeschädigt?',
  'Schutzmaßnahmen gegen elektrischen Schlag nach DIN EN 115-1:2017 '
  'durchführen')
p('42.1', '5.11.2', 'H', GRP_ELEKTRO, F_BEWEGT, W_,
  'Ist ein Hauptschalter vorhanden, der das unbeabsichtigte Einschalten der '
  'Anlage verhindert?',
  'Hauptschalter nach DIN EN 115-1:2017 einbauen', ref='qi_hauptschalter')
p('42.2', '5.11.2', 'M', GRP_ELEKTRO, F_BEWEGT, W_,
  'Ist dieser Hauptschalter für seinen Zweck geeignet (Lage, Ausführung, '
  'Sicherung gegen Wiedereinschalten)?',
  'Geeigneten Hauptschalter nach DIN EN 115-1:2017 einbauen',
  ref='qi_hauptschalter_sicherbar')

# 5.12 Elektrische Steuerungssysteme
p('43', '5.12.1.3', 'N', GRP_STEUERUNG, F_ELEKTRISCH, NK,
  'Ist ein Schutz gegen elektrostatische Aufladung vorhanden (z. B. Handlauf, '
  'Stufenband)?',
  'Abhilfe gegen elektrostatische Aufladung nach DIN EN 115-1:2017 schaffen')
p('44', '5.12.1.1', 'H', GRP_STEUERUNG, F_ELEKTRISCH, W_,
  'Sind unmittelbar mit der Stromversorgung verbundene Motoren geschützt?',
  'Schutzeinrichtung für die Motoren nach DIN EN 115-1:2017 einbauen')
p('45', '5.12.1.2', 'H', GRP_STEUERUNG, F_BEWEGT, B_,
  'Sind die Sicherheitseinrichtungen selbst gegen Manipulation und Ausfall '
  'geschützt?',
  'Schutz der Sicherheitseinrichtungen nach DIN EN 115-1:2017 herstellen')
p('46.1', '5.12.3.1.2', 'H', GRP_NOTHALT, F_NOTFALL, B_,
  'Ist im Publikumsbereich eine Notabschalteinrichtung vorhanden?',
  'Notabschalteinrichtungen nach DIN EN 115-1:2017 einbauen',
  ref='qb_nothalt_vorhanden')
p('46.2', '5.12.3.1.1', 'M', GRP_NOTHALT, F_NOTFALL, B_,
  'Sind Gestaltung und Anordnung der Notabschalteinrichtung angemessen?',
  'Notabschalteinrichtungen nach DIN EN 115-1:2017 gestalten und anordnen',
  na=True, ref='qb_nothalt_erreichbar')
p('47', '5.12.3.1.3', 'H', GRP_NOTHALT, F_NOTFALL, B_,
  'Ist die Stellung der Ausschalteinrichtung erkennbar?',
  'Ausschaltanzeiger nach DIN EN 115-1:2017 vorsehen', na=True)
p('48.1', '5.12.3.2', 'M', GRP_INSP, F_BEWEGT, W_,
  'Ist eine Revisionssteuerung vorhanden?',
  'Steckdosen und Revisionssteuerung nach DIN EN 115-1:2017 vorsehen',
  ref='qi_inspektionssteuerung', cond=eq('qi_inspektionssteuerung', 'keine'))
p('48.2', '5.12.3.2.5', 'N', GRP_INSP, F_BEWEGT, W_,
  'Ist die Revisionssteuerung mit beiden Händen gleichzeitig zu betätigen '
  '(Zweiknopfausführung)?',
  'Revisionssteuerung in Zweiknopfausführung nach DIN EN 115-1:2017 vorsehen',
  ref='qi_inspektionssteuerung', cond=eq('qi_inspektionssteuerung', 'einknopf'))

# 5.13 Schnittstellen mit dem Gebäude
p('49', '5.13.1.1', 'H', GRP_GEBAEUDE, F_STOSS, NK,
  'Beträgt die freie Höhe über den Stufen, Paletten oder dem Gurt an allen '
  'Stellen mindestens 2,30 m?',
  'Freie Höhe herstellen oder den Bereich mit mindestens 50 Lux beleuchten, '
  'scharfe Kanten beseitigen und Abweiser bzw. Warnschilder anbringen',
  ref='qb_kreuzungshoehe')
p('50', '5.13.1.2', 'H', GRP_GEBAEUDE, F_QUETSCH, NK,
  'Beträgt der horizontale Abstand zwischen Handlauf und Gebäudeteilen '
  'mindestens 80 mm?',
  'Horizontalen Abstand von mindestens 80 mm herstellen')
p('51', '5.13.1.3', 'H', GRP_GEBAEUDE, F_STOSS, NK,
  'Sind bauliche Hindernisse, die zu Verletzungen führen können, durch '
  'Schutzmaßnahmen entschärft?',
  'Abweiser an baulichen Hindernissen einbauen')
p('52', '5.13.1.4', 'M', GRP_GEBAEUDE, F_STURZ, B_,
  'Ist ausreichender Stauraum an den Zu- und Abgängen vorhanden?',
  'Stauraum herstellen oder zusätzliche Notausschalteinrichtungen einbauen',
  ref='qb_stauraum')
p('53', '5.13.1.5', 'N', GRP_GEBAEUDE, F_STURZ, NK,
  'Wird erkannt, wenn eine nachfolgende Anlage anhält oder der Ausgang durch '
  'bauliche Maßnahmen blockiert ist?',
  'Elektrische Sicherheitseinrichtung zur Erkennung nachrüsten', na=True)
p('54', '5.13.1.6', 'H', GRP_GEBAEUDE, F_ABSTURZ, NK,
  'Besteht an den Zu- und Abgängen ein angemessener Schutz gegen Absturz?',
  'Geeignete Hindernisse gegen Absturz einbauen', na=True,
  ref='qb_absturzseite')
p('55', '5.13.1.7', 'M', GRP_LICHT, F_BELEUCHTUNG, NK,
  'Ist die Beleuchtung an der Kammschnittlinie angepasst?',
  'Beleuchtung an der Kammschnittlinie nach DIN EN 115-1:2017 vorsehen')
p('56', '5.13.2.1', 'M', GRP_GEBAEUDE, F_ORGA, W_,
  'Sind Betriebsräume außerhalb der Tragkonstruktion absperrbar?',
  'Betriebsräume mit einem Schloss nach DIN EN 13015 sichern', na=True)
p('57', '5.13.2.2', 'M', GRP_LICHT, F_BELEUCHTUNG, W_,
  'Ist die Beleuchtung in Betriebsräumen und Arbeitsbereichen außerhalb der '
  'Tragkonstruktion angepasst?',
  'Beleuchtung in den Betriebsräumen nach DIN EN 115-1:2017 vorsehen', na=True)
p('58', '5.13.2.3', 'M', GRP_LICHT, F_FLUCHT, W_,
  'Ist eine Notbeleuchtung für die sichere Evakuierung vorhanden?',
  'Notbeleuchtung nach DIN EN 115-1:2017 einbauen', na=True)
p('59', '5.13.2.4', 'H', GRP_GEBAEUDE, F_ERGONOMIE, W_,
  'Sind die Arbeitsflächen in Betriebsräumen außerhalb der Tragkonstruktion '
  'angemessen?',
  'Angemessene Arbeitsflächen nach DIN EN 115-1:2017 vorsehen', na=True)
p('60', '5.13.2.5', 'H', GRP_GEBAEUDE, F_ERGONOMIE, W_,
  'Sind Zugangshöhe und Zugangsbreite zu den Betriebsräumen angemessen?',
  'Zugänge zu den Betriebsräumen nach DIN EN 115-1:2017 herstellen', na=True)
p('61', '5.13.2.6', 'H', GRP_GEBAEUDE, F_STOSS, W_,
  'Ist die freie Höhe in den Betriebsräumen angemessen?',
  'Freie Höhe herstellen oder scharfe Kanten beseitigen und Abweiser bzw. '
  'Warnschilder anbringen', na=True)
p('62', '5.13.3', 'H', GRP_ELEKTRO, F_ELEKTRISCH, W_,
  'Ist die elektrische Energieversorgung der Anlage angemessen ausgeführt?',
  'Elektrische Energieversorgung nach DIN EN 115-1:2017 herstellen')

# 5.14 Sicherheitszeichen für den Benutzer
p('63', '5.14', 'M', GRP_ORGA, F_ORGA, NK,
  'Ist ein vollständiger Satz Sicherheitszeichen für die Benutzer angebracht?',
  'Sicherheitszeichen nach DIN EN 115-1:2017 anbringen', ref='qb_hinweise')

# 5.15 Einsatz von Einkaufs- und Gepäckwagen
p('64.1', '5.15.1', 'H', GRP_ZUGANG, F_LAST, NK,
  'Sind an der Fahrtreppe Hindernisse vorhanden, die den Zugang mit Einkaufs- '
  'und Gepäckwagen verhindern?',
  'Hindernisse zur Verhinderung des Zugangs nach DIN EN 115-1:2017 einbauen',
  na=True)
p('64.2', '5.15.1', 'M', GRP_ZUGANG, F_LAST, NK,
  'Sind diese Hindernisse ausreichend wirksam?',
  'Wirksame Hindernisse nach DIN EN 115-1:2017 einbauen', na=True)
p('65', '5.15.2', 'N', GRP_ZUGANG, F_LAST, NK,
  'Werden auf dem Fahrsteig nur darauf abgestimmte Einkaufs- und Gepäckwagen '
  'eingesetzt?',
  'Auf den Fahrsteig abgestimmte Wagen bereitstellen', na=True,
  ref='qb_wagen_geeignet')

# ---- Fragen und Gefährdungen erzeugen --------------------------------------
JA, NEIN, NZ = 'ja', 'nein', 'nicht_anwendbar'

for i, d in enumerate(P, 1):
    nr = d['nr']
    code = 'FT-N' + nr.replace('.', '-')
    ui = '13.' + nr
    quelle = [en115_2('Tab. B.2 Nr. %s' % nr), en115_1(d['ab'])]
    prio = d['prio']
    mittel = '%s (EN 115-2: Priorität %s, %s)' % (d['mass'], PRIO_LABEL[prio],
                                                  ZEITPLAN[prio])
    if d['ref']:
        trigger = d['ref']
        cond = d['cond'] or no(trigger)
        fragen = [FILTER, (trigger, 'TRIGGER', 'ALWAYS')]
        hinweis = ('Prüfpunkt %s der EN 115-2 wird aus der Antwort auf die '
                   'Frage im Betreiber- bzw. Instandhaltungsteil abgeleitet.' % nr)
    else:
        opts = [(JA, 'Anforderung erfüllt'), (NEIN, 'Anforderung nicht erfüllt')]
        if d['na']:
            opts.append((NZ, 'Nicht anwendbar'))
        qc = 'qn_' + nr.replace('.', '_')
        sel(qc, d['frage'], opts, ui=ui, visible_when=EN,
            help=d['help'] or ('DIN EN 115-1:2017, Abschnitt %s · Prüfliste '
                               'EN 115-2 Anhang B, Nr. %s · Prioritätsstufe %s'
                               % (d['ab'], nr, PRIO_LABEL[prio])))
        trigger = qc
        cond = eq(qc, NEIN)
        fragen = [FILTER, (qc, 'TRIGGER', 'CONDITIONAL', {'required_when': EN})]
        hinweis = None

    regeln = [r(cond, STUFE[prio], prio=200, sofort=d['sofort'], mittel=mittel,
                evidence='HIGH_CONFIDENCE', sources=quelle,
                notes='Stufe aus der Prioritätsstufe %s der EN 115-2 '
                      '(Anhang B ist informativ).' % PRIO_LABEL[prio],
                klaerung=['K-N01'])]
    if d['na'] and not d['ref']:
        regeln.insert(0, r(eq(trigger, NZ), 'NOT_APPLICABLE', prio=900,
                           evidence='HIGH_CONFIDENCE',
                           notes='Prüfpunkt an dieser Anlage nicht anwendbar '
                                 '(Tabelle B.2 sieht das ausdrücklich vor).'))

    hz(code, 'EN 115-2 Nr. %s: %s' % (nr, d['frage'].rstrip('?')), d['grp'],
       fragen, regeln, sources=quelle, factor=d['fak'], persons=d['pers'],
       bereich='N', description=hinweis, klaerung=['K-N02'])
