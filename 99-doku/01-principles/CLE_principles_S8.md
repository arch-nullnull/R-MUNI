================================================================================
CLE CLEANING SCRIPTS – PRINCIPLES
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : CLE_principles_S5
Tag             : #dev #principles #cle #cleaning #s5 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-15
Ablageort       : 00-concept/01-principles/CLE_principles_S5.md
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Die CLE-Scripts (CLE00–CLE53) sind dedizierte Cleaning-Utilities für das
R+MUNI Blueprint-System. Ihr einziger Zweck: definierte Artifact- und
Stages-Ordner zuverlässig leeren — reproduzierbar, protokolliert und ohne
manuelle Eingriffe.

Kernprinzip: Jedes CLE-Script macht genau eine Sache und hat ein klar
definiertes Ziel (einen oder mehrere Ordner, oder gezielte Dateien).
Kein CLE-Script erzeugt Inhalte, transformiert Daten oder ruft andere
Scripts auf.

CLE-Scripts sind Vorbereitungs-Werkzeuge, keine Flow-Stages. Sie sichern
saubere Ausgangszustände bevor ein Flow startet — manuell oder automatisch
über den Scriptrunner (FLW).


2. ZWEI LÖSCH-MODI
--------------------------------------------------------------------------------
Die CLE-Reihe kennt zwei fundamental verschiedene Lösch-Modi:

MODUS A — Ordner-Clean (Standardfall, CLE10–CLE53):
  Löscht den gesamten Inhalt eines Ordners.
  Der Ordner selbst bleibt erhalten.
  Kern-Funktion: clean_folder()
  Log-Tag:       [DEL-F] für Dateien, [DEL-D] für Unterordner

MODUS B — Datei-Delete (Spezialfall, CLE26):
  Löscht gezielt benannte Einzeldateien.
  Alle anderen Dateien im Ordner bleiben erhalten.
  Kern-Funktion: delete_file()
  Log-Tag:       [DEL-F] für die gelöschte Datei

Die Wahl des Modus ergibt sich aus dem fachlichen Anwendungsfall —
nicht aus technischer Präferenz. CLE26 existiert weil im ID-losen
Import-Szenario exakt eine Datei (elements.csv) erhalten bleiben muss.


3. ROOT-AUFLÖSUNG (AUTARK / INLINE)
--------------------------------------------------------------------------------
Jedes CLE-Script (CLE10–CLE53) löst root.cfg inline auf — ohne Import
von CLE00 oder HLP00. Damit ist jedes Script vollständig autark und
in beliebiger Reihenfolge ausführbar, auch wenn andere CLE-Scripts
nicht vorhanden sind.

Auflösungs-Logik:
  script_dir = os.path.dirname(os.path.abspath(__file__))
  cfg_path   = os.path.abspath(os.path.join(script_dir, "..", "..", "root.cfg"))

Das entspricht der Blueprint-Konvention: Script liegt zwei Ebenen unter
<rootfolder> (in 01-artifacts\01-scripts\), root.cfg liegt direkt im
<rootfolder>.

CLE00 ist die einzige Ausnahme: es ist ein reines Diagnose-Script das
die Root-Auflösung protokolliert und ein Referenz-Log für die CLE-Reihe
schreibt. Es wird nicht importiert.


4. BASISPFAD-VARIABLEN
--------------------------------------------------------------------------------
Die CLE-Scripts verwenden zwei verschiedene Basis-Variablen aus root.cfg:

  CLE1x – CLE4x  →  cfg["<artifacts>"]  →  <rootfolder>\01-artifacts
  CLE5x           →  cfg["<stages>"]     →  <rootfolder>\02-stages

Alle Ziel-Ordner werden relativ zu dieser Basis aufgebaut:
  ziel = os.path.join(basepath, relativ)

Diese Trennung ist bewusst: die Stages-Gruppe (CLE5x) operiert auf
einem anderen Ast der Ordnerstruktur als alle anderen Gruppen.


5. GRUPPEN-SCHEMA
--------------------------------------------------------------------------------
Die Nummerierung folgt einem festen Schema das die Zugehörigkeit
jedes Scripts sofort erkennbar macht:

  CLE00   Basis / Diagnose
  CLE1x   XML-Gruppe      (01-artifacts\00-xml)
  CLE2x   CSV-Gruppe      (01-artifacts\02-csv)
  CLE3x   XLSX-Gruppe     (01-artifacts\03-XLSX)
  CLE4x   Reports-Gruppe  (01-artifacts\05-reports)
  CLE5x   Stages-Gruppe   (02-stages)

Innerhalb jeder Gruppe gilt dasselbe Nummern-Muster:
  x0  →  Master / All     (alle Unterordner der Gruppe)
  x1  →  All Childs       (alle Child-Ordner kombiniert)
  x2  →  ArchiMate Child  (nur ArchiMate-Unterordner)
  x3  →  BPMN Child       (nur BPMN-Unterordner)
  x4  →  Import           (04-import Ordner)
  x5  →  Export           (99-exports Ordner)

Ausnahme CLE26: Spezialfall innerhalb der CSV-Gruppe, Datei-Delete Modus.
Die Nummer 26 signalisiert bewusst: "gehört zu CSV (2x), ist aber kein
Standard-Ordner-Clean".


6. LOGGING-PRINZIP
--------------------------------------------------------------------------------
Alle CLE-Scripts schreiben Logs im Append-Modus nach:
  <rootfolder>\02-stages\99-logs\CLE<Nr>-<Name>.log

Jeder Eintrag hat einen Timestamp und ein Kürzel-Präfix:
  [CLE10] 2026-03-15 10:23:45 | <Message>

Log-Tags (einheitlich über die gesamte Reihe):
  [DEL-F]  — Datei gelöscht
  [DEL-D]  — Unterordner gelöscht (mit shutil.rmtree)
  [SKIP]   — Ziel nicht gefunden, übersprungen (kein Abbruch)
  [FEHLER] — Lösch-Operation fehlgeschlagen (Exception)
  [OK]     — Abschluss-Zeile mit Zusammenfassung

Jedes Script beginnt mit einer ===Start=== und endet mit einer
===Ende=== Zeile — für klare Abgrenzung bei mehreren Läufen im
selben Log.

Besonderheit CLE26: Log zeigt "Ziel-Datei" statt "Ziel-Ordner" —
bewusste visuelle Unterscheidung zum Standardfall.

Besonderheit CLE53: löscht 02-stages\99-logs — damit auch alle
bestehenden CLE-Logs. CLE53 schreibt kein neues Log (Ziel-Ordner
gerade geleert). Nur Konsolen-Ausgabe bleibt sichtbar.


7. FEHLERVERHALTEN
--------------------------------------------------------------------------------
Nicht vorhandene Ziele → [SKIP], kein Abbruch.
  Begründung: CLE-Scripts sollen in Flows sicher ausführbar sein,
  auch wenn ein Ziel-Ordner noch nie befüllt wurde.

Lösch-Fehler (z.B. Dateisystem-Sperre) → [FEHLER] geloggt,
  Verarbeitung der restlichen Ziele wird fortgesetzt.
  Das Script endet ohne sys.exit(1) — Fehleranzahl steht in [OK]-Zeile.

Konfigurationsfehler (root.cfg fehlt oder <artifacts>/<stages>
  nicht auflösbar) → sofortiger Abbruch mit sys.exit(1).
  Kein Silent-Fail bei Basis-Konfiguration.


8. DESTRUKTIVE OPERATIONEN – REGELN
--------------------------------------------------------------------------------
CLE-Scripts löschen sofort und ohne Bestätigungsabfrage.
Es gibt kein Undo. Gelöschte Inhalte sind weg.

Vor dem Einsatz von CLE-Scripts in einem neuen Kontext:
  → Prüfen ob Git aktiv ist (bevorzugter Schutz im Blueprint)
  → Alternativ: HLP06 Backup erstellen

CLE-Scripts löschen NIE:
  - Den Ordner selbst (nur Inhalt)
  - Dateien außerhalb der definierten ZIEL_LISTE / ZIEL_DATEIEN
  - Modell-Dateien unter 00-model
  - Scripts unter 01-artifacts\01-scripts
  - root.cfg oder andere Konfigurations-Dateien


9. KEINE EXTERNEN ABHÄNGIGKEITEN
--------------------------------------------------------------------------------
Alle CLE-Scripts verwenden ausschließlich Python stdlib:
  os, sys, shutil, datetime

Keine pip-Pakete erforderlich. Lauffähig auf jeder Python 3.10+
Installation ohne Vorbereitung.


10. VERHÄLTNIS ZU HLP03
--------------------------------------------------------------------------------
HLP03_clean.py ist der generische Vorläufer der CLE-Reihe:
  - HLP03 nimmt Ordner als Kommandozeilen-Argumente entgegen
  - HLP03 hat keine Blueprint-Semantik (kein root.cfg, kein <artifacts>)
  - HLP03 loggt in einen fixen logs/ Ordner relativ zum Script

CLE-Scripts sind die spezialisierte Weiterentwicklung:
  - Feste, benannte Ziel-Ordner (kein Argument nötig)
  - root.cfg-Auflösung → absolute, konfigurierte Pfade
  - Logs in den Blueprint-Standard-Pfad (02-stages\99-logs)
  - Direkt in Flows (FLW-Reihe / Scriptrunner) einbindbar

HLP03 bleibt im Blueprint als generisches Werkzeug erhalten.
CLE-Scripts ersetzen HLP03 nicht — sie ergänzen ihn für
reihenspezifische, reproduzierbare Anwendungsfälle.


11. EINBINDUNG IN FLOWS (FLW-REIHE)
--------------------------------------------------------------------------------
CLE-Scripts sind für den Scriptrunner (FLW00-scriptrunner.py)
und flowmapping.txt vorbereitet. Typischer Einsatz als Prolog
eines Flows — Ziel-Ordner leeren bevor neue Inhalte erzeugt werden.

Beispiel BPMN-Flow-Prolog in flowmapping.txt:
  CLE13-xml_bpmn_child.py
  CLE23-csv_bpmn_child.py
  CLE33-xlsx_bpmn_child.py
  [... Flow-Scripts ...]

Die konkrete Einbindung in flowmapping.txt erfolgt wenn die
jeweilige Flow-Reihe vollständig aufgebaut ist.


================================================================================
CLE_principles_S5 | Stage 5 | 2026-03-15 | R+MUNI Blueprint
================================================================================
