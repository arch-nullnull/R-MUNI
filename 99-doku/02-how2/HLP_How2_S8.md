================================================================================
HLP HELPER SCRIPTS – HOW2 (DEV)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : HLP_How2_S3
Tag             : #dev #how2 #hlp #s3 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-02
Rückkopplungsschutz : S3 — Inhalt read-only, kein inhaltlicher Eingriff
Ablageort       : 00-concept/02-how2/HLP_How2_S3.txt
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.10+ (keine externen Pakete erforderlich)
- Scripts liegen in 02-artifacts/01-scripts/
- logs/ und backups/ und context/ Verzeichnisse werden automatisch erstellt


KURZREFERENZ ALLER SCRIPTS
--------------------------------------------------------------------------------

HLP00 – Root und Umgebung loggen
  python HLP00_resolve_root.py
  → Zeigt und loggt: Script-Pfad, ROOT, OS, Python-Version, CWD
  → Log: logs/HLP00_root.log
  → Nützlich als erster Check wenn etwas nicht stimmt

HLP01 – Datei oder Ordner kopieren (Quelle bleibt)
  python HLP01_copy.py <quelle> <ziel>
  Beispiele:
    python HLP01_copy.py ordner_a/datei.txt ordner_b/datei.txt
    python HLP01_copy.py 02-artifacts/02-csv/00-master archiv/master-backup
  → Bei Ordner: rekursive Kopie. Ziel wird überschrieben wenn vorhanden.
  → Log: logs/HLP01_copy.log

HLP02 – Datei oder Ordner verschieben (Quelle wird gelöscht)
  python HLP02_move.py <quelle> <ziel>
  Beispiele:
    python HLP02_move.py temp/export.csv 02-artifacts/02-csv/03-child/00-archimatechild/export.csv
  → Zielverzeichnis wird automatisch erstellt
  → ACHTUNG: Quelle wird danach gelöscht
  → Log: logs/HLP02_move.log

HLP03 – Ordnerinhalt leeren (Ordner selbst bleibt)
  python HLP03_clean.py <ordner> [<ordner2> ...]
  Beispiele:
    python HLP03_clean.py 02-artifacts/02-csv/00-master
    python HLP03_clean.py 03-stages/00-archimatearchive 03-stages/01-bpmnarchive
  → ACHTUNG: Löscht ALLES im Ordner ohne Bestätigung
  → Mehrere Ordner in einem Aufruf möglich
  → Log: logs/HLP03_clean.log

HLP04 – Verzeichnisbaum dokumentieren
  python HLP04_dirlog.py <ordner> [<ordner2> ...]
  Beispiele:
    python HLP04_dirlog.py .
    python HLP04_dirlog.py 02-artifacts 03-stages
  → Zeigt und loggt Dateibaum mit Dateigrößen
  → Log: logs/HLP04_dirlog.log (akkumulierend)
  → Nützlich für Statuscheck und Dokumentation

HLP05 – Kontext- und Strukturdateien erstellen
  python HLP05_context_structure.py [<ordner>] [--context-only] [--structure-only]
  Beispiele:
    python HLP05_context_structure.py
    python HLP05_context_structure.py 02-artifacts --structure-only
  → context/context.json: Umgebungsmetadaten (OS, Python, Hostname, Pfade)
  → context/structure.json: Kompletter Dateibaum als JSON
  → Log: logs/HLP05_context.log

HLP06 – Backup erstellen
  python HLP06_backup.py [--src <ordner>] [--dest <ordner>] [--exclude <name> ...]
  Beispiele:
    python HLP06_backup.py
    python HLP06_backup.py --dest D:/backups
    python HLP06_backup.py --src 02-artifacts --dest ../backups --exclude temp
    python HLP06_backup.py --no-checksums   (schneller, keine SHA-256)
  → Standard-Quelle: Scriptverzeichnis (ROOT)
  → Standard-Ziel: ROOT/backups/
  → Archivname: MUNI_backup_YYYYMMDD_HHMMSS.zip
  → Enthält manifest.json mit SHA-256 Checksums
  → Log: logs/HLP06_backup.log

HLP07 – Backup wiederherstellen
  python HLP07_restore.py <backup.zip> [--dest <ordner>] [--dry-run] [--verify-only] [--no-verify]
  Beispiele:
    python HLP07_restore.py backups/MUNI_backup_20260302_120000.zip
    python HLP07_restore.py backup.zip --dest C:/restored --dry-run
    python HLP07_restore.py backup.zip --verify-only
  → Standard-Ziel: Original-Pfad aus manifest.json
  → --dry-run: zeigt was gemacht würde, schreibt nichts
  → --verify-only: prüft Checksums vorhandener Dateien ohne Extract
  → --no-verify: überspringt Checksum-Prüfung nach Restore
  → Log: logs/HLP07_restore.log


TYPISCHE ANWENDUNGSFÄLLE
--------------------------------------------------------------------------------

Vor einem riskanten Flow-Lauf sichern:
  python HLP06_backup.py
  → Danach Flow ausführen. Bei Fehler mit HLP07 wiederherstellen.

Master CSVs leeren vor sauberem Lauf:
  python HLP03_clean.py 02-artifacts/02-csv/00-master
  Danach CSV05 ausführen um Header wieder zu erzeugen.

Archiv-Verzeichnisse leeren nach abgebrochenem XML Flow:
  python HLP03_clean.py 03-stages/00-archimatearchive 03-stages/01-bpmnarchive

Aktuellen Stand dokumentieren:
  python HLP05_context_structure.py
  python HLP04_dirlog.py .

Datei aus Archiv ins active Verzeichnis schieben:
  python HLP01_copy.py 03-stages/01-bpmnarchive/MeinProzess.bpmn 01-model/01-bpmn/00-bpmnactive/MeinProzess.bpmn

Backup auf anderen Rechner übertragen und wiederherstellen:
  1. HLP06 auf Quellrechner ausführen
  2. ZIP auf Zielrechner kopieren
  3. python HLP07_restore.py backup.zip --dest <Zielpfad>


PFADANGABEN – REGELN
--------------------------------------------------------------------------------
- Relative Pfade werden gegen ROOT aufgelöst (= Verzeichnis der HLP-Scripts)
- Absolute Pfade werden direkt verwendet
- Alle HLP-Scripts verstehen beide Varianten automatisch


BACKUP WIEDERHERSTELLEN – DETAILABLAUF
--------------------------------------------------------------------------------
1. HLP07 liest manifest.json aus dem ZIP
2. Zeigt Backup-Info (Datum, Quelle, Dateianzahl, Größe)
3. Extrahiert alle Dateien nach Zielverzeichnis
4. Führt Checksum-Verifikation durch (SHA-256)
5. Meldet OK/FEHLER pro Datei

Bei Checksum-Fehler:
  → Meldung im Log + Konsole
  → Restore ist abgeschlossen aber Dateien sind möglicherweise korrumpiert
  → Anderes Backup verwenden oder Quelle prüfen

--dry-run zeigt den vollständigen Restore-Plan ohne eine Datei zu schreiben.
Empfohlen vor dem ersten Restore auf ein neues Zielsystem.
