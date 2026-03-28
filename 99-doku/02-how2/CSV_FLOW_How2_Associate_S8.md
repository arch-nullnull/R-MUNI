================================================================================
CSV FLOW — HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : CSV_FLOW_How2_Associate_S8
Tag             : #associate #how2 #csvflow #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : ENTWURF
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Hinweis         : Inhalt initial ident mit DEV-Gegenstück — inhaltliche Trennung in Stage 1
================================================================================



VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.10+
- openpyxl installiert (für CSV07/CSV08)
- BLUEPRINT_ROOT korrekt in root.txt eingetragen
- Ordnerstruktur gemäß structure.txt vorhanden


KOMPLETTER FLOW – SCHRITT FÜR SCHRITT
--------------------------------------------------------------------------------

Schritt 0: Master CSVs leeren (manuell)
  Die Dateien in 02-artifacts/02-csv/00-master/ müssen vor einem sauberen
  Lauf manuell auf den Header-Stand zurückgesetzt werden:
    elements.csv   → nur: "ID","Type","Name","Documentation","Specialization"
    relations.csv  → nur: "ID","Type","Name","Documentation","Source","Target","Specialization"
    properties.csv → nur: "ID","Key","Value"

  ACHTUNG: Wenn du nur ergänzen (nicht neu aufbauen) willst, diesen Schritt
  überspringen. Der Flow hängt immer an.

Schritt 1: Umgebung validieren
  python CSV00-validate_environment.py
  → Prüft root.txt, löst BLUEPRINT_ROOT auf
  → Erzeugt: 03-stages/99-logs/CSV00-root.resolved.txt
  → Bei Fehler: Abbruch mit Fehlermeldung

Schritt 2: Modell-Inventar erstellen
  python CSV01-validate_model.py
  → Scannt 01-model/00-archimate/ nach .archimate Dateien
  → Erzeugt: 03-stages/model-scope.txt
  → Nur informativ, trifft keine Entscheidungen

Schritt 3: Scope auflösen
  python CSV03-resolve_run_scope.py
  → Liest csvmapping.txt (02-artifacts/02-csv/01-mapping/)
  → Matched Modelle aus model-scope.txt gegen Mapping-Regeln
  → Erzeugt: 03-stages/run-scope.txt mit SOURCE=archi Einträgen
  → Bei keinem Match: Abbruch

Schritt 4: Inventar erweitern
  python CSV04-model-overview.py
  → Fügt OEF, XLSX, CSV Artefakte zum run-scope hinzu
  → ÜBERSCHREIBT run-scope.txt vollständig (TD-02 beachten!)
  → Nur ausführen wenn automatische Inventarisierung gewünscht

Schritt 5: Master CSV Struktur sicherstellen
  python CSV05-create_master_csvs.py
  → Erstellt fehlende Master CSVs mit korrektem Header
  → Überschreibt NIE vorhandene Dateien

Schritt 6: Archi-Child-CSVs anhängen
  python CSV06-append_child_to_master.py
  → Liest aus: 02-artifacts/02-csv/03-child/00-archimatechild/
  → Hängt an Master CSVs an (Header wird übersprungen)
  → Fehlende Child-Dateien → Warnung, kein Abbruch

Schritt 7: XLSX konvertieren und anhängen
  python CSV07-xlsx_2_csv.py
  → Verarbeitet SOURCE=XLSX Einträge aus run-scope.txt
  → Mapping via 02-artifacts/03-XLSX/01-mapping/csvmapping.txt
  → Hängt an Master CSVs an

Schritt 8: Properties aus XLSX anhängen
  python CSV08-properties2csv.py
  → Verarbeitet SOURCE=XLSX Einträge aus run-scope.txt
  → Nur "Properties" Sheet wird gelesen
  → Mapping via propmapping.txt
  → Validiert Owner-IDs gegen Master CSVs

Schritt 9: master.xml in CSV konvertieren
  python CSV09-masterxml2csv.py
  → Liest aus: 02-artifacts/00-xml/00-master/master.xml
  → Dispatcher: sourceSystem="archi" → OVERWRITE, "bpmn" → APPEND
  → Mapping via 02-artifacts/00-xml/01-mapping/mastercsvmapping.txt

Schritt 10: Export-Snapshot erstellen
  python CSV99-export_snapshot.py
  → Dedupliziert Master CSVs (last-wins)
  → Filtert Typen gemäß csvexport.txt
  → Schreibt nach: 02-artifacts/02-csv/04-import/
  → Diese Dateien sind der Archi-Import


HÄUFIGE FEHLER UND LÖSUNGEN
--------------------------------------------------------------------------------

Fehler: "CSV00-root.resolved.txt not found"
  Ursache: CSV00 wurde nicht ausgeführt oder ist fehlgeschlagen.
  Lösung: CSV00 neu ausführen, Logfile prüfen.

Fehler: "no models matched mapping rules; run scope is empty"
  Ursache: Kein Modell in model-scope.txt passt zu den Regeln in csvmapping.txt.
  Lösung: csvmapping.txt prüfen, Modellname stimmt nicht mit Pattern überein.
  Tipp: Pattern "*" matcht alles.

Fehler: "Owner ID not found in master CSVs" (CSV08)
  Ursache: Die Properties-XLSX referenziert eine ID die noch nicht in den
  Master CSVs steht. Meist weil CSV06/CSV07 noch nicht ausgeführt wurden.
  Lösung: Reihenfolge einhalten (06 → 07 → 08).

Fehler: Master CSVs wachsen bei jedem Lauf
  Ursache: Master CSVs werden nicht geleert vor dem Lauf.
  Lösung: Schritt 0 ausführen (manuell leeren auf Header).

Inhalt in 04-import/ fehlt oder ist leer
  Ursache: Master CSVs waren leer als CSV99 lief.
  Lösung: Alle Stages 00–09 der Reihe nach ausführen, dann CSV99.


KONFIGURATIONSDATEIEN – KURZREFERENZ
--------------------------------------------------------------------------------

02-artifacts/02-csv/01-mapping/csvmapping.txt
  Format: "XLSX_Header","Sheet","CSV_Header","target.csv"
  Zweck: Steuert welche XLSX-Spalten in welche CSV-Spalten fließen (CSV07)

02-artifacts/03-XLSX/01-mapping/csvmapping.txt
  Gleicher Zweck, aber für XLSX im XLSX-Unterordner.

02-artifacts/03-XLSX/01-mapping/propmapping.txt
  Format: "XLSX_Header","Sheet","CSV_Header","properties.csv"
  Zweck: Mapping für Properties-Sheet (CSV08)

02-artifacts/02-csv/02-sync/csvexport.txt
  Format: ein Typ pro Zeile (z.B. "Junction")
  Zweck: Diese Typen werden von CSV99 aus dem Export ausgeschlossen.

03-stages/run-scope.txt
  Format: SOURCE=<typ> / MODEL=<datei> (Paare)
  Zweck: Steuert welche Quellen im aktuellen Lauf aktiv sind.
  ACHTUNG: CSV04 überschreibt diese Datei vollständig.


ARCHI IMPORT
--------------------------------------------------------------------------------
Nach erfolgreichem CSV99 liegen in 02-artifacts/02-csv/04-import/ drei Dateien:
  elements.csv
  relations.csv
  properties.csv

In Archi 5.8:
  File → Import → CSV → Verzeichnis 04-import/ auswählen → Import

Hinweis: Archi vergibt bei neuen Elementen (ohne ID) neue IDs.
Elemente mit bestehender ID werden aktualisiert.