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
   visible_when=yes('qz_bel_vorhanden'))

yn('qz_weg_sicher', 'Sicherer, freier Verkehrsweg zum Triebwerks-/Steuerungsraum '
   '(trocken, sauber, ohne Stolperstellen, ohne Absturzkante)?', ui='5.3')
yn('qz_weg_rutschig', 'Verkehrsweg rutschig, glatt oder verschmutzt?', ui='5.3a',
   visible_when=no('qz_weg_sicher'))
yn('qz_weg_stolper', 'Stolperstellen auf dem Verkehrsweg?', ui='5.3b',
   visible_when=no('qz_weg_sicher'))
yn('qz_weg_eng', 'Enge oder niedrige Durchgänge (Breite < 0,60 m oder Höhe < 2,00 m)?',
   ui='5.4')

sel('qz_aufstieg', 'Art des Aufstiegs zum Triebwerksraum', ui='5.5',
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
yn('qz_absturz_gekennzeichnet', 'Verkehrsweg an der Absturzkante festgelegt und '
   'gekennzeichnet?', ui='5.7b',
   visible_when=all_(yes('qz_absturzkante'), no('qz_absturz_gesichert')))
yn('qz_uebersteigen', 'Muss ein Treppenauge, eine Brüstung oder ein Fenster '
   'überstiegen werden?', ui='5.8')

sel('qz_von_innen', 'Lässt sich der Zugangsbereich / Triebwerksraum jederzeit von '
    'innen verlassen?', ui='5.9',
    options=[('ja', 'Ja, ohne Schlüssel (Panikfunktion, Drücker innen)'),
             ('schluessel_hinterlegt', 'Nur mit Schlüssel, Schlüssel dauerhaft innen hinterlegt'),
             ('nein', 'Nein – Einschließen möglich')])

sel('qz_durch_fremde', 'Führt der Zugang durch fremde Räume?', ui='5.10',
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
yn('qz_tuer_mass', 'Durchgangsmaß der Zugangstür ausreichend (mind. 2,00 m hoch, '
   '0,60 m breit)?', ui='5.12c', visible_when=yes('qz_tuer_vorhanden'))

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
    ('qz_bel_defekt', 'OPTIONAL', 'NEVER')],
   [r(no('qz_bel_vorhanden'), 'HIGH', mfrom=('N20-Z1', 'Keine Beleuchtung'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qz_bel_ausreichend'), 'MEDIUM', mfrom=('N20-Z1', 'Leuchten an ungeeigneter'),
      evidence='HIGH_CONFIDENCE'),
    r(yes('qz_bel_defekt'), 'MEDIUM', sofort='Defekte Leuchten umgehend instand setzen',
      mittel='Beleuchtung der Zuwege dauerhaft instand halten (Prüfintervall festlegen)')],
   sources=[trbs3121('Anh. 1 Nr. 8'), src('OTHER', 'ASR A3.4')],
   factor=F_BELEUCHTUNG, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z02', 'Unsicherer Verkehrsweg zum Triebwerks-/Steuerungsraum (Rutschen, '
   'Stolpern, Enge)', GRP_Z,
   [('qz_weg_sicher', 'TRIGGER', 'ALWAYS'),
    ('qz_weg_rutschig', 'OPTIONAL', 'NEVER'),
    ('qz_weg_stolper', 'OPTIONAL', 'NEVER'),
    ('qz_weg_eng', 'DOCUMENTATION', 'NEVER',
     {'notes': 'Entscheidung 02.09.2026 (K-Z03): nur Dokumentation, keine Stufe.'})],
   [r(no('qz_weg_sicher'), 'MEDIUM', mfrom=('N20-Z3', 'Wege, Treppen rutschig'),
      evidence='HIGH_CONFIDENCE')],
   sources=[trbs3121('Anh. 1 Nr. 5'), en8120('5.2.2.1')],
   factor=F_STURZ, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z03', 'Unsicherer Aufstieg (Treppe, Leiter) zum Triebwerksraum', GRP_Z,
   [('qz_aufstieg', 'TRIGGER', 'ALWAYS'),
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
      mfrom=('N20-Z2', 'Sicherer Aufstieg fehlt'), evidence='HIGH_CONFIDENCE'),
    r(yes('qz_aufstieg_bruch'), 'HIGH', mfrom=('N20-Z2', 'Bruchgefahr'),
      evidence='HIGH_CONFIDENCE')],
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
      mfrom=('N20-Z6', 'Absturzkante vorhanden'), evidence='HIGH_CONFIDENCE'),
    r(yes('qz_uebersteigen'), 'HIGH', mfrom=('N20-Z6', 'Zugang erfordert'),
      evidence='HIGH_CONFIDENCE')],
   sources=[trbs3121('Anh. 1 Nr. 5'), src('OTHER', 'ASR A2.1')],
   factor=F_ABSTURZ, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z05', 'Einschließen im Zugangsbereich / Triebwerksraum (keine Panikfunktion)',
   GRP_Z,
   [('qz_von_innen', 'TRIGGER', 'ALWAYS')],
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
   [r(eq('qz_durch_fremde', 'wohnung'), 'HIGH', mfrom=('N20-Z8', 'Zugang führt durch eine Wohnung'),
      evidence='HIGH_CONFIDENCE'),
    r(eq('qz_durch_fremde', 'arbeits_lager'), 'MEDIUM',
      mfrom=('N20-Z8', 'Zugang führt durch Arbeits'), evidence='HIGH_CONFIDENCE'),
    r(yes('qz_material_erschwert'), 'MEDIUM', mfrom=('N20-Z8', 'Art des Zugangs'),
      evidence='HIGH_CONFIDENCE')],
   sources=[trbs3121('Anh. 1 Nr. 5'), en8120('5.2.2.1')],
   factor=F_ERGONOMIE, persons=[BEAUFTRAGTE, WARTUNG], agg='MAXIMUM', bereich='Z')

hz('MF-Z07', 'Fehlende oder unzureichende Zugangstür zum Triebwerks-/Maschinenraum',
   GRP_Z,
   [('qa_maschinenraum', 'APPLICABILITY', 'NEVER'),
    ('qz_tuer_vorhanden', 'TRIGGER', 'ALWAYS'),
    ('qz_tuer_abschliessbar', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_tuer_vorhanden')}),
    ('qz_tuer_zustand', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_tuer_vorhanden')}),
    ('qz_tuer_mass', 'TRIGGER', 'CONDITIONAL', {'required_when': yes('qz_tuer_vorhanden')})],
   [r(no('qz_tuer_vorhanden'), 'HIGH', mfrom=('N20-Z9', 'Zugangstür fehlt'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qz_tuer_abschliessbar'), 'HIGH', mfrom=('N20-Z9', 'Zugangstür fehlt'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qz_tuer_zustand'), 'MEDIUM', mfrom=('N20-Z9', 'Zugangstür vorhanden, aber'),
      evidence='HIGH_CONFIDENCE'),
    r(no('qz_tuer_mass'), 'MEDIUM', mfrom=('N20-Z9', 'Durchgangshöhe'),
      evidence='HIGH_CONFIDENCE')],
   sources=[en8120('5.2.3.3'), trbs3121('Anh. 1 Nr. 5')],
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
      evidence='HIGH_CONFIDENCE'),
    r(eq('qz_zugang_befreiung', 'jederzeit'), 'NO_RISK', evidence='HIGH_CONFIDENCE',
      klaerung='K-Z01')],
   sources=[law('BetrSichV', 'Anh. 1 Nr. 4.1'), trbs3121('4.4')],
   factor=F_NOTFALL, persons=[NUTZER, BEAUFTRAGTE], bereich='Z')
