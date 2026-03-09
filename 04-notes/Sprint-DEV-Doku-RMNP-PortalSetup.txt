================================================================================
SPRINT DEV-DOKUMENTATION
================================================================================
Projekt            : R+MUNI Blueprint
Sprint-Bezeichnung : SPRINT-RMNP01-PortalSetup
Datum              : 2026-03-09
Stage              : 5 (aktiv)
Status             : Dev-Dokumentation (nicht auditpflichtig per GOV 10.8)
Erstellt durch     : Entwickler + Claude (Pair-Session)
Vorgänger-Sprint   : Stage 4 Freeze (2026-03-09)
================================================================================


--------------------------------------------------------------------------------
1. STAGE-KONTEXT UND SPRINT-BEGRÜNDUNG
--------------------------------------------------------------------------------

1.1 Stage-Modell (Ist-Zustand)
-------------------------------
Stage 3  FREEZE
         Stage 3 ist eingefroren. Änderungen ausschließlich für Bugfixing
         zulässig. Neue Features sind in Stage 3 nicht erlaubt.

Stage 4  FREEZE
         Stage 4 ist eingefroren. Alle Scripts und Logik read-only.
         Kein Eingriff zulässig außer explizit freigegebene Bugfixes.

Stage 5  AKTIV
         Erste Außenwirkungsphase. Realer Betrieb, Kundenkontakt,
         Ökosystem-Aufbau. Erweiterungen additiv, kein Eingriff in S3/S4.

1.2 Auslöser (gemäß GOV 10.3 / 10.5)
---------------------------------------
Auslöser-Typ : Feature-Zuwachs (Stage-5-Ziel 4.1)

Vorgeschichte:  Stage 5 definiert als Ziel 4.1 den Aufbau eines
                standardisierten Atlassian-Setups als Kundeninterface.
                Bisher existierte kein dediziertes Endkunden-Portal.
                Das alte RMUNI Service-Desk-Projekt war ein Testaufbau
                ohne produktive Konfiguration.

Entscheidung:   Aufbau eines sauberen Customer Service Management (CSM)
                Projekts als Endkunden-Portal für R+MUNI.
                Altes Testprojekt RMUNI in Papierkorb verschoben.
                Neues Projekt RMNP sauber und ohne Altlasten aufgebaut.


--------------------------------------------------------------------------------
2. ZIEL DES SPRINTS
--------------------------------------------------------------------------------

Primärziel:
  Funktionsfähiges Endkunden-Portal auf Basis Atlassian CSM (Free Plan)
  mit 3 definierten Request-Typen für Beta-Kunden und spätere Kunden.

Nebenziel:
  Konzeptklärung: Wozu dient ein Endkunden-Portal im R+MUNI Kontext?
  Entscheidungsgrundlage für künftige Portal-Erweiterungen schaffen.

Abgrenzung:
  - Kein Eingriff in Confluence (produktiv, unangetastet)
  - Kein Eingriff in MUNIEA Projekt (ATL-Flow Stage 4)
  - Kein Branding-Vollausbau (iterativ in Stage 5)
  - Kein E-Mail-Kanal (bewusst nicht aktiviert, Free Plan reicht)


--------------------------------------------------------------------------------
3. KONZEPTENTSCHEIDUNGEN (Pair-Session)
--------------------------------------------------------------------------------

3.1 Portal-Scope
-----------------
Entschieden: A + B Modell

  A) Feedback & Support-Kanal
     Kunde meldet Probleme, stellt Fragen, verfolgt Status.
     Kanal: JSM/CSM Portal (Portal-only Customer, unbegrenzt, kostenlos)

  B) Onboarding & Wissens-Selbstbedienung
     Kunde findet Dokumentation, Anleitungen, How2s.
     Kanal: Confluence öffentliche Seiten (Share-Link, kein Login nötig)
     → Confluence-Anbindung an Portal: bewusst zurückgestellt, eigener Schritt

  Nicht im Scope:
     Vertriebsanfragen → bewusst ausgeschlossen
     Direkter Kundenaccount-Aufbau → optional, kein Zwang

3.2 Request-Typen
------------------
Entschieden: 3 Formulare, keine Vertriebsanfragen

  Bug          → Vorgangstyp: Problem
                 Felder: Zusammenfassung (P), Beschreibung (P),
                         Affected services (O), Attachment (O)

  Feature Request → Vorgangstyp: Suggestion
                 Felder: Zusammenfassung (P), Beschreibung (P),
                         Impact (O), Attachment (O)

  DEV Anfrage  → Vorgangstyp: Question (neuer dedizierter Typ)
                 Felder: Zusammenfassung (P), Beschreibung (P)
                 Hinweis: DEV Anfrage = Hilfe bei R+MUNI,
                          ob daraus eine Leistung wird: situativ,
                          workloadabhängig, bewusst offen gehalten

  Legende: P = Pflichtfeld, O = Optionales Feld

3.3 Technische Erkenntnis — Contact/Standard Formular
-------------------------------------------------------
Das CSM-Standard-Formular "Contact" ist ein System-Formular
für E-Mail-Kanal und KI-Agent. Es lässt sich NICHT als
eigenständige Option auf der Support-Website platzieren.
Lösung: Neuer dedizierter Issue-Typ für DEV Anfrage angelegt.
Contact-Formular zurückbenannt auf Standard — bleibt als
System-Hintergrundformular erhalten, stört nicht.

3.4 Kundenzugriff
------------------
Einstellung: JEDER (offen)
Begründung:  R+MUNI-Philosophie — Offenheit und Ehrlichkeit.
             Kein Zwang zur Registrierung, kein Kontrollaufwand.
             Jeder mit der Portal-URL kann eine Anfrage stellen.

3.5 Free Plan Bewertung
------------------------
Ergebnis: Free Plan trägt den vollständigen Use Case

  JSM Free:   Portal funktioniert, keine SLA nötig, kein E-Mail-Kanal nötig
  Conf Free:  Öffentliche Seiten als Wissensbasis, ein Space für alle Kunden
  Jira Free:  Public, keine Kundentrennung nötig (bewusst gewollt)

  Grenze erreicht: NEIN — Free Plan reicht für aktuelle Beta-Phase


--------------------------------------------------------------------------------
4. UMSETZUNG
--------------------------------------------------------------------------------

4.1 Atlassian-Aktionen (manuell durch Entwickler, GUI-geführt durch Claude)
-----------------------------------------------------------------------------
  ✅ Altes RMUNI Service-Desk-Projekt in Papierkorb verschoben
  ✅ Neues CSM-Projekt angelegt
     Name: R+MUNI Portal | Key: RMNP | Typ: Customer Service Management
  ✅ Kundenerfahrung "R MUNI" konfiguriert
  ✅ Formular "Bug" erstellt (Vorgangstyp: Problem)
  ✅ Formular "Feature Request" erstellt (Vorgangstyp: Suggestion)
  ✅ Formular "DEV Anfrage" erstellt (neuer Vorgangstyp: Question)
  ✅ Kundenzugriff auf "Jeder" gesetzt
  ✅ Branding: Logo hinterlegt (Iteration folgt)
  ✅ Portal-URL verifiziert

4.2 Portal-URL (Endkunden-Einstieg)
-------------------------------------
  https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP/

4.3 Nicht angetastet
---------------------
  ✅ Confluence — produktiv, kein Eingriff
  ✅ MUNIEA Projekt — ATL-Flow Stage 4, kein Eingriff
  ✅ Stage-3/4-Scripts — read-only, kein Eingriff


--------------------------------------------------------------------------------
5. OFFENE PUNKTE / NÄCHSTE SCHRITTE
--------------------------------------------------------------------------------

  [ ] Portal selbst testen (Inkognito-Fenster, alle 3 Formulare durchspielen)
  [ ] Branding vervollständigen (Hauptfarbe, Symbol)
  [ ] Confluence FAQ-Seite erstellen und an Portal verlinken (eigener Sprint)
  [ ] Portal-URL in Confluence R+MUNI Hauptseite publizieren
  [ ] Erste Kunden-Kommunikation mit Portal-URL (Beta-Tester)
  [ ] Kundenservice-Agent konfigurieren (Stage 5+, nicht dringend)


--------------------------------------------------------------------------------
6. ERKENNTNISSE FÜR DEN BLUEPRINT
--------------------------------------------------------------------------------

  • CSM (Customer Service Management) ist die richtige Vorlage für
    externes Endkunden-Portal — nicht der klassische IT Service Desk
  • Contact/Standard Formular in CSM ist System-reserviert —
    eigene Formulare für Portal-sichtbare Request-Typen anlegen
  • Free Plan trägt R+MUNI Portal vollständig — kein Upgrade nötig
  • Offener Kundenzugriff ("Jeder") passt zur R+MUNI Philosophie
    und reduziert Onboarding-Aufwand auf null
  • Confluence bleibt bewusst getrennt vom Portal-Projekt —
    Verknüpfung ist ein eigener bewusster Schritt, kein Automatismus


================================================================================
SPRINT-RMNP01-PortalSetup
ABGESCHLOSSEN | 2026-03-09
R+MUNI Blueprint | Stage 5 | Erstellt durch: Markus Resel + Claude (Pair-Session)
================================================================================
