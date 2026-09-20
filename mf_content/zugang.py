# -*- coding: utf-8 -*-
"""Z – Zugang zum Triebwerks-/Steuerungsraum (Blaupause: Schindler M019, M019b,
M020a, M107, M117, M120; Inhalte aus App-Kategorien Z1–Z3, Z5–Z10)."""
from .common import *

GRP_Z = 'Zugang und Verkehrswege'
GRP_BEL = 'Beleuchtung'
GRP_NOT = 'Notruf und Personenbefreiung'

# ---- Fragen ----------------------------------------------------------------
yn('qz_bel_vorhanden', 'Beleuchtung an den Zuwegen zum Triebwerks-/Steuerungsraum vorhanden?',
   ui='5.1')
yn('qz_bel_ausreichend', 'Beleuchtung an den Zuwegen ausreichend (mind. 50 Lux, '
   'funktionsfähig, Leuchten an geeigneter Stelle)?', ui='5.2',
   visible_when=yes('qz_bel_vorhanden'))
yn('qz_bel_defekt', 'Defekte Leuchten oder Leuchtkörper an den Zuwegen?', ui='5.2a',
   visible_when=no('qz_bel_ausreichend'),
   help='Folgefrage zu 5.2: nennt den Grund der unzureichenden Beleuchtung und steuert die '
        'Maßnahme (Instandsetzung statt Umbau).')

yn('qz_weg_sicher', 'Sicherer, freier Verkehrsweg zum Triebwerks-/Steuerungsraum '
   '(trocken, sauber, ohne Stolperstellen)?', ui='5.3',
   help='Absturzkanten und Überstiege auf dem Zugangsweg unter 5.7/5.8 erfassen.')
yn('qz_weg_rutschig', 'Verkehrsweg rutschig, glatt oder verschmutzt?', ui='5.3a',
   visible_when=no('qz_weg_sicher'))
yn('qz_weg_stolper', 'Stolperstellen auf dem Verkehrsweg?', ui='5.3b',
   visible_when=no('qz_weg_sicher'))
yn('qz_weg_eng', 'Enge oder niedrige Durchgänge (Breite < 0,60 m oder Höhe < 2,00 m)?',
   ui='5.4')

sel('qz_aufstieg', 'Art des Aufstiegs zum Triebwerksraum', ui='5.5',
    visible_when=yes('qa_maschinenraum'),
    options=[('ebenerdig', 'Ebenerdig / kein Aufstieg nötig'),
             ('treppe_handlauf', 'Treppe mit Handlauf'),
             ('treppe_ohne_handlauf', 'Treppe ohne Handlauf'),
             ('zugtreppe_ok', 'Ordnungsgemäße Zug-/Klapptreppe'),
             ('zugtreppe_mangel', 'Zug-/Klapptreppe nicht sicherheitsgerecht'),
             ('leiter_fest', 'Fest angebrachte Steigleiter mit Rückenschutz/Haltegriff'),
             ('leiter_mobil', 'Nur mobile Leiter / Anlegeleiter'),
             ('kein_sicherer', 'Kein sicherer Aufstieg vorhanden')])
yn('qz_aufstieg_bruch', 'Bruch- oder Kippgefahr am Aufstieg (beschädigte Stufen, '
   'lose Leiter, fehlende Befestigung)?', ui='5.6',
   visible_when=neq('qz_aufstieg', 'ebenerdig'))

yn('qz_absturzkante', 'Führt der Zugang über eine Dachfläche, Dachkante, Empore '
   'oder eine andere Absturzkante?', ui='5.7')
yn('qz_absturz_gesichert', 'Absturzkante durch Geländer oder Umwehrung dauerhaft '
   'gesichert?', ui='5.7a', visible_when=yes('qz_absturzkante'))
yn('qz_absturz_gekennzeichnet', 'Verkehrsweg an der Absturzkante festgelegt, '
   'gekennzeichnet und mit ausreichendem Sicherheitsabstand zur Absturzkante geführt '
   '(auf Dachflächen mindestens 2,00 m nach ASR A2.1)?', ui='5.7b',
   visible_when=all_(yes('qz_absturzkante'), no('qz_absturz_gesichert')),
   help='Regelprüfung 20.09.2026: Der Abstand gehört in die Frage, nicht erst in die Maßnahme: Ein '
        'gekennzeichneter Weg dicht an der Kante ist keine wirksame Kompensation. Auf '
        'Dachflächen gilt das Maß von 2,00 m nach ASR A2.1; im Gebäudeinneren (Empore, '
        'Treppenauge) ist es regelmäßig unerfüllbar – dort ist ohnehin eine Umwehrung '
        'baurechtlich gefordert, zu bewerten über 5.7a. Wird der Abstand nicht '
        'eingehalten, ist hier „Nein" zu wählen; dann greift die Hoch-Regel.')
yn('qz_uebersteigen', 'Muss ein Treppenauge, eine Brüstung oder ein Fenster '
   'überstiegen werden?', ui='5.8')

sel('qz_von_innen', 'Lässt sich der Zugangsbereich / Triebwerksraum jederzeit von '
    'innen verlassen?', ui='5.9', visible_when=yes('qa_maschinenraum'),
    options=[('ja', 'Ja, ohne Schlüssel (Panikfunktion, Drücker innen)'),
             ('schluessel_hinterlegt', 'Nur mit Schlüssel, Schlüssel dauerhaft innen hinterlegt'),
             ('nein', 'Nein – Einschließen möglich')])

sel('qz_durch_fremde', 'Führt der Zugang durch fremde Räume?', ui='5.10',
    help='Regelprüfung 20.09.2026: Bewertet wird hier die Zugangsorganisation für Wartung und Prüfung '
         '(Zutrittsregelung, Schlüssel, Terminabstimmung). Ob der Befreiungsdienst die '
         'Anlage im Notfall rechtzeitig erreicht, ist getrennt unter 3.4 zu bewerten – '
         'führt der Zugang durch eine Wohnung, ist 3.4 besonders sorgfältig zu prüfen.',
    options=[('nein', 'Nein, direkter Zugang'),
             ('arbeits_lager', 'Durch Arbeits-, Lager- oder Technikräume Dritter'),
             ('wohnung', 'Durch eine Wohnung oder einen nur zeitweise zugänglichen Bereich')])
yn('qz_material_erschwert', 'Erschwert die Art des Zugangs den Transport von '
   'Material und Werkzeug (z. B. nur über Leiter, Dachluke, enge Wendeltreppe)?',
   ui='5.11')

yn('qz_tuer_vorhanden', 'Zugangstür zum Triebwerks-/Maschinenraum vorhanden?', ui='5.12',
   visible_when=yes('qa_maschinenraum'))
yn('qz_tuer_abschliessbar', 'Zugangstür abschließbar (Zutritt nur für befugte Personen)?',
   ui='5.12a', visible_when=yes('qz_tuer_vorhanden'))
yn('qz_tuer_zustand', 'Zugangstür unbeschädigt und leichtgängig?', ui='5.12b',
   visible_when=yes('qz_tuer_vorhanden'))
yn('qz_tuer_mass', 'Durchgangsmaß der Zugangstür ausreichend (mind. 1,80 m hoch, '
   '0,60 m breit)?', ui='5.12c', visible_when=yes('qz_tuer_vorhanden'),
   help='Regelprüfung 20.09.2026: Maß von 2,00 m auf 1,80 m berichtigt. DIN EN 81-20 5.2.3.3 fordert für die '
        'Zugangstür zum Triebwerksraum 0,60 m x 1,80 m; mit 2,00 m erzeugte die Frage bei '
        'normgerechten Türen einen Mangel. EN 81-1/-2 forderten dasselbe Maß, ein '
        'Vorbehalt zum Errichtungsregelwerk (1.28) ist deshalb entbehrlich – nur bei '
        'TRA-Anlagen vor 1999 kann das Maß abweichen; das ist im Bericht zu würdigen, '
        'nicht über eine Zusatzbedingung, die die Regel fail-open machen würde.')

yn('qz_schaltschrank_abschliessbar', 'Ohne Triebwerksraum: Steuerschrank (an der '
   'Haltestelle oder im Schacht) abschließbar, Zutritt nur für befugte Personen?',
   ui='5.14', visible_when=no('qa_maschinenraum'),
   help='Gegenstück zu 5.12a für maschinenraumlose Anlagen (Prüfbericht 20.09.2026): Der '
        'Steuerschrank ersetzt den Triebwerksraum und muss gegen unbefugten Zugriff '
        'verschlossen sein (DIN EN 81-20 5.2.6, Steuerschränke außerhalb von Triebwerksräumen).')

yn('qz_flucht_frei', 'Flucht- und Rettungsweg vom Triebwerks-/Steuerungsraum '
   'frei und benutzbar?', ui='5.13')
yn('qz_flucht_gekennz', 'Flucht- und Rettungsweg gekennzeichnet und beleuchtet?',
   ui='5.13a', visible_when=yes('qz_flucht_frei'))
yn('qz_flucht_eingeengt', 'Fluchtweg durch Lagerung eingeengt?', ui='5.13b',
   visible_when=yes('qz_flucht_frei'))

sel('qz_zugang_befreiung', 'Zugang zur Anlage für die Personenbefreiung jederzeit '
    'gewährleistet?', ui='3.4',
    options=[('jederzeit', 'Ja, jederzeit (Schlüsseltresor / ständig besetzte Stelle vor Ort)'),
             ('leitwarte', 'Nur über Schlüssel bei Leitwarte, Pforte oder Hausmeister'),
             ('nein', 'Nein, nicht jederzeit möglich')])

# ---- Klärungen -------------------------------------------------------------
k('K-Z01', 'Zugang', 'Schlüsseltresor',
  'Ist ein Zugang „jederzeit über Schlüsseltresor" wirklich „Kein Risiko" – oder '
  'ein niedriges Restrisiko (Tresor kann fehlen/defekt sein)?',
  'Kein Risiko (wie App-Katalog Z5)',
  'Niedrig (so bewertet es die Schindler-App bei „Ja, über Schlüsseltresor")',
  'App und Schindler weichen voneinander ab.')
k('K-Z02', 'Zugang', 'Fluchtweg Triebwerksraum',
  'Versperrter Flucht-/Rettungsweg im Triebwerksraum: Hoch oder Niedrig?',
  'Hoch (App-Katalog Z10)',
  'Niedrig (Schindler M120, da nur Instandhaltungspersonal betroffen; an den '
  'Fahrkorbausgängen dagegen Mittel)',
  'App und Schindler weichen deutlich voneinander ab.')
k('K-Z03', 'Zugang', 'Enge Durchgänge',
  'Enge/niedrige Durchgänge (< 0,60 m / < 2,00 m) als eigene Stufe Mittel – oder '
  'nur als Hinweis ohne Stufe?', 'Mittel', 'Nur Dokumentation',
  'Schindler zählt es zu M019 (Hoch im Worst Case), der App-Katalog kennt es nicht.')
k('K-Z04', 'Zugang', 'Mobile Leiter',
  'Zugang nur über mobile Anlegeleiter: Mittel oder Hoch?', 'Mittel',
  'Hoch (Absturz)', 'Im App-Katalog nicht als eigene Option enthalten.')

# ---- Gefährdungen ----------------------------------------------------------
hz('MF-Z01', 'Unzureichende Beleuchtung an den Zuwegen zum Triebwerks-/Steuerungsraum',
   GRP_BEL,
   [('qz_bel_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qz_bel_ausreichend', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_bel_vorhanden')}),
    ('qz_bel_defekt', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qz_bel_ausreichend')})],
   [r(no('qz_bel_vorhanden'), 'HIGH', mfrom=('N20-Z1', 'Keine Beleuchtung'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qz_bel_ausreichend'), 'MEDIUM', mfrom=('N20-Z1', 'Leuchten an ungeeigneter'),
      mittel='Beleuchtung der Zuwege so herstellen, dass dauerhaft mindestens 50 lx erreicht '
             'werden – Leuchten ergänzen, Leuchtmittel erneuern oder Leuchten versetzen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Mittelfristmaßnahme verallgemeinert. „Leuchten versetzen" traf nur einen der '
            'drei von 5.2 erfassten Mängel (zu wenig Lux, nicht funktionsfähig, ungeeignete '
            'Stelle) und beseitigte bei zu geringer Beleuchtungsstärke die Ursache nicht; '
            'zusammen mit R3 entstand unter MAXIMUM zudem der Widerspruch „versetzen" gegen '
            '„instand setzen". Stufe, Bedingung und Priorität bleiben.'),
    r(yes('qz_bel_defekt'), 'MEDIUM',
      sofort='Zuweg nur mit Handlampe begehen; Betreiber unverzüglich zur Instandsetzung '
             'auffordern',
      mittel='Defekte Leuchten und Leuchtmittel instand setzen und die Beleuchtung der Zuwege '
             'in die wiederkehrende Instandhaltung aufnehmen (Prüfintervall festlegen)',
      notes='Regelprüfung 20.09.2026: Sofort- und Mittelfristmaßnahme waren gegeneinander vertauscht: Die '
            'Instandsetzung [TECH] schützte den Prüfer, der den Zuweg jetzt begehen muss, '
            'gerade nicht und setzt je nach Defekt eine Elektrofachkraft voraus, während das '
            'Prüfintervall [ORGA] nur die Wiederholung verhindert. Damit war das TOP-Prinzip '
            'umgekehrt. Stufe Mittel und Bedingung bleiben.')],
   sources=[trbs3121('Anh. 1 Nr. 8'), src('OTHER', 'ASR A3.4')],
   factor=F_BELEUCHTUNG, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z02', 'Unsicherer Verkehrsweg zum Triebwerks-/Steuerungsraum (Rutschen, '
   'Stolpern, Enge)', GRP_Z,
   [('qz_weg_sicher', 'TRIGGER', 'ALWAYS'),
    ('qz_weg_rutschig', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qz_weg_sicher')}),
    ('qz_weg_stolper', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qz_weg_sicher')}),
    ('qz_weg_eng', 'DOCUMENTATION', 'NEVER',
     {'notes': 'Entscheidung 02.09.2026 (K-Z03): nur Dokumentation, keine Stufe.'})],
   [r(no('qz_weg_sicher'), 'MEDIUM', mfrom=('N20-Z3', 'Wege, Treppen rutschig'),
      sofort='Verkehrsweg vor dem Begehen prüfen, Stolper- und Rutschstellen kennzeichnen, '
             'abgestellte Gegenstände aus dem Verkehrsweg entfernen lassen; rutschhemmendes '
             'Schuhwerk tragen',
      mittel='Ursache beseitigen – Verkehrsweg dauerhaft freihalten, Bodenschäden instand '
             'setzen, rutschhemmenden Belag herstellen; Reinigungsintervall zusätzlich '
             'festlegen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Mittelfristmaßnahme war rein organisatorisch („Bodenbelag prüfen und häufig '
            'reinigen"), obwohl technische Abhilfe möglich und nach TOP vorrangig ist, und '
            'traf nicht alle von 5.3 erfassten Fälle: Ein Verkehrsweg kann auch zugestellt '
            'sein – dagegen hilft Reinigen nicht, und dieser Restfall wird weder von 5.3a noch '
            'von 5.3b erfasst. Die Bedingung bleibt bewusst weit: Die Aggregation ist MAXIMUM '
            'und alle drei Regeln liegen auf Mittel, ein Doppelbefund ändert also nichts, '
            'während eine Einschränkung den Befund bei 5.3=Nein mit 5.3a/5.3b=Nein verlieren '
            'würde (fail-open).'),
    r(yes('qz_weg_rutschig'), 'MEDIUM',
      sofort='Rutschstellen kennzeichnen und reinigen lassen; rutschhemmendes Schuhwerk tragen',
      mittel='Rutschhemmenden Bodenbelag herstellen bzw. Ursache der Verschmutzung/Nässe beseitigen',
      evidence='HIGH_CONFIDENCE',
      notes='Prüfbericht 20.09.2026: Folgefrage mit eigener Maßnahme statt optionaler Frage ohne Wirkung.'),
    r(yes('qz_weg_stolper'), 'MEDIUM',
      sofort='Stolperstellen kennzeichnen (Warnmarkierung) und Beschäftigte hinweisen',
      mittel='Stolperstellen beseitigen (Schwellen, Kabel, Bodenschäden) oder dauerhaft sichern',
      evidence='HIGH_CONFIDENCE',
      notes='Prüfbericht 20.09.2026: Folgefrage mit eigener Maßnahme statt optionaler Frage ohne Wirkung.')],
   sources=[trbs3121('Anh. 1 Nr. 5'), en8120('5.2.2.1')],
   factor=F_STURZ, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z03', 'Unsicherer Aufstieg (Treppe, Leiter) zum Triebwerksraum', GRP_Z,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qz_aufstieg', 'TRIGGER', 'ALWAYS'),
    ('qz_aufstieg_bruch', 'TRIGGER', 'CONDITIONAL',
     {'required_when': neq('qz_aufstieg', 'ebenerdig')})],
   [r(eq('qz_aufstieg', 'treppe_ohne_handlauf'), 'MEDIUM',
      mfrom=('N20-Z2', 'Treppe ohne Handlauf'), evidence='HIGH_CONFIDENCE'),
    r(eq('qz_aufstieg', 'zugtreppe_mangel'), 'MEDIUM',
      mfrom=('N20-Z2', 'Zugtreppe nicht'), evidence='HIGH_CONFIDENCE'),
    r(eq('qz_aufstieg', 'leiter_mobil'), 'HIGH',
      sofort='Leiter gegen Wegrutschen sichern, nur zu zweit benutzen',
      mittel='Fest angebrachte Steigleiter mit Haltegriffen oder Treppe herstellen',
      evidence='HYPOTHESIS', klaerung='K-Z04'),
    r(eq('qz_aufstieg', 'kein_sicherer'), 'HIGH',
      mfrom=('N20-Z2', 'Sicherer Aufstieg fehlt'),
      sofort='Aufstieg unterlassen, Zugang sperren und Betreiber unverzüglich unterrichten; '
             'Begehung erst nach Herstellung eines sicheren Aufstiegs',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Sofortmaßnahme ersetzt. „Geeignete Aufstiegshilfe verwenden" war in sich '
            'widersprüchlich: Ist festgestellt, dass kein sicherer Aufstieg vorhanden ist, '
            'kann nicht zugleich eine geeignete Aufstiegshilfe verwendet werden – eine '
            'Leerformel derselben Art wie das bereits beanstandete „Vorsicht walten lassen". '
            'Stufe Hoch und Mittelfristmaßnahme bleiben.'),
    r(yes('qz_aufstieg_bruch'), 'HIGH', mfrom=('N20-Z2', 'Bruchgefahr'),
      sofort='Aufstieg sofort sperren und nicht benutzen, Betreiber unverzüglich unterrichten; '
             'Zugang bis zur Instandsetzung nur über einen anderen sicheren Weg',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Sofortmaßnahme ersetzt. „Nur mit Absturzsicherung begehen" greift hier nicht: '
            'Gegen das Durchbrechen einer beschädigten Stufe oder das Kippen einer losen '
            'Leiter schützt PSA gegen Absturz nicht, und im Zugangsbereich zum Triebwerksraum '
            'ist in aller Regel kein geprüfter Anschlagpunkt vorhanden. Stufe Hoch und '
            'Mittelfristmaßnahme bleiben.')],
   sources=[trbs3121('Anh. 1 Nr. 5'), en8120('5.2.2.2'), src('OTHER', 'ASR A1.8')],
   factor=F_ABSTURZ, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z04', 'Absturzgefahr im Zugangsbereich (Dachfläche, Absturzkante, Übersteigen)',
   GRP_Z,
   [('qz_absturzkante', 'TRIGGER', 'ALWAYS'),
    ('qz_absturz_gesichert', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': yes('qz_absturzkante')}),
    ('qz_absturz_gekennzeichnet', 'COMPENSATION', 'CONDITIONAL',
     {'required_when': all_(yes('qz_absturzkante'), no('qz_absturz_gesichert'))}),
    ('qz_uebersteigen', 'TRIGGER', 'ALWAYS')],
   [r(all_(yes('qz_absturzkante'), no('qz_absturz_gesichert'),
           no('qz_absturz_gekennzeichnet')), 'HIGH',
      mfrom=('N20-Z6', 'Zugang über Dachfläche'), evidence='HIGH_CONFIDENCE'),
    r(all_(yes('qz_absturzkante'), no('qz_absturz_gesichert'),
           yes('qz_absturz_gekennzeichnet')), 'MEDIUM',
      mfrom=('N20-Z6', 'Absturzkante vorhanden'), evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Stufe und Maßnahmen bleiben – für den Fall mit eingehaltenem Abstand ist '
            'Mittel (wirksame, aber unvollständige Schutzmaßnahme) richtig. Die Regel setzte '
            'die Kompensation aber voraus, ohne sie abzuprüfen: 5.7b fragte nur nach '
            'Festlegung und Kennzeichnung, den Abstand nannte erst die Sofortmaßnahme. Ein '
            'gekennzeichneter Weg dicht an der Kante ist keine wirksame Kompensation und '
            'durfte den Fall nicht auf Mittel herabstufen. Der Abstand steht deshalb jetzt in '
            'der Frage 5.7b selbst; wird er nicht eingehalten, ergibt 5.7b „Nein" und R1 '
            '(Hoch) greift von selbst – eine zusätzliche Regel ist nicht nötig.'),
    r(yes('qz_uebersteigen'), 'HIGH', mfrom=('N20-Z6', 'Zugang erfordert'),
      evidence='HIGH_CONFIDENCE')],
   sources=[trbs3121('Anh. 1 Nr. 5'), src('OTHER', 'ASR A2.1')],
   factor=F_ABSTURZ, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z05', 'Einschließen im Zugangsbereich / Triebwerksraum (keine Panikfunktion)',
   GRP_Z,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qz_von_innen', 'TRIGGER', 'ALWAYS')],
   [r(eq('qz_von_innen', 'nein'), 'HIGH', mfrom=('N20-Z7', 'Zugangsbereich kann'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qz_von_innen', 'schluessel_hinterlegt'), 'MEDIUM',
      mfrom=('N20-Z7', 'Tür von innen'), evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.3.3'), trbs3121('Anh. 1 Nr. 5')],
   factor=F_EINSPERREN, persons=[BEAUFTRAGTE, WARTUNG], bereich='Z')

hz('MF-Z06', 'Zugang über fremde Räume, erschwerter Material- und Werkzeugtransport',
   GRP_Z,
   [('qz_durch_fremde', 'TRIGGER', 'ALWAYS'),
    ('qz_material_erschwert', 'TRIGGER', 'ALWAYS')],
   [r(eq('qz_durch_fremde', 'wohnung'), 'MEDIUM', mfrom=('N20-Z8', 'Zugang führt durch eine Wohnung'),
      sofort='Zutritt und Schlüsselregelung vorab schriftlich mit dem Betreiber vereinbaren; '
             'Erreichbarkeit des Wohnungsinhabers im Notfallplan hinterlegen',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Hoch auf Mittel. Die Stufe passte weder zum Gefährdungsfaktor dieser '
            'Gefährdung (physische Belastung, Zugangsorganisation) noch zum Stufenmaßstab: '
            'Ein Zugang durch eine Wohnung bedroht Leben und Gesundheit nicht unmittelbar. '
            'Das lebensbedrohliche Szenario – der Befreiungsdienst kommt nicht rechtzeitig an '
            'die Anlage – ist in MF-Z09 über 3.4 mit Hoch und dem richtigen Betroffenenkreis '
            'erfasst; eine Querbedingung auf 3.4 wurde bewusst NICHT eingebaut, sie erzeugte '
            'nur einen Doppelbefund. Stattdessen verweist die Hilfe zu 5.10 auf 3.4. Die '
            'unbestimmte Sofortmaßnahme („im Notfall Dritte hinzuziehen") ist konkretisiert.'),
    r(eq('qz_durch_fremde', 'arbeits_lager'), 'MEDIUM',
      mfrom=('N20-Z8', 'Zugang führt durch Arbeits'), evidence='HIGH_CONFIDENCE'),
    r(yes('qz_material_erschwert'), 'MEDIUM', mfrom=('N20-Z8', 'Art des Zugangs'),
      sofort='Material in tragbaren Teilmengen befördern, Lasten mit Seil oder Hebehilfe '
             'getrennt hochgeben; Leiter oder Treppe nur mit freien Händen begehen '
             '(Dreipunktkontakt)',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Sofortmaßnahme ersetzt. „Geeignete Transporthilfen verwenden" ist eine '
            'Leerformel derselben Art, die der Katalog an anderen Stellen bereits ersetzt hat: '
            'Sie benennt nicht, was zu tun ist, und ist im Prüfmoment ohne vorhandene '
            'Hilfsmittel unwirksam. Der entscheidende Grundsatz – beim Auf- und Abstieg keine '
            'Last in der Hand – fehlte. Bedingung, Stufe und Mittelfristmaßnahme bleiben.')],
   sources=[trbs3121('Anh. 1 Nr. 5'), en8120('5.2.2.1')],
   factor=F_ERGONOMIE, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z07', 'Fehlende oder unzureichende Zugangstür zum Triebwerks-/Maschinenraum bzw. '
   'nicht abschließbarer Steuerschrank',
   GRP_Z,
   [('qa_maschinenraum', 'MODIFIER', 'ALWAYS',
     {'notes': 'Schaltet zwischen Zugangstür (mit Triebwerksraum) und Steuerschrank (ohne) um '
               'und ist deshalb Pflicht – ohne die Antwort ließe sich weder der eine noch der '
               'andere Zweig bewerten (fail-closed statt Regellücke).'}),
    ('qz_tuer_vorhanden', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qa_maschinenraum')}),
    ('qz_schaltschrank_abschliessbar', 'TRIGGER', 'CONDITIONAL', {'required_when': no('qa_maschinenraum')}),
    ('qz_tuer_abschliessbar', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_tuer_vorhanden')}),
    ('qz_tuer_zustand', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_tuer_vorhanden')}),
    ('qz_tuer_mass', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_tuer_vorhanden')})],
   [r(no('qz_tuer_vorhanden'), 'HIGH', mfrom=('N20-Z9', 'Zugangstür fehlt'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qz_tuer_abschliessbar'), 'HIGH', mfrom=('N20-Z9', 'Zugangstür fehlt'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qz_tuer_zustand'), 'MEDIUM', mfrom=('N20-Z9', 'Zugangstür vorhanden, aber'),
      sofort='Tür beim Betreten gegen Zufallen sichern (feststellen oder aufkeilen), Raum '
             'nicht allein betreten, beim Betreiber an- und abmelden; Betreiber unverzüglich '
             'unterrichten',
      evidence='HIGH_CONFIDENCE',
      notes='Regelprüfung 20.09.2026: Sofortmaßnahme ersetzt. „Tür gangbar machen" war inhaltsgleich mit der '
            'Mittelfristmaßnahme („Tür instand setzen oder ersetzen") und damit keine '
            'eigenständige Sofortmaßnahme; je nach Schadensbild (verzogenes Türblatt, '
            'defektes Schloss) ist sie im Prüfmoment gar nicht ausführbar. Vor allem schützte '
            'sie nicht vor der eigentlichen Gefahr, dem Einschließen im Triebwerksraum. Stufe '
            'Mittel und Bedingung bleiben.'),
    r(no('qz_tuer_mass'), 'MEDIUM', mfrom=('N20-Z9', 'Durchgangshöhe'),
      mittel='Anstoßschutz (Polsterung) und dauerhafte Kennzeichnung anbringen; Türöffnung '
             'nach DIN EN 81-20 5.2.3.3 anpassen, soweit verhältnismäßig',
      evidence='HIGH_CONFIDENCE', sources=[en8120('5.2.3.3')],
      notes='Regelprüfung 20.09.2026: Das Höhenmaß in 5.12c ist von 2,00 m auf 1,80 m berichtigt – die Regel '
            'erzeugte sonst bei normgerechten Türen (1,80 m bis unter 2,00 m) einen Mangel. '
            'Die Mittelfristmaßnahme ist um den Anstoßschutz erweitert: „Türöffnung anpassen" '
            'als einzige Maßnahme ist für eine geringfügige Maßunterschreitung '
            'unverhältnismäßig, obwohl eine mildere technische Lösung zur Verfügung steht. '
            'Sofortmaßnahme und Stufe bleiben.'),
    r(no('qz_schaltschrank_abschliessbar'), 'HIGH',
      sofort='Steuerschrank gegen unbefugten Zugriff sichern (Schloss, Zutritt beschränken); '
             'Betreiber informieren',
      mittel='Abschließbaren Steuerschrank herstellen, Zutritt nur für befugte Personen '
             '(DIN EN 81-20 5.2.6, Steuerschränke außerhalb von Triebwerksräumen)',
      evidence='INFERRED',
      notes='Prüfbericht 20.09.2026: Gegenstück zu 5.12a für maschinenraumlose Anlagen – bisher '
            'entfiel die Gefährdung dort vollständig (nur im Cyber-Teil 2.1 erfasst).')],
   sources=[en8120('5.2.3.3'), en8120('5.2.6'), trbs3121('Anh. 1 Nr. 5')],
   factor=F_EINSPERREN, persons=[BEAUFTRAGTE, WARTUNG, NUTZER], agg='MAXIMUM', bereich='Z')

hz('MF-Z08', 'Fehlende oder versperrte Flucht- und Rettungswege im Bereich des '
   'Triebwerks-/Steuerungsraums', GRP_Z,
   [('qz_flucht_frei', 'TRIGGER', 'ALWAYS'),
    ('qz_flucht_gekennz', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_flucht_frei')}),
    ('qz_flucht_eingeengt', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_flucht_frei')})],
   [r(no('qz_flucht_frei'), 'LOW', mfrom=('N20-Z10', 'Flucht- und Rettungsweg versperrt'),
      evidence='HIGH_CONFIDENCE', klaerung='K-Z02',
      notes='Entscheidung 02.09.2026: Niedrig (nur Instandhaltungspersonal betroffen, wie Schindler M120).'),
    r(no('qz_flucht_gekennz'), 'LOW', mfrom=('N20-Z10', 'Kennzeichnung'),
      evidence='HIGH_CONFIDENCE', klaerung='K-Z02'),
    r(yes('qz_flucht_eingeengt'), 'LOW', mfrom=('N20-Z10', 'Fluchtweg durch Lagerung'),
      evidence='HIGH_CONFIDENCE', klaerung='K-Z02')],
   sources=[src('OTHER', 'ASR A2.3'), law('ArbStättV', '§ 4')],
   factor=F_FLUCHT, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z09', 'Zugang zur Anlage für die Personenbefreiung nicht jederzeit gewährleistet',
   GRP_NOT,
   [('qz_zugang_befreiung', 'TRIGGER', 'ALWAYS')],
   [r(eq('qz_zugang_befreiung', 'nein'), 'HIGH', mfrom=('N20-Z5', 'Zugang nicht jederzeit'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qz_zugang_befreiung', 'leitwarte'), 'MEDIUM', mfrom=('N20-Z5', 'Zugang nur möglich'),
      sofort='Erreichbarkeit der Leitwarte und Schlüsselübergabe mit dem Notdienst abstimmen und im '
             'Notfallplan festhalten',
      mittel='Schlüsseldepot bzw. Schlüsseltresor mit Zugriff für den Befreiungsdienst '
             'einrichten; ersatzweise, wo technisch nicht möglich, ständige Besetzung von '
             'Leitwarte oder Pforte vertraglich sicherstellen',
      evidence='HIGH_CONFIDENCE', pb='H11 – Sofortmaßnahme ergänzt',
      notes='Regelprüfung 20.09.2026: Mittelfristmaßnahme war rein organisatorisch („ständige Besetzung der '
            'Leitwarte/Pforte gewährleisten"), obwohl mit dem Schlüsseldepot eine technische '
            'Lösung zur Verfügung steht, die dieselbe Ursache dauerhaft und personenunabhängig '
            'beseitigt – genau diese Lösung nennt die Parallelregel R1 bereits. TOP-Verstoß '
            'behoben. Stufe, Bedingung und Sofortmaßnahme bleiben.'),
    r(eq('qz_zugang_befreiung', 'jederzeit'), 'NO_RISK', evidence='HIGH_CONFIDENCE',
      klaerung='K-Z01')],
   sources=[law('BetrSichV', 'Anh. 1 Nr. 4.1'), trbs3121('3.1.3'), trbs3121('3.7.3')],
   factor=F_NOTFALL, persons=[NUTZER, BEAUFTRAGTE], bereich='Z')
