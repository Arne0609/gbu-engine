# -*- coding: utf-8 -*-
"""Prüfhinweise für sicherheitskritische Fragen (Prüfbericht 15.09.2026, M01;
zweite Prüfung 16.09.2026: „sicherheitskritische Fragen zuerst“).

Aufbau je Text: Wie prüfen – woran erkennt man Ja/Nein – Nachweis.
Ein vorhandener help-Text aus der Frage-Definition hat Vorrang. Die Texte sind
fachlich gegenzulesen (Blatt „Fragen“ der Regelprüfung)."""

HILFE = {
    'qa_ucm_a3':
        'Prüfen: Typenschild/Baumusterbescheinigung der UCM-Komponenten (z. B. Bremse als '
        'Bremselement mit Baumusterprüfung, Überwachung der Türzonen). Ja nur mit Nachweis in '
        'den Anlagenunterlagen; das Baujahr allein ist kein Nachweis.',
    'qa_fahrkorbtuer':
        'Ja, wenn jeder Fahrkorbzugang eine Tür oder ein Gitter mit Schließstellungsüberwachung '
        'hat. Lichtgitter oder Scherengitter ohne Tür unter 8.9/8.9a erfassen.',
    'qt_verriegelung_elektrisch':
        'Prüfen: Tür bei Fahrkorb außerhalb der Zone öffnen lassen bzw. Kontakt am Verriegelungsbolzen '
        'kontrollieren – die Fahrt darf erst bei eingegriffenem Riegel möglich sein (Riegelkontakt im '
        'Sicherheitskreis). Nein bei reinen Türkontakten ohne Riegelüberwachung.',
    'qt_fehlschliess':
        'Prüfen: Tür mit Hindernis nicht vollständig schließen lassen – die Anlage darf nicht anfahren; '
        'die Tür muss selbsttätig nachschließen.',
    'qt_selbstschliessend':
        'Prüfen: Schachttür bei Fahrkorb außerhalb der Zone mit Notentriegelung öffnen und loslassen – '
        'sie muss durch Feder oder Gewicht selbsttätig schließen.',
    'qt_schliesst_nach_notentriegelung':
        'Wie 7.3, aber vollständig bis zur Verriegelung: Nach dem Loslassen muss der Riegel wieder '
        'eingreifen. Bei jeder Haltestelle prüfen; eine einzige Abweichung = Nein.',
    'qt_notentriegelung_alle':
        'An jeder Schachttür prüfen, ob die Notentriegelung vorhanden und mit dem hinterlegten '
        'Schlüssel bedienbar ist.',
    'qt_schliesskante':
        'Lichtgitter = mehrstrahlige Erkennung über die Türhöhe. Einzel-Lichtschranke nur bei '
        'nachgewiesener Kraftbegrenzung (150 N) und kinetischer Energie ≤ 10 J wählen, sonst '
        '„Keine Schließkantensicherung“.',
    'qk_notruf_vorhanden':
        'Prüfen: Notruf aus dem Fahrkorb auslösen und Verbindung bis zur Notrufstelle nachverfolgen.',
    'qk_notruf_art':
        'Nach dem tatsächlichen Empfänger einstufen, nicht nach der Beschriftung des Tasters. '
        'Klingel im Gebäude ohne ständig besetzte Stelle = „nicht ständig besetzt“.',
    'qk_notruf_24h':
        'Nachweis: Vertrag oder Aufschaltbestätigung des Notrufdienstes; bei der Prüfung einen '
        'Testnotruf absetzen.',
    'qk_notbeleuchtung':
        'Prüfen: Netz abschalten (Hauptschalter der Fahrkorbbeleuchtung) – die Notbeleuchtung muss '
        'selbsttätig einschalten. Ein nur beleuchteter Notruftaster ist keine Notbeleuchtung.',
    'qk_stufe_mm':
        'An jeder Haltestelle in beiden Fahrtrichtungen messen, beladen und leer, falls möglich; '
        'den größten Wert eintragen.',
    'qk_abstand_schwelle_mm':
        'Horizontaler Abstand zwischen Fahrkorbschwelle und Schachtwand bzw. Schachttürschwelle, an '
        'der ungünstigsten Stelle über die Fahrbahn gemessen (Inspektionsfahrt).',
    'qk_fk_tuer_verriegelt':
        'Prüfen: Fahrkorb außerhalb der Entriegelungszone anhalten und versuchen, die Fahrkorbtür von '
        'innen aufzuschieben – sie darf sich nicht öffnen lassen.',
    'qf_schutzraum':
        'Mit dem Fahrkorb auf dem voll zusammengedrückten Puffer (bzw. Berechnung aus den Unterlagen) '
        'den freien Raum über dem Fahrkorbdach bestimmen. Nachträgliche Einbauten im Schachtkopf '
        'mitprüfen.',
    'qf_gelaender':
        'Erforderlich, wenn der freie Abstand zwischen Außenkante Fahrkorbdach und Schachtwand mehr '
        'als 0,30 m beträgt (TRBS 3121 Anh. 1 Nr. 15).',
    'qf_inspektion':
        'Prüfen: Inspektionsschalter umschalten – Normalbetrieb muss gesperrt sein, Fahrt nur mit '
        'Richtungstaste und Freigabe.',
    'qf_nothalt':
        'Prüfen: Not-Halt vom Zugang aus erreichbar betätigen – Fahrt darf nicht möglich sein.',
    'qf_dach_tragfaehig':
        'Nachweis aus den Herstellerunterlagen; bei Zweifeln (dünne Bleche, sichtbare Verformung) '
        'Nein wählen, bis der Nachweis vorliegt.',
    'qg_nothalt':
        'Prüfen: Not-Halt in der Grube betätigen – Fahrt darf nicht möglich sein. Erreichbarkeit '
        'von der Schachttür aus unter 11.4a erfassen.',
    'qg_schutzraum':
        'Mit dem Fahrkorb auf dem voll zusammengedrückten Puffer den freien Raum in der Grube '
        'bestimmen (bzw. aus den Unterlagen).',
    'qg_puffer':
        'Sichtprüfung: Puffer unter Fahrkorb und Gegengewicht vorhanden und fest verankert.',
    'qg_gg_abtrennung':
        'Messen: Abtrennung von höchstens 0,30 m bis mindestens 2,0 m über der Schachtgrubensohle, '
        'in der Breite des Gegengewichts (TRBS 3121 Anh. 1 Nr. 2).',
    'qs_fang':
        'Nachweis über Typenschild und Prüfbuch; Sichtprüfung der Fangvorrichtung bei Inspektionsfahrt.',
    'qs_begrenzer':
        'Sichtprüfung im Triebwerksraum bzw. Schachtkopf; Typenschild und Auslösegeschwindigkeit '
        'mit dem Prüfbuch abgleichen.',
    'qm_hauptschalter':
        'Prüfen: Hauptschalter ausschalten – Antrieb und Steuerung müssen spannungsfrei sein '
        '(Beleuchtung und Notruf bleiben versorgt). Abschließbarkeit unter 5.51a erfassen.',
    'qm_zweikreisbremse':
        'Nachweis aus den Herstellerunterlagen bzw. Baumuster der Bremse: zwei mechanisch unabhängig '
        'wirkende Bremskreise.',
    'qm_bremse_ueberwacht':
        'Prüfen: Bremskontrollschalter vorhanden und im Steuerungsplan eingebunden; bei Fehlfunktion '
        'darf die Anlage nicht erneut anfahren.',
    'qm_schuetze_unabhaengig':
        'Stromlaufplan prüfen: zwei voneinander unabhängige Schütze oder gleichwertige Abschaltung '
        'des Antriebs (TRBS 3121 Anh. 1 Nr. 20).',
    'qm_steuerung_selbstueberw':
        'Nur Ja, wenn die Baumusterbescheinigung der Steuerung die Überwachung des Einzelschützes '
        'ausdrücklich nennt.',
    'qm_rohrbruch':
        'Nachweis aus den Herstellerunterlagen; Rohrbruchventil am Zylinder bzw. in der Leitung '
        'unmittelbar am Zylinder.',
    'qm_absperrventil':
        'Sichtprüfung am Aggregat: Absperrventil in der Leitung zum Zylinder vorhanden und bedienbar.',
    'qm_notbetrieb':
        'Prüfen: Einrichtung vorhanden, vollständig und für die beauftragte Person bedienbar; '
        'Notbefreiungsanleitung an der Einrichtung.',
    'qd_notfallplan':
        'Nachweis: Aushang bzw. Dokument mit Ansprechpartnern, Notrufdienst, Befreiungsdienst und '
        'Zugangsregelung (BetrSichV Anh. 1 Nr. 4.1, TRBS 3121 Abschnitt 3.6).',
    'qu_asbest_unbekannt':
        'Ja, wenn keine Schadstofferkundung vorliegt und asbesthaltige Bauteile nach Baujahr oder '
        'Bauart nicht auszuschließen sind. Das ist kein Befund, sondern ein Erkundungsbedarf.',
    'qz_zugang_befreiung':
        'Prüfen, ob der Befreiungsdienst rund um die Uhr ins Gebäude und zur Anlage kommt '
        '(Schlüsseltresor, Pförtner, Schließanlage).',
}
