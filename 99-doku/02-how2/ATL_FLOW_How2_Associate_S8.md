================================================================================
ATL FLOW — HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : ATL_FLOW_How2_Associate_S8
Tag             : #associate #how2 #atlflow #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : ENTWURF
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Hinweis         : Inhalt initial ident mit DEV-Gegenstück — inhaltliche Trennung in Stage 1
================================================================================

Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-08
Ablageort       : 00-concept/02-how2/ATL_FLOW_How2_S4.txt
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.10+ (keine externen Pakete erforderlich)
- BLUEPRINT_ROOT korrekt in root.txt eingetragen
- Ordnerstruktur gemäß structure.txt vorhanden
- run-scope.txt enthält ein aktives SOURCE=ATL Pair
- master.xml in 02-artifacts/00-xml/00-master/ vorhanden
- Jira-Projekt R+MUNI EA (MUNIEA) vorhanden
- 9 Komponenten im Projekt angelegt (siehe Abschnitt Jira-Vorbereitung)


================================================================================
SCHRITT 0 – JIRA-VORBEREITUNG (einmalig)
================================================================================

Projekt: R+MUNI EA (Key: MUNIEA, Typ: Kanban)

Folgende 9 Komponenten müssen im Projekt vorhanden sein:
  Strategy
  Business
  Application
  Technology & Physical
  Motivation
  Implementation & Migration
  Relations
  Other
  Views

Anlegen: Jira → R+MUNI EA → Projekteinstellungen → Komponenten

ACHTUNG: Die Komponentennamen müssen EXAKT so geschrieben sein wie oben.
ATL02 schreibt diese Strings in die CSV — Jira matched beim Import auf
den exakten Namen.

"Views" ist für manuelle Einträge reserviert — ATL02 befüllt diese
Komponente nicht automatisch.


================================================================================
SCHRITT 1 – run-scope.txt VORBEREITEN
================================================================================

Datei: 03-stages/run-scope.txt

Folgendes Pair muss aktiv (uncommentiert) eingetragen sein:

  SOURCE=ATL
  MODEL=R+Muni Architecture Modell.xml

Regeln:
  - Beide Zeilen direkt untereinander, keine Leerzeile dazwischen
  - Kein führendes # (sonst inaktiv)
  - MODEL= muss exakt dem Modellnamen in master.xml entsprechen

Bestehende SOURCE=ARCHIMATE oder SOURCE=BPMN Einträge bleiben unverändert.


================================================================================
SCHRITT 2 – ATL00: SCOPE UND VORAUSSETZUNGEN PRÜFEN
================================================================================

  cd 02-artifacts/01-scripts/
  py ATL00-validate_atl_scope.py

Was passiert:
  → Root-Pfad aus root.txt auflösen
  → run-scope.txt auf aktives SOURCE=ATL Pair prüfen
  → master.xml auf Existenz und Lesbarkeit prüfen
  → Ordner prüfen: 03-stages/00-archimatearchive/ + 03-stages/99-logs/
  → Schreibt: 03-stages/99-logs/ATL00-root.resolved.txt
  → Schreibt: 03-stages/99-logs/ATL00-validate_atl_scope.log

Erwartete Konsolenausgabe (Erfolg):
  [ATL00] OK | ATL Scope validiert -> 1 Modell(e) aktiv

Bei Fehler:
  Kein SOURCE=ATL  → Schritt 1 wiederholen
  master.xml fehlt → Pfad in root.txt prüfen, XML Flow ausführen
  Ordner fehlt     → Ordner manuell anlegen, dann ATL00 wiederholen


================================================================================
SCHRITT 3 – ATL01: MASTER.XML IN LAYER-CSVs TRANSFORMIEREN
================================================================================

  py ATL01-masterXml2AtlCsv.py

Was passiert:
  → ATL00-root.resolved.txt lesen
  → run-scope.txt → SOURCE=ATL Modelle ermitteln
  → master.xml parsen (nur Scope-Modell)
  → Elemente nach ArchiMate 3.2 Layer gruppieren
  → BPMN-Prozesse per Name-Match anreichern
  → ID-Kollisionen per merge behandeln
  → Schreibt: 03-stages/00-archimatearchive/atl_<layer>.csv
    (nur Layer die Objekte enthalten erzeugen eine Datei)
  → Schreibt: 03-stages/99-logs/ATL01-masterXml2AtlCsv.log

Erwartete Konsolenausgabe (Erfolg):
  [ATL01] OK | N Datei(en) -> 03-stages/00-archimatearchive/

Hinweis: Dateien werden bei jedem Lauf überschrieben.


================================================================================
SCHRITT 4 – ATL02: LAYER-CSVs IN JIRA-IMPORT-CSV UMWANDELN
================================================================================

  py ATL02-atlCsv2JiraCsv.py

Was passiert:
  → ATL00-root.resolved.txt lesen
  → Alle atl_*.csv aus 03-stages/00-archimatearchive/ lesen
  → Pro Zeile eine Jira-Issue-Zeile bauen:
      Summary           = Name (Fallback: [ArchiType] objectKey)
      Issue Type        = Task
      Component/s       = Layer-Name (Jira Komponente)
      Labels            = ArchiType (Stichwort, Leerzeichen → Underscore)
      External issue ID = objectKey (Merge-Schlüssel)
  → Alle Layer in einer CSV zusammenführen
  → Schreibt: 03-stages/00-archimatearchive/jira_ea_import.csv
  → Schreibt: 03-stages/99-logs/ATL02-atlCsv2JiraCsv.log

Erwartete Konsolenausgabe (Erfolg):
  [ATL02] OK | N Zeilen -> 03-stages/00-archimatearchive/jira_ea_import.csv

Hinweis: Datei wird bei jedem Lauf überschrieben.


================================================================================
SCHRITT 5 – JIRA CSV-IMPORT DURCHFÜHREN
================================================================================

1. Jira öffnen → Projekt R+MUNI EA (MUNIEA)

2. Import starten:
   Im Projekt → ... (drei Punkte oben rechts) → Importieren → CSV

3. Datei hochladen:
   03-stages/00-archimatearchive/jira_ea_import.csv

4. Einstellungen:
   Trennzeichen : Komma
   Encoding     : UTF-8 (BOM wird automatisch erkannt)
   Vorhandene Konfiguration: NEIN (kein Haken)

5. Feld-Mapping (Pflicht):
   Summary             → Zusammenfassung      (Pflicht)
   Issue Type          → Vorgangstyp          (Pflicht, Wert: Task/Aufgabe)
   External issue ID   → Externe Vorgangs-ID  (Merge-Schlüssel — wichtig!)
   Description         → Beschreibung
   Component/s         → Komponente/n
   Labels              → Stichwörter

   EA-ObjectKey, EA-ArchiType, EA-Layer, EA-SourceModel:
   → Können ignoriert oder auf Custom Fields gemappt werden

6. Import starten

Erwartetes Ergebnis:
  Erster Import  → Issues werden neu angelegt
  Zweiter Import → Issues werden aktualisiert (kein Duplikat)
                   Voraussetzung: External issue ID korrekt gemappt

WICHTIG: "Externe Vorgangs-ID" beim Mapping nicht vergessen —
das ist der Schlüssel für saubere Updates beim zweiten Import.


================================================================================
SCHRITT 6 – CONFLUENCE JIRA-ISSUES-MAKRO EINRICHTEN
================================================================================

Voraussetzung: Schritt 5 (Jira-Import) abgeschlossen.

1. Confluence Seite bearbeiten → + → Makro → "Jira Issues"

2. JQL-Filter eingeben:

   Alle EA-Objekte:
     project = MUNIEA

   Nach Layer (Komponente, grob):
     project = MUNIEA AND component = "Application"
     project = MUNIEA AND component = "Business"
     project = MUNIEA AND component = "Technology & Physical"

   Nach ArchiType (Stichwort, fein):
     project = MUNIEA AND labels = "ApplicationComponent"
     project = MUNIEA AND labels = "BusinessProcess"
     project = MUNIEA AND labels = "Node"

   Kombiniert:
     project = MUNIEA AND component = "Business" AND labels = "BusinessProcess"

3. Spalten empfohlen: Summary, Component/s, Labels, Description

4. Speichern → live Tabelle in Confluence


================================================================================
WIEDERHOLUNG NACH MODELLÄNDERUNGEN
================================================================================

Wenn das ArchiMate-Modell in Archi geändert wurde:

1. XML Flow ausführen (XML00 → XML07) → master.xml aktualisieren
2. ATL Flow ausführen (ATL00 → ATL01 → ATL02)
3. jira_ea_import.csv erneut in Jira importieren
   → External issue ID sorgt für Update statt Duplikat
4. Confluence aktualisiert sich automatisch (live via Makro)

Kein manuelles Löschen in Jira erforderlich.


================================================================================
FEHLERBEHANDLUNG
================================================================================

FEHLER: ATL00-root.resolved.txt nicht gefunden
→ ATL00 muss vor ATL01/ATL02 ausgeführt werden
→ py ATL00-validate_atl_scope.py

FEHLER: Kein aktives SOURCE=ATL Pair
→ 03-stages/run-scope.txt öffnen
→ SOURCE=ATL / MODEL=... Pair uncommentieren oder eintragen

FEHLER: master.xml nicht gefunden
→ XML Flow (XML00–XML07) muss vorher ausgeführt worden sein
→ Pfad: 02-artifacts/00-xml/00-master/master.xml

FEHLER: Ausgabe-Ordner fehlt
→ 03-stages/00-archimatearchive/ manuell anlegen
→ ATL00 erneut ausführen

FEHLER: Keine atl_*.csv beim ATL02-Lauf
→ ATL01 muss vor ATL02 ausgeführt werden

FEHLER: Jira — Komponente wird nicht erkannt
→ Komponentennamen in Jira prüfen (exakte Schreibweise erforderlich)
→ Jira → R+MUNI EA → Projekteinstellungen → Komponenten

FEHLER: Jira — Duplikate beim zweiten Import
→ "Externe Vorgangs-ID" beim Feld-Mapping nicht vergessen
→ External issue ID muss auf Externe Vorgangs-ID gemappt sein


================================================================================
DATEIEN UND ABLAGEN
================================================================================

Scripts:
  02-artifacts/01-scripts/ATL00-validate_atl_scope.py
  02-artifacts/01-scripts/ATL01-masterXml2AtlCsv.py
  02-artifacts/01-scripts/ATL02-atlCsv2JiraCsv.py

Temporäre Outputs (werden bei jedem Lauf überschrieben):
  03-stages/00-archimatearchive/atl_business.csv
  03-stages/00-archimatearchive/atl_technology.csv
  03-stages/00-archimatearchive/atl_<weitere layer bei Bedarf>.csv
  03-stages/00-archimatearchive/jira_ea_import.csv

Logs:
  03-stages/99-logs/ATL00-root.resolved.txt
  03-stages/99-logs/ATL00-validate_atl_scope.log
  03-stages/99-logs/ATL01-masterXml2AtlCsv.log
  03-stages/99-logs/ATL02-atlCsv2JiraCsv.log

Konfiguration:
  03-stages/run-scope.txt   (SOURCE=ATL Pair manuell eintragen)

Jira:
  Projekt   : R+MUNI EA (MUNIEA)
  Typ       : Kanban
  Komponent.: Strategy, Business, Application, Technology & Physical,
              Motivation, Implementation & Migration, Relations, Other, Views


================================================================================
ATL FLOW HOW2 | S4 | ENDE
================================================================================
