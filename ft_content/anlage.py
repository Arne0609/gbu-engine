# -*- coding: utf-8 -*-
"""A – Anlagenmerkmale. Reine Filter-/Modifier-Fragen (keine eigene Gefährdung).

qa_teil_instandhaltung schaltet den kompletten Erhebungsbereich I ab, wenn nur
die Betreiber-GBU erstellt wird – die I-Gefährdungen werden dann NOT_APPLICABLE
statt INCOMPLETE."""
from .common import *

sel('qa_anlagenart', 'Anlagenart', ui='1.1',
    options=[('fahrtreppe', 'Fahrtreppe (Stufenband)'),
             ('fahrsteig_geneigt', 'Fahrsteig, geneigt (Palettenband)'),
             ('fahrsteig_horizontal', 'Fahrsteig, horizontal (Palettenband)')],
    help='Steuert stufen- bzw. palettenbezogene Gefährdungen und die '
         'Wagenbeförderung.')

sel('qa_aufstellung', 'Aufstellung', ui='1.2',
    options=[('innen', 'Innen'),
             ('aussen_ueberdacht', 'Außen, überdacht'),
             ('aussen', 'Außen, frei bewittert')],
    help='Außenanlagen: Nässe, Eis, Laub, Sonneneinstrahlung – wirkt auf '
         'Rutschgefahr und Reinigungsintervalle.')

num('qa_foerderhoehe', 'Förderhöhe [m]', ui='1.3', min=0.5, max=60)
num('qa_neigung', 'Neigung [Grad]', ui='1.4', min=0, max=35,
    visible_when=nin('qa_anlagenart', ['fahrsteig_horizontal']))
num('qa_bandbreite', 'Nutzbare Breite des Stufen-/Palettenbandes [m]', ui='1.5',
    min=0.4, max=2.0,
    help='Für die Instandhaltung maßgeblich: unter 0,80 m ist ein sicheres '
         'Arbeiten im Band regelmäßig nicht möglich (DGUV 209-085 Anhang 2).')

sel('qa_normstand', 'Regelwerk bei Inverkehrbringen / letzter wesentlicher Änderung',
    ui='1.6',
    options=[('vor_en115', 'Vor DIN EN 115 (Altanlage)'),
             ('en115_1995', 'DIN EN 115:1995'),
             ('en115_1_2008', 'DIN EN 115-1:2008'),
             ('en115_1_2017', 'DIN EN 115-1:2017 oder neuer'),
             ('unbekannt', 'Unbekannt / keine Unterlagen')],
    help='Nur Dokumentation und Einordnung des Sollzustands – keine automatische '
         'Stufenänderung. Für Bestandsanlagen ist DIN EN 115-2 die Maßstabsnorm.')

yn('qa_oeffentlich', 'Öffentlich zugängliche Anlage (Publikumsverkehr)?', ui='1.7')
yn('qa_arbeitsstaette', 'Wird die Anlage von Beschäftigten als Verkehrsweg genutzt '
   '(Arbeitsstätte)?', ui='1.8',
   help='Dann gelten ArbStättV und ASR A1.8 unmittelbar für den Betreiber.')
yn('qa_kinder', 'Nutzung durch unbeaufsichtigte Kinder zu erwarten?', ui='1.9')
yn('qa_pmem', 'Nutzung durch Personen mit eingeschränkter Mobilität '
   '(Rollator, Gehhilfe, Sehbehinderung) zu erwarten?', ui='1.10')

sel('qa_wagen', 'Beförderung von Wagen zugelassen', ui='1.11',
    options=[('keine', 'Nein, keine Wagen'),
             ('einkaufswagen', 'Einkaufswagen'),
             ('gepaeckwagen', 'Gepäck- oder Transportwagen')])

sel('qa_betriebsart', 'Betriebsart', ui='1.12',
    options=[('dauerlauf', 'Dauerlauf'),
             ('bedarf', 'Bedarfssteuerung (Sensor-/Impulsstart)'),
             ('handstart', 'Start von Hand durch Beschäftigte')])

yn('qa_mehrere', 'Mehrere Anlagen unmittelbar neben- oder hintereinander?', ui='1.13')
yn('qa_kreuzung', 'Kreuzt die Anlage eine Decke, ein Bauteil oder eine andere '
   'Anlage (Deckenabweiser erforderlich)?', ui='1.14')
yn('qa_besteigbar', 'Ist die Balustrade von einer angrenzenden Ebene, Galerie oder '
   'Treppe aus besteigbar?', ui='1.15')
yn('qa_glasbalustrade', 'Balustrade aus Glas?', ui='1.16')
yn('qa_station_begehbar', 'Begehbare Umkehr- und Antriebsstation vorhanden?', ui='1.17',
   help='Nein bedeutet: Zugang nur über das geöffnete Stufen-/Palettenband.')
yn('qa_vernetzt', 'Steuerung vernetzt oder fernüberwacht?', ui='1.18',
   help='Nur Dokumentation; die Cyber-Bewertung läuft über den eigenen Cyber-Typ.')

# ---- Filter für den Instandhaltungsteil -------------------------------------
yn('qa_teil_instandhaltung', 'Soll auch die Gefährdungsbeurteilung für '
   'Instandhaltung, Montage und Reinigung erstellt werden?', ui='1.19',
   help='Nein = reine Betreiber-GBU. Der Erhebungsbereich I wird dann nicht '
        'bewertet (nicht zutreffend statt unvollständig).')

sel('qa_ih_durchfuehrung', 'Wer führt Instandhaltung und Reinigung durch?', ui='1.20',
    visible_when=yes('qa_teil_instandhaltung'),
    options=[('fremdfirma', 'Ausschließlich Fremdfirma (Wartungsvertrag)'),
             ('eigen', 'Ausschließlich eigenes Personal'),
             ('beides', 'Eigenes Personal und Fremdfirma')])
