================================================================================
SPRINT DEV-DOKUMENTATION
================================================================================
Projekt            : R+MUNI Blueprint
Sprint-Bezeichnung : SPRINT-RMNP02-PortalArtikel
Datum              : 2026-03-10
Stage              : 5 (aktiv)
Status             : ABGESCHLOSSEN
Erstellt durch     : Entwickler + Claude (Pair-Session)
Vorgänger-Sprint   : SPRINT-RMNP01-PortalSetup (2026-03-09)
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

Vorgeschichte:  Portal war technisch aufgebaut (SPRINT-RMNP01).
                Inhalte fehlten noch vollständig.
                Erster Beta-Kunde aktiv — Außenwirkung benötigt Substanz.

Entscheidung:   Aufbau der Portal-Inhaltsstruktur für externe Besucher.
                Klärung welche Atlassian Free Plan Funktionen nutzbar sind.
                Erstes Externes Wiki aufbauen.


--------------------------------------------------------------------------------
2. ZIEL DES SPRINTS
--------------------------------------------------------------------------------

Primärziel:
  Ersten externen Wiki-Beitrag im Kundenportal sichtbar machen.
  Portal-Inhaltsstruktur für Beta-Kunden aufbauen.

Nebenziel:
  Free Plan Grenzen konkret verstehen und dokumentieren.
  Atlassian-Komplexität bewerten und Blueprint-Empfehlung ableiten.

Abgrenzung:
  - Kein Eingriff in Stage 3/4 Scripts
  - Kein vollständiger Portal-Ausbau (iterativ)
  - Kein GitHub-Ausweichen solange Atlassian-Welt ausreicht


--------------------------------------------------------------------------------
3. KONZEPTENTSCHEIDUNGEN (Pair-Session)
--------------------------------------------------------------------------------

3.1 Kein GitHub-Ausweichen (vorerst)
--------------------------------------
Entschieden: Atlassian-Welt zuerst vollständig nutzen bevor auf GitHub
             ausgewichen wird.
Begründung:  GitHub bleibt als Option für wirklich öffentliche Inhalte
             ohne Login — aber erst wenn der Bedarf klar ist.
             Zu früh auf GitHub auszuweichen wäre Komplexität ohne Mehrwert.

3.2 Zwei-Ebenen-Struktur für Portal-Inhalte
---------------------------------------------
Entschieden: Zwei-Ebenen-Modell

  Ebene 1 — Übersicht:
    Confluence Seite "R+MUNI extern" im Space "Externes Wiki" (Key: EW)
    Zielgruppe: eingeladene Beta-User mit Confluence-Zugang
    Inhalt: Grundhaltung, Kostenlosigkeit, Archi-Verweis, Portal-Link

  Ebene 2 — Artikel:
    Native JSM Artikel direkt im Portal
    Zielgruppe: alle Portal-Besucher, kein Login nötig
    Inhalt: Kurzbeschreibungen, FAQ, Mitmachen-Info

3.3 Atlassian Setup — Scoping vor Atlassian
---------------------------------------------
Auslöser:  10-User-Limit unerwartet schnell erreicht.
           Bundle-Modell hat ~80% der Session-Zeit gekostet.

Analyse:   Nicht alle brauchen aktiven Zugriff.
           Kunden und Lieferanten kommen erst später wenn Scope das hergibt.
           Ohne klaren Scope ist das Limit zu schnell erreicht.

Entscheidung für den Blueprint:
  Scoping muss VOR Atlassian-Setup kommen.

  Fragen die zuerst beantwortet werden müssen:
    - Wer braucht welchen Zugriff?
    - Wer bearbeitet Tickets aktiv?
    - Wer ist nur lesend dabei?
    - Braucht jeder Kunde wirklich einen eigenen Atlassian-Bereich?

  Erst nach dem Scoping: Atlassian einrichten — nackt starten,
  kein Bundle-Overhead, keine unnötige Komplexität.

3.4 Fokus-Korrektur — Atlassian Portal ist nicht der R+MUNI Kern
------------------------------------------------------------------
Erkenntnis: Der Bedarf für einen Endkunden-View war ursprünglich
            validiert — aber für Lerninhalte und IMS-Einstieg,
            nicht für R+MUNI als Toolset.

Problem:    Atlassian Portal liefert schnell sichtbare Ergebnisse.
            Das verführt zu übermäßiger Investition in die
            Präsentationsschicht — auf Kosten der Kernfunktionen.

Entscheidung:
  Portal bleibt wie es ist — funktioniert für Beta, reicht.
  Kein weiterer Ausbau bis realer Bedarf aus dem Kundenbetrieb kommt.
  Fokus zurück auf: Listen-Imports, Integrationen, XML-Kreislauf.
  Das ist der R+MUNI Kernwert — nicht das Portal-Design.


--------------------------------------------------------------------------------
4. UMSETZUNG
--------------------------------------------------------------------------------

4.1 Free Plan Grenzen geklärt
-------------------------------
  ❌ Öffentlicher Link (Confluence)    → nur Premium — Abo-Falle
  ❌ Space auf anonym/öffentlich        → nur Premium
  ✅ Normaler Link kopieren & einbauen  → funktioniert
  ✅ JSM Artikel (nativer Weg)          → funktioniert
  ✅ Support-Website Seiten             → funktioniert

  Bonus-Erkenntnis:
    Neue Confluence Spaces tauchen in der Seitenleiste nicht automatisch
    auf. Lösung: direkt per URL aufrufen → Stern ⭐ klicken → fertig.

4.2 Externes Wiki aufgebaut
-----------------------------
  ✅ Space "Externes Wiki" (Key: EW) aktiviert und als Favorit markiert
  ✅ Seite "R+MUNI extern" erstellt
     Inhalt: Grundhaltung, Kostenlosigkeit, Archi-Verweis, Portal-Link
     URL: https://ims-blueprint-ticketsystem.atlassian.net/wiki/x/EACTAQ
  ✅ Seite "DEV Zeugs" erstellt
     Inhalt: GitHub, Modelle, technische Infos
  ✅ Space-Startseite mit Willkommenstext und MUNI-Akronym befüllt

4.3 JSM Support-Website konfiguriert
--------------------------------------
  ✅ Kundenerfahrung "R MUNI" konfiguriert
  ✅ Support-Website URL: /helpcenter/RMNP/
  ✅ Esel-Logo eingebunden
  ✅ Confluence-Karte der "R+MUNI extern" Seite eingebettet
  ✅ Seite "Externe Info" unter Support-Website → Seiten erstellt

4.4 JSM Artikel erstellt
--------------------------
  ✅ Artikel-Bereich neu erstellt (alter Bereich gelöscht, neu aufgebaut)
  ✅ Vorlagen entfernt
  ✅ Artikel als Beiträge im Portal sichtbar
     Methode: Neu erstellen statt reparieren — schnellster Weg

4.5 Beta-Kunde Onboarding gestartet
--------------------------------------
  ✅ Einladung an Beta-Kunden verschickt
  ✅ Customer Bereiche in Atlassian eingerichtet
     (Jira Projekt + Confluence Extern/Intern)
  ✅ Head of Teams eingeladen
  ✅ Erste Bestandsaufnahme der Kundenumgebung gemacht
  ✅ Archi Entwickler supported

4.6 Erster Praxiseinsatz mit Firmen-KI-Tool (Pair-Session)
------------------------------------------------------------
  Ergebnis: Toolset hat gehalten — mit Einschränkungen

  Probleme festgestellt:
    • ADM Drift beim ersten Prompt
      Modell hat selbständig abgekürzt ohne Rückfrage
      → klare Prompt-Disziplin notwendig
    • Content aufbauen und halten schwierig unter
      Firmenkonto-Einschränkungen
    • Quellenwarnungen wurden hingenommen
      → in Prod-Umgebungen potenziell problematisch
    • Python und Toolset lief — aber mit Fragezeichen


--------------------------------------------------------------------------------
5. OFFENE PUNKTE / NÄCHSTE SCHRITTE
--------------------------------------------------------------------------------

  [zurückgestellt] Weitere Artikel ausbauen
                   Begründung: Entscheidung 3.4 — Bedarf erst aus
                   realem Kundenbetrieb validieren

  [zurückgestellt] Confluence-Link in Artikel einbauen
                   Begründung: Folgt aus Artikel-Ausbau

  [zurückgestellt] Artikel auf Portal-Startseite prüfen
                   Begründung: Folgt aus Artikel-Ausbau

  [ ] Scoping-Dokument für Atlassian User-Modell erstellen
      (Wer braucht was — vor nächstem Kunden-Onboarding)


--------------------------------------------------------------------------------
6. ERKENNTNISSE FÜR DEN BLUEPRINT
--------------------------------------------------------------------------------

  • JSM Artikel sind der native, kostenfreie Weg für Portal-Inhalte
    → erscheinen automatisch als Beiträge, keine Login-Schranke

  • Confluence "Öffentlicher Link" = Abo-Falle
    → nicht im Free Plan nutzbar, irreführend platziert

  • Scoping vor Atlassian
    → ohne klaren User-Scope ist das 10-User-Limit zu schnell erreicht
    → Wer braucht was? Erst dann einrichten.

  • Atlassian Bundle = Komplexitätsfalle
    → nackt starten (Jira + Confluence ohne Bundle) ist der bessere
       Onboarding-Weg für neue Kunden

  • Vor-Ort-Aufwand realistisch einplanen
    → Minimum 1 Tag (Download, Adaption, erster CSV-Test)
    → Eher 2 Tage wenn Accounts erst eingerichtet werden müssen

  • KI-Tool ADM-Drift ist reales Risiko
    → Modelle kürzen selbständig ab wenn Prompt nicht präzise genug
    → Prompt-Disziplin und klare Kontextführung notwendig

  • Neu erstellen statt reparieren
    → manchmal der schnellste Weg (z.B. Artikel-Bereich Reset)

  • Atlassian Portal ist Präsentationsschicht — nicht R+MUNI Kern
    → Fokus bleibt auf Listen-Imports, Integrationen, XML-Kreislauf


================================================================================
SPRINT-RMNP02-PortalArtikel
ABGESCHLOSSEN | 2026-03-10
R+MUNI Blueprint | Stage 5 | Erstellt durch: Entwickler + Claude (Pair-Session)
================================================================================
