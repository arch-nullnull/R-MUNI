================================================================================
SPRINT DEFINITION
================================================================================
Projekt             : R+MUNI Blueprint
Sprint-Bezeichnung  : SPRINT-CSV-Refactoring
Datum               : 2026-03-11
Stage               : 5 (aktiv)
Status              : Sprint Definition — noch nicht implementiert
Erstellt durch      : Entwickler + Claude (Pair-Session)
================================================================================


--------------------------------------------------------------------------------
1. AUSGANGSLAGE & MOTIVATION
--------------------------------------------------------------------------------

1.1 Ist-Zustand CSV-Reihe
--------------------------
Die CSV-Reihe (CSV00–CSV99) ist historisch gewachsen und enthält heute
drei logisch unterschiedliche Flows die in einer einzigen Script-Reihe
vermischt sind:

  Flow A — Archi CSV Ingest (Kernflow)
    CSV00  Umgebung validieren
    CSV01  Modell validieren
    CSV02  (leer / Platzhalter)
    CSV03  run-scope auflösen
    CSV04  Modellübersicht erstellen
    CSV05  Master-CSVs anlegen/sicherstellen
    CSV06  Child-CSVs in Master einhängen  ← hardcoded Dateinamen

  Flow B — XLSX Spin-out
    CSV07  XLSX → CSV konvertieren
    CSV08  Properties aus XLSX → CSV

  Flow C — Master-XML Spin-out (MaM)
    CSV09  master.xml → CSV (Master-to-Blueprint)

  Fixpunkt (bleibt immer)
    CSV99  Export Snapshot erstellen

  CSV06 war hardcoded auf Standardnamen — wurde als Bugfix behoben:
    SPRINT-CSV06-RunScopeAware (2026-03-11)
  CSV06 liest nun SOURCE=CSV aus run-scope.txt, Fallback bleibt erhalten.

1.2 Neu entdeckte Archi-Funktion
----------------------------------
Archi 5.x unterstützt beim CSV-Export ein konfigurierbares "File prefix".
Damit können mehrere Modelle parallel in denselben child-Ordner exportiert
werden ohne Namenskollision:
  → MUNI FLOW elements.csv
  → MUNI EA elements.csv

Die CSV-Reihe kann diesen Vorteil aktuell nicht nutzen — CSV06 ignoriert
Prefixes vollständig.

1.3 Bestehende run-scope.txt Einträge (bereits vorbereitet, inaktiv)
----------------------------------------------------------------------
In 03-stages/run-scope.txt sind SOURCE=CSV Einträge bereits auskommentiert
vorhanden:
  #SOURCE=CSV
  #MODEL=elements.csv

  #SOURCE=CSV
  #MODEL=properties.csv

  #SOURCE=CSV
  #MODEL=relations.csv

Diese Vorbereitung zeigt: das Konzept war bereits gedacht,
die Implementierung fehlt noch.


--------------------------------------------------------------------------------
2. ENTSCHEIDUNGEN & GRUNDSÄTZE DIESES SPRINTS
--------------------------------------------------------------------------------

2.1 CSV00-CSV09 bleiben unberührt
-----------------------------------
Die bestehende CSV-Reihe wird nicht angefasst. Sie läuft weiter wie bisher.
Kein Umbau, kein Einfrieren, kein Deprecated-Flag — sie existiert parallel
bis die neuen Reihen stabil laufen und die BPMN Flows mit HLP-Bausteinen
bereit sind umzuschalten.

  CSV99 bleibt dauerhaft — als fixer Abschluss-Script für alle CSV-Flows.

2.2 Neue Reihen werden parallel aufgebaut
-------------------------------------------
Drei eigenständige neue Reihen entstehen additiv:

  CSV10+   →  neuer Archi CSV Core Flow (run-scope-aware, Prefix-fähig)
               startet bei 10 weil 00-09 in der CSV-Reihe belegt sind

  XLSX00+  →  XLSX Ingest Flow (heute CSV07/08, neu und sauber aufgebaut)
               eigenes Kürzel, startet bei 00

  MaM00+   →  Master-to-Blueprint Flow (heute CSV09, neu aufgebaut)
               eigenes Kürzel, startet bei 00

2.3 HLP-Bausteine nach Bedarf — nicht auf Vorrat
--------------------------------------------------
Neue HLP-Files entstehen nur wenn beim Aufbau klar wird dass zwei oder
mehr der neuen Flows dieselbe Logik brauchen. Bestehende HLP-Files
werden zuerst geprüft und wo möglich wiederverwendet.

2.4 Naming — Entscheidung festgehalten
----------------------------------------
Script-Name beschreibt was das Script tut. Kein HLP-Bezug im Dateinamen.
Herkunft aus einem HLP-Baustein wird ausschließlich im Script-Header
als Kommentar dokumentiert.

  Beispiel eigenständig:
    XLSX01-copy.py

  Beispiel HLP-Ableitung (Kommentar im Header):
    # Basis: HLP01_copy.py — spezialisiert für XLSX Ingest
    XLSX01-copy.py

  Konvention bleibt durchgehend: ABC(D)00-beschreibung.py
  Keine Ausnahmen, kein Mischmasch.


--------------------------------------------------------------------------------
3. SPRINT-ZIELE
--------------------------------------------------------------------------------

3.1 Ziel 1 — CSV10+ aufbauen (run-scope-aware, Prefix-fähig)
--------------------------------------------------------------
Neuer Archi CSV Core Flow ab CSV10. Liest SOURCE=CSV Einträge aus
run-scope.txt und verwendet diese als Dateinamen für die child-CSVs.

Basis: CSV06 wurde bereits als Bugfix run-scope-aware gemacht
(SPRINT-CSV06-RunScopeAware, 2026-03-11). CSV10+ baut darauf auf
und erweitert den vollständigen Flow neu und sauber.

Fallback: Sind keine aktiven SOURCE=CSV Einträge vorhanden →
hardcoded elements.csv / relations.csv / properties.csv.

Beispiel run-scope.txt (aktiv mit Prefix):
  SOURCE=CSV
  MODEL=MUNI FLOW elements.csv

  SOURCE=CSV
  MODEL=MUNI FLOW relations.csv

  SOURCE=CSV
  MODEL=MUNI FLOW properties.csv

→ CSV10+ sucht genau diese Dateien im child-Ordner.
→ Archi-Export mit File prefix "MUNI FLOW" läuft direkt durch ohne
  manuelle Umbenennung.

3.2 Ziel 2 — XLSX00+ aufbauen
-------------------------------
Eigenständiger XLSX Ingest Flow. Logik aus CSV07/CSV08 als Basis —
neu und sauber aufgebaut, nicht kopiert.

3.3 Ziel 3 — MaM00+ aufbauen
------------------------------
Eigenständiger Master-to-Blueprint Flow. Logik aus CSV09 als Basis —
neu und sauber aufgebaut, nicht kopiert.

3.4 Ziel 4 — run-scope.txt Einträge aktivieren
------------------------------------------------
Die auskommentierten SOURCE=CSV Einträge werden aktiviert und um den
Archi-Prefix erweitert sobald CSV10+ läuft.
Keine Änderung am run-scope.txt Format — Konvention gilt unverändert.

3.5 Ziel 5 — flowmapping.txt aktualisieren
--------------------------------------------
flowmapping.txt wird um die drei neuen Flow-Einträge erweitert sodass
FLW00-scriptrunner.py die neuen Flows einzeln oder kombiniert ausführen
kann. Die bestehenden CSV-Flow-Einträge bleiben unverändert.

3.6 Ziel 6 — GOV 7.5 Präzisierung Naming
-------------------------------------------
GOV Kapitel 7.5 Script-Benennung wird um das konkrete Naming Schema
erweitert:
  - Schema ABC(D)00-beschreibung.py normativ verankert
  - Regel zu HLP-Ableitungen (Name vs. Kommentar) dokumentiert
  - Neue Kürzel CSV10/XLSX/MaM als Präzedenzbeispiele aufgenommen

HLP-Struktur und Baukasten-Prinzip bleiben in Principles und
SCRIPT-BAUKASTEN.txt — nicht in der GOV.


--------------------------------------------------------------------------------
4. ABGRENZUNG — WAS DIESER SPRINT NICHT TUT
--------------------------------------------------------------------------------

- Kein Eingriff in CSV00-CSV09 (laufen unverändert weiter)
- CSV99 wird nicht verschoben — bleibt dauerhaft wo sie ist
- Keine Änderung an master.xml Struktur
- Keine Änderung an mapping.txt / M2Bmapping.txt
- Kein Eingriff in Stage-3/4-Scripts (read-only per Stage 5 GOV)
- Keine neuen SOURCE-Typen in run-scope.txt — CSV ist bereits vorbereitet
- Kein Umbau der bestehenden Flows — nur paralleler Aufbau


--------------------------------------------------------------------------------
5. BETROFFENE DATEIEN
--------------------------------------------------------------------------------

Neu zu erstellen:
  CSV10+                               neuer Archi CSV Core Flow
  XLSX00+                              neuer XLSX Ingest Flow
  MaM00+                               neuer MaM Flow
  Sprint-DEV-Doku-CSV-Refactoring.txt  Entwicklungsdokumentation

Zu ändern:
  run-scope.txt                        SOURCE=CSV aktivieren + Prefix
  flowmapping.txt                      drei neue Flows eintragen
  Global_GOV.txt                       Kapitel 7.5 Präzisierung Naming

Ggf. neue HLP-Files:
  HLPxx-...                            nur wenn zwei+ Flows dieselbe Logik brauchen

Unverändert:
  CSV00-CSV09, CSV99                   laufen weiter wie bisher
  alle anderen Script-Reihen           unberührt


--------------------------------------------------------------------------------
6. REIHENFOLGE DER UMSETZUNG
--------------------------------------------------------------------------------

Schritt 1   CSV10+ aufbauen
            → run-scope-aware, Prefix-fähig, Fallback auf hardcoded Namen

Schritt 2   run-scope.txt SOURCE=CSV aktivieren und Prefix setzen

Schritt 3   XLSX00+ aufbauen
            → CSV07/08 als Referenz, nicht als Kopiervorlage

Schritt 4   MaM00+ aufbauen
            → CSV09 als Referenz, nicht als Kopiervorlage

Schritt 5   flowmapping.txt aktualisieren
            → drei neue Flows eintragen, bestehende unverändert

Schritt 6   GOV 7.5 Präzisierung Naming

Schritt 7   Sprint-DEV-Doku abschließen und GOV-Check


--------------------------------------------------------------------------------
7. ERFOLGSKRITERIEN
--------------------------------------------------------------------------------

  OK  CSV10+ liest Dateinamen aus run-scope.txt wenn SOURCE=CSV aktiv
  OK  Archi-Export mit File prefix läuft ohne manuelle Umbenennung durch
  OK  Fallback auf hardcoded Namen funktioniert wenn kein SOURCE=CSV aktiv
  OK  XLSX00+ läuft eigenständig ohne CSV-Reihe
  OK  MaM00+ läuft eigenständig ohne CSV-Reihe
  OK  CSV00-CSV09 laufen unverändert weiter
  OK  Neue Flows in flowmapping.txt eingetragen
  OK  FLW00-scriptrunner.py kann neue Flows einzeln ausführen
  OK  GOV 7.5 um Naming Schema erweitert
  OK  Kein Stage-3/4-Script wurde verändert


--------------------------------------------------------------------------------
8. GOVERNANCE-KONFORMITÄTSCHECK
--------------------------------------------------------------------------------

GOV 10.3  Zulässiger Auslöser        OK  Feature-Zuwachs + strukturelle Bereinigung
GOV 10.5  Fachlicher Mehrwert        OK  Multi-Modell CSV Export, saubere Flow-Trennung
GOV 10.5  Keine implizite Gov-Änd.   OK  GOV 7.5 Erweiterung explizit als Ziel
GOV 10.6  Ziel explizit definiert    OK  Abschnitt 3
GOV 10.6  Ziel überprüfbar           OK  Erfolgskriterien Abschnitt 7
GOV 10.7  Zwischenschritte           OK  Abschnitt 6
GOV 10.8  Dev-Doku                   OFFEN  wird im Sprint erstellt
GOV 10.9  Stage-Ende Doku            OFFEN  verpflichtend bei Stage-Abschluss
GOV 10.10 Keine Gov-Regel aufgehoben OK  additiv, kein Eingriff in Stage 3/4
Stage 5   Rückkopplungsschutz        OK  CSV00-09 unberührt, nur paralleler Aufbau


================================================================================
END OF SPRINT DEFINITION
SPRINT-CSV-Refactoring | Stage 5 | 2026-03-11
================================================================================
